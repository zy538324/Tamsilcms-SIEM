"""Ingestion service entry point for MVP-3 inventory data and MVP-4 telemetry."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import csv
import io
import asyncpg
from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request, status
from fastapi.responses import JSONResponse, Response

from .config import Settings, load_settings
from .models import (
    HardwareInventory,
    LocalGroupsInventory,
    LocalUsersInventory,
    OsInventory,
    SoftwareInventory,
    AssetInventoryOverview,
    AssetInventoryPage,
    AssetInventoryStats,
    AssetRecord,
    AssetRecordPage,
    InventorySnapshot,
    AssetStatePage,
    AssetStateResponse,
    TelemetryIngestResponse,
    TelemetryPayload,
    TelemetrySeries,
    TelemetryMetricSummary,
    TelemetryBaseline,
    TelemetryAnomaly,
)
from .storage import InventoryStore, TelemetryReplayError
from .state import derive_state
from .telemetry import TelemetryValidationError, metric_unit, normalise_samples

app = FastAPI(title="Ingestion Service", version="0.1.0")


def get_settings() -> Settings:
    return load_settings()


def get_store() -> InventoryStore:
    store = getattr(app.state, "store", None)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="storage_unavailable",
        )
    return store


def validate_sample_timestamps(
    payload: TelemetryPayload,
    now: datetime,
    stale_seconds: int,
    future_seconds: int,
) -> None:
    oldest_allowed = now - timedelta(seconds=stale_seconds)
    newest_allowed = now + timedelta(seconds=future_seconds)
    for sample in payload.samples:
        if sample.observed_at < oldest_allowed:
            raise TelemetryValidationError("sample_stale")
        if sample.observed_at > newest_allowed:
            raise TelemetryValidationError("sample_in_future")


def validate_sample_uniqueness(payload: TelemetryPayload) -> None:
    seen_names: set[str] = set()
    for sample in payload.samples:
        if sample.name in seen_names:
            raise TelemetryValidationError("duplicate_metric")
        seen_names.add(sample.name)


def validate_sample_count(payload: TelemetryPayload) -> None:
    if not payload.samples:
        raise TelemetryValidationError("samples_required")


def validate_schema_version(payload: TelemetryPayload) -> None:
    if payload.schema_version != "v1":
        raise TelemetryValidationError("schema_version_unsupported")


async def enforce_https(request: Request) -> None:
    forwarded_proto = request.headers.get("x-forwarded-proto", "http")
    if forwarded_proto.lower() != "https":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="https_required",
        )


@app.on_event("startup")
async def startup() -> None:
    settings = load_settings()
    pool = await asyncpg.create_pool(
        dsn=settings.database_dsn,
        min_size=settings.database_min_connections,
        max_size=settings.database_max_connections,
    )
    app.state.pool = pool
    app.state.store = InventoryStore(pool=pool)


@app.on_event("shutdown")
async def shutdown() -> None:
    pool = getattr(app.state, "pool", None)
    if pool:
        await pool.close()


@app.get("/health", response_class=JSONResponse)
async def health_check(settings: Settings = Depends(get_settings)) -> dict:
    return {
        "status": "ok",
        "service": settings.service_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/inventory/hardware", status_code=status.HTTP_202_ACCEPTED)
async def ingest_hardware(
    payload: HardwareInventory,
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> dict:
    await store.upsert_hardware(payload)
    return {"status": "accepted"}


@app.post("/telemetry", status_code=status.HTTP_202_ACCEPTED)
async def ingest_telemetry(
    payload: TelemetryPayload,
    store: InventoryStore = Depends(get_store),
    settings: Settings = Depends(get_settings),
    _: None = Depends(enforce_https),
) -> TelemetryIngestResponse:
    if len(payload.samples) > settings.telemetry_sample_limit:
        await store.record_telemetry_rejection(
            payload_id=payload.payload_id,
            tenant_id=payload.tenant_id,
            asset_id=payload.asset_id,
            reason="payload_too_large",
        )
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="payload_too_large",
        )
    now = datetime.now(timezone.utc)
    if payload.collected_at < now - timedelta(seconds=settings.telemetry_stale_seconds):
        await store.record_telemetry_rejection(
            payload_id=payload.payload_id,
            tenant_id=payload.tenant_id,
            asset_id=payload.asset_id,
            reason="payload_stale",
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="payload_stale",
        )
    if payload.collected_at > now + timedelta(seconds=settings.telemetry_future_seconds):
        await store.record_telemetry_rejection(
            payload_id=payload.payload_id,
            tenant_id=payload.tenant_id,
            asset_id=payload.asset_id,
            reason="payload_in_future",
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="payload_in_future",
        )
    try:
        validate_schema_version(payload)
        validate_sample_count(payload)
        validate_sample_timestamps(
            payload=payload,
            now=now,
            stale_seconds=settings.telemetry_stale_seconds,
            future_seconds=settings.telemetry_future_seconds,
        )
        validate_sample_uniqueness(payload)
        samples = normalise_samples(payload.samples)
    except TelemetryValidationError as exc:
        await store.record_telemetry_rejection(
            payload_id=payload.payload_id,
            tenant_id=payload.tenant_id,
            asset_id=payload.asset_id,
            reason=exc.reason,
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.reason,
        ) from exc
    try:
        await store.ingest_telemetry(
            payload=payload,
            samples=samples,
            baseline_window=settings.telemetry_baseline_window,
            anomaly_threshold=settings.telemetry_anomaly_stddev_threshold,
        )
    except TelemetryReplayError as exc:
        await store.record_telemetry_rejection(
            payload_id=payload.payload_id,
            tenant_id=payload.tenant_id,
            asset_id=payload.asset_id,
            reason="payload_replay",
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="payload_replay",
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive fallback
        await store.record_telemetry_rejection(
            payload_id=payload.payload_id,
            tenant_id=payload.tenant_id,
            asset_id=payload.asset_id,
            reason="ingest_failed",
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ingest_failed",
        ) from exc
    return TelemetryIngestResponse(
        status="accepted",
        accepted_samples=len(samples),
    )


@app.get(
    "/telemetry/{asset_id}/metrics",
    response_model=list[TelemetryMetricSummary],
)
async def list_telemetry_metrics(
    asset_id: str = Path(..., min_length=8, max_length=64),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> list[TelemetryMetricSummary]:
    return await store.list_telemetry_metrics(asset_id)


@app.get(
    "/telemetry/{asset_id}/series",
    response_model=TelemetrySeries,
)
async def get_telemetry_series(
    asset_id: str = Path(..., min_length=8, max_length=64),
    metric_name: str = Query(..., min_length=3, max_length=128),
    since: datetime | None = Query(default=None),
    until: datetime | None = Query(default=None),
    limit: int = Query(default=500, ge=1, le=5000),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> TelemetrySeries:
    try:
        metric_unit(metric_name)
    except TelemetryValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.reason,
        ) from exc
    return await store.get_telemetry_series(
        asset_id=asset_id,
        metric_name=metric_name,
        since=since,
        until=until,
        limit=limit,
    )


@app.get(
    "/telemetry/{asset_id}/baselines",
    response_model=list[TelemetryBaseline],
)
async def list_telemetry_baselines(
    asset_id: str = Path(..., min_length=8, max_length=64),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> list[TelemetryBaseline]:
    return await store.list_telemetry_baselines(asset_id)


@app.get(
    "/telemetry/{asset_id}/anomalies",
    response_model=list[TelemetryAnomaly],
)
async def list_telemetry_anomalies(
    asset_id: str = Path(..., min_length=8, max_length=64),
    status: str | None = Query(default=None, min_length=3, max_length=16),
    since: datetime | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=1000),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> list[TelemetryAnomaly]:
    return await store.list_telemetry_anomalies(
        asset_id=asset_id,
        status=status,
        since=since,
        limit=limit,
    )

@app.post("/inventory/os", status_code=status.HTTP_202_ACCEPTED)
async def ingest_os(
    payload: OsInventory,
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> dict:
    await store.upsert_os(payload)
    return {"status": "accepted"}


@app.post("/inventory/software", status_code=status.HTTP_202_ACCEPTED)
async def ingest_software(
    payload: SoftwareInventory,
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> dict:
    await store.upsert_software(payload)
    return {"status": "accepted"}


@app.post("/inventory/users", status_code=status.HTTP_202_ACCEPTED)
async def ingest_users(
    payload: LocalUsersInventory,
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> dict:
    await store.upsert_users(payload)
    return {"status": "accepted"}


@app.post("/inventory/groups", status_code=status.HTTP_202_ACCEPTED)
async def ingest_groups(
    payload: LocalGroupsInventory,
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> dict:
    await store.upsert_groups(payload)
    return {"status": "accepted"}


@app.get("/inventory/{asset_id}", response_model=InventorySnapshot)
async def get_inventory(
    asset_id: str = Path(..., min_length=8, max_length=64),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> InventorySnapshot:
    snapshot = await store.snapshot(asset_id)
    return snapshot


@app.get("/inventory/{asset_id}/state", response_model=AssetStateResponse)
async def get_inventory_state(
    asset_id: str = Path(..., min_length=8, max_length=64),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> AssetStateResponse:
    snapshot = await store.snapshot(asset_id)
    state = derive_state(asset_id, snapshot)
    return AssetStateResponse(**state.__dict__)


@app.get("/inventory/assets", response_model=list[AssetRecord])
async def list_assets(
    tenant_id: str | None = Query(default=None, min_length=8, max_length=64),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0, le=100000),
    since: datetime | None = Query(default=None),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> list[AssetRecord]:
    return await store.list_assets(
        tenant_id=tenant_id,
        limit=limit,
        offset=offset,
        since=since,
    )


@app.get("/inventory/assets/page", response_model=AssetRecordPage)
async def list_assets_page(
    tenant_id: str | None = Query(default=None, min_length=8, max_length=64),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0, le=100000),
    since: datetime | None = Query(default=None),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> AssetRecordPage:
    items, total = await store.list_assets_page(
        tenant_id=tenant_id,
        limit=limit,
        offset=offset,
        since=since,
    )
    return AssetRecordPage(
        items=items,
        limit=limit,
        offset=offset,
        total=total,
    )


@app.get("/inventory/assets/state", response_model=list[AssetStateResponse])
async def list_asset_states(
    tenant_id: str | None = Query(default=None, min_length=8, max_length=64),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0, le=100000),
    since: datetime | None = Query(default=None),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> list[AssetStateResponse]:
    return await store.list_asset_states(
        tenant_id=tenant_id,
        limit=limit,
        offset=offset,
        since=since,
    )


@app.get("/inventory/assets/state/page", response_model=AssetStatePage)
async def list_asset_states_page(
    tenant_id: str | None = Query(default=None, min_length=8, max_length=64),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0, le=100000),
    since: datetime | None = Query(default=None),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> AssetStatePage:
    items, total = await store.list_asset_states_page(
        tenant_id=tenant_id,
        limit=limit,
        offset=offset,
        since=since,
    )
    return AssetStatePage(
        items=items,
        limit=limit,
        offset=offset,
        total=total,
    )


@app.get("/inventory/assets/overview", response_model=list[AssetInventoryOverview])
async def list_asset_overviews(
    tenant_id: str | None = Query(default=None, min_length=8, max_length=64),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0, le=100000),
    since: datetime | None = Query(default=None),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> list[AssetInventoryOverview]:
    return await store.list_asset_overviews(
        tenant_id=tenant_id, limit=limit, offset=offset, since=since
    )


@app.get("/inventory/assets/overview/page", response_model=AssetInventoryPage)
async def list_asset_overview_page(
    tenant_id: str | None = Query(default=None, min_length=8, max_length=64),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0, le=100000),
    since: datetime | None = Query(default=None),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> AssetInventoryPage:
    items, total = await store.list_asset_overview_page(
        tenant_id=tenant_id,
        limit=limit,
        offset=offset,
        since=since,
    )
    return AssetInventoryPage(
        items=items,
        limit=limit,
        offset=offset,
        total=total,
    )


@app.get("/inventory/assets/overview.csv", response_class=Response)
async def export_asset_overviews_csv(
    tenant_id: str | None = Query(default=None, min_length=8, max_length=64),
    limit: int = Query(default=500, ge=1, le=2000),
    offset: int = Query(default=0, ge=0, le=100000),
    since: datetime | None = Query(default=None),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> Response:
    records = await store.list_asset_overviews(
        tenant_id=tenant_id,
        limit=limit,
        offset=offset,
        since=since,
    )
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "asset_id",
            "tenant_id",
            "hostname",
            "os_name",
            "os_version",
            "hardware_model",
            "software_count",
            "users_count",
            "groups_count",
            "last_seen_at",
            "updated_at",
        ]
    )
    for record in records:
        writer.writerow(
            [
                record.asset_id,
                record.tenant_id,
                record.hostname,
                record.os_name,
                record.os_version,
                record.hardware_model,
                record.software_count,
                record.users_count,
                record.groups_count,
                record.last_seen_at.isoformat() if record.last_seen_at else None,
                record.updated_at.isoformat(),
            ]
        )
    content = buffer.getvalue()
    return Response(content=content, media_type="text/csv")


@app.get(
    "/inventory/assets/{asset_id}/overview",
    response_model=AssetInventoryOverview,
)
async def get_asset_overview(
    asset_id: str = Path(..., min_length=8, max_length=64),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> AssetInventoryOverview:
    overview = await store.get_asset_overview(asset_id)
    if not overview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="asset_not_found",
        )
    return overview


@app.get("/inventory/assets/stats", response_model=AssetInventoryStats)
async def get_asset_inventory_stats(
    tenant_id: str | None = Query(default=None, min_length=8, max_length=64),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> AssetInventoryStats:
    return await store.get_asset_inventory_stats(tenant_id=tenant_id)

"""Ingestion service entry point for MVP-3 inventory data."""
from __future__ import annotations

from datetime import datetime, timezone
import asyncpg
from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request, status
from fastapi.responses import JSONResponse

from .config import Settings, load_settings
from .models import (
    HardwareInventory,
    LocalGroupsInventory,
    LocalUsersInventory,
    OsInventory,
    SoftwareInventory,
    AssetInventoryOverview,
    AssetRecord,
    InventorySnapshot,
    AssetStateResponse,
)
from .storage import InventoryStore
from .state import derive_state

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
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> list[AssetRecord]:
    return await store.list_assets(tenant_id)


@app.get("/inventory/assets/state", response_model=list[AssetStateResponse])
async def list_asset_states(
    tenant_id: str | None = Query(default=None, min_length=8, max_length=64),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> list[AssetStateResponse]:
    return await store.list_asset_states(tenant_id)


@app.get("/inventory/assets/overview", response_model=list[AssetInventoryOverview])
async def list_asset_overviews(
    tenant_id: str | None = Query(default=None, min_length=8, max_length=64),
    store: InventoryStore = Depends(get_store),
    _: None = Depends(enforce_https),
) -> list[AssetInventoryOverview]:
    return await store.list_asset_overviews(tenant_id)


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

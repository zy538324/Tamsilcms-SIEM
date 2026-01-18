"""Ingestion service entry point for MVP-3 inventory data."""
from __future__ import annotations

from datetime import datetime, timezone
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from .config import Settings, load_settings
from .models import (
    HardwareInventory,
    LocalGroupsInventory,
    LocalUsersInventory,
    OsInventory,
    SoftwareInventory,
    InventorySnapshot,
    AssetStateResponse,
)
from .persistence import (
    persist_groups,
    persist_hardware,
    persist_os,
    persist_software,
    persist_users,
)
from .storage import store
from .state import derive_state

app = FastAPI(title="Ingestion Service", version="0.1.0")


def get_settings() -> Settings:
    return load_settings()


async def enforce_https(request: Request) -> None:
    forwarded_proto = request.headers.get("x-forwarded-proto", "http")
    if forwarded_proto.lower() != "https":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="https_required",
        )


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
    _: None = Depends(enforce_https),
) -> dict:
    store.upsert_hardware(payload)
    persist_hardware(payload)
    return {"status": "accepted"}


@app.post("/inventory/os", status_code=status.HTTP_202_ACCEPTED)
async def ingest_os(
    payload: OsInventory,
    _: None = Depends(enforce_https),
) -> dict:
    store.upsert_os(payload)
    persist_os(payload)
    return {"status": "accepted"}


@app.post("/inventory/software", status_code=status.HTTP_202_ACCEPTED)
async def ingest_software(
    payload: SoftwareInventory,
    _: None = Depends(enforce_https),
) -> dict:
    store.upsert_software(payload)
    persist_software(payload)
    return {"status": "accepted"}


@app.post("/inventory/users", status_code=status.HTTP_202_ACCEPTED)
async def ingest_users(
    payload: LocalUsersInventory,
    _: None = Depends(enforce_https),
) -> dict:
    store.upsert_users(payload)
    persist_users(payload)
    return {"status": "accepted"}


@app.post("/inventory/groups", status_code=status.HTTP_202_ACCEPTED)
async def ingest_groups(
    payload: LocalGroupsInventory,
    _: None = Depends(enforce_https),
) -> dict:
    store.upsert_groups(payload)
    persist_groups(payload)
    return {"status": "accepted"}


@app.get("/inventory/{asset_id}", response_model=InventorySnapshot)
async def get_inventory(
    asset_id: str,
    _: None = Depends(enforce_https),
) -> InventorySnapshot:
    snapshot = store.snapshot(asset_id)
    return snapshot


@app.get("/inventory/{asset_id}/state", response_model=AssetStateResponse)
async def get_inventory_state(
    asset_id: str,
    _: None = Depends(enforce_https),
) -> AssetStateResponse:
    snapshot = store.snapshot(asset_id)
    state = derive_state(asset_id, snapshot)
    return AssetStateResponse(**state.__dict__)

"""Pydantic models for MVP-3 inventory ingestion and MVP-4 telemetry."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class InventoryBase(BaseModel):
    tenant_id: str = Field(..., min_length=8, max_length=64)
    asset_id: str = Field(..., min_length=8, max_length=64)
    collected_at: datetime
    hostname: Optional[str] = None


class HardwareInventory(InventoryBase):
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    cpu_model: Optional[str] = None
    cpu_cores: Optional[int] = None
    memory_mb: Optional[int] = None
    storage_gb: Optional[int] = None


class OsInventory(InventoryBase):
    os_name: str = Field(..., min_length=1, max_length=64)
    os_version: str = Field(..., min_length=1, max_length=64)
    kernel_version: Optional[str] = None
    architecture: Optional[str] = None
    install_date: Optional[str] = None


class SoftwareItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    vendor: Optional[str] = None
    version: Optional[str] = None
    install_date: Optional[str] = None
    source: Optional[str] = None


class SoftwareInventory(InventoryBase):
    items: List[SoftwareItem]


class LocalUser(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    display_name: Optional[str] = None
    uid: Optional[str] = None
    is_admin: bool = False
    last_login_at: Optional[datetime] = None


class LocalUsersInventory(InventoryBase):
    users: List[LocalUser]


class LocalGroup(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    gid: Optional[str] = None
    members: List[str] = Field(default_factory=list)


class LocalGroupsInventory(InventoryBase):
    groups: List[LocalGroup]


class InventorySnapshot(BaseModel):
    hardware: Optional[HardwareInventory] = None
    os: Optional[OsInventory] = None
    software: Optional[SoftwareInventory] = None
    users: Optional[LocalUsersInventory] = None
    groups: Optional[LocalGroupsInventory] = None


class AssetStateResponse(BaseModel):
    asset_id: str
    hostname: Optional[str] = None
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    software_count: int
    users_count: int
    groups_count: int


class AssetRecord(BaseModel):
    asset_id: str
    tenant_id: str
    hostname: str
    asset_type: str
    environment: Optional[str] = None
    status: str
    criticality: Optional[str] = None
    last_seen_at: Optional[datetime] = None
    updated_at: datetime


class AssetRecordPage(BaseModel):
    items: List[AssetRecord]
    limit: int
    offset: int
    total: int


class AssetInventoryOverview(BaseModel):
    asset_id: str
    tenant_id: str
    hostname: str
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    hardware_model: Optional[str] = None
    software_count: int
    users_count: int
    groups_count: int
    last_seen_at: Optional[datetime] = None
    updated_at: datetime


class AssetStatePage(BaseModel):
    items: List[AssetStateResponse]
    limit: int
    offset: int
    total: int


class AssetInventoryPage(BaseModel):
    items: List[AssetInventoryOverview]
    limit: int
    offset: int
    total: int


class AssetInventoryStats(BaseModel):
    total_assets: int
    assets_with_hardware: int
    assets_with_os: int
    assets_with_software: int
    assets_with_users: int
    assets_with_groups: int


class TelemetrySample(BaseModel):
    name: str = Field(..., min_length=3, max_length=128)
    value: float
    unit: Optional[str] = Field(default=None, max_length=32)
    observed_at: datetime


class TelemetryPayload(BaseModel):
    payload_id: UUID
    tenant_id: str = Field(..., min_length=8, max_length=64)
    asset_id: str = Field(..., min_length=8, max_length=64)
    collected_at: datetime
    hostname: Optional[str] = None
    schema_version: str = Field(default="v1", max_length=16)
    samples: List[TelemetrySample]


class TelemetryIngestResponse(BaseModel):
    status: str
    accepted_samples: int


class TelemetryMetricSummary(BaseModel):
    name: str
    unit: str
    last_value: float
    last_observed_at: datetime


class TelemetryPoint(BaseModel):
    observed_at: datetime
    value: float


class TelemetrySeries(BaseModel):
    asset_id: str
    metric_name: str
    unit: str
    points: List[TelemetryPoint]

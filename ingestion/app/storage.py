"""In-memory storage for MVP-3 inventory ingestion."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from .models import (
    HardwareInventory,
    InventorySnapshot,
    LocalGroupsInventory,
    LocalUsersInventory,
    OsInventory,
    SoftwareInventory,
)


@dataclass
class InventoryStore:
    hardware: Dict[str, HardwareInventory]
    os: Dict[str, OsInventory]
    software: Dict[str, SoftwareInventory]
    users: Dict[str, LocalUsersInventory]
    groups: Dict[str, LocalGroupsInventory]

    def __init__(self) -> None:
        self.hardware = {}
        self.os = {}
        self.software = {}
        self.users = {}
        self.groups = {}

    def upsert_hardware(self, payload: HardwareInventory) -> None:
        self.hardware[payload.asset_id] = payload

    def upsert_os(self, payload: OsInventory) -> None:
        self.os[payload.asset_id] = payload

    def upsert_software(self, payload: SoftwareInventory) -> None:
        self.software[payload.asset_id] = payload

    def upsert_users(self, payload: LocalUsersInventory) -> None:
        self.users[payload.asset_id] = payload

    def upsert_groups(self, payload: LocalGroupsInventory) -> None:
        self.groups[payload.asset_id] = payload

    def snapshot(self, asset_id: str) -> InventorySnapshot:
        return InventorySnapshot(
            hardware=self.hardware.get(asset_id),
            os=self.os.get(asset_id),
            software=self.software.get(asset_id),
            users=self.users.get(asset_id),
            groups=self.groups.get(asset_id),
        )


store = InventoryStore()

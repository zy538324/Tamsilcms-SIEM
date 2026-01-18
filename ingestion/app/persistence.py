"""Persistence stubs for MVP-3.

These functions define the contract for storing inventory in PostgreSQL. Replace
with actual database integration in the next iteration.
"""
from __future__ import annotations

from .models import (
    HardwareInventory,
    LocalGroupsInventory,
    LocalUsersInventory,
    OsInventory,
    SoftwareInventory,
)


def persist_hardware(_: HardwareInventory) -> None:
    return None


def persist_os(_: OsInventory) -> None:
    return None


def persist_software(_: SoftwareInventory) -> None:
    return None


def persist_users(_: LocalUsersInventory) -> None:
    return None


def persist_groups(_: LocalGroupsInventory) -> None:
    return None


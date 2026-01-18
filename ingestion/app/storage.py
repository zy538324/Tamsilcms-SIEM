"""PostgreSQL-backed storage for MVP-3 inventory ingestion."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional

import asyncpg

from .models import (
    AssetInventoryOverview,
    AssetRecord,
    AssetStateResponse,
    HardwareInventory,
    InventorySnapshot,
    LocalGroup,
    LocalGroupsInventory,
    LocalUser,
    LocalUsersInventory,
    OsInventory,
    SoftwareInventory,
    SoftwareItem,
)


def _parse_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _to_iso_date(value: Optional[date]) -> Optional[str]:
    return value.isoformat() if value else None


@dataclass
class InventoryStore:
    pool: asyncpg.Pool

    async def _ensure_tenant(self, tenant_id: str) -> None:
        tenant_name = f"tenant-{tenant_id}"
        tenant_slug = f"tenant-{tenant_id}"
        await self.pool.execute(
            """
            INSERT INTO tenants (tenant_id, name, slug)
            VALUES ($1, $2, $3)
            ON CONFLICT (tenant_id) DO NOTHING
            """,
            tenant_id,
            tenant_name,
            tenant_slug,
        )

    async def _ensure_asset(
        self,
        tenant_id: str,
        asset_id: str,
        hostname: Optional[str],
        collected_at: datetime,
    ) -> None:
        await self._ensure_tenant(tenant_id)
        resolved_hostname = hostname or asset_id
        await self.pool.execute(
            """
            INSERT INTO assets (
                asset_id,
                tenant_id,
                hostname,
                asset_type,
                last_seen_at
            )
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (asset_id) DO UPDATE
            SET hostname = EXCLUDED.hostname,
                updated_at = NOW(),
                last_seen_at = EXCLUDED.last_seen_at
            """,
            asset_id,
            tenant_id,
            resolved_hostname,
            "unknown",
            collected_at,
        )

    async def upsert_hardware(self, payload: HardwareInventory) -> None:
        await self._ensure_asset(
            payload.tenant_id,
            payload.asset_id,
            payload.hostname,
            payload.collected_at,
        )
        await self.pool.execute(
            """
            INSERT INTO hardware_inventory (
                asset_id,
                manufacturer,
                model,
                serial_number,
                cpu_model,
                cpu_cores,
                memory_mb,
                storage_gb,
                updated_at
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (asset_id) DO UPDATE
            SET manufacturer = EXCLUDED.manufacturer,
                model = EXCLUDED.model,
                serial_number = EXCLUDED.serial_number,
                cpu_model = EXCLUDED.cpu_model,
                cpu_cores = EXCLUDED.cpu_cores,
                memory_mb = EXCLUDED.memory_mb,
                storage_gb = EXCLUDED.storage_gb,
                updated_at = EXCLUDED.updated_at
            """,
            payload.asset_id,
            payload.manufacturer,
            payload.model,
            payload.serial_number,
            payload.cpu_model,
            payload.cpu_cores,
            payload.memory_mb,
            payload.storage_gb,
            payload.collected_at,
        )

    async def upsert_os(self, payload: OsInventory) -> None:
        await self._ensure_asset(
            payload.tenant_id,
            payload.asset_id,
            payload.hostname,
            payload.collected_at,
        )
        await self.pool.execute(
            """
            INSERT INTO os_inventory (
                asset_id,
                os_name,
                os_version,
                kernel_version,
                architecture,
                install_date,
                updated_at
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (asset_id) DO UPDATE
            SET os_name = EXCLUDED.os_name,
                os_version = EXCLUDED.os_version,
                kernel_version = EXCLUDED.kernel_version,
                architecture = EXCLUDED.architecture,
                install_date = EXCLUDED.install_date,
                updated_at = EXCLUDED.updated_at
            """,
            payload.asset_id,
            payload.os_name,
            payload.os_version,
            payload.kernel_version,
            payload.architecture,
            _parse_date(payload.install_date),
            payload.collected_at,
        )

    async def upsert_software(self, payload: SoftwareInventory) -> None:
        await self._ensure_asset(
            payload.tenant_id,
            payload.asset_id,
            payload.hostname,
            payload.collected_at,
        )
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    "DELETE FROM software_inventory WHERE asset_id = $1",
                    payload.asset_id,
                )
                for item in payload.items:
                    await connection.execute(
                        """
                        INSERT INTO software_inventory (
                            asset_id,
                            name,
                            vendor,
                            version,
                            install_date,
                            source,
                            updated_at
                        )
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                        """,
                        payload.asset_id,
                        item.name,
                        item.vendor,
                        item.version,
                        _parse_date(item.install_date),
                        item.source,
                        payload.collected_at,
                    )

    async def upsert_users(self, payload: LocalUsersInventory) -> None:
        await self._ensure_asset(
            payload.tenant_id,
            payload.asset_id,
            payload.hostname,
            payload.collected_at,
        )
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    "DELETE FROM local_users WHERE asset_id = $1",
                    payload.asset_id,
                )
                for user in payload.users:
                    await connection.execute(
                        """
                        INSERT INTO local_users (
                            asset_id,
                            username,
                            display_name,
                            uid,
                            is_admin,
                            last_login_at,
                            updated_at
                        )
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                        """,
                        payload.asset_id,
                        user.username,
                        user.display_name,
                        user.uid,
                        user.is_admin,
                        user.last_login_at,
                        payload.collected_at,
                    )

    async def upsert_groups(self, payload: LocalGroupsInventory) -> None:
        await self._ensure_asset(
            payload.tenant_id,
            payload.asset_id,
            payload.hostname,
            payload.collected_at,
        )
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    """
                    DELETE FROM local_group_members
                    WHERE group_id IN (
                        SELECT group_id FROM local_groups WHERE asset_id = $1
                    )
                    """,
                    payload.asset_id,
                )
                await connection.execute(
                    "DELETE FROM local_groups WHERE asset_id = $1",
                    payload.asset_id,
                )

                for group in payload.groups:
                    group_id = await connection.fetchval(
                        """
                        INSERT INTO local_groups (
                            asset_id,
                            name,
                            gid,
                            updated_at
                        )
                        VALUES ($1, $2, $3, $4)
                        RETURNING group_id
                        """,
                        payload.asset_id,
                        group.name,
                        group.gid,
                        payload.collected_at,
                    )

                    for member in group.members:
                        await connection.execute(
                            """
                            INSERT INTO local_group_members (
                                group_id,
                                member_name
                            )
                            VALUES ($1, $2)
                            ON CONFLICT (group_id, member_name) DO NOTHING
                            """,
                            group_id,
                            member,
                        )

    async def snapshot(self, asset_id: str) -> InventorySnapshot:
        asset = await self._fetch_asset_context(asset_id)
        tenant_id = asset["tenant_id"] if asset else ""
        hostname = asset["hostname"] if asset else None

        hardware = await self._fetch_hardware(asset_id, tenant_id, hostname)
        os_inventory = await self._fetch_os(asset_id, tenant_id, hostname)
        software = await self._fetch_software(asset_id, tenant_id, hostname)
        users = await self._fetch_users(asset_id, tenant_id, hostname)
        groups = await self._fetch_groups(asset_id, tenant_id, hostname)
        return InventorySnapshot(
            hardware=hardware,
            os=os_inventory,
            software=software,
            users=users,
            groups=groups,
        )

    async def list_assets(
        self,
        tenant_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AssetRecord]:
        if tenant_id:
            rows = await self.pool.fetch(
                """
                SELECT asset_id,
                       tenant_id,
                       hostname,
                       asset_type,
                       environment,
                       status,
                       criticality,
                       last_seen_at,
                       updated_at
                FROM assets
                WHERE tenant_id = $1
                ORDER BY updated_at DESC
                LIMIT $2 OFFSET $3
                """,
                tenant_id,
                limit,
                offset,
            )
        else:
            rows = await self.pool.fetch(
                """
                SELECT asset_id,
                       tenant_id,
                       hostname,
                       asset_type,
                       environment,
                       status,
                       criticality,
                       last_seen_at,
                       updated_at
                FROM assets
                ORDER BY updated_at DESC
                LIMIT $1 OFFSET $2
                """,
                limit,
                offset,
            )
        return [
            AssetRecord(
                asset_id=str(row["asset_id"]),
                tenant_id=str(row["tenant_id"]),
                hostname=row["hostname"],
                asset_type=row["asset_type"],
                environment=row["environment"],
                status=row["status"],
                criticality=row["criticality"],
                last_seen_at=row["last_seen_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

    async def list_asset_states(
        self,
        tenant_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AssetStateResponse]:
        base_query = """
            SELECT a.asset_id,
                   a.hostname,
                   os.os_name,
                   os.os_version,
                   COALESCE(sw.software_count, 0) AS software_count,
                   COALESCE(u.user_count, 0) AS users_count,
                   COALESCE(g.group_count, 0) AS groups_count
            FROM assets a
            LEFT JOIN os_inventory os ON os.asset_id = a.asset_id
            LEFT JOIN (
                SELECT asset_id, COUNT(*) AS software_count
                FROM software_inventory
                GROUP BY asset_id
            ) sw ON sw.asset_id = a.asset_id
            LEFT JOIN (
                SELECT asset_id, COUNT(*) AS user_count
                FROM local_users
                GROUP BY asset_id
            ) u ON u.asset_id = a.asset_id
            LEFT JOIN (
                SELECT asset_id, COUNT(*) AS group_count
                FROM local_groups
                GROUP BY asset_id
            ) g ON g.asset_id = a.asset_id
        """
        if tenant_id:
            rows = await self.pool.fetch(
                base_query
                + " WHERE a.tenant_id = $1 ORDER BY a.updated_at DESC LIMIT $2 OFFSET $3",
                tenant_id,
                limit,
                offset,
            )
        else:
            rows = await self.pool.fetch(
                base_query + " ORDER BY a.updated_at DESC LIMIT $1 OFFSET $2",
                limit,
                offset,
            )
        return [
            AssetStateResponse(
                asset_id=str(row["asset_id"]),
                hostname=row["hostname"],
                os_name=row["os_name"],
                os_version=row["os_version"],
                software_count=row["software_count"],
                users_count=row["users_count"],
                groups_count=row["groups_count"],
            )
            for row in rows
        ]

    async def list_asset_overviews(
        self,
        tenant_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AssetInventoryOverview]:
        base_query = """
            SELECT a.asset_id,
                   a.tenant_id,
                   a.hostname,
                   a.last_seen_at,
                   a.updated_at,
                   os.os_name,
                   os.os_version,
                   hw.model AS hardware_model,
                   COALESCE(sw.software_count, 0) AS software_count,
                   COALESCE(u.user_count, 0) AS users_count,
                   COALESCE(g.group_count, 0) AS groups_count
            FROM assets a
            LEFT JOIN os_inventory os ON os.asset_id = a.asset_id
            LEFT JOIN hardware_inventory hw ON hw.asset_id = a.asset_id
            LEFT JOIN (
                SELECT asset_id, COUNT(*) AS software_count
                FROM software_inventory
                GROUP BY asset_id
            ) sw ON sw.asset_id = a.asset_id
            LEFT JOIN (
                SELECT asset_id, COUNT(*) AS user_count
                FROM local_users
                GROUP BY asset_id
            ) u ON u.asset_id = a.asset_id
            LEFT JOIN (
                SELECT asset_id, COUNT(*) AS group_count
                FROM local_groups
                GROUP BY asset_id
            ) g ON g.asset_id = a.asset_id
        """
        if tenant_id:
            rows = await self.pool.fetch(
                base_query
                + " WHERE a.tenant_id = $1 ORDER BY a.updated_at DESC LIMIT $2 OFFSET $3",
                tenant_id,
                limit,
                offset,
            )
        else:
            rows = await self.pool.fetch(
                base_query + " ORDER BY a.updated_at DESC LIMIT $1 OFFSET $2",
                limit,
                offset,
            )
        return [
            AssetInventoryOverview(
                asset_id=str(row["asset_id"]),
                tenant_id=str(row["tenant_id"]),
                hostname=row["hostname"],
                os_name=row["os_name"],
                os_version=row["os_version"],
                hardware_model=row["hardware_model"],
                software_count=row["software_count"],
                users_count=row["users_count"],
                groups_count=row["groups_count"],
                last_seen_at=row["last_seen_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]

    async def get_asset_overview(
        self, asset_id: str
    ) -> Optional[AssetInventoryOverview]:
        row = await self.pool.fetchrow(
            """
            SELECT a.asset_id,
                   a.tenant_id,
                   a.hostname,
                   a.last_seen_at,
                   a.updated_at,
                   os.os_name,
                   os.os_version,
                   hw.model AS hardware_model,
                   COALESCE(sw.software_count, 0) AS software_count,
                   COALESCE(u.user_count, 0) AS users_count,
                   COALESCE(g.group_count, 0) AS groups_count
            FROM assets a
            LEFT JOIN os_inventory os ON os.asset_id = a.asset_id
            LEFT JOIN hardware_inventory hw ON hw.asset_id = a.asset_id
            LEFT JOIN (
                SELECT asset_id, COUNT(*) AS software_count
                FROM software_inventory
                GROUP BY asset_id
            ) sw ON sw.asset_id = a.asset_id
            LEFT JOIN (
                SELECT asset_id, COUNT(*) AS user_count
                FROM local_users
                GROUP BY asset_id
            ) u ON u.asset_id = a.asset_id
            LEFT JOIN (
                SELECT asset_id, COUNT(*) AS group_count
                FROM local_groups
                GROUP BY asset_id
            ) g ON g.asset_id = a.asset_id
            WHERE a.asset_id = $1
            """,
            asset_id,
        )
        if not row:
            return None
        return AssetInventoryOverview(
            asset_id=str(row["asset_id"]),
            tenant_id=str(row["tenant_id"]),
            hostname=row["hostname"],
            os_name=row["os_name"],
            os_version=row["os_version"],
            hardware_model=row["hardware_model"],
            software_count=row["software_count"],
            users_count=row["users_count"],
            groups_count=row["groups_count"],
            last_seen_at=row["last_seen_at"],
            updated_at=row["updated_at"],
        )

    async def _fetch_asset_context(self, asset_id: str) -> Optional[asyncpg.Record]:
        return await self.pool.fetchrow(
            """
            SELECT tenant_id,
                   hostname
            FROM assets
            WHERE asset_id = $1
            """,
            asset_id,
        )

    async def _fetch_hardware(
        self,
        asset_id: str,
        tenant_id: str,
        hostname: Optional[str],
    ) -> Optional[HardwareInventory]:
        row = await self.pool.fetchrow(
            """
            SELECT manufacturer,
                   model,
                   serial_number,
                   cpu_model,
                   cpu_cores,
                   memory_mb,
                   storage_gb,
                   updated_at
            FROM hardware_inventory
            WHERE asset_id = $1
            """,
            asset_id,
        )
        if not row:
            return None
        return HardwareInventory(
            tenant_id=tenant_id,
            asset_id=asset_id,
            collected_at=row["updated_at"],
            hostname=hostname,
            manufacturer=row["manufacturer"],
            model=row["model"],
            serial_number=row["serial_number"],
            cpu_model=row["cpu_model"],
            cpu_cores=row["cpu_cores"],
            memory_mb=row["memory_mb"],
            storage_gb=row["storage_gb"],
        )

    async def _fetch_os(
        self,
        asset_id: str,
        tenant_id: str,
        hostname: Optional[str],
    ) -> Optional[OsInventory]:
        row = await self.pool.fetchrow(
            """
            SELECT os_name,
                   os_version,
                   kernel_version,
                   architecture,
                   install_date,
                   updated_at
            FROM os_inventory
            WHERE asset_id = $1
            """,
            asset_id,
        )
        if not row:
            return None
        return OsInventory(
            tenant_id=tenant_id,
            asset_id=asset_id,
            collected_at=row["updated_at"],
            hostname=hostname,
            os_name=row["os_name"],
            os_version=row["os_version"],
            kernel_version=row["kernel_version"],
            architecture=row["architecture"],
            install_date=_to_iso_date(row["install_date"]),
        )

    async def _fetch_software(
        self,
        asset_id: str,
        tenant_id: str,
        hostname: Optional[str],
    ) -> Optional[SoftwareInventory]:
        rows = await self.pool.fetch(
            """
            SELECT name,
                   vendor,
                   version,
                   install_date,
                   source,
                   updated_at
            FROM software_inventory
            WHERE asset_id = $1
            ORDER BY name
            """,
            asset_id,
        )
        if not rows:
            return None
        collected_at = max(row["updated_at"] for row in rows)
        items = [
            SoftwareItem(
                name=row["name"],
                vendor=row["vendor"],
                version=row["version"],
                install_date=_to_iso_date(row["install_date"]),
                source=row["source"],
            )
            for row in rows
        ]
        return SoftwareInventory(
            tenant_id=tenant_id,
            asset_id=asset_id,
            collected_at=collected_at,
            hostname=hostname,
            items=items,
        )

    async def _fetch_users(
        self,
        asset_id: str,
        tenant_id: str,
        hostname: Optional[str],
    ) -> Optional[LocalUsersInventory]:
        rows = await self.pool.fetch(
            """
            SELECT username,
                   display_name,
                   uid,
                   is_admin,
                   last_login_at,
                   updated_at
            FROM local_users
            WHERE asset_id = $1
            ORDER BY username
            """,
            asset_id,
        )
        if not rows:
            return None
        collected_at = max(row["updated_at"] for row in rows)
        users = [
            LocalUser(
                username=row["username"],
                display_name=row["display_name"],
                uid=row["uid"],
                is_admin=row["is_admin"],
                last_login_at=row["last_login_at"],
            )
            for row in rows
        ]
        return LocalUsersInventory(
            tenant_id=tenant_id,
            asset_id=asset_id,
            collected_at=collected_at,
            hostname=hostname,
            users=users,
        )

    async def _fetch_groups(
        self,
        asset_id: str,
        tenant_id: str,
        hostname: Optional[str],
    ) -> Optional[LocalGroupsInventory]:
        rows = await self.pool.fetch(
            """
            SELECT g.group_id,
                   g.name,
                   g.gid,
                   g.updated_at,
                   COALESCE(
                       ARRAY_AGG(m.member_name) FILTER (WHERE m.member_name IS NOT NULL),
                       ARRAY[]::text[]
                   ) AS members
            FROM local_groups g
            LEFT JOIN local_group_members m ON m.group_id = g.group_id
            WHERE g.asset_id = $1
            GROUP BY g.group_id
            ORDER BY g.name
            """,
            asset_id,
        )
        if not rows:
            return None
        collected_at = max(row["updated_at"] for row in rows)
        groups = [
            LocalGroup(
                name=row["name"],
                gid=row["gid"],
                members=list(row["members"] or []),
            )
            for row in rows
        ]
        return LocalGroupsInventory(
            tenant_id=tenant_id,
            asset_id=asset_id,
            collected_at=collected_at,
            hostname=hostname,
            groups=groups,
        )

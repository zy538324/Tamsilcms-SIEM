"""Database connection helpers for the ingestion service."""
from __future__ import annotations

import asyncpg

from .config import Settings


async def create_pool(settings: Settings) -> asyncpg.Pool:
    """Create and validate an asyncpg pool for ingestion storage."""
    pool = await asyncpg.create_pool(
        dsn=settings.database_dsn,
        min_size=settings.database_min_connections,
        max_size=settings.database_max_connections,
    )
    async with pool.acquire() as connection:
        await connection.execute("SELECT 1")
    return pool

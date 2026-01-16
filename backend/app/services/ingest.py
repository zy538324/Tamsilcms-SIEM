from datetime import datetime
from typing import Iterable

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_api_key
from app.models import Agent, LogEntry
from app.schemas import IngestPayload, LogEvent


async def _get_agent(session: AsyncSession, agent_id: str) -> Agent | None:
    result = await session.execute(select(Agent).where(Agent.id == agent_id))
    return result.scalar_one_or_none()


def _prepare_rows(events: Iterable[LogEvent], received_at: datetime) -> list[LogEntry]:
    return [
        LogEntry(
            agent_id=event.agent_id,
            log_source=event.log_source,
            event_time=event.event_time,
            received_at=received_at,
            event_level=event.event_level,
            event_id=event.event_id,
            message=event.message,
        )
        for event in events
    ]


async def ingest_events(session: AsyncSession, payload: IngestPayload, api_key: str) -> None:
    agent = await _get_agent(session, payload.agent_id)
    if not agent or not verify_api_key(api_key, agent.api_key_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    for event in payload.events:
        if event.agent_id != payload.agent_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agent mismatch")

    received_at = datetime.utcnow()
    rows = _prepare_rows(payload.events, received_at)

    session.add_all(rows)
    await session.commit()

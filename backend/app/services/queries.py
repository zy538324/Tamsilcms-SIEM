from datetime import datetime
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Agent, LogEntry
from app.schemas import AgentResponse, LogResponse


async def fetch_agents(session: AsyncSession, limit: int, offset: int) -> List[AgentResponse]:
    last_seen = func.max(LogEntry.received_at).label("last_seen")
    log_count = func.count(LogEntry.id).label("log_count")

    query = (
        select(Agent, last_seen, log_count)
        .outerjoin(LogEntry, LogEntry.agent_id == Agent.id)
        .group_by(Agent.id)
        .order_by(last_seen.desc().nullslast(), Agent.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    result = await session.execute(query)
    agents: List[AgentResponse] = []
    for row in result:
        agent = row[0]
        agents.append(
            AgentResponse(
                id=agent.id,
                hostname=agent.hostname,
                os_type=agent.os_type,
                os_version=agent.os_version,
                created_at=agent.created_at,
                last_seen=row[1],
                log_count=row[2] or 0,
            )
        )
    return agents


async def fetch_logs(
    session: AsyncSession,
    agent_id: Optional[str],
    log_source: Optional[str],
    event_level: Optional[str],
    search: Optional[str],
    start_time: Optional[str],
    end_time: Optional[str],
    limit: int,
    offset: int,
) -> List[LogResponse]:
    query = select(LogEntry).order_by(LogEntry.event_time.desc()).limit(limit).offset(offset)

    if agent_id:
        query = query.where(LogEntry.agent_id == agent_id)
    if log_source:
        query = query.where(LogEntry.log_source == log_source)
    if event_level:
        query = query.where(LogEntry.event_level == event_level.upper())
    if search:
        query = query.where(LogEntry.message.ilike(f"%{search}%"))
    if start_time:
        query = query.where(LogEntry.event_time >= datetime.fromisoformat(start_time))
    if end_time:
        query = query.where(LogEntry.event_time <= datetime.fromisoformat(end_time))

    result = await session.execute(query)
    return [
        LogResponse(
            id=row.id,
            agent_id=row.agent_id,
            log_source=row.log_source,
            event_time=row.event_time,
            received_at=row.received_at,
            event_level=row.event_level,
            event_id=row.event_id,
            message=row.message,
        )
        for row in result.scalars().all()
    ]

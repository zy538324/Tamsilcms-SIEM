from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.schemas import AgentResponse, IngestPayload, LogResponse
from app.services.ingest import ingest_events
from app.services.queries import fetch_agents, fetch_logs

api_router = APIRouter()


@api_router.post("/logs/ingest", status_code=status.HTTP_202_ACCEPTED)
async def ingest_logs(
    payload: IngestPayload,
    session: AsyncSession = Depends(get_session),
    x_agent_key: Optional[str] = Header(default=None, alias="X-Agent-Key"),
) -> dict:
    if not x_agent_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key")

    await ingest_events(session, payload, x_agent_key)
    return {"status": "accepted", "received": len(payload.events)}


@api_router.get("/agents", response_model=List[AgentResponse])
async def list_agents(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> List[AgentResponse]:
    return await fetch_agents(session, limit=limit, offset=offset)


@api_router.get("/logs", response_model=List[LogResponse])
async def list_logs(
    session: AsyncSession = Depends(get_session),
    agent_id: Optional[str] = Query(default=None),
    log_source: Optional[str] = Query(default=None),
    event_level: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    start_time: Optional[str] = Query(default=None),
    end_time: Optional[str] = Query(default=None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> List[LogResponse]:
    return await fetch_logs(
        session,
        agent_id=agent_id,
        log_source=log_source,
        event_level=event_level,
        search=search,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
        offset=offset,
    )

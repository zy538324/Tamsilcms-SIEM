from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class LogEvent(BaseModel):
    agent_id: str = Field(..., description="Agent UUID")
    hostname: str = Field(..., max_length=255)
    os_type: str = Field(..., max_length=50)
    os_version: str = Field(..., max_length=100)
    log_source: str = Field(..., max_length=255)
    event_time: datetime
    event_level: str = Field(..., max_length=20)
    event_id: str = Field(..., max_length=50)
    message: str = Field(..., max_length=4000)

    @field_validator("event_level")
    @classmethod
    def normalise_level(cls, value: str) -> str:
        return value.upper()


class IngestPayload(BaseModel):
    agent_id: str
    events: List[LogEvent] = Field(..., max_length=500)

    @field_validator("events")
    @classmethod
    def enforce_batch_limit(cls, value: List[LogEvent]) -> List[LogEvent]:
        if len(value) > 500:
            raise ValueError("Batch size exceeds limit")
        return value


class AgentResponse(BaseModel):
    id: str
    hostname: str
    os_type: str
    os_version: str
    created_at: datetime
    last_seen: Optional[datetime]
    log_count: int


class LogResponse(BaseModel):
    id: int
    agent_id: str
    log_source: str
    event_time: datetime
    received_at: datetime
    event_level: str
    event_id: str
    message: str

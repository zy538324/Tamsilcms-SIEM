"""Pydantic models for request and response schemas."""
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class HelloRequest(BaseModel):
    """Signed hello payload emitted by agents via the transport layer."""

    tenant_id: str = Field(..., min_length=8, max_length=64)
    asset_id: str = Field(..., min_length=8, max_length=64)
    identity_id: str = Field(..., min_length=8, max_length=64)
    event_id: str = Field(..., min_length=8, max_length=64)
    agent_version: str = Field(..., min_length=1, max_length=32)
    hostname: str = Field(..., min_length=1, max_length=255)
    os: str = Field(..., min_length=1, max_length=64)
    uptime_seconds: int = Field(..., ge=0)
    trust_state: str = Field(..., min_length=1, max_length=32)
    sent_at: datetime


class HelloResponse(BaseModel):
    """Response returned after verification."""

    status: str
    received_at: datetime
    service: str


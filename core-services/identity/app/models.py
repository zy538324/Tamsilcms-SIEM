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


class HeartbeatEventResponse(BaseModel):
    """Heartbeat event representation for diagnostics."""

    event_id: str
    agent_id: str
    hostname: str
    os: str
    uptime_seconds: int
    trust_state: str
    received_at: datetime


class AgentStateResponse(BaseModel):
    """Agent state representation for MVP-2 visibility."""

    identity_id: str
    hostname: str
    os: str
    last_seen_at: datetime
    trust_state: str


class AgentPresenceResponse(BaseModel):
    """Agent presence state for online/offline visibility."""

    identity_id: str
    hostname: str
    os: str
    trust_state: str
    last_seen_at: datetime
    status: str


class RiskScoreResponse(BaseModel):
    """Risk score representation for MVP-2 visibility."""

    identity_id: str
    score: float
    rationale: str


class CertificateIssueRequest(BaseModel):
    """Request to register a new client certificate fingerprint."""

    identity_id: str = Field(..., min_length=8, max_length=64)
    fingerprint_sha256: str = Field(..., min_length=8, max_length=128)
    expires_at: datetime


class CertificateIssueResponse(BaseModel):
    """Response after certificate issuance registration."""

    status: str
    issued_at: datetime
    expires_at: datetime


class CertificateRevokeRequest(BaseModel):
    """Request to revoke a certificate fingerprint."""

    fingerprint_sha256: str = Field(..., min_length=8, max_length=128)
    reason: str = Field(..., min_length=3, max_length=255)


class CertificateRevokeResponse(BaseModel):
    """Response after certificate revocation."""

    status: str
    revoked_at: datetime

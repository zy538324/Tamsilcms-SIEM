"""Identity service entry point.

This service validates signed agent "hello" messages delivered via the
transport layer. It enforces strict request validation and HTTPS-only access.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse

from .config import Settings, load_settings
from .certificates import CertificateRecord, registry
from .events import HeartbeatEvent, store
from .models import (
    CertificateIssueRequest,
    CertificateIssueResponse,
    CertificateRevokeRequest,
    CertificateRevokeResponse,
    HelloRequest,
    HelloResponse,
    HeartbeatEventResponse,
)
from .security import SignatureError, verify_signature

app = FastAPI(title="Identity Service", version="0.1.0")


def get_settings() -> Settings:
    """Dependency to load settings once per request."""
    return load_settings()


async def enforce_https(request: Request) -> None:
    """Reject non-HTTPS requests.

    In production, transport terminates TLS and forwards HTTPS headers.
    """
    forwarded_proto = request.headers.get("x-forwarded-proto", "http")
    if forwarded_proto.lower() != "https":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="https_required",
        )


@app.get("/health", response_class=JSONResponse)
async def health_check(settings: Settings = Depends(get_settings)) -> dict:
    """Simple health endpoint for load balancers."""
    return {
        "status": "ok",
        "service": settings.service_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/hello", response_model=HelloResponse)
async def hello(
    request: Request,
    payload: HelloRequest,
    settings: Settings = Depends(get_settings),
    signature: Optional[str] = Header(None, alias="X-Request-Signature"),
    timestamp: Optional[str] = Header(None, alias="X-Request-Timestamp"),
    client_identity: Optional[str] = Header(None, alias="X-Client-Identity"),
    client_cert_fingerprint: Optional[str] = Header(
        None, alias="X-Client-Cert-Sha256"
    ),
    _: None = Depends(enforce_https),
) -> HelloResponse:
    """Accept a signed hello payload and verify its authenticity.

    Transport supplies the client identity and certificate fingerprint.
    """
    if not signature or not timestamp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="missing_signature_headers",
        )

    if not client_identity or not client_cert_fingerprint:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="missing_transport_identity",
        )

    try:
        timestamp_int = int(timestamp)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid_timestamp",
        ) from exc

    raw_body = json.dumps(payload.model_dump(), separators=(",", ":")).encode(
        "utf-8"
    )
    valid, reason = verify_signature(settings, raw_body, signature, timestamp_int)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=reason,
        )

    store.record(
        HeartbeatEvent(
            event_id=payload.event_id,
            agent_id=payload.identity_id,
            hostname=payload.hostname,
            os=payload.os,
            uptime_seconds=payload.uptime_seconds,
            trust_state=payload.trust_state,
            received_at=datetime.now(timezone.utc),
        )
    )

    return HelloResponse(
        status="verified",
        received_at=datetime.now(timezone.utc),
        service=settings.service_name,
    )


@app.get("/heartbeats", response_model=list[HeartbeatEventResponse])
async def list_heartbeats() -> list[HeartbeatEventResponse]:
    """Return recent heartbeat events (in-memory)."""
    events = store.list_recent()
    return [
        HeartbeatEventResponse(
            event_id=event.event_id,
            agent_id=event.agent_id,
            hostname=event.hostname,
            os=event.os,
            uptime_seconds=event.uptime_seconds,
            trust_state=event.trust_state,
            received_at=event.received_at,
        )
        for event in events
    ]


@app.post("/certificates/issue", response_model=CertificateIssueResponse)
async def issue_certificate(
    payload: CertificateIssueRequest,
    settings: Settings = Depends(get_settings),
    _: None = Depends(enforce_https),
) -> CertificateIssueResponse:
    """Register a new client certificate fingerprint for an identity."""
    issued_at = datetime.now(timezone.utc)
    record = CertificateRecord(
        identity_id=payload.identity_id,
        fingerprint_sha256=payload.fingerprint_sha256,
        issued_at=issued_at,
        expires_at=payload.expires_at,
    )
    registry.issue(record)
    return CertificateIssueResponse(
        status="issued",
        issued_at=issued_at,
        expires_at=payload.expires_at,
    )


@app.post("/certificates/revoke", response_model=CertificateRevokeResponse)
async def revoke_certificate(
    payload: CertificateRevokeRequest,
    settings: Settings = Depends(get_settings),
    _: None = Depends(enforce_https),
) -> CertificateRevokeResponse:
    """Revoke a client certificate fingerprint."""
    record = registry.revoke(payload.fingerprint_sha256, payload.reason)
    if not record or not record.revoked_at:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="certificate_not_found",
        )
    return CertificateRevokeResponse(
        status="revoked",
        revoked_at=record.revoked_at,
    )

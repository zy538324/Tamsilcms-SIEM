"""Transport gateway entry point.

The transport layer is the only component permitted to perform network I/O.
It validates transport headers and proxies signed hello payloads to the
identity service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse

from .config import Settings, load_settings
from .models import HelloRequest, HelloResponse
from .security import enforce_mtls_only, enforce_transport_identity

app = FastAPI(title="Transport Gateway", version="0.1.0")


def get_settings() -> Settings:
    """Dependency to load settings once per request."""
    return load_settings()


async def enforce_https(request: Request) -> None:
    """Reject non-HTTPS requests.

    Transport terminates TLS at the edge proxy and forwards HTTPS headers.
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


@app.post("/mtls/hello", response_model=HelloResponse)
async def mtls_hello(
    payload: HelloRequest,
    settings: Settings = Depends(get_settings),
    signature: Optional[str] = Header(None, alias="X-Request-Signature"),
    timestamp: Optional[str] = Header(None, alias="X-Request-Timestamp"),
    client_identity: Optional[str] = Header(None, alias="X-Client-Identity"),
    client_cert_fingerprint: Optional[str] = Header(
        None, alias="X-Client-Cert-Sha256"
    ),
    mtls_state: Optional[str] = Header(None, alias="X-Client-MTLS"),
    _: None = Depends(enforce_https),
) -> HelloResponse:
    """Validate transport headers and proxy the hello to identity."""
    enforce_transport_identity(client_identity, client_cert_fingerprint)
    enforce_mtls_only(mtls_state)

    if not signature or not timestamp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="missing_signature_headers",
        )

    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
        response = await client.post(
            f"{settings.identity_service_url}/hello",
            json=payload.model_dump(),
            headers={
                "X-Request-Signature": signature,
                "X-Request-Timestamp": timestamp,
                "X-Client-Identity": client_identity,
                "X-Client-Cert-Sha256": client_cert_fingerprint,
                "X-Forwarded-Proto": "https",
            },
        )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("detail", "identity_error"),
        )

    return HelloResponse(**response.json())


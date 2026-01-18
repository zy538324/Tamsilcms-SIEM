"""Send a signed hello payload to the transport gateway.

This script simulates the MVP-1 agent hello flow. It does not perform mTLS
itself; instead it expects transport to validate mTLS headers injected by the
edge proxy.
"""
from __future__ import annotations

import argparse
import os
import platform
import time
import uuid
from datetime import datetime, timezone
from typing import Dict

import httpx

from .signing import sign_payload


def build_payload(args: argparse.Namespace) -> Dict[str, object]:
    """Build the hello payload using canonical IDs and runtime info."""
    return {
        "tenant_id": args.tenant_id,
        "asset_id": args.asset_id,
        "identity_id": args.identity_id,
        "event_id": str(uuid.uuid4()),
        "agent_version": args.agent_version,
        "hostname": args.hostname,
        "os": args.os_name,
        "uptime_seconds": int(args.uptime_seconds),
        "trust_state": args.trust_state,
        "sent_at": datetime.now(timezone.utc).isoformat(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a signed hello payload")
    parser.add_argument("--tenant-id", default=str(uuid.uuid4()))
    parser.add_argument("--asset-id", default=str(uuid.uuid4()))
    parser.add_argument("--identity-id", default=str(uuid.uuid4()))
    parser.add_argument("--agent-version", default="0.1.0")
    parser.add_argument("--hostname", default=platform.node())
    parser.add_argument("--os-name", default=platform.system())
    parser.add_argument("--uptime-seconds", default="0")
    parser.add_argument("--trust-state", default="bootstrap")
    parser.add_argument("--transport-url", default=os.environ.get("TRANSPORT_URL", "https://localhost:8081"))
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    shared_key = os.environ.get("AGENT_HMAC_SHARED_KEY", "")
    fingerprint = os.environ.get("AGENT_CERT_FINGERPRINT", "sha256:placeholder")
    identity_header = os.environ.get("AGENT_IDENTITY", "agent-placeholder")

    payload = build_payload(args)
    timestamp = int(time.time())
    signature = sign_payload(shared_key, payload, timestamp)

    headers = {
        "X-Request-Signature": signature,
        "X-Request-Timestamp": str(timestamp),
        "X-Client-Identity": identity_header,
        "X-Client-Cert-Sha256": fingerprint,
        "X-Client-MTLS": "success",
        "X-Forwarded-Proto": "https",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{args.transport_url}/mtls/hello",
            json=payload,
            headers=headers,
        )

    response.raise_for_status()
    print(response.json())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())


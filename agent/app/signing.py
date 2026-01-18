"""Signing helpers for agent payloads."""
from __future__ import annotations

import base64
import hashlib
import hmac
from typing import Dict


def canonical_json(payload: Dict[str, object]) -> bytes:
    """Return a canonical JSON representation without whitespace."""
    import json

    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


def sign_payload(shared_key: str, payload: Dict[str, object], timestamp: int) -> str:
    """Create a base64 HMAC signature for the payload."""
    if not shared_key:
        raise ValueError("shared_key_missing")

    message = f"{timestamp}.".encode("utf-8") + canonical_json(payload)
    digest = hmac.new(shared_key.encode("utf-8"), message, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


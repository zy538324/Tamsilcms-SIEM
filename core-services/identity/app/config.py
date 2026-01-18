"""Configuration for the Identity service.

All secrets are sourced from environment variables to avoid hard-coding.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime settings sourced from environment variables."""

    environment: str
    hmac_shared_key: str
    signature_ttl_seconds: int
    service_name: str


def load_settings() -> Settings:
    """Load settings from the environment with secure defaults."""
    return Settings(
        environment=os.environ.get("IDENTITY_ENV", "development"),
        hmac_shared_key=os.environ.get("IDENTITY_HMAC_SHARED_KEY", ""),
        signature_ttl_seconds=int(os.environ.get("IDENTITY_SIGNATURE_TTL", "120")),
        service_name=os.environ.get("IDENTITY_SERVICE_NAME", "identity-service"),
    )


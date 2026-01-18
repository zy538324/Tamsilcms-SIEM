"""Configuration for the Transport gateway.

All secrets are sourced from environment variables to avoid hard-coding.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime settings sourced from environment variables."""

    environment: str
    identity_service_url: str
    request_timeout_seconds: float
    service_name: str
    trusted_fingerprints: str


def load_settings() -> Settings:
    """Load settings from the environment with secure defaults."""
    return Settings(
        environment=os.environ.get("TRANSPORT_ENV", "development"),
        identity_service_url=os.environ.get(
            "TRANSPORT_IDENTITY_URL", "https://identity.local"
        ),
        request_timeout_seconds=float(
            os.environ.get("TRANSPORT_REQUEST_TIMEOUT", "5")
        ),
        service_name=os.environ.get("TRANSPORT_SERVICE_NAME", "transport-gateway"),
        trusted_fingerprints=os.environ.get("TRANSPORT_TRUSTED_FINGERPRINTS", ""),
    )

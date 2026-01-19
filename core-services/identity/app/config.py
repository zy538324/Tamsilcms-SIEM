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
    heartbeat_offline_threshold_seconds: int
    tasks_enabled: bool
    task_allowlist_patterns: tuple[str, ...]
    task_max_payload_bytes: int
    task_max_output_bytes: int
    task_max_ttl_seconds: int


def load_settings() -> Settings:
    """Load settings from the environment with secure defaults."""
    allowlist = tuple(
        pattern.strip()
        for pattern in os.environ.get("IDENTITY_TASK_ALLOWLIST", "").split(",")
        if pattern.strip()
    )
    return Settings(
        environment=os.environ.get("IDENTITY_ENV", "development"),
        hmac_shared_key=os.environ.get("IDENTITY_HMAC_SHARED_KEY", ""),
        signature_ttl_seconds=int(os.environ.get("IDENTITY_SIGNATURE_TTL", "120")),
        service_name=os.environ.get("IDENTITY_SERVICE_NAME", "identity-service"),
        heartbeat_offline_threshold_seconds=int(
            os.environ.get("IDENTITY_OFFLINE_THRESHOLD", "120")
        ),
        tasks_enabled=os.environ.get("IDENTITY_TASKS_ENABLED", "false").lower() == "true",
        task_allowlist_patterns=allowlist,
        task_max_payload_bytes=int(os.environ.get("IDENTITY_TASK_MAX_PAYLOAD", "4096")),
        task_max_output_bytes=int(os.environ.get("IDENTITY_TASK_MAX_OUTPUT", "8192")),
        task_max_ttl_seconds=int(os.environ.get("IDENTITY_TASK_MAX_TTL", "900")),
    )

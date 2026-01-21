# Default PostgreSQL DSN: postgresql://tamsilsiem:changeme@localhost:5432/tamsil
"""Configuration for the Detection & Correlation service."""
from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime settings sourced from environment variables."""

    service_name: str = Field(default="detection-service", min_length=3)
    https_enforced: bool = True
    max_event_age_seconds: int = Field(default=3600, ge=60, le=86400)
    suppression_window_seconds: int = Field(default=900, ge=60, le=86400)
    max_supporting_events: int = Field(default=50, ge=1, le=500)
    allow_findings_without_context: bool = False
    max_findings_per_request: int = Field(default=25, ge=1, le=200)
    retention_events: int = Field(default=5000, ge=100, le=20000)
    retention_findings: int = Field(default=2000, ge=100, le=10000)
    correlation_time_window_seconds: int = Field(default=1800, ge=60, le=86400)
    max_sequence_events: int = Field(default=15, ge=1, le=100)
    allowed_explanation_variables: set[str] = Field(
        default_factory=lambda: {
            "event_type",
            "asset_id",
            "identity_id",
            "metric_name",
            "metric_value",
            "baseline_value",
            "time_window",
            "missing_patches",
            "network_destination",
            "process_name",
            "multiplier",
        }
    )


@lru_cache(maxsize=1)
def load_settings() -> Settings:
    """Load settings with caching for request reuse."""
    return Settings()

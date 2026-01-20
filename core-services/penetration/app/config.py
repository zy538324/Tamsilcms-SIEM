"""Configuration for the Penetration Testing Orchestrator (MVP-12)."""
from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime settings sourced from environment variables."""

    service_name: str = Field(default="penetration-test-orchestrator", min_length=3)
    storage_path: str = Field(default="data/penetration/store.json", min_length=3)
    https_enforced: bool = True
    api_key: Optional[str] = None
    max_results_per_test: int = Field(default=250, ge=25, le=2000)
    max_observations_per_request: int = Field(default=75, ge=1, le=500)
    max_evidence_per_test: int = Field(default=300, ge=50, le=5000)
    default_rate_limit_per_minute: int = Field(default=120, ge=10, le=2000)
    default_max_duration_minutes: int = Field(default=180, ge=5, le=1440)
    integration_mode: str = Field(
        default="local",
        description="local|simulate_outage|disabled",
    )


@lru_cache(maxsize=1)
def load_settings() -> Settings:
    """Load settings with caching for request reuse."""
    return Settings()

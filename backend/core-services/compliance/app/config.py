"""Configuration for the Compliance & Audit Automation service (MVP-13)."""
from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime settings sourced from environment variables."""

    service_name: str = Field(default="compliance-service", min_length=3)
    storage_path: str = Field(default="data/compliance/store.json", min_length=3)
    https_enforced: bool = True
    api_key: Optional[str] = None
    max_evidence_records: int = Field(default=1000, ge=100, le=20000)
    max_assessments_per_control: int = Field(default=365, ge=10, le=5000)
    max_exceptions_per_control: int = Field(default=100, ge=1, le=1000)
    default_evaluation_frequency_days: int = Field(default=30, ge=1, le=365)


@lru_cache(maxsize=1)
def load_settings() -> Settings:
    """Load settings with caching for request reuse."""
    return Settings()

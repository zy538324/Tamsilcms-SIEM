"""Configuration for the ingestion service."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str
    service_name: str


def load_settings() -> Settings:
    return Settings(
        environment=os.environ.get("INGESTION_ENV", "development"),
        service_name=os.environ.get("INGESTION_SERVICE_NAME", "ingestion-service"),
    )


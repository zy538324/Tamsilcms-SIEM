import os

DATABASE_URL = os.environ.get("SIEM_DATABASE_URL") or os.environ.get("PSA_DATABASE_URL") or "sqlite:///./siem.db"

SERVICE_NAME = "siem"

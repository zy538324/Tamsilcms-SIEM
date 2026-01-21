import os

AUDIT_DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("AUDIT_DATABASE_URL", "sqlite:///./audit.db")
PSA_BASE_URL = os.getenv("PSA_BASE_URL", "http://localhost:8001")
SERVICE_NAME = "auditing"

import os

DATABASE_URL = os.environ.get("DATABASE_URL") or os.environ.get("EDR_DATABASE_URL") or os.environ.get("PSA_DATABASE_URL") or "sqlite:///./edr.db"

SERVICE_NAME = "edr"

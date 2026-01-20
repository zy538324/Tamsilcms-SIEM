import os

RMM_DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("RMM_DATABASE_URL", "sqlite:///./rmm.db")
PSA_BASE_URL = os.getenv("PSA_BASE_URL", "http://localhost:8001")
SERVICE_NAME = "rmm"

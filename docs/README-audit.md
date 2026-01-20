# Auditing Service

This service provides Compliance Auditing data models and APIs for frameworks, controls, assessments, evidence, gaps, attestations and audit sessions.

Run locally:

1. Install dependencies from `requirements.txt`.
2. Start with `uvicorn core-services.auditing.app.main:app --port 8010 --reload`.

Environment variables:
- `AUDIT_DATABASE_URL` - DB connection string (default sqlite `sqlite:///./audit.db`)
- `PSA_BASE_URL` - PSA API base URL (default `http://localhost:8001`)

# SIEM service

Minimal SIEM prototype for ingestion, normalization and findings.

Run locally:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn core-services.siem.app.main:app --reload --port 8002
```

Endpoints under `/siem` (e.g. `POST /siem/raw_events`).

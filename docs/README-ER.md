# EDR service

Minimal EDR prototype for telemetry ingestion, detection and escalation to PSA.

Run locally:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn core-services.edr.app.main:app --reload --port 8003
```

Endpoints under `/edr` (e.g. `POST /edr/process_events`, `POST /edr/detections/{id}/escalate`).

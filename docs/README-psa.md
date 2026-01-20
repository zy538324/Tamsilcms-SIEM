# PSA service

Minimal PSA (Process & Service Authority) prototype.

Run locally:

1. Create virtualenv and install requirements:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run service:

```powershell
uvicorn core-services.psa.app.main:app --reload --port 8001
```

API endpoints are under `/psa` (e.g. `POST /psa/cases`). Defaults to a local `sqlite:///./psa.db` if `PSA_DATABASE_URL` is not set.

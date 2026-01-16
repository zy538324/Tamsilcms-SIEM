# Tamsilcms SIEM (Low-Level Foundation)

## Project Overview
This repository provides a minimal, production-minded SIEM foundation consisting of a log collector agent, a secure ingestion API, and a simple dashboard backed by PostgreSQL. The design is deliberately lean: collect, validate, store, and display logs with no enrichment or alerting at this stage.

## Architecture
```
[ Endpoint ]
   |
   | (JSON events over HTTPS)
   v
[ Ingestion API (FastAPI) ]
   |
   | (validated, normalised events)
   v
[ PostgreSQL ]
   |
   | (SQL queries)
   v
[ Dashboard (HTML/CSS/JS) ]
```

## Components
- **Agent (Python)**: Reads local log files, batches events, and sends them securely with retry and spooling.
- **Backend (FastAPI)**: Authenticates agents via API key, validates payloads, and writes logs to PostgreSQL.
- **Dashboard (HTML/CSS/JS)**: Presents log stream and agent list with pagination and filtering.

## Local Development
1. Copy the environment template.
   ```bash
   cp .env.example .env
   ```
2. Start PostgreSQL.
   ```bash
   docker compose up -d postgres
   ```
3. Apply the schema.
   ```bash
   psql "$DATABASE_URL" -f db/schema.sql
   ```
4. Run the backend API.
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8080
   ```
5. Serve the dashboard (optional for local browsing).
   ```bash
   cd frontend
   python -m http.server 8000
   ```

## Agent Setup
1. Copy the agent environment template (or export environment variables).
2. Run the agent:
   ```bash
   cd agent
   pip install -r requirements.txt
   python agent.py
   ```

## Security Notes
- API keys are stored hashed (PBKDF2) and never logged.
- All endpoints enforce payload size limits and schema validation.
- Use HTTPS in production and restrict database permissions to least privilege.

## Roadmap
- Alerting engine
- Enrichment pipeline
- Rule management and correlation

## Why this approach?
The stack prioritises strong foundations: secure ingestion, durable storage, and readable data. This ensures later features (alerting, correlation, intelligence feeds) can be added without reworking core data handling.

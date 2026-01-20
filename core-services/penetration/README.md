# Penetration Testing Orchestrator (MVP-12)

## Overview
The penetration testing orchestrator schedules and controls authenticated validation, safe exploit simulation, and result normalisation. It enforces authorisation, scope boundaries, and safety controls while producing immutable evidence and dispatch summaries for downstream vulnerability, detection, and PSA workflows.

## API Surface

### Core Endpoints
- `POST /tests` — Create a new authorised test plan.
- `POST /tests/{test_id}/start` — Start execution within the approved window.
- `POST /tests/{test_id}/abort` — Abort a running test immediately.
- `POST /tests/{test_id}/results` — Ingest observations and normalise findings.
- `GET /tests` — List test plans.
- `GET /tests/{test_id}` — Retrieve a specific test plan.
- `GET /tests/{test_id}/results` — List normalised results.
- `GET /tests/{test_id}/evidence` — List evidence bundle items.
- `GET /tests/{test_id}/dispatches` — View downstream dispatch records.

## Execution Guarantees
- Tests cannot start outside the authorised window.
- Decommissioned assets in scope block execution.
- Credential revocation aborts the test immediately.
- Detection system failure can trigger automatic aborts.
- Observations are normalised without trusting external severity scores.
- Evidence is hashed to detect tampering.

## Deployment Notes
Run locally:
```bash
uvicorn core-services.penetration.app.main:app --host 0.0.0.0 --port 8086
```

Environment variables:
- `PEN_TEST_SERVICE_NAME`
- `PEN_TEST_STORAGE_PATH`
- `PEN_TEST_API_KEY`
- `PEN_TEST_HTTPS_ENFORCED`
- `PEN_TEST_MAX_RESULTS_PER_TEST`
- `PEN_TEST_MAX_OBSERVATIONS_PER_REQUEST`
- `PEN_TEST_MAX_EVIDENCE_PER_TEST`
- `PEN_TEST_DEFAULT_RATE_LIMIT_PER_MINUTE`
- `PEN_TEST_DEFAULT_MAX_DURATION_MINUTES`
- `PEN_TEST_INTEGRATION_MODE`

## Optimisation TODOs
- Replace JSON storage with PostgreSQL and migrations.
- Add job queue support for scheduled execution windows.
- Provide signed evidence exports for audit delivery.

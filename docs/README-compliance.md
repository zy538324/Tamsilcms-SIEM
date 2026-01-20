# Compliance & Audit Automation (MVP-13)

## Overview
MVP-13 automates continuous compliance assessment. Controls are machine-readable, evidence is extracted from existing system activity, and audit bundles are generated without manual spreadsheets or screenshots.

## API Surface

### Core Endpoints
- `POST /controls` — Create a control definition.
- `GET /controls` — List controls.
- `POST /evidence` — Ingest evidence from system sources.
- `GET /controls/{control_id}/evidence` — List evidence for a control.
- `POST /controls/{control_id}/assess` — Evaluate a control.
- `GET /controls/{control_id}/assessments` — List control assessments.
- `POST /controls/{control_id}/exceptions` — Record a time-bound exception.
- `GET /controls/{control_id}/exceptions` — List exceptions.
- `POST /frameworks/mappings` — Map controls to frameworks.
- `GET /frameworks/mappings` — List mappings.
- `POST /audit/bundles` — Generate an audit bundle.

## Execution Guarantees
- Controls are immutable once published.
- Missing evidence yields explicit manual evidence required status.
- Exceptions are time-bound and applied conservatively.
- Evidence remains attributable and timestamped.

## Deployment Notes
Run locally:
```bash
uvicorn core-services.compliance.app.main:app --host 0.0.0.0 --port 8087
```

Environment variables:
- `COMPLIANCE_SERVICE_NAME`
- `COMPLIANCE_STORAGE_PATH`
- `COMPLIANCE_API_KEY`
- `COMPLIANCE_HTTPS_ENFORCED`
- `COMPLIANCE_MAX_EVIDENCE_RECORDS`
- `COMPLIANCE_MAX_ASSESSMENTS_PER_CONTROL`
- `COMPLIANCE_MAX_EXCEPTIONS_PER_CONTROL`
- `COMPLIANCE_DEFAULT_EVALUATION_FREQUENCY_DAYS`

## Optimisation TODOs
- Add PostgreSQL persistence with migrations.
- Add signed audit bundle exports.
- Add scheduled evaluation jobs with queue integration.

# MVP-11 — PSA Workflow Engine (Human Accountability & Operational Control)

## Overview
MVP-11 introduces the PSA workflow engine that converts system intelligence into auditable, controlled human action. Tickets are derived from findings and system signals, never from manual summaries. The service enforces computed priority, immutable evidence, and accountable decision recording.

## Scope (Hard Limits)
Included:
- Ticket generation from system intelligence.
- SLA and priority derived from risk.
- Change tracking, ownership, and accountability.
- Evidence attachment and integrity hashing.
- Human decision recording with mandatory justification.

Excluded:
- Billing/invoicing and payroll time tracking.
- Customer-facing portals (initially).
- Free-form workflow engines.

## Service Surface

### Core API
- `POST /intake`
  - Accepts ticket intelligence (finding, patch failure, defence action, vulnerability).
  - Enforces risk threshold.
  - Deduplicates by tenant/asset/source and merges evidence.

- `POST /intake/resolve`
  - Resolves a ticket when upstream evidence confirms remediation.
  - Manual closure is not supported.

- `GET /tickets`
  - Returns ticket queue sorted by computed priority and SLA deadline.

- `GET /tickets/{ticket_id}`
  - Retrieves the immutable ticket view.

- `POST /tickets/{ticket_id}/actions`
  - Records human actions (acknowledge, remediate, defer, accept risk, escalate).
  - Justification is mandatory for non-remediation actions.
  - Risk acceptance requires an approver identity.
  - Remediation requires an automation request reference.

- `GET /tickets/{ticket_id}/actions`
  - Returns action history for audit.

- `GET /tickets/{ticket_id}/evidence`
  - Returns immutable evidence records.

## Domain Objects
- **Ticket**: Derived from intelligence with computed priority and SLA.
- **Action**: Human response with identity, timestamp, and justification.
- **Evidence**: Immutable references with integrity hashes.

## Priority & SLA Engine
Priority is computed from risk score, asset criticality, exposure level, and time sensitivity. SLA deadlines are calculated per priority and recalculated whenever risk changes.

## Traceability Guarantees
- Actions require identity and justification (when applicable).
- No manual edits to findings, evidence, or risk scores.
- Tickets resolve only via upstream intelligence.
- Evidence hashes provide tamper detection.

## Failure Mode Testing
The following scenarios are explicitly supported by deterministic behaviour:
- **Flood of findings**: deduplication prevents ticket spam; evidence is merged.
- **Rapid risk changes**: priority and SLA are recomputed per intake.
- **Ticket reopening**: resolved tickets reopen automatically when new evidence arrives.
- **Conflicting human actions**: all actions are recorded, and the latest action drives state.
- **Manual tampering attempts**: no endpoints allow direct edits or deletes.
- **SLA breach scenarios**: SLA deadlines remain visible in ticket responses.

## Deployment Notes
Run locally:
```bash
uvicorn core-services.psa.app.main:app --host 0.0.0.0 --port 8083
```

Environment variables:
- `PSA_WORKFLOW_SERVICE_NAME`
- `PSA_WORKFLOW_STORAGE_PATH`
- `PSA_WORKFLOW_RISK_THRESHOLD`
- `PSA_WORKFLOW_API_KEY`
- `PSA_WORKFLOW_HTTPS_ENFORCED`

## Optimisation TODOs
- Add persistent storage (PostgreSQL) with migrations.
- Add queue backpressure for intake spikes.
- Add integration to automate patch/containment workflows.

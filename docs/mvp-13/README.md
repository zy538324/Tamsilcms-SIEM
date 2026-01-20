# MVP-13 — Compliance & Audit Automation (Living Governance & Continuous Assurance)

## Overview
MVP-13 provides continuous compliance assessment grounded in observable system behaviour. Controls are machine-readable, evidence is extracted from existing system telemetry, and audit-ready bundles are generated without manual spreadsheets or screenshots.

## Scope Boundaries

Included:
- Control modelling and framework mapping.
- Evidence extraction and mapping.
- Continuous assessment and drift detection.
- Audit-ready reporting bundles.

Excluded:
- Legal interpretation of regulations.
- Policy document authoring.
- External auditor portals.
- Certification claims.

## Core Design Principle
Controls are behaviours, not documents:
- Evidence is derived from system activity.
- Assertions are backed by immutable data.
- Gaps are surfaced transparently.

## Control Definition
Each control includes:
- `control_id`
- `framework`
- `control_statement`
- `expected_system_behaviour`
- `evidence_sources`
- `assessment_logic`
- `evaluation_frequency`

Controls are immutable once published.

## Evidence Extraction
Evidence is sourced from existing MVPs:
- Patch history (MVP-6)
- Event timelines (MVP-7)
- Detection findings (MVP-8)
- Defence actions (MVP-9)
- Vulnerability state (MVP-10)
- PSA actions and approvals (MVP-11)
- Pen test results (MVP-12)

Evidence is timestamped, attributable, immutable, and traceable.

## Assessment Logic
Control assessment types:
- Boolean (pass/fail)
- Threshold-based
- Time-window based
- Behavioural
- Manual evidence required

Outputs:
- `compliant`
- `non_compliant`
- `partially_compliant`
- `not_applicable`
- `manual_evidence_required`

Uncertainty is explicitly shown.

## Drift Detection
Controls are evaluated on schedule and on evidence updates. Drift changes are recorded and surfaced, and may raise PSA tickets in future policy integrations.

## Exceptions
Risk exceptions must include:
- Approver identity
- Justification
- Time limit

Expired exceptions revert to non-compliant status.

## Audit Bundles
Bundles include:
- Scope definition
- Control list
- Assessment results
- Linked evidence
- Exceptions and approvals

Bundles are immutable and reproducible.

## Failure Mode Testing
Explicitly handled:
- Evidence source outage
- Conflicting evidence
- Control logic errors
- Manual evidence abuse
- Exception expiry
- Framework updates

Expected behaviour:
- Conservative assessment
- Transparent uncertainty
- No silent assumptions

## Completion Goal Posts
MVP-13 is complete only when:
- Controls are machine-readable and immutable.
- Evidence is automatically extracted.
- Compliance is continuously evaluated.
- Drift is detected and visible.
- Exceptions are controlled and time-bound.
- Audit bundles are reproducible.
- Evidence is immutable and attributable.
- Framework mappings avoid duplication.
- Manual assertions are minimised and flagged.

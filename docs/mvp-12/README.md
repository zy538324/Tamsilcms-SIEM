# MVP-12 — Penetration Testing Orchestration (Controlled Adversarial Validation)

## Overview
MVP-12 turns penetration testing into a continuous, authorised health check. Tests are expressed as immutable plans, executed safely, and normalised into evidence-driven findings that feed vulnerability, detection, and PSA workflows.

## Scope Boundaries (Hard Limits)

Included:
- Authenticated vulnerability scanning orchestration.
- Controlled attack simulation with non-destructive payloads.
- Result normalisation and evidence capture.
- Integration hooks for vulnerability and PSA engines.

Excluded:
- Zero-day exploit development.
- Destructive payloads or data exfiltration.
- Credential harvesting outside test scope.
- Autonomous tool-driven testing.

## Core Design Principle
The platform must never surprise itself:
- Tests are authorised, attributable, and reversible.
- Execution is explainable and bounded.
- Tests must be defensible to risk owners.

## Pen Test Object (First-Class)
Each test plan includes:
- `test_id`
- `tenant_id`
- `scope` (assets, networks, exclusions)
- `test_type` (network, host, auth, config)
- `method` (scan, simulate, validate)
- `credentials` (reference only)
- `start/end window`
- `authorisation` identity and policy reference

No test executes without this object.

## Minimum Test Types

### Network Exposure Validation
- Port scanning (scoped)
- Service fingerprinting
- TLS configuration checks

### Authenticated Vulnerability Validation
- Authenticated scanning with approved credentials
- Patch validation
- Configuration checks

### Exploitability Simulation (Non-Destructive)
- Safe payloads only
- Detection-only mode
- Validate exploit path, not impact

## Execution Orchestration
- Scheduled, triggered, or on-demand execution.
- Maintenance windows and rate limits enforced.
- Mandatory allow-lists and payload restrictions.
- Immediate abort support for safety.

## Result Normalisation & Interpretation
Raw observations are normalised into:
- Observed weakness
- Evidence
- Confidence level
- Environmental context

Outputs feed:
- Vulnerability engine (MVP-10)
- Detection engine (MVP-8)
- PSA workflow engine (MVP-11)

## Detection & Defence Validation
Each test records:
- Detections fired
- Defences acted
- Defences failed

This produces control effectiveness metrics, not raw vulnerability lists.

## Evidence & Audit Model
Each test produces an immutable evidence bundle:
- Authorisation record
- Scope definition
- Methods used
- Raw observations
- Normalised results
- Detection response summary

## Failure Mode Testing (Mandatory)
Explicitly handled:
- Decommissioned asset targets
- Credential revocation mid-test
- Backend outage during test
- Detection system failure
- Excessive findings volume
- Unauthorised execution attempts

Expected behaviour:
- Safe aborts
- Clear attribution
- Honest reporting

## Completion Goal Posts
MVP-12 is complete only when:
- Tests are authorised and scoped.
- Execution is safe and predictable.
- Results are normalised and contextualised.
- Detection response is measured.
- Findings feed risk and PSA workflows.
- Evidence bundles are immutable.
- No test can run anonymously.

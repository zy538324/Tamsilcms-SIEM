# MVP-6 — Patch Management Engine (Controlled Automation Plane)

## Purpose (Why This Exists)
MVP-6 answers a single question: **Can the platform keep systems up to date automatically, safely, and provably?**

Patch management is not just updates. It is:
- Risk reduction
- Change control
- Business continuity
- Compliance evidence

A patch that installs silently but breaks a system is a failure.
A patch that installs successfully but cannot be proven is also a failure.

## Scope Boundaries (Hard Limits)
### Included
- Patch detection
- Patch classification
- Patch scheduling
- Patch execution
- Reboot handling
- Result verification
- Evidence capture

### Explicitly Excluded
- Third-party app catalogues beyond basics
- Feature upgrades (e.g. OS major version jumps)
- User-driven approvals (later with PSA integration)

This MVP focuses on OS and core platform hygiene only.

## Patch Philosophy (Critical Design Rule)
You are not “running updates”. You are executing controlled change operations.

That means:
- Detection is separate from execution.
- Execution is reversible where possible.
- Every change has a paper trail.
- Silence is never treated as success.

## Patch Detection Layer
### Agent-Side Detection Modules
Detection is local, not inferred remotely.

Minimum supported:
- **Windows**:
  - Windows Update API
  - Microsoft Update (OS + MS products)
- **Linux**:
  - Distro package manager (apt, yum, dnf, zypper)
- **macOS** (optional early, recommended):
  - softwareupdate

Detection collects (read-only):
- Patch identifier
- Severity (if available)
- Category (security, critical, optional)
- Supersedence info
- Reboot requirement flag

### Normalisation & Storage
Backend normalises patches into a canonical schema:
- patch_id
- vendor
- severity
- affected_component
- requires_reboot
- release_date
- detection_timestamp

This enables correlation with vulnerabilities and compliance.

## Patch Policy Engine
Patch management without policy is chaos.

### Policy Definition (Declarative)
Policies define:
- Which patches are allowed
- Which are deferred
- Maintenance windows
- Reboot rules
- Retry behaviour
- Exclusions

Policies are:
- Signed
- Versioned
- Assigned per tenant, group, or asset

No ad-hoc patching.

### Eligibility Evaluation
Before scheduling, the system evaluates:
- Asset criticality
- Current health (from MVP-4 telemetry)
- Recent failures
- Business hours
- Reboot tolerance

If conditions are unsafe, patching is deferred, not forced.

## Patch Scheduling Engine
### Scheduling Model
Patches are converted into **execution plans**, not tasks.

An execution plan contains:
- Patch list
- Execution order
- Pre-checks
- Post-checks
- Rollback plan
- Reboot strategy

Execution plans are then broken into MVP-5 tasks.

### Throttling & Blast Radius Control
Mandatory controls:
- Max concurrent patching per tenant
- Staggered execution
- Canary assets first (optional but recommended)

This prevents fleet-wide outages.

## Patch Execution (Built on MVP-5)
### Execution Characteristics
Patch execution must:
- Use system context
- Honour timeouts
- Capture installer output
- Detect partial success
- Survive reboots

No silent assumptions.

### Reboot Handling
Reboots are the hardest part. You must support:
- Immediate reboot
- Deferred reboot
- Maintenance-window reboot
- Multi-stage reboot detection

The agent must:
- Detect reboot occurred
- Resume reporting
- Confirm patch state post-boot

A reboot without confirmation is a failed patch.

## Verification & Validation
After execution, the system must verify:
- Patch no longer appears in detection
- System health is nominal
- No critical services failed
- Agent integrity intact

Verification failures are treated as incidents, not warnings.

## Failure Handling & Rollback
Failures are expected. Lying about them is not acceptable.

### Failure Types
- Install failure
- Timeout
- Reboot failure
- Post-check failure

### Required Behaviour
- Record failure type
- Stop further patching on that asset
- Flag asset as “patch-blocked”
- Escalate via PSA later

Rollback where possible:
- Package rollback (Linux)
- Restore points (Windows, if enabled)

If rollback is impossible, that fact must be recorded explicitly.

## Evidence & Audit Model
Patch management produces compliance-grade evidence.

Each patch cycle records:
- Detection state
- Policy decision
- Execution timestamps
- Output logs
- Reboot confirmation
- Final state

This evidence feeds:
- Compliance
- SIEM
- PSA
- Reporting

Nothing is manually written. Everything is derived.

## Minimal UI (Patch Control View)
### Required Views
- Patch compliance overview: compliant, pending, failed
- Per-asset patch history
- Upcoming maintenance windows

### UX Rules
- No “install now” buttons
- All actions flow from policy
- Manual override requires elevated role and justification

## Failure Mode Testing (Mandatory)
You must explicitly test:
- Patch requires reboot but reboot blocked
- Agent crashes mid-patch
- Network drops during install
- Backend unavailable
- Patch superseded mid-cycle
- Disk full during update
- System fails to boot post-patch

The system must:
- Recover
- Report accurately
- Never mark success incorrectly

## MVP-6 Completion Goal Posts (Non-Negotiable)
MVP-6 is finished only when all are true:
- The platform can reliably detect missing patches.
- Patch decisions are driven solely by policy.
- Patches execute via MVP-5, not custom logic.
- Reboots are handled deterministically.
- Post-patch verification confirms actual state.
- Failures are visible and not silently retried forever.
- Patch history is immutable and auditable.
- Compliance status is derived, not manually set.
- No patch installs without traceable authorisation.
- You trust the system to run unattended overnight.

If any one fails, MVP-6 is not complete.

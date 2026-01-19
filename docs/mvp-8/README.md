# MVP-8 — Detection & Correlation Engine (Reasoned Judgement Layer)

## 1. Purpose of MVP-8 (Why This Exists)

MVP-8 answers this question:

> “Given everything we know, does this behaviour matter?”

Not “is this bad?”. Not “raise an alert.” The core intent is to determine whether behaviour is **meaningfully suspicious in context**.

This layer converts events into **findings**. A finding is an assertion with evidence, not an alert demanding action.

## 2. Scope Boundaries (Hard Limits)

### Included

- Rule-based detection
- Temporal correlation
- Cross-domain correlation
- Contextual risk amplification
- Explainable output

### Explicitly Excluded

- Automated response
- Ticket creation
- User notification
- Machine learning models

Those come later, once trust is earned.

## 3. Detection Philosophy (Lock This In)

Three principles govern MVP-8:

1. **Context beats signatures**
2. **Correlation beats volume**
3. **Explainability beats cleverness**

If you cannot explain why a finding exists in plain language, it does not belong here.

## 4. Inputs to the Detection Engine

MVP-8 consumes **only verified data** from earlier MVPs.

### Mandatory Inputs

- Normalised events (MVP-7)
- Telemetry baselines (MVP-4)
- Patch and system state (MVP-6)
- Asset metadata (MVP-3)
- Identity context (users, roles, privileges)

**No raw logs. No untrusted feeds.**

## 5. Detection Engine Architecture

### 5.1 Rule Engine (Core)

Rules are **declarative** and **versioned**. Each rule defines:

- Trigger conditions
- Time windows
- Required context
- Suppression logic
- Output template

Rules are evaluated continuously or in near-real-time.

Rules must be:

- Deterministic
- Side-effect free
- Idempotent

### 5.2 Rule Types (Minimum Set)

**Single-Event Rules**

Example: Execution of unsigned binary from temp directory.

**Sequence Rules**

Example: Failed login attempts followed by successful privileged login within 10 minutes.

**Behavioural Deviation Rules**

Example: CPU usage 4× baseline during off-hours.

**Cross-Domain Rules**

Example: Patch missing + exploit-like process behaviour.

Each rule type increases confidence, not noise.

## 6. Correlation Model

Correlation is not aggregation. It is **relationship building**.

### Correlation Axes

- Time (what happened before and after)
- Identity (who initiated it)
- Asset (where it occurred)
- Process lineage (parent-child)
- Network flow (direction and destination)

Correlations must be **explicit** and **queryable**.

## 7. Findings Model (This Is Critical)

A finding is the atomic output of MVP-8.

### Finding Structure

- `finding_id`
- `finding_type`
- `severity` (tentative, not final)
- `confidence_score`
- `supporting_events` (IDs)
- `correlation_graph`
- `context_snapshot`
- `explanation_text`
- `creation_timestamp`

Findings are immutable once created. They can be superseded, not edited.

## 8. Explainability Requirement

Every finding must generate a **human-readable explanation** that answers:

- What happened?
- Why this matters?
- What evidence supports this?
- What context increases or reduces concern?

This explanation must be auto-generated from the rule logic itself, not hand-written summaries.

If the system cannot explain itself, it is wrong.

## 9. Suppression & Noise Control

Suppress aggressively and transparently.

### Suppression Mechanisms

- Duplicate detection
- Time-based suppression
- Contextual suppression (e.g. maintenance windows)
- Explicit allow-listing

Suppression decisions are **logged and auditable**. Silencing without record is forbidden.

## 10. Risk Scoring (Local, Not Global)

At this stage, risk scoring is **relative, not absolute**.

Risk considers:

- Asset criticality
- Exposure (from MVP-6)
- Behaviour rarity
- Privilege level involved

The output is:

> “More concerning than baseline”

Not “critical incident”. Final prioritisation comes later.

## 11. Storage & Lifecycle

Findings are stored separately from raw events.

### Lifecycle States

- `open`
- `superseded`
- `dismissed` (with reason)
- `escalated` (future MVP)

Dismissals require justification and identity.

## 12. Minimal UI (Findings Review)

### Required Views

- Findings list (filterable)
- Per-finding detail:
  - Explanation
  - Supporting events
  - Timeline reconstruction
  - Suppression / dismissal controls (role-restricted)

### UX Rules

- No alert fatigue design
- No colour abuse
- Confidence shown numerically and descriptively

This UI is for analysts, not managers.

## 13. Failure Mode Testing (Mandatory)

You must explicitly test:

- Event storms
- Rule misfires
- Overlapping rules
- Missing context
- Delayed events
- Suppressed findings resurfacing

Expected behaviour:

- Deterministic output
- No runaway finding creation
- Clear explanations even when wrong

## 14. MVP-8 Completion Goal Posts (Non-Negotiable)

MVP-8 is finished only when all are true:

- Events are transformed into structured findings
- Findings reference concrete supporting evidence
- Correlation across time and domains works
- Each finding has an explainable rationale
- Noise is actively suppressed and logged
- Findings are immutable once created
- Analysts can reconstruct reasoning end-to-end
- Risk scoring is contextual, not static
- No automated action occurs yet
- You trust findings enough to review them daily

If any one fails, MVP-8 is incomplete.

1. PURPOSE AND GOVERNANCE MODEL
Core purpose

Compliance Auditing exists to answer, defensibly and repeatably:

Which controls apply to this organisation?

What evidence demonstrates each control is met?

Over what period was that control effective?

Who attested to adequacy, and when?

What gaps exist, and what is being done about them?

Compliance is assertion plus evidence, never assertion alone.

What Compliance Auditing must never do

Generate evidence itself

Modify security data

Infer control effectiveness without artefacts

Auto-pass controls

Override risk decisions

Compliance Auditing consumes, it does not invent.

2. HIGH-LEVEL SYSTEM RESPONSIBILITIES
What this module owns

Framework modelling (CE, CAF, NIST, ISO)

Control definitions and applicability

Evidence mapping and lifecycle

Control assessments

Gap identification

Audit history and traceability

Attestation and sign-off

What it explicitly does not own

Detection

Remediation

Risk scoring

Incident response

Asset truth

It is a lens, not an actuator.

3. COMPLIANCE PHILOSOPHY (CRITICAL)

Your system must support three simultaneous truths:

A control may be designed

A control may be implemented

A control may be operating effectively

Most tools collapse these. Yours must not.

A control can exist on paper and still fail operationally.
Auditors will ask the difference.

4. DATA ARCHITECTURE OVERVIEW

Compliance data is:

Highly relational

Slowly changing

Historically sensitive

Evidence-dense

PostgreSQL is the correct choice.

You will model:

Frameworks

Controls

Control applicability

Assessments

Evidence artefacts

Gaps and actions

Attestations

Everything must be time-bounded.

5. DATABASE SCHEMA (DETAILED)
A. FRAMEWORKS AND CONTROLS
compliance_frameworks
Field	Type	Purpose
id	UUID (PK)	Framework ID
name	TEXT	ISO 27001, CAF v4
version	TEXT	Version
authority	TEXT	NCSC, ISO
description	TEXT	Summary
compliance_controls

Canonical controls.

Field	Type
id	UUID
framework_id	UUID
control_code	TEXT
title	TEXT
description	TEXT
control_type	TEXT
control_relationships

Maps equivalence across frameworks.

Field	Type
control_id	UUID
related_control_id	UUID
relationship_type	TEXT

This prevents duplicate evidence.

B. CONTROL APPLICABILITY
control_applicability

Controls do not always apply.

Field	Type
id	UUID
organisation_id	UUID
control_id	UUID
applicable	BOOLEAN
justification	TEXT
decided_at	TIMESTAMP

Auditors love this table.

C. ASSESSMENTS
control_assessments

This is the assessment engine.

Field	Type	Purpose
id	UUID	Assessment ID
organisation_id	UUID	Org
control_id	UUID	Control
assessment_status	TEXT	pass, fail, partial
effectiveness	TEXT	effective, weak
assessed_by	UUID	Auditor
assessed_at	TIMESTAMP	Time
notes	TEXT	Commentary

Assessments are snapshots, not mutable state.

D. EVIDENCE MANAGEMENT
control_evidence

Links controls to artefacts.

Field	Type
id	UUID
control_id	UUID
evidence_type	TEXT
source_system	TEXT
storage_uri	TEXT
hash	TEXT
valid_from	TIMESTAMP
valid_to	TIMESTAMP

Evidence expires. This matters.

evidence_sources

Traceability.

Field	Type
evidence_id	UUID
originating_entity	TEXT
originating_id	UUID

This lets you say where it came from.

E. GAPS AND REMEDIATION
control_gaps
Field	Type
id	UUID
control_id	UUID
organisation_id	UUID
gap_description	TEXT
severity	INTEGER
identified_at	TIMESTAMP
gap_cases
Field	Type
gap_id	UUID
psa_case_id	UUID

Compliance gaps become work.

F. ATTESTATION AND SIGN-OFF
control_attestations
Field	Type
id	UUID
control_id	UUID
organisation_id	UUID
attested_by	UUID
role	TEXT
statement	TEXT
attested_at	TIMESTAMP

This table is legally meaningful.

G. AUDIT HISTORY (NON-NEGOTIABLE)
audit_sessions
Field	Type
id	UUID
organisation_id	UUID
framework_id	UUID
started_at	TIMESTAMP
completed_at	TIMESTAMP
status	TEXT
audit_events
Field	Type
audit_session_id	UUID
event_type	TEXT
actor_id	UUID
timestamp	TIMESTAMP
metadata	JSONB

This preserves institutional memory.

6. CORE WORKFLOWS
Framework onboarding

Framework defined

Controls imported

Equivalences mapped

Applicability decision

Controls marked applicable or excluded

Justification recorded

Locked for audit period

Assessment execution

Evidence linked

Assessment recorded

Gaps identified

PSA cases created

Evidence lifecycle

Evidence collected from PSA, SIEM, EDR, VM

Validity window enforced

Expiry triggers reassessment

Attestation

Senior role signs control

Statement preserved

Time-bounded responsibility recorded

7. SECURITY, LEGAL AND AUDIT INTEGRITY

This module must guarantee:

Evidence immutability

Assessment traceability

Separation of assessor and implementer

Historical reconstruction

No silent changes

If challenged in court, this module must hold.

8. DESIGN TRAPS TO AVOID

These destroy compliance credibility:

Treating controls as checkboxes

Reusing expired evidence

Auto-passing based on tooling presence

Mixing risk acceptance with compliance

Allowing edits without versioning

Compliance is about process discipline, not tool count.

9. HOW THIS CONSUMES YOUR PLATFORM

From PSA

Cases, tasks, approvals

Human decisions

From SIEM

Log evidence

Detection coverage

From EDR

Endpoint protection proof

Response capability

From Vulnerability Management

Risk posture

Acceptance records

From Pen Testing

Control effectiveness validation

Compliance Auditing is where everything converges.

10. WHY THIS DESIGN IS DEFENSIBLE

With this structure:

You can prove governance over time

You can answer “why” questions calmly

You can support multiple frameworks without duplication

You can survive regulator, customer, and legal scrutiny

This is compliance as institutional memory, not box-ticking.
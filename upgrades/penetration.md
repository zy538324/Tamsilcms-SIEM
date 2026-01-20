1. PURPOSE AND PHILOSOPHICAL MODEL
Core purpose

Penetration Testing exists to answer six uncomfortable questions:

Which vulnerabilities are actually exploitable in practice?

What attack paths exist across systems, identities, and trust boundaries?

How far can an attacker realistically go?

Which controls fail silently?

Which alerts fire too late or not at all?

Can we prove what was tested, how, and with what outcome?

Pen Testing does not replace:

SIEM detections

EDR containment

Vulnerability scanning

Compliance controls

It challenges their assumptions.

What Pen Testing must never do

Run without authorisation and scope

Generate untraceable findings

Override or delete security telemetry

Mutate production state without recording it

Close its own findings

Pen Testing produces findings and evidence, never closure.

2. HIGH-LEVEL SYSTEM RESPONSIBILITIES
What the Pen Testing module owns

Engagement definition and scoping

Attack surface modelling

Tool orchestration and result ingestion

Manual tester findings

Exploitability confirmation

Attack chain construction

Evidence capture

Mapping findings into PSA work

What it explicitly does not own

Asset inventory (referenced)

Vulnerability canon (referenced)

Incident response

Remediation execution

Compliance sign-off

Pen Testing informs risk and response, it does not decide them.

3. OPERATIONAL MODEL

Pen Testing is time-boxed and scoped, unlike other modules.

Each test is an engagement, with:

Explicit authorisation

Defined scope

Defined attack class

Defined timeframe

Defined objectives

This is non-negotiable for legal, ethical, and audit reasons.

4. DATA ARCHITECTURE OVERVIEW

This module is relational, hierarchical, and evidence-heavy.

You must model:

Engagements

Scope

Test executions

Findings

Attack chains

Evidence

Links to vulnerabilities and controls

PostgreSQL is appropriate, but immutability and provenance matter more than speed.

5. DATABASE SCHEMA (DETAILED)
A. ENGAGEMENT AND SCOPE
pentest_engagements
Field	Type	Purpose
id	UUID (PK)	Engagement ID
organisation_id	UUID (FK)	Target org
name	TEXT	Engagement name
engagement_type	TEXT	internal, external
start_date	TIMESTAMP	Authorised start
end_date	TIMESTAMP	Authorised end
status	TEXT	planned, active, closed
authorised_by	UUID (FK users)	Approval

This table is legally significant.

pentest_scope
Field	Type
id	UUID
engagement_id	UUID
asset_id	UUID
scope_type	TEXT
notes	TEXT

Every action must be justifiable against scope.

B. ATTACK SURFACE AND TECHNIQUES
attack_surfaces
Field	Type
id	UUID
engagement_id	UUID
surface_type	TEXT
description	TEXT
discovered_at	TIMESTAMP

Used to record what was found to exist, not just tested.

attack_techniques
Field	Type
id	UUID
technique_id	TEXT
name	TEXT
category	TEXT

This allows mapping later to detection and controls.

C. TOOL EXECUTION AND RESULTS
pentest_tools
Field	Type
id	UUID
name	TEXT
version	TEXT
tool_type	TEXT
pentest_tool_runs
Field	Type
id	UUID
engagement_id	UUID
tool_id	UUID
started_at	TIMESTAMP
completed_at	TIMESTAMP
status	TEXT
raw_output_uri	TEXT

Raw outputs must be preserved, not summarised away.

D. FINDINGS (THE CORE OUTPUT)
pentest_findings

This table is the heart of the module.

Field	Type	Purpose
id	UUID (PK)	Finding ID
engagement_id	UUID	Source
asset_id	UUID	Target
finding_type	TEXT	exploit, misconfig
title	TEXT	Short summary
description	TEXT	Full narrative
severity	INTEGER	Risk
confidence	INTEGER	Certainty
exploit_proven	BOOLEAN	Yes/no
discovered_at	TIMESTAMP	Time

This is not a CVE table. This is what actually worked.

finding_vulnerabilities
Field	Type
finding_id	UUID
vulnerability_id	UUID

This links Pen Testing back to Vulnerability Management.

E. ATTACK CHAINS (CRITICAL)
attack_chains
Field	Type
id	UUID
engagement_id	UUID
description	TEXT
impact	TEXT
created_at	TIMESTAMP
attack_chain_steps
Field	Type
chain_id	UUID
step_order	INTEGER
technique_id	TEXT
finding_id	UUID
notes	TEXT

This is how you demonstrate real attacker journeys.

F. EVIDENCE AND PROOF
pentest_evidence
Field	Type
id	UUID
finding_id	UUID
evidence_type	TEXT
storage_uri	TEXT
hash	TEXT
captured_at	TIMESTAMP

Evidence must be immutable and attributable.

G. PSA INTEGRATION
pentest_cases
Field	Type
finding_id	UUID
psa_case_id	UUID
created_at	TIMESTAMP

Findings become work, not just reports.

6. CORE WORKFLOWS
Engagement creation

Scope defined

Authorisation recorded

Assets locked

Time window enforced

Testing execution

Tools run

Manual actions recorded

Evidence captured

Findings created only when exploitability is confirmed

Analysis and chaining

Findings linked

Attack paths constructed

Business impact articulated

Handoff to PSA

Remediation cases created

Evidence attached

Ownership assigned

No auto-closure

7. SECURITY, LEGAL AND AUDIT CONTROLS

This module must enforce:

Scope enforcement

Time-bound authorisation

Non-repudiation of actions

Evidence integrity

Clear separation between testing and fixing

Pen Testing without this becomes a liability.

8. DESIGN TRAPS TO AVOID

These destroy credibility fast:

Dumping scanner output as findings

Treating exploitation as binary without confidence

Failing to record scope decisions

Producing PDF-only results

Losing linkage to vulnerabilities and controls

A good pen test teaches. A bad one performs.

9. HOW PEN TESTING FITS YOUR PLATFORM

Feeds Vulnerability Management

Confirms exploitability

Adjusts risk scores

Feeds SIEM

Tests detection logic

Validates alerts

Feeds EDR

Tests behavioural coverage

Identifies blind spots

Feeds PSA

Creates accountable remediation work

Preserves institutional memory

This is how testing becomes learning.

10. WHY THIS DESIGN HOLDS UP

With this structure:

You can prove what was tested and why

You can replay attacker paths

You can show improvement over time

You can survive regulators and lawyers

This is Penetration Testing as engineering discipline, not spectacle.
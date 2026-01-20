1. SIEM PURPOSE AND THREAT MODEL
Core purpose

The SIEM exists to answer four questions with defensible precision:

What events occurred?

Where did they originate?

How do they relate to each other?

Do they represent risk that requires human action?

It does not own response, remediation, closure, or attestation.
Those belong to the PSA.

The SIEM’s output is findings and signals, not decisions.

Threat model assumptions

Your SIEM must assume:

Logs may be incomplete, delayed, duplicated, or maliciously noisy

Sources may lie, misconfigure themselves, or drift over time

Attackers may deliberately attempt log flooding or evasion

Operators will misinterpret raw data without context

Therefore:

Normalisation is mandatory

Correlation must be explainable

Raw events must remain immutable

Derived conclusions must be traceable

2. HIGH-LEVEL SYSTEM RESPONSIBILITIES
What the SIEM owns

Event ingestion and validation

Normalisation into a canonical schema

Enrichment (asset, identity, geo, time)

Correlation and rule evaluation

Finding generation

Evidence preservation

Escalation into PSA cases

What the SIEM explicitly does not own

Ticket lifecycle

Human decision logging

SLA enforcement

Final severity acceptance

Compliance attestation

This separation is non-negotiable.

3. DATA ARCHITECTURE OVERVIEW

A serious SIEM cannot be a single database.

You need three distinct data planes, even if they physically live on the same infrastructure initially.

Raw event store (append-only, high volume)

Normalised event store (queryable, structured)

Findings and intelligence store (relational, auditable)

PostgreSQL is suitable for planes 2 and 3.
Plane 1 may eventually move to object storage or a log-optimised backend, but we will design it so that is not a schema-breaking change.

4. DATABASE SCHEMA (DETAILED)
A. EVENT INGESTION AND RAW STORAGE
raw_events

Immutable record of received data.

Field	Type	Purpose
id	UUID (PK)	Event ID
source_system	TEXT	windows, firewall, edr
received_at	TIMESTAMP	Ingest time
event_time	TIMESTAMP	Source time
payload	JSONB	Original event
payload_hash	TEXT	Integrity
ingestion_node	TEXT	Receiver ID

Rules:

Never updated

Never deleted

Retention configurable by policy

B. NORMALISED EVENT MODEL
events

Canonical security events.

Field	Type	Purpose
id	UUID (PK)	Normalised ID
raw_event_id	UUID (FK)	Provenance
event_category	TEXT	auth, process, network
event_type	TEXT	login_failed, exec
severity	INTEGER	Normalised scale
asset_id	UUID (FK assets)	Affected asset
user_id	UUID (nullable)	Actor
source_ip	INET	Source
destination_ip	INET	Target
event_time	TIMESTAMP	True time

This table is what analysts query daily.

event_tags
Field	Type
event_id	UUID
tag	TEXT

Used for ATT&CK-style mapping, tool labels, heuristics.

C. ENRICHMENT AND CONTEXT
event_enrichment
Field	Type
event_id	UUID
enrichment_type	TEXT
enrichment_data	JSONB
created_at	TIMESTAMP

Examples:

GeoIP

ASN

Asset criticality

Identity role

D. CORRELATION AND RULES
correlation_rules
Field	Type
id	UUID
name	TEXT
description	TEXT
logic	JSONB
enabled	BOOLEAN
severity	INTEGER

Logic must be stored, not hard-coded, to remain auditable.

correlation_hits
Field	Type
id	UUID
rule_id	UUID
triggered_at	TIMESTAMP
event_ids	UUID[]
confidence	INTEGER

This is how you explain why something fired.

E. FINDINGS (SIEM OUTPUT)
siem_findings

This is the SIEM’s most important table.

Field	Type	Purpose
id	UUID (PK)	Finding ID
organisation_id	UUID	Tenant
finding_type	TEXT	brute_force, lateral_move
severity	INTEGER	Risk signal
confidence	INTEGER	How sure
status	TEXT	new, escalated
created_at	TIMESTAMP	Detection time
psa_case_id	UUID (nullable)	Linked case

Once escalated, ownership transfers to the PSA.

finding_events
Field	Type
finding_id	UUID
event_id	UUID

Allows full replay and justification.

F. EVIDENCE HANDOFF TO PSA

The SIEM does not store long-term evidence itself.

Instead, it packages evidence for PSA ingestion.

evidence_packages
Field	Type
id	UUID
finding_id	UUID
package_uri	TEXT
hash	TEXT
created_at	TIMESTAMP

This allows:

Case attachment

Audit reproduction

Legal defensibility

5. CORE SIEM WORKFLOWS
Ingestion → normalisation

Event received

Hash computed

Stored raw

Parsed into canonical schema

Asset and identity resolved

Enrichment applied

Failures here must be observable, not silent.

Correlation → finding

Rules evaluate sliding windows

Context merged across assets and users

Confidence calculated

Finding created

Related events linked

Escalation → PSA

Severity threshold crossed

PSA case created

Evidence package attached

SIEM marks finding as escalated

PSA now owns the clock

No SIEM auto-closure after this point.

6. SECURITY AND AUDITABILITY

The SIEM must enforce:

Append-only raw logs

Provenance tracking (raw → normalised → finding)

Rule transparency (no black boxes)

Time integrity (clock drift awareness)

Every finding must be answerable with:
“This is what we saw, this is how we reasoned, this is what we passed on.”

7. DESIGN TRAPS TO AVOID

These kill SIEMs in production:

Treating SIEM as a dashboard, not a data system

Letting rules mutate silently

Overwriting events during “normalisation”

Mixing alerting logic with ticket logic

Collapsing confidence and severity into one number

Avoid these and your SIEM remains trustworthy.

8. HOW THIS DOCKS INTO YOUR PSA

SIEM creates findings

Findings escalate into cases

PSA assigns ownership and tasks

SIEM remains read-only post-escalation

Evidence flows one way, never back

This clean boundary is what lets compliance and audits work later without special handling.
1. PSA PURPOSE AND OPERATING MODEL
Core purpose

The PSA exists to answer six non-negotiable questions at any point in time:

What happened?

When did we know?

Who owned it?

What actions were taken?

Was it resolved correctly?

Can we prove all of the above later?

Every other system feeds signals.
The PSA turns signals into decisions, work, accountability and evidence.

What the PSA must never do

Perform detection itself

Infer technical truth beyond what is supplied

Mutate or overwrite original evidence

Become a dumping ground for raw logs

The PSA is authoritative on process, not on telemetry.

2. HIGH-LEVEL SYSTEM RESPONSIBILITIES
PSA as the system of record

The PSA is the authoritative owner of:

Tickets and cases

Tasks and work items

Ownership and escalation

SLAs and response clocks

Human decisions and approvals

Evidence attachments and attestations

Audit trails and timelines

Other systems may generate findings.
Only the PSA may declare work to be done, done, or accepted.

Integration posture

All other modules integrate into the PSA, not sideways.

RMM → creates incidents, tasks, remediation actions

SIEM → raises security events, investigations

EDR → generates detections requiring response

Vulnerability Management → generates risk remediation tickets

Pen Testing → generates findings and remediation plans

Compliance → generates gaps, actions, evidence requests

This prevents fractured accountability.

3. PSA CORE DOMAIN MODEL (CONCEPTUAL)

At a conceptual level, the PSA revolves around five immutable ideas:

Organisation / Tenant

Asset (device, system, service)

Issue (something that requires attention)

Work (actions taken)

Evidence (proof of action or state)

Everything else decorates these.

4. DATABASE ARCHITECTURE (POSTGRESQL)

You should treat the PSA database as relational, strongly consistent, and auditable.

PostgreSQL as primary datastore

Strict foreign keys

No silent deletes

Soft deletes only with tombstones

Time fields always UTC

Append-only where evidence or history is involved

I will break this down by functional cluster.

A. TENANCY, IDENTITY AND STRUCTURE
organisations

Represents a customer, internal business unit, or environment.

Field	Type	Purpose
id	UUID (PK)	Organisation ID
name	TEXT	Display name
type	TEXT	internal, customer, lab
status	TEXT	active, suspended
created_at	TIMESTAMP	Creation time
users

Human operators.

Field	Type	Purpose
id	UUID (PK)	User ID
organisation_id	UUID (FK)	Owning org
email	TEXT	Identity
display_name	TEXT	Name
status	TEXT	active, disabled
created_at	TIMESTAMP	Creation time
roles

Abstract permissions.

Field	Type
id	UUID (PK)
name	TEXT
scope	TEXT
user_roles

Many-to-many.

Field	Type
user_id	UUID (FK)
role_id	UUID (FK)
B. ASSETS (SHARED ACROSS ALL MODULES)

The PSA must not duplicate asset truth but must reference it.

assets

Authoritative pointer to anything work can be done to.

Field	Type	Purpose
id	UUID (PK)	Asset ID
organisation_id	UUID (FK)	Owner
asset_type	TEXT	endpoint, server, app
external_ref	TEXT	RMM/EDR/SIEM ID
name	TEXT	Human readable
status	TEXT	active, retired

This table is referenced by every other module.

C. TICKETS AND CASES (THE HEART)
cases

Top-level container. Think “incident”, “request”, “investigation”.

Field	Type	Purpose
id	UUID (PK)	Case ID
organisation_id	UUID (FK)	Owner
case_type	TEXT	incident, problem, change, audit
source_system	TEXT	rmm, siem, manual
severity	INTEGER	Normalised scale
status	TEXT	open, in_progress, resolved
opened_at	TIMESTAMP	Clock start
closed_at	TIMESTAMP	Clock stop
case_assets

Cases may affect multiple assets.

Field	Type
case_id	UUID (FK)
asset_id	UUID (FK)
case_relationships

Parent/child or related cases.

Field	Type
parent_case_id	UUID
child_case_id	UUID
relationship_type	TEXT

This enables SIEM incidents spawning multiple remediation tasks.

D. TASKS AND WORK ITEMS
tasks

Atomic units of work.

Field	Type	Purpose
id	UUID (PK)	Task ID
case_id	UUID (FK)	Owning case
assigned_to	UUID (FK users)	Owner
task_type	TEXT	investigation, remediation
status	TEXT	pending, running, done
created_at	TIMESTAMP	Created
completed_at	TIMESTAMP	Finished
task_actions

Granular steps taken.

Field	Type
id	UUID
task_id	UUID
action_type	TEXT
description	TEXT
performed_by	UUID
performed_at	TIMESTAMP

This is how you reconstruct exactly what was done.

E. SLA, ESCALATION AND TIME
sla_policies
Field	Type
id	UUID
name	TEXT
response_minutes	INTEGER
resolution_minutes	INTEGER
case_sla

Tracks live SLA clocks.

Field	Type
case_id	UUID
sla_id	UUID
breached	BOOLEAN
breached_at	TIMESTAMP
F. EVIDENCE AND ATTACHMENTS (CRITICAL)
evidence_items

This table underpins compliance and legal defensibility.

Field	Type	Purpose
id	UUID (PK)	Evidence ID
case_id	UUID (FK)	Related case
evidence_type	TEXT	log, screenshot, report
source_system	TEXT	siem, edr, manual
hash	TEXT	Integrity
stored_uri	TEXT	Object storage
created_at	TIMESTAMP	Capture time

Evidence is immutable once stored.

evidence_links

Reuse evidence across cases or audits.

Field	Type
evidence_id	UUID
linked_entity	TEXT
linked_id	UUID
G. AUDIT LOG (NON-NEGOTIABLE)
audit_log

Append-only.

Field	Type
id	UUID
actor_id	UUID
action	TEXT
entity_type	TEXT
entity_id	UUID
timestamp	TIMESTAMP
metadata	JSONB

Every button click that matters ends here.

5. CORE WORKFLOWS
Inbound signal → case

External system posts finding

Normalisation layer maps severity and category

PSA creates case

Assets are attached

SLA clock starts

Owner assigned or queued

Case → tasks

Tasks generated automatically or manually

Tasks may invoke:

RMM scripts

EDR actions

Scans

Results flow back as task actions

Evidence attached automatically

Resolution → evidence closure

Human attests resolution

Supporting evidence linked

Case closed

Audit log sealed

This is what auditors care about.

6. SECURITY AND GOVERNANCE

The PSA must enforce:

RBAC at case, task and evidence level

Separation of duty (cannot approve own work)

Immutable evidence storage

Full timeline reconstruction

If this is weak, compliance collapses later.

7. DESIGN TRAPS TO AVOID

These are common failures in commercial PSAs:

Treating tickets as free-text blobs

Allowing evidence to be edited or deleted

Letting tools auto-close cases without human acknowledgement

Losing linkage between detection and response

Mixing raw telemetry into PSA tables

Avoid these and your system will age well.

8. WHY THIS WORKS AS A SPINE

With this PSA in place:

SIEM feeds events → cases

EDR feeds detections → tasks

Vulnerability scans feed remediation plans

Pen tests feed structured findings

Compliance audits pull evidence and timelines

Nothing duplicates truth. Everything converges here.
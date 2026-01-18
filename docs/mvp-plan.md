# MVP Workflow Command Plan

This document captures the staged MVP roadmap. MVP-0 is fully defined and locked in this repository as a non-negotiable baseline.

## MVP-0 — Ground Rules & Repo Structure (Foundation Lock)

**Objective**
Create an irreversible baseline so architectural drift is impossible.

**Outcomes**
- Mono-repo initialised with strict boundaries:
  - /agent
  - /transport
  - /ingestion
  - /core-services
  - /data-model
  - /ui
  - /policies
  - /docs
- Enforced rules:
  - One agent binary only.
  - No direct DB access from UI.
  - No module talks to the network directly (transport layer is the only network boundary).
- Canonical IDs defined:
  - tenant_id
  - asset_id
  - identity_id
  - event_id

**Exit Condition**
Repo exists, build pipelines stubbed, no functionality yet, but rules are locked.

## MVP-1 — Secure Identity & Transport Plane

**Objective**
Nothing runs unless identity and trust are solved.

**Exit Condition**
An agent can cryptographically authenticate to the platform and exchange a signed “hello”.


# Unified Security & Operations Platform

## Project Overview
This repository hosts the mono-repo for the Unified Security & Operations Platform. The initial baseline locks the repository structure and architectural boundaries to prevent drift while MVP-0 is completed.

### Purpose
Establish an irreversible foundation for a zero-trust security and operations platform with clearly defined module boundaries, canonical identifiers, and secure-by-design principles.

### Stack (initial)
- C++ (agent core, future MVPs)
- Backend services (TBD, to be defined in MVP-1+)
- UI (TBD, no UI work in MVP-0)

### Key Principles (MVP-0)
- One agent binary only.
- No direct DB access from the UI.
- No module talks to the network directly (all network operations are delegated to the transport layer).
- Canonical identifiers: tenant_id, asset_id, identity_id, event_id.

## Repository Structure
This mono-repo is intentionally partitioned into strict, non-overlapping domains. Each directory contains its own README describing its scope and constraints.

```
/agent
/transport
/ingestion
/core-services
/data-model
/ui
/policies
/docs
```

## Status
MVP-0 complete: structure locked, policies defined, and build pipeline stubbed.

## Security & Governance
All code must be secure, modular, and documented. Secrets must be handled via environment variables or OS secret stores. No Docker usage is permitted in this repository.


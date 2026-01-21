# Agent Architecture (Production-Grade Endpoint Substrate)

## Overview
This document describes the multi-service hostile-environment agent for SIEM, EDR, Vulnerability Management, Pen Testing, Compliance, and RMM. The agent is Windows-first, but portable, and strictly adheres to institutional control principles.

## Service Layout
- **Agent Core Service**: Orchestrates identity, config, module registry, telemetry, evidence, uplink.
- **Sensor Service**: Captures process, file, registry, network, and user events. Emits facts only.
- **Execution Service**: Executes scripts, patches, installs, and remote ops. Strictly gated.
- **User Interaction Helper**: Optional, runs in user context for UI and notifications.
- **Watchdog Service**: Monitors agent health, restarts, and anti-tamper.

## IPC & Boundaries
- Named pipes, shared memory (ACLs), strict message schemas (see ipc/messages.h).
- No service trusts another blindly.

## Subsystems
- Identity & Trust
- Config Manager
- Module Registry
- Telemetry Router
- Command Dispatcher
- Evidence Broker

## Evidence System
- Immutable, hashed, time-stamped, source-tagged, linked to case/control/task.

## Compliance & Audit
- Local control checks, artefact collection, evidence bundles. Never declares compliance.

## Update Pipeline
- Signed, staged, rollback-capable, silent, safe.

## Patch Command Channel (Phase 2)
The agent polls the command channel for signed patch jobs, acknowledges receipt, executes them in the
execution service, and reports results to both RMM and PSA.

### Patch Job Command Schema (Canonical Payload)
```json
{
  "job_id": "patch-job-001",
  "asset_id": "asset-123",
  "scheduled_at": "2024-05-01T01:00:00Z",
  "reboot_policy": "if_required",
  "issued_at": 1714500000,
  "nonce": "c3f42aa1d0d34f08babb7816f3f0c1f0",
  "patches": [
    {
      "patch_id": "patch-001",
      "title": "Windows Security Update",
      "vendor": "Microsoft",
      "severity": "critical",
      "kb": "KB5010001"
    }
  ]
}
```

### Signed Command Envelope
The backend wraps the canonical payload with a signature:
```json
{
  "job_id": "patch-job-001",
  "asset_id": "asset-123",
  "scheduled_at": "2024-05-01T01:00:00Z",
  "reboot_policy": "if_required",
  "issued_at": 1714500000,
  "nonce": "c3f42aa1d0d34f08babb7816f3f0c1f0",
  "patches": [
    {
      "patch_id": "patch-001",
      "title": "Windows Security Update",
      "vendor": "Microsoft",
      "severity": "critical",
      "kb": "KB5010001"
    }
  ],
  "signature": "base64(hmac_sha256(shared_key, issued_at + '.' + canonical_payload))"
}
```

### Command Channel Endpoints (mTLS or API key + nonce)
- `GET /mtls/rmm/patch-jobs/next?asset_id={asset_id}` returns a signed patch job or 204 if none.
- `POST /mtls/rmm/patch-jobs/ack` acknowledges receipt/execution state.
- `POST /mtls/rmm/patch-jobs/result` posts execution results and summaries.

### Security Controls
- HMAC signatures validated with shared key (`AGENT_HMAC_SHARED_KEY`).
- Nonce and timestamp required; replay protection enforces ±5 minute skew.
- mTLS supported via agent cert/key or API key via `AGENT_API_KEY`.

## Build System
- CMake, multi-binary output, strict boundaries.

## Threat Model
- Privilege separation, crash containment, anti-tamper, binary integrity, controlled update pipeline.

## Next Steps
- IPC schema implementation
- Windows kernel interaction boundaries
- Secure update pipeline design
- C++ project layout and build system
- Threat modelling the agent itself

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

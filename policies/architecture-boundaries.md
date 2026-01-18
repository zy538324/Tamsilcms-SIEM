# Architecture Boundaries (MVP-0)

This document locks the architectural constraints for the platform. No module may violate these rules.

## Non-Negotiable Constraints
1. **One agent binary only**
   - The agent is a single privileged binary, deployed per host.
   - Sub-modules must compile into or link against the same binary.

2. **No direct DB access from the UI**
   - The UI can only communicate with core-services via approved APIs.
   - Direct DB drivers or ORM access from UI code is prohibited.

3. **No module talks to the network directly**
   - All networking must be routed through the `/transport` layer.
   - Other modules must expose interfaces that are transport-agnostic.

## Enforcement Guidance
- Reviews must reject any PR that violates these boundaries.
- CI policy checks can be added in later MVPs to enforce directory-level rules.


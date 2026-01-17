# Agent

Scope: Single privileged agent binary responsible for host-level operations.

Constraints:
- Must compile to a single binary.
- No direct network calls (all egress via /transport).
- Runs as LocalSystem (Windows) or root systemd service (Linux) in later MVPs.


# Agent

Scope: Single privileged agent binary responsible for host-level operations.

Constraints:
- Must compile to a single binary.
- No direct network calls (all egress via /transport).
- Runs as LocalSystem (Windows) or root systemd service (Linux) in later MVPs.

Runtime configuration:
- `config/agent_config.ini` is loaded from the executable directory by default (override with `AGENT_CONFIG_PATH`).
- `config/agent.env` provides a starter environment file for shared key and identity defaults.

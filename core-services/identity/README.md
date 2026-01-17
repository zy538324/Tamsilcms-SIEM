# Identity (Core Services)

Scope: Identity lifecycle management for agents, services, and operators.

MVP-1 Responsibilities:
- Certificate issuance request validation.
- Rotation scheduling for server certificates.
- Identity registry anchored to canonical identifiers.

Constraints:
- No direct network I/O; transport handles all connections.
- No inline secrets; use environment variables or secure stores.


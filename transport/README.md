# Transport

Scope: The only module permitted to perform network I/O. All services and agents must use transport interfaces.

Responsibilities:
- TLS enforcement (TLS 1.3 only).
- mTLS and certificate pinning logic.
- Connection lifecycle and retries.


# PKI (Transport)

Scope: Transport-managed public key infrastructure for platform mTLS.

Goals (MVP-1):
- Root CA created offline.
- Intermediate CA managed by the platform.
- Strict TLS 1.3 and mTLS enforcement.
- Certificate pinning in the agent.

Constraints:
- No direct network operations outside the /transport module.
- Private key material must be stored in OS-managed secret stores.


# MVP-1 — Secure Identity & Transport Plane

## Objective
Nothing runs unless identity and trust are solved. This phase establishes a zero-trust control plane and cryptographic trust.

## Deliverables
1. **PKI**
   - Root CA (offline) documented creation process.
   - Intermediate CA (platform-controlled) lifecycle and rotation.

2. **Identity lifecycle**
   - Agent certificate issuance workflow (request, validation, approval).
   - Server certificate rotation schedule and revocation handling.

3. **Enforcement**
   - mTLS only.
   - TLS 1.3 only.
   - Certificate pinning in the agent.

## Exit Condition
An agent can cryptographically authenticate to the platform and exchange a signed “hello”.


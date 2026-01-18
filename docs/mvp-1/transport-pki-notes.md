# Transport PKI Notes (Draft)

These notes define the intended PKI workflow for MVP-1. Implementation details will be defined once the transport service is scaffolded.

## Root CA (Offline)
- Created and stored offline.
- Used only to sign the Intermediate CA.

## Intermediate CA (Platform)
- Hosted within the transport layer.
- Rotated on a defined schedule and upon compromise.

## Agent Certificate Lifecycle
1. Agent generates a key pair locally.
2. Agent submits a signed CSR via transport.
3. Core-services validates identity.
4. Transport signs with the Intermediate CA.

## Security Considerations
- Private keys never leave the generating host.
- CRLs/OCSP endpoints are served by transport.
- Certificate pinning enforced by the agent runtime.


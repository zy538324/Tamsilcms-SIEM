# Identity (Core Services)

Scope: Identity lifecycle management for agents, services, and operators.

## MVP-1 Runtime Stub
This directory now includes a minimal FastAPI service that accepts signed
"hello" payloads from agents via the transport layer. It validates request
headers, enforces HTTPS-only access, and checks an HMAC signature (temporary
placeholder until mTLS certificate verification is wired through transport).

### Key Endpoints
- `GET /health`: health check for load balancers.
- `POST /hello`: signed hello payload verification.

### Environment Variables
- `IDENTITY_ENV`: runtime environment name.
- `IDENTITY_HMAC_SHARED_KEY`: shared secret for HMAC verification.
- `IDENTITY_SIGNATURE_TTL`: allowed timestamp skew in seconds.
- `IDENTITY_SERVICE_NAME`: service identifier for responses.

Constraints:
- No direct network I/O; transport handles all connections.
- No inline secrets; use environment variables or secure stores.


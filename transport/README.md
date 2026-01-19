# Transport

Scope: The only module permitted to perform network I/O. All services and agents must use transport interfaces.

Responsibilities:
- TLS enforcement (TLS 1.3 only).
- mTLS and certificate pinning logic.
- Connection lifecycle and retries.

## MVP-1 Runtime Stub
This directory now includes a minimal FastAPI gateway that accepts mTLS-backed
"hello" payloads from agents and proxies them to core-services identity.

### Key Endpoints
- `GET /health`: health check for load balancers.
- `POST /mtls/hello`: forwards signed hello payloads to identity.
- `POST /mtls/events`: forwards signed event batches to ingestion.

### Environment Variables
- `TRANSPORT_ENV`: runtime environment name.
- `TRANSPORT_IDENTITY_URL`: base URL for the identity service.
- `TRANSPORT_REQUEST_TIMEOUT`: outbound request timeout in seconds.
- `TRANSPORT_SERVICE_NAME`: service identifier for responses.
- `TRANSPORT_TRUSTED_FINGERPRINTS`: comma-separated certificate fingerprints (optional allow list).

Constraints:
- Only transport performs network I/O.
- No inline secrets; use environment variables or secure stores.

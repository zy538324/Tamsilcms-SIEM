# Patch Management (Core Services)

Scope: Controlled patch management engine that normalises detections, applies
policy, produces execution plans, and captures evidence for audit.

## MVP-6 Runtime Stub
This directory includes a FastAPI service that accepts patch detection payloads,
creates policy-bound execution plans, and records evidence for compliance.

### Key Endpoints
- `GET /health`: health check for load balancers.
- `POST /detections`: ingest normalised patch detections.
- `POST /policies`: create or update a signed policy definition.
- `POST /plans`: generate a policy-driven execution plan.
- `POST /plans/{plan_id}/results`: record execution results and verification.
- `GET /plans/{plan_id}/tasks`: generate MVP-5 task manifest.
- `GET /evidence/{plan_id}`: retrieve immutable evidence.

### Environment Variables
- `PATCH_ENV`: runtime environment name.
- `PATCH_SERVICE_NAME`: service identifier for responses.
- `PATCH_API_KEY`: optional API key (X-API-Key header).
- `PATCH_STORAGE_PATH`: JSON persistence path for state.
- `PATCH_MAX_LOG_BYTES`: maximum bytes per log field.
- `PATCH_MAX_PATCHES_PER_BATCH`: limit on detection payload size.

Constraints:
- No direct network I/O; transport handles all connections.
- No inline secrets; use environment variables or secure stores.

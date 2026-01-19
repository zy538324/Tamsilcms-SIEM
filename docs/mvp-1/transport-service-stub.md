# Transport Service Stub (MVP-1)

This stub provides a minimal HTTP gateway for agent hello messages. It validates
mTLS headers and forwards signed payloads to the identity service.

## Rationale
- Enforces the rule that only the transport module performs network I/O.
- Centralises TLS/mTLS controls and header validation.
- Keeps identity service transport-agnostic.

## Run Locally (No Docker)
```bash
cd transport
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
TRANSPORT_IDENTITY_URL="https://localhost:8082" \
TRANSPORT_TRUSTED_FINGERPRINTS="sha256:examplefingerprint" \
uvicorn app.main:app --host 0.0.0.0 --port 8081
```

## Required Headers
- `X-Client-MTLS`: must be `success`.
- `X-Client-Identity`: identity provided by mTLS verification.
- `X-Client-Cert-Sha256`: certificate fingerprint.
- `X-Request-Signature`: base64 HMAC signature from agent.
- `X-Request-Timestamp`: Unix epoch seconds.

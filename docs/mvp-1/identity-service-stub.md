# Identity Service Stub (MVP-1)

This stub provides a minimal HTTP API for validating signed agent hello
payloads. It is intentionally constrained and does not implement UI or
persistence.

## Rationale
- Ensures transport-layer mTLS remains the only network boundary.
- Demonstrates signature verification and replay protection.
- Provides a secure baseline for later certificate validation.

## Run Locally (No Docker)
```bash
cd core-services/identity
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
IDENTITY_HMAC_SHARED_KEY="replace-me" \
IDENTITY_SIGNATURE_TTL=120 \
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Signature Format
- Header `X-Request-Timestamp`: Unix epoch seconds.
- Header `X-Request-Signature`: Base64 HMAC SHA-256 signature of
  `"{timestamp}." + canonical_json_payload`.


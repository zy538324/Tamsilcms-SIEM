# Ingestion

Scope: Data ingress pipelines for telemetry, logs, and events.

## Telemetry (MVP-4)
The ingestion service now accepts telemetry payloads and exposes read-only views for
metrics, series, baselines, and anomalies. Payloads are validated for schema version,
sample count, timestamps, uniqueness, units, and value ranges to prevent malformed
data from contaminating downstream analytics.

Endpoints (read-only views are query-only):
- `POST /telemetry`
- `GET /telemetry/{asset_id}/metrics`
- `GET /telemetry/{asset_id}/series`
- `GET /telemetry/{asset_id}/baselines`
- `GET /telemetry/{asset_id}/anomalies`

Constraints:
- No direct network I/O; must use /transport.
- No direct DB access from UI.

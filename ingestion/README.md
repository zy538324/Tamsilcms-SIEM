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

## Event Ingestion (MVP-7)
The ingestion service now accepts signed, immutable event batches and exposes
read-only queries for timelines, event detail, data gaps, and clock drift. Events
are verified for schema compliance, payload hashes, sequence continuity, and
timestamp bounds before being stored in the append-only ledger.

Endpoints:
- `POST /events`
- `GET /events/recent`
- `GET /events/{event_id}`
- `GET /events/assets/{asset_id}/timeline`
- `GET /events/assets/{asset_id}/gaps`
- `GET /events/assets/{asset_id}/clock-drifts`
- `GET /events/assets/{asset_id}/export.csv`

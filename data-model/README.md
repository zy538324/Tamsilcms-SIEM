# Data Model

Scope: Canonical schemas and shared domain models.

This module now includes a PostgreSQL schema scaffold that captures the full
planned data model across identity, assets, telemetry, SIEM events, detections,
patch management, vulnerability intelligence, compliance, and PSA workflows.

## Files
- `schema.sql`: forward-looking relational schema for the platform.

Constraints:
- Canonical identifiers (`tenant_id`, `asset_id`, `identity_id`, `event_id`) are
  mandatory across tables.
- No direct DB access from the UI.


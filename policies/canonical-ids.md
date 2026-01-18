# Canonical Identifiers

These identifiers are the canonical keys used across the platform. They must be used consistently in all services, events, and data models.

- **tenant_id**: Globally unique tenant identifier.
- **asset_id**: Unique identifier for a managed asset.
- **identity_id**: Unique identifier for an identity (user, service, or agent).
- **event_id**: Unique identifier for an event in the SIEM ledger.

## Format Guidance (Initial)
- Use ULIDs or UUIDv7 for sortable, globally unique IDs.
- IDs must be generated in core-services or data-model layers.
- Do not generate identifiers in the UI.


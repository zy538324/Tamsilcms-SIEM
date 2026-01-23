#[derive(Debug, Clone)]
pub struct TelemetryBatch {
    pub batch_id: String,
    pub event_count: usize,
}

pub fn prepare_telemetry_batch() -> TelemetryBatch {
    // TODO: Normalise sensor events and prepare SIEM payloads.
    TelemetryBatch {
        batch_id: "batch-placeholder".to_string(),
        event_count: 0,
    }
}

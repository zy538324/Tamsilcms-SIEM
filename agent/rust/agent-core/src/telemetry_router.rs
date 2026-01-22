#[derive(Debug, Clone)]
pub struct TelemetryPayload {
    pub stream: String,
    pub payload_bytes: usize,
}

pub fn route_telemetry(payload: TelemetryPayload) -> bool {
    // TODO: Apply filtering, attach identity, and forward to SIEM/EDR pipelines.
    !payload.stream.is_empty() && payload.payload_bytes > 0
}

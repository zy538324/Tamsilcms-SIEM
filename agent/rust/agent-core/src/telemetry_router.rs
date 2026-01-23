use crate::security::{validate_bounded_string, ValidationLimits};

#[derive(Debug, Clone)]
pub struct TelemetryPayload {
    pub stream: String,
    pub payload_bytes: usize,
}

pub fn route_telemetry(payload: TelemetryPayload) -> bool {
    // TODO: Apply filtering, attach identity, and forward to SIEM/EDR pipelines.
    let limits = ValidationLimits::default_limits();
    validate_bounded_string(&payload.stream, limits.max_stream_len) && payload.payload_bytes > 0
}

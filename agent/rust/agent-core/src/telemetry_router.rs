use crate::policy::PolicyBundle;
use crate::security::{validate_bounded_string, ValidationLimits};

#[derive(Debug, Clone)]
pub struct TelemetryPayload {
    pub stream: String,
    pub payload_bytes: usize,
}

pub fn route_telemetry(payload: TelemetryPayload, policy: &PolicyBundle) -> bool {
    // TODO: Apply filtering, attach identity, and forward to SIEM/EDR pipelines.
    let limits = ValidationLimits::default_limits();
    if !validate_bounded_string(&payload.stream, limits.max_stream_len) {
        return false;
    }
    if !policy.telemetry_streams.iter().any(|stream| stream == &payload.stream) {
        return false;
    }
    payload.payload_bytes > 0
}

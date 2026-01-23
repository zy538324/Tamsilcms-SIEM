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

#[cfg(test)]
mod tests {
    use super::{route_telemetry, TelemetryPayload};
    use crate::policy::{ExecutionPolicy, PolicyBundle};

    fn build_policy() -> PolicyBundle {
        PolicyBundle {
            schema_version: 1,
            version: "policy-test".to_string(),
            issued_at_unix_time_ms: 0,
            expires_at_unix_time_ms: u64::MAX,
            signing_key_id: "key-test".to_string(),
            signature: "signature".to_string(),
            execution: ExecutionPolicy {
                allowed_actions: vec!["patch-apply".to_string(), "script-run".to_string()],
                max_arguments: 2,
                max_argument_length: 8,
            },
            telemetry_streams: vec!["agent".to_string(), "sensor".to_string()],
        }
    }

    #[test]
    fn accepts_allowed_stream() {
        let policy = build_policy();
        let payload = TelemetryPayload {
            stream: "sensor".to_string(),
            payload_bytes: 12,
        };
        assert!(route_telemetry(payload, &policy));
    }

    #[test]
    fn rejects_unknown_stream() {
        let policy = build_policy();
        let payload = TelemetryPayload {
            stream: "unknown".to_string(),
            payload_bytes: 12,
        };
        assert!(!route_telemetry(payload, &policy));
    }

    #[test]
    fn rejects_empty_payload() {
        let policy = build_policy();
        let payload = TelemetryPayload {
            stream: "agent".to_string(),
            payload_bytes: 0,
        };
        assert!(!route_telemetry(payload, &policy));
    }
}

use crate::command_router::{route_command, SignedCommand};
use crate::policy::PolicyBundle;
use crate::telemetry_router::{route_telemetry, TelemetryPayload};

pub fn route_proto_envelope(
    envelope: &crate::proto::agent_ipc::Envelope,
    policy: &PolicyBundle,
    now_unix_time_ms: u64,
) -> bool {
    match &envelope.payload {
        Some(crate::proto::agent_ipc::envelope::Payload::ExecutionCommand(command)) => {
            route_command(SignedCommand {
                command_id: command.command_id.clone(),
                signed_payload: command.signed_blob.clone(),
                action: command.action.clone(),
                arguments: command.arguments.clone(),
                not_before_unix_time_ms: command.not_before_unix_time_ms,
                not_after_unix_time_ms: command.not_after_unix_time_ms,
            }, policy, now_unix_time_ms)
        }
        Some(crate::proto::agent_ipc::envelope::Payload::SensorEvent(_)) => {
            route_telemetry(TelemetryPayload {
                stream: "sensor".to_string(),
                payload_bytes: prost::Message::encoded_len(envelope),
            }, policy)
        }
        Some(crate::proto::agent_ipc::envelope::Payload::ExecutionResult(_))
        | Some(crate::proto::agent_ipc::envelope::Payload::EvidencePackage(_))
        | Some(crate::proto::agent_ipc::envelope::Payload::ComplianceAssertion(_))
        | Some(crate::proto::agent_ipc::envelope::Payload::HealthHeartbeat(_)) => {
            route_telemetry(TelemetryPayload {
                stream: "agent".to_string(),
                payload_bytes: prost::Message::encoded_len(envelope),
            }, policy)
        }
        None => false,
    }
}

#[cfg(test)]
mod tests {
    use super::route_proto_envelope;
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
                allowed_actions: vec!["script-run".to_string()],
                max_arguments: 2,
                max_argument_length: 8,
            },
            telemetry_streams: vec!["agent".to_string(), "sensor".to_string()],
        }
    }

    #[test]
    fn routes_sensor_event() {
        let policy = build_policy();
        let envelope = crate::proto::agent_ipc::Envelope {
            schema_version: 1,
            asset_id: "asset".to_string(),
            agent_id: "agent".to_string(),
            unix_time_ms: 1,
            payload: Some(crate::proto::agent_ipc::envelope::Payload::SensorEvent(
                crate::proto::agent_ipc::SensorEvent {
                    event_type: crate::proto::agent_ipc::EventType::EventTypeProcessStart as i32,
                    details: None,
                },
            )),
        };

        assert!(route_proto_envelope(&envelope, &policy, 1));
    }

    #[test]
    fn rejects_disallowed_command() {
        let policy = build_policy();
        let envelope = crate::proto::agent_ipc::Envelope {
            schema_version: 1,
            asset_id: "asset".to_string(),
            agent_id: "agent".to_string(),
            unix_time_ms: 1,
            payload: Some(crate::proto::agent_ipc::envelope::Payload::ExecutionCommand(
                crate::proto::agent_ipc::ExecutionCommand {
                    command_id: "cmd".to_string(),
                    signed_blob: "signed".to_string(),
                    action: "forbidden".to_string(),
                    arguments: vec![],
                    not_before_unix_time_ms: 1,
                    not_after_unix_time_ms: 2,
                },
            )),
        };

        assert!(!route_proto_envelope(&envelope, &policy, 1));
    }
}

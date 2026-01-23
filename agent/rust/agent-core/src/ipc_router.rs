use crate::command_router::{route_command, SignedCommand};
use crate::telemetry_router::{route_telemetry, TelemetryPayload};

pub fn route_proto_envelope(envelope: &crate::proto::agent_ipc::Envelope) -> bool {
    match &envelope.payload {
        Some(crate::proto::agent_ipc::envelope::Payload::ExecutionCommand(command)) => {
            route_command(SignedCommand {
                command_id: command.command_id.clone(),
                payload: command.signed_blob.clone(),
            })
        }
        Some(crate::proto::agent_ipc::envelope::Payload::SensorEvent(_)) => {
            route_telemetry(TelemetryPayload {
                stream: "sensor".to_string(),
                payload_bytes: prost::Message::encoded_len(envelope),
            })
        }
        Some(crate::proto::agent_ipc::envelope::Payload::ExecutionResult(_))
        | Some(crate::proto::agent_ipc::envelope::Payload::EvidencePackage(_))
        | Some(crate::proto::agent_ipc::envelope::Payload::ComplianceAssertion(_))
        | Some(crate::proto::agent_ipc::envelope::Payload::HealthHeartbeat(_)) => {
            route_telemetry(TelemetryPayload {
                stream: "agent".to_string(),
                payload_bytes: prost::Message::encoded_len(envelope),
            })
        }
        None => false,
    }
}

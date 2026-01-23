#[derive(Debug, Clone)]
pub struct EnvelopeMeta {
    pub schema_version: u32,
    pub payload_bytes: usize,
}

pub fn validate_schema_version(schema_version: u32, expected: u32) -> bool {
    schema_version == expected
}

pub fn validate_payload_size(payload_bytes: usize, max_payload_bytes: usize) -> bool {
    payload_bytes <= max_payload_bytes
}

pub fn validate_proto_envelope(
    envelope: &crate::proto::agent_ipc::Envelope,
    expected_version: u32,
    max_payload_bytes: usize,
) -> bool {
    let schema_ok = validate_schema_version(envelope.schema_version, expected_version);
    let payload_ok = envelope.payload.is_some();
    let encoded_len = prost::Message::encoded_len(envelope);
    let size_ok = validate_payload_size(encoded_len, max_payload_bytes);
    schema_ok && payload_ok && size_ok
}

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

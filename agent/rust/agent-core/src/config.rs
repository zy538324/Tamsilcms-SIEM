use serde::Deserialize;

#[derive(Debug, Deserialize, Clone)]
pub struct CoreConfig {
    pub asset_id: String,
    pub agent_id: String,
    pub ipc_pipe_name: String,
    pub max_payload_bytes: usize,
}

impl CoreConfig {
    pub fn placeholder() -> Self {
        Self {
            asset_id: "asset-placeholder".to_string(),
            agent_id: "agent-core".to_string(),
            ipc_pipe_name: r"\\.\pipe\tamsilcms-agent-core".to_string(),
            max_payload_bytes: 1024 * 1024,
        }
    }
}

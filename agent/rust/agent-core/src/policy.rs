use std::collections::HashSet;
use std::env;
use std::fs;

use serde::Deserialize;

use crate::security::{validate_bounded_string, ValidationLimits};

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ExecutionPolicy {
    pub allowed_actions: Vec<String>,
    pub max_arguments: usize,
    pub max_argument_length: usize,
}

#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct PolicyBundle {
    pub schema_version: u32,
    pub version: String,
    pub issued_at_unix_time_ms: u64,
    pub expires_at_unix_time_ms: u64,
    pub signing_key_id: String,
    pub signature: String,
    pub execution: ExecutionPolicy,
    pub telemetry_streams: Vec<String>,
}

impl PolicyBundle {
    pub fn placeholder() -> Self {
        Self {
            schema_version: 1,
            version: "policy-placeholder".to_string(),
            issued_at_unix_time_ms: 0,
            expires_at_unix_time_ms: u64::MAX,
            signing_key_id: "signing-key-placeholder".to_string(),
            signature: "signature-placeholder".to_string(),
            execution: ExecutionPolicy {
                allowed_actions: vec!["script-run".to_string(), "patch-apply".to_string()],
                max_arguments: 8,
                max_argument_length: 256,
            },
            telemetry_streams: vec!["sensor".to_string(), "agent".to_string()],
        }
    }

    pub fn from_env() -> Self {
        if let Ok(path) = env::var("AGENT_POLICY_PATH") {
            if let Ok(raw) = fs::read_to_string(path) {
                if let Ok(policy) = serde_json::from_str::<PolicyBundle>(&raw) {
                    return policy;
                }
            }
        }

        if let Ok(raw) = env::var("AGENT_POLICY_JSON") {
            if let Ok(policy) = serde_json::from_str::<PolicyBundle>(&raw) {
                return policy;
            }
        }

        Self::placeholder()
    }

    pub fn validate(&self, now_unix_time_ms: u64) -> bool {
        // TODO: Add signature verification once policy bundles are signed and pinned.
        let limits = ValidationLimits::default_limits();
        if self.schema_version == 0 {
            return false;
        }
        if !validate_bounded_string(&self.version, 64) {
            return false;
        }
        if !validate_bounded_string(&self.signing_key_id, 128) {
            return false;
        }
        if !validate_bounded_string(&self.signature, limits.max_payload_len) {
            return false;
        }
        if self.issued_at_unix_time_ms > self.expires_at_unix_time_ms {
            return false;
        }
        if now_unix_time_ms < self.issued_at_unix_time_ms
            || now_unix_time_ms > self.expires_at_unix_time_ms
        {
            return false;
        }

        if self.execution.allowed_actions.is_empty()
            || self.execution.max_arguments == 0
            || self.execution.max_argument_length == 0
        {
            return false;
        }

        let mut unique_actions = HashSet::new();
        for action in &self.execution.allowed_actions {
            if !validate_bounded_string(action, limits.max_command_id_len) {
                return false;
            }
            if !is_valid_action_name(action) {
                return false;
            }
            if !unique_actions.insert(action) {
                return false;
            }
        }

        if self.telemetry_streams.is_empty() {
            return false;
        }

        let mut unique_streams = HashSet::new();
        for stream in &self.telemetry_streams {
            if !validate_bounded_string(stream, limits.max_stream_len) {
                return false;
            }
            if !unique_streams.insert(stream) {
                return false;
            }
        }

        true
    }

    pub fn allows_action(&self, action: &str) -> bool {
        self.execution.allowed_actions.iter().any(|item| item == action)
    }
}

fn is_valid_action_name(action: &str) -> bool {
    action
        .chars()
        .all(|ch| ch.is_ascii_lowercase() || ch == '-' || ch == '_')
}

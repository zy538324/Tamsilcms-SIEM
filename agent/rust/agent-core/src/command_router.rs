use crate::policy::PolicyBundle;
use crate::security::{validate_bounded_string, ValidationLimits};

#[derive(Debug, Clone)]
pub struct SignedCommand {
    pub command_id: String,
    pub signed_payload: String,
    pub action: String,
    pub arguments: Vec<String>,
    pub not_before_unix_time_ms: u64,
    pub not_after_unix_time_ms: u64,
}

pub fn route_command(command: SignedCommand, policy: &PolicyBundle, now_unix_time_ms: u64) -> bool {
    // TODO: Verify signature against trust bundle and enforcement keys.
    let limits = ValidationLimits::default_limits();
    if !validate_bounded_string(&command.command_id, limits.max_command_id_len) {
        return false;
    }
    if !validate_bounded_string(&command.signed_payload, limits.max_payload_len) {
        return false;
    }
    if !validate_bounded_string(&command.action, limits.max_command_id_len) {
        return false;
    }
    if !policy.allows_action(&command.action) {
        return false;
    }
    if command.arguments.len() > policy.execution.max_arguments {
        return false;
    }
    if !command
        .arguments
        .iter()
        .all(|arg| validate_bounded_string(arg, policy.execution.max_argument_length))
    {
        return false;
    }
    if command.not_before_unix_time_ms > command.not_after_unix_time_ms {
        return false;
    }
    if now_unix_time_ms < command.not_before_unix_time_ms
        || now_unix_time_ms > command.not_after_unix_time_ms
    {
        return false;
    }

    true
}

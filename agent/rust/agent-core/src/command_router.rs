use crate::security::{validate_bounded_string, ValidationLimits};

#[derive(Debug, Clone)]
pub struct SignedCommand {
    pub command_id: String,
    pub payload: String,
}

pub fn route_command(command: SignedCommand) -> bool {
    // TODO: Verify signature, enforce scope, and forward to C++ exec service.
    let limits = ValidationLimits::default_limits();
    validate_bounded_string(&command.command_id, limits.max_command_id_len)
        && validate_bounded_string(&command.payload, limits.max_payload_len)
}

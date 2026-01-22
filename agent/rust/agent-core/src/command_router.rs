#[derive(Debug, Clone)]
pub struct SignedCommand {
    pub command_id: String,
    pub payload: String,
}

pub fn route_command(command: SignedCommand) -> bool {
    // TODO: Verify signature, enforce scope, and forward to C++ exec service.
    !command.command_id.is_empty() && !command.payload.is_empty()
}

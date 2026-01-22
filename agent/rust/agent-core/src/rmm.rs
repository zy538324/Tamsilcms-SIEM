#[derive(Debug, Clone)]
pub struct ExecutionRequest {
    pub command_id: String,
    pub signed_payload: String,
}

pub fn queue_execution_request() -> ExecutionRequest {
    // TODO: Validate signed command from PSA and return a validated request.
    ExecutionRequest {
        command_id: "command-placeholder".to_string(),
        signed_payload: "signed-payload-placeholder".to_string(),
    }
}

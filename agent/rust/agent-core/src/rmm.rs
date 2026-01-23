use crate::policy::PolicyBundle;

#[derive(Debug, Clone)]
pub struct ExecutionRequest {
    pub command_id: String,
    pub signed_payload: String,
    pub action: String,
    pub arguments: Vec<String>,
}

pub fn queue_execution_request(policy: &PolicyBundle) -> Option<ExecutionRequest> {
    // TODO: Validate signed command from PSA and return a validated request.
    let action = policy.execution.allowed_actions.first()?.clone();
    Some(ExecutionRequest {
        command_id: "command-placeholder".to_string(),
        signed_payload: "signed-payload-placeholder".to_string(),
        action,
        arguments: vec!["--dry-run".to_string()],
    })
}

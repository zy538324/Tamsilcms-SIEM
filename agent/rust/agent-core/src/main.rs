use std::time::Duration;

use serde::Deserialize;
use tokio::signal;
use tracing::{info, warn};

#[derive(Debug, Deserialize)]
struct CoreConfig {
    asset_id: String,
    agent_id: String,
    ipc_pipe_name: String,
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt()
        .with_env_filter("info")
        .init();

    let config = CoreConfig {
        asset_id: "asset-placeholder".to_string(),
        agent_id: "agent-core".to_string(),
        ipc_pipe_name: r"\\.\pipe\tamsilcms-agent-core".to_string(),
    };

    info!(asset_id = %config.asset_id, agent_id = %config.agent_id, "agent core starting");
    warn!("placeholder: load config, establish trust, and start IPC listeners");

    // TODO: Load configuration from disk/env, validate policies, and initialise trust.
    // TODO: Start IPC listeners for sensor/exec/user-helper services.
    // TODO: Enforce rate limits and schema validation on all inbound messages.

    loop {
        tokio::select! {
            _ = signal::ctrl_c() => {
                info!("shutdown signal received");
                break;
            }
            _ = tokio::time::sleep(Duration::from_secs(30)) => {
                info!("heartbeat tick");
            }
        }
    }

    info!("agent core stopping");
}

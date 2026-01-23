use std::time::Duration;

use tokio::signal;
use tracing::info;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt()
        .with_env_filter("info")
        .init();

    info!("agent watchdog starting");

    // TODO: Monitor agent-core health via IPC heartbeat.
    // TODO: Perform minimal restart logic and report status to agent-core.

    loop {
        tokio::select! {
            _ = signal::ctrl_c() => {
                info!("shutdown signal received");
                break;
            }
            _ = tokio::time::sleep(Duration::from_secs(15)) => {
                info!("watchdog tick");
            }
        }
    }

    info!("agent watchdog stopping");
}

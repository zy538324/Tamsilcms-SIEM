use std::time::Duration;

use tokio::signal;
use tracing::{info, warn};

mod compliance;
mod config;
mod edr;
mod evidence;
mod identity;
mod ipc;
mod ipc_validation;
mod policy;
mod rate_limit;
mod rmm;
mod siem;
mod update;
mod vulnerability;

use crate::compliance::run_self_audit;
use crate::config::CoreConfig;
use crate::edr::evaluate_rules;
use crate::identity::{verify_trust_bundle, AgentIdentity};
use crate::ipc::IpcServer;
use crate::policy::PolicyBundle;
use crate::rate_limit::RateLimiter;
use crate::rmm::queue_execution_request;
use crate::siem::prepare_telemetry_batch;
use crate::vulnerability::assess_exposure;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt()
        .with_env_filter("info")
        .init();

    let config = CoreConfig::from_env();
    let identity = AgentIdentity::new(config.asset_id.clone(), config.agent_id.clone());

    info!(asset_id = %identity.asset_id, agent_id = %identity.agent_id, "agent core starting");

    verify_trust_bundle();

    let policy = PolicyBundle::placeholder();
    if !policy.validate() {
        warn!("policy validation failed; refusing to start services");
        return;
    }

    let rate_limiter = RateLimiter::new(600);
    let ipc_server = IpcServer::new(config.ipc_pipe_name.clone(), config.max_payload_bytes, rate_limiter);
    ipc_server.start();

    let _compliance_results = run_self_audit();
    let _detections = evaluate_rules();
    let _execution_request = queue_execution_request();
    let _telemetry_batch = prepare_telemetry_batch();
    let _vulnerability_findings = assess_exposure();

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

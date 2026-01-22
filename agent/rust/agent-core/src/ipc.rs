use std::sync::{Arc, Mutex};

use crate::ipc_validation::{validate_payload_size, validate_schema_version, EnvelopeMeta};
use crate::rate_limit::RateLimiter;

pub const IPC_SCHEMA_VERSION: u32 = 1;

#[derive(Debug)]
pub struct IpcServer {
    pub pipe_name: String,
    pub max_payload_bytes: usize,
    pub rate_limiter: Arc<Mutex<RateLimiter>>,
}

impl IpcServer {
    pub fn new(pipe_name: String, max_payload_bytes: usize, rate_limiter: RateLimiter) -> Self {
        Self {
            pipe_name,
            max_payload_bytes,
            rate_limiter: Arc::new(Mutex::new(rate_limiter)),
        }
    }

    pub fn validate_envelope(&self, envelope: &EnvelopeMeta) -> bool {
        if !validate_schema_version(envelope.schema_version, IPC_SCHEMA_VERSION) {
            return false;
        }

        if !validate_payload_size(envelope.payload_bytes, self.max_payload_bytes) {
            return false;
        }

        let mut limiter = self.rate_limiter.lock().unwrap_or_else(|poisoned| poisoned.into_inner());
        limiter.allow()
    }

    pub fn start(&self) {
        // TODO: Bind to named pipe, accept only authorised clients, and decode protobuf messages.
        // TODO: Validate schema version, size, and required fields before routing.
    }
}

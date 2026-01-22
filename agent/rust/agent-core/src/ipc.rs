use crate::rate_limit::RateLimiter;

#[derive(Debug)]
pub struct IpcServer {
    pub pipe_name: String,
    pub max_payload_bytes: usize,
    pub rate_limiter: RateLimiter,
}

impl IpcServer {
    pub fn new(pipe_name: String, max_payload_bytes: usize, rate_limiter: RateLimiter) -> Self {
        Self {
            pipe_name,
            max_payload_bytes,
            rate_limiter,
        }
    }

    pub fn start(&self) {
        // TODO: Bind to named pipe, accept only authorised clients, and decode protobuf messages.
        // TODO: Validate schema version, size, and required fields before routing.
    }
}

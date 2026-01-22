#[derive(Debug, Clone)]
pub struct RateLimiter {
    max_per_minute: u32,
}

impl RateLimiter {
    pub fn new(max_per_minute: u32) -> Self {
        Self { max_per_minute }
    }

    pub fn allow(&self) -> bool {
        // TODO: Implement token bucket or leaky bucket logic with monotonic time.
        self.max_per_minute > 0
    }
}

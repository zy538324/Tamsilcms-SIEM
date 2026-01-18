#pragma once

namespace agent {

int ComputeHeartbeatIntervalSeconds(int base_interval_seconds,
                                    int failure_count,
                                    int max_interval_seconds);

}  // namespace agent

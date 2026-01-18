#include "agent_retry.h"

#include <algorithm>

namespace agent {

int ComputeHeartbeatIntervalSeconds(int base_interval_seconds,
                                    int failure_count,
                                    int max_interval_seconds) {
    if (base_interval_seconds <= 0) {
        return 30;
    }
    if (failure_count <= 0) {
        return base_interval_seconds;
    }
    int interval = base_interval_seconds;
    for (int i = 0; i < failure_count; ++i) {
        interval *= 2;
        if (interval >= max_interval_seconds) {
            return max_interval_seconds;
        }
    }
    return std::min(interval, max_interval_seconds);
}

}  // namespace agent

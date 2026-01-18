#include "agent_uptime.h"

namespace agent {

UptimeTracker::UptimeTracker() : start_(std::chrono::steady_clock::now()) {}

long long UptimeTracker::UptimeSeconds() const {
    auto now = std::chrono::steady_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(now - start_);
    return elapsed.count();
}

}  // namespace agent

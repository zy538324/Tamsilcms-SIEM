#pragma once

#include <chrono>

namespace agent {

class UptimeTracker {
   public:
    UptimeTracker();

    long long UptimeSeconds() const;

   private:
    std::chrono::steady_clock::time_point start_;
};

}  // namespace agent

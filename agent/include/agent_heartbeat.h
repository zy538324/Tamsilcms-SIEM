#pragma once

#include <string>

#include "agent_config.h"

namespace agent {

struct HeartbeatPayload {
    std::string json_body;
    long long timestamp;
    std::string signature;
};

class HeartbeatSender {
   public:
    explicit HeartbeatSender(const Config& config);

    bool SendHeartbeat(const HeartbeatPayload& payload, std::string* response_body) const;

   private:
    Config config_;
};

HeartbeatPayload BuildHeartbeatPayload(const Config& config,
                                       const std::string& event_id,
                                       long long uptime_seconds);

}  // namespace agent

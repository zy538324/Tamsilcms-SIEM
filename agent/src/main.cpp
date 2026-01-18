#include "agent_config.h"
#include "agent_heartbeat.h"
#include "agent_integrity.h"
#include "agent_uptime.h"
#include "agent_watchdog.h"

#include <chrono>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <thread>

namespace {
std::string GenerateEventId() {
    std::ostringstream stream;
    std::random_device device;
    std::mt19937 generator(device());
    std::uniform_int_distribution<int> dist(0, 255);
    stream << std::hex;
    for (int i = 0; i < 16; ++i) {
        stream << dist(generator);
    }
    return stream.str();
}
}  // namespace

int main() {
    try {
        agent::Config config = agent::LoadConfig();
        if (config.tenant_id.empty() || config.asset_id.empty() || config.identity_id.empty()) {
            std::cerr << "Missing canonical identifiers." << std::endl;
            return 1;
        }

        if (!agent::VerifySelfIntegrity(argv[0], config.expected_binary_hash)) {
            std::cerr << "Integrity verification failed." << std::endl;
            return 1;
        }

        agent::HeartbeatSender sender(config);
        agent::HeartbeatWatchdog watchdog(std::chrono::seconds(config.watchdog_timeout_seconds));
        agent::UptimeTracker uptime;
        watchdog.Start();

        while (true) {
            std::string event_id = GenerateEventId();
            agent::HeartbeatPayload payload =
                agent::BuildHeartbeatPayload(config, event_id, uptime.UptimeSeconds());

            std::string response;
            bool ok = sender.SendHeartbeat(payload, &response);
            if (!ok) {
                std::cerr << "Heartbeat failed." << std::endl;
            } else {
                watchdog.NotifyHeartbeat();
                std::cout << response << std::endl;
            }

            std::this_thread::sleep_for(
                std::chrono::seconds(config.heartbeat_interval_seconds));
        }
    } catch (const std::exception& ex) {
        std::cerr << "Agent error: " << ex.what() << std::endl;
        return 1;
    }
}

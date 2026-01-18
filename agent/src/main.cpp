#include "agent_config.h"
#include "agent_crash.h"
#include "agent_heartbeat.h"
#include "agent_id.h"
#include "agent_integrity.h"
#include "agent_retry.h"
#include "agent_uptime.h"
#include "agent_watchdog.h"

#include <chrono>
#include <iostream>
#include <string>
#include <thread>

int main() {
    try {
        agent::InstallCrashHandler();
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
        int failure_count = 0;
        watchdog.Start();

        while (true) {
            std::string event_id = agent::GenerateEventId();
            agent::HeartbeatPayload payload =
                agent::BuildHeartbeatPayload(config, event_id, uptime.UptimeSeconds());

            std::string response;
            bool ok = sender.SendHeartbeat(payload, &response);
            if (!ok) {
                std::cerr << "Heartbeat failed." << std::endl;
                failure_count += 1;
            } else {
                watchdog.NotifyHeartbeat();
                std::cout << response << std::endl;
                failure_count = 0;
            }

            int interval_seconds = agent::ComputeHeartbeatIntervalSeconds(
                config.heartbeat_interval_seconds,
                failure_count,
                config.max_heartbeat_interval_seconds);
            std::this_thread::sleep_for(std::chrono::seconds(interval_seconds));
        }
    } catch (const std::exception& ex) {
        std::cerr << "Agent error: " << ex.what() << std::endl;
        return 1;
    }
}

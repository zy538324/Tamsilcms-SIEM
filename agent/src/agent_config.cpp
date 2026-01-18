#include "agent_config.h"

#include <cstdlib>

namespace agent {

namespace {
std::string GetEnv(const char* key, const std::string& fallback) {
    const char* value = std::getenv(key);
    if (value == nullptr) {
        return fallback;
    }
    return std::string(value);
}
}  // namespace

Config LoadConfig() {
    Config config{};
    config.transport_url = GetEnv("AGENT_TRANSPORT_URL", "https://localhost:8081");
    config.tenant_id = GetEnv("AGENT_TENANT_ID", "");
    config.asset_id = GetEnv("AGENT_ASSET_ID", "");
    config.identity_id = GetEnv("AGENT_IDENTITY_ID", "");
    config.agent_version = GetEnv("AGENT_VERSION", "0.1.0");
    config.hostname = GetEnv("AGENT_HOSTNAME", "");
    config.os_name = GetEnv("AGENT_OS_NAME", "");
    config.trust_state = GetEnv("AGENT_TRUST_STATE", "bootstrap");
    config.shared_key = GetEnv("AGENT_HMAC_SHARED_KEY", "");
    config.cert_fingerprint = GetEnv("AGENT_CERT_FINGERPRINT", "sha256:placeholder");
    config.identity_header = GetEnv("AGENT_IDENTITY", "agent-placeholder");
    config.heartbeat_interval_seconds = std::stoi(GetEnv("AGENT_HEARTBEAT_INTERVAL", "45"));
    config.watchdog_timeout_seconds = std::stoi(GetEnv("AGENT_WATCHDOG_TIMEOUT", "120"));
    config.expected_binary_hash = GetEnv("AGENT_EXPECTED_SHA256", "");
    return config;
}

}  // namespace agent

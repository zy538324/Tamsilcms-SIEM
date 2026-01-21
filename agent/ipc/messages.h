// IPC Message Schemas for Agent Services
// All messages are typed, versioned, and strictly structured
#pragma once
#include <cstdint>
#include <array>
#include <string>
#include <vector>
#include <chrono>

namespace agent_ipc {
    struct TelemetryEnvelope {
        std::string asset_id;
        std::string agent_id;
        std::chrono::system_clock::time_point event_time;
        std::vector<uint8_t> payload;
        uint32_t version;
    };

    struct DetectionReport {
        std::string asset_id;
        std::string detection_id;
        int severity;
        std::string rule_id;
        std::chrono::system_clock::time_point detected_at;
        std::vector<uint8_t> evidence;
        uint32_t version;
    };

    struct ExecutionResult {
        std::string asset_id;
        std::string job_id;
        int exit_code;
        std::string stdout_data;
        std::string stderr_data;
        std::chrono::system_clock::time_point completed_at;
        uint32_t version;
    };

    struct EvidencePackage {
        std::string asset_id;
        std::string evidence_id;
        std::string case_id;
        std::vector<uint8_t> data;
        std::string hash;
        std::chrono::system_clock::time_point captured_at;
        uint32_t version;
    };

    struct HealthHeartbeat {
        std::string asset_id;
        std::string agent_id;
        std::chrono::system_clock::time_point timestamp;
        uint32_t version;
    };

    struct ComplianceAssertion {
        std::string asset_id;
        std::string control_id;
        bool passed;
        std::string evidence_path;
        std::chrono::system_clock::time_point evaluated_at;
        uint32_t version;
    };
}

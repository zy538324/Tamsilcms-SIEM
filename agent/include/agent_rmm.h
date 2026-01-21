// agent_rmm.h
// RMM telemetry models and client for patch, script, remote session, and evidence reporting.
#pragma once

#include <chrono>
#include <string>
#include <vector>

#include "agent_config.h"

namespace agent_rmm {

struct RmmConfigProfile {
    std::string profile_id;
    std::string name;
    std::string version;
    std::string status;
    std::string checksum;
    std::chrono::system_clock::time_point applied_at;
};

struct RmmPatchCatalogItem {
    std::string patch_id;
    std::string title;
    std::string vendor;
    std::string severity;
    std::string kb;
    std::string release_date;
};

struct RmmPatchJob {
    std::string job_id;
    std::string patch_id;
    std::string status;
    std::string result;
    std::chrono::system_clock::time_point scheduled_at;
    std::chrono::system_clock::time_point applied_at;
};

struct RmmScriptResult {
    std::string job_id;
    std::string script_type;
    int exit_code;
    std::string stdout_summary;
    std::string stderr_summary;
    std::chrono::system_clock::time_point started_at;
    std::chrono::system_clock::time_point completed_at;
};

struct RmmRemoteSession {
    std::string session_id;
    std::string operator_id;
    std::string status;
    std::chrono::system_clock::time_point started_at;
    std::chrono::system_clock::time_point ended_at;
};

struct RmmEvidenceRecord {
    std::string evidence_id;
    std::string evidence_type;
    std::string hash;
    std::string storage_uri;
    std::string related_id;
    std::chrono::system_clock::time_point captured_at;
};

struct RmmDeviceInventory {
    std::string hostname;
    std::string os_name;
    std::string os_version;
    std::string serial_number;
    std::chrono::system_clock::time_point collected_at;
};

class RmmTelemetryClient {
public:
    explicit RmmTelemetryClient(const agent::Config& config);

    bool SendConfigProfile(const RmmConfigProfile& profile) const;
    bool SendPatchCatalog(const std::vector<RmmPatchCatalogItem>& items) const;
    bool SendPatchJob(const RmmPatchJob& job) const;
    bool SendScriptResult(const RmmScriptResult& result) const;
    bool SendRemoteSession(const RmmRemoteSession& session) const;
    bool SendEvidenceRecord(const RmmEvidenceRecord& record) const;
    bool SendDeviceInventory(const RmmDeviceInventory& inventory) const;

private:
    agent::Config config_;
};

}  // namespace agent_rmm

// agent_rmm.cpp
// RMM telemetry emission using lightweight JSON and libcurl.
#include "agent_rmm.h"

#include <curl/curl.h>

#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>

namespace agent_rmm {

namespace {
std::string JsonEscape(const std::string& input) {
    std::ostringstream escaped;
    for (char c : input) {
        switch (c) {
            case '"':
                escaped << "\\\"";
                break;
            case '\\':
                escaped << "\\\\";
                break;
            case '\n':
                escaped << "\\n";
                break;
            case '\r':
                escaped << "\\r";
                break;
            case '\t':
                escaped << "\\t";
                break;
            default:
                escaped << c;
                break;
        }
    }
    return escaped.str();
}

std::string GenerateCorrelationId() {
    std::random_device random_device;
    std::mt19937 rng(random_device());
    std::uniform_int_distribution<int> dist(0, 15);
    std::ostringstream stream;
    for (int i = 0; i < 32; ++i) {
        stream << std::hex << dist(rng);
    }
    return stream.str();
}

std::string BuildIsoTimestamp(const std::chrono::system_clock::time_point& time_point) {
    auto now_time = std::chrono::system_clock::to_time_t(time_point);
    std::tm utc_tm{};
#if defined(_WIN32)
    gmtime_s(&utc_tm, &now_time);
#else
    gmtime_r(&now_time, &utc_tm);
#endif
    std::ostringstream stream;
    stream << std::put_time(&utc_tm, "%FT%TZ");
    return stream.str();
}

bool PostJson(const std::string& url, const std::string& body) {
    CURL* curl = curl_easy_init();
    if (!curl) {
        return false;
    }

    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, "X-Forwarded-Proto: https");

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body.c_str());

    CURLcode result = curl_easy_perform(curl);
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);

    return result == CURLE_OK;
}

std::string BuildEndpoint(const agent::Config& config, const std::string& path) {
    return config.transport_url + "/rmm" + path;
}

void AppendString(std::ostringstream& stream, const std::string& key, const std::string& value, bool trailing_comma = true) {
    stream << "\"" << key << "\":\"" << JsonEscape(value) << "\"";
    if (trailing_comma) {
        stream << ",";
    }
}

void AppendInt(std::ostringstream& stream, const std::string& key, int value, bool trailing_comma = true) {
    stream << "\"" << key << "\":" << value;
    if (trailing_comma) {
        stream << ",";
    }
}

void LogOutcome(const std::string& category, const std::string& correlation_id, bool ok) {
    std::cout << "[RMM] " << category << " correlation_id=" << correlation_id
              << " status=" << (ok ? "success" : "failed") << std::endl;
}
}  // namespace

RmmTelemetryClient::RmmTelemetryClient(const agent::Config& config) : config_(config) {}

bool RmmTelemetryClient::SendConfigProfile(const RmmConfigProfile& profile) const {
    std::string correlation_id = GenerateCorrelationId();
    std::ostringstream payload;
    payload << '{';
    AppendString(payload, "name", profile.name);
    AppendString(payload, "profile_type", profile.profile_type);
    AppendString(payload, "description", profile.description, false);
    payload << '}';

    bool ok = PostJson(BuildEndpoint(config_, "/configuration_profiles"), payload.str());
    LogOutcome("config_profile", correlation_id, ok);
    return ok;
}

bool RmmTelemetryClient::SendPatchCatalog(const std::vector<RmmPatchCatalogItem>& items) const {
    std::string correlation_id = GenerateCorrelationId();
    bool ok = true;
    for (const auto& item : items) {
        std::ostringstream payload;
        payload << '{';
        AppendString(payload, "vendor", item.vendor);
        AppendString(payload, "product", item.product);
        AppendString(payload, "patch_id", item.patch_id);
        AppendString(payload, "release_date", item.release_date);
        AppendInt(payload, "severity", item.severity, false);
        payload << '}';

        ok = PostJson(BuildEndpoint(config_, "/patch_catalog"), payload.str()) && ok;
    }
    LogOutcome("patch_catalog", correlation_id, ok);
    return ok;
}

bool RmmTelemetryClient::SendPatchJob(const RmmPatchJob& job) const {
    std::string correlation_id = GenerateCorrelationId();
    std::ostringstream payload;
    payload << '{';
    AppendString(payload, "psa_case_id", job.psa_case_id);
    AppendString(payload, "scheduled_for", job.scheduled_for);
    AppendString(payload, "reboot_policy", job.reboot_policy, false);
    payload << '}';

    bool ok = PostJson(BuildEndpoint(config_, "/patch_jobs"), payload.str());
    LogOutcome("patch_job", correlation_id, ok);
    return ok;
}

bool RmmTelemetryClient::SendScriptResult(const RmmScriptResult& result) const {
    std::string correlation_id = GenerateCorrelationId();
    std::ostringstream payload;
    payload << '{';
    AppendString(payload, "job_id", result.job_id);
    AppendString(payload, "stdout", result.stdout_data);
    AppendString(payload, "stderr", result.stderr_data);
    AppendInt(payload, "exit_code", result.exit_code);
    AppendString(payload, "hash", result.hash, false);
    payload << '}';

    bool ok = PostJson(BuildEndpoint(config_, "/script_results"), payload.str());
    LogOutcome("script_result", correlation_id, ok);
    return ok;
}

bool RmmTelemetryClient::SendRemoteSession(const RmmRemoteSession& session) const {
    std::string correlation_id = GenerateCorrelationId();
    std::ostringstream payload;
    payload << '{';
    AppendString(payload, "asset_id", session.asset_id);
    AppendString(payload, "initiated_by", session.initiated_by);
    AppendString(payload, "session_type", session.session_type, false);
    payload << '}';

    bool ok = PostJson(BuildEndpoint(config_, "/remote_sessions"), payload.str());
    LogOutcome("remote_session", correlation_id, ok);
    return ok;
}

bool RmmTelemetryClient::SendEvidenceRecord(const RmmEvidenceRecord& record) const {
    std::string correlation_id = GenerateCorrelationId();
    std::ostringstream payload;
    payload << '{';
    AppendString(payload, "asset_id", record.asset_id);
    AppendString(payload, "evidence_type", record.evidence_type);
    AppendString(payload, "related_entity", record.related_entity);
    AppendString(payload, "related_id", record.related_id);
    AppendString(payload, "hash", record.hash);
    AppendString(payload, "storage_uri", record.storage_uri);
    payload << '}';

    bool ok = PostJson(BuildEndpoint(config_, "/evidence"), payload.str());
    LogOutcome("evidence", correlation_id, ok);
    return ok;
}

bool RmmTelemetryClient::SendDeviceInventory(const RmmDeviceInventory& inventory) const {
    std::string correlation_id = GenerateCorrelationId();
    std::ostringstream payload;
    payload << '{';
    AppendString(payload, "asset_id", inventory.asset_id);
    AppendString(payload, "hostname", inventory.hostname);
    AppendString(payload, "os_name", inventory.os_name);
    AppendString(payload, "os_version", inventory.os_version);
    AppendString(payload, "serial_number", inventory.serial_number);
    AppendString(payload, "collected_at", BuildIsoTimestamp(inventory.collected_at), false);
    payload << '}';

    bool ok = PostJson(BuildEndpoint(config_, "/device_inventory"), payload.str());
    LogOutcome("device_inventory", correlation_id, ok);
    return ok;
}

}  // namespace agent_rmm

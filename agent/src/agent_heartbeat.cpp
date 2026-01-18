#include "agent_heartbeat.h"

#include <curl/curl.h>

#include <chrono>
#include <iomanip>
#include <sstream>
#include <string>

#include "agent_signing.h"

namespace agent {

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

std::string BuildTimestampIso8601() {
    auto now = std::chrono::system_clock::now();
    auto now_time = std::chrono::system_clock::to_time_t(now);
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

size_t WriteCallback(char* ptr, size_t size, size_t nmemb, void* userdata) {
    auto* output = static_cast<std::string*>(userdata);
    output->append(ptr, size * nmemb);
    return size * nmemb;
}
}  // namespace

HeartbeatSender::HeartbeatSender(const Config& config) : config_(config) {}

HeartbeatPayload BuildHeartbeatPayload(const Config& config, const std::string& event_id) {
    std::ostringstream payload;
    payload << '{'
            << "\"tenant_id\":\"" << JsonEscape(config.tenant_id) << "\"," 
            << "\"asset_id\":\"" << JsonEscape(config.asset_id) << "\"," 
            << "\"identity_id\":\"" << JsonEscape(config.identity_id) << "\"," 
            << "\"event_id\":\"" << JsonEscape(event_id) << "\"," 
            << "\"agent_version\":\"" << JsonEscape(config.agent_version) << "\"," 
            << "\"hostname\":\"" << JsonEscape(config.hostname) << "\"," 
            << "\"os\":\"" << JsonEscape(config.os_name) << "\"," 
            << "\"uptime_seconds\":" << 0 << ','
            << "\"trust_state\":\"" << JsonEscape(config.trust_state) << "\"," 
            << "\"sent_at\":\"" << BuildTimestampIso8601() << "\"";
    payload << '}';

    long long timestamp = std::chrono::duration_cast<std::chrono::seconds>(
                               std::chrono::system_clock::now().time_since_epoch())
                               .count();
    std::string signature = SignPayload(config.shared_key, payload.str(), timestamp);

    return HeartbeatPayload{payload.str(), timestamp, signature};
}

bool HeartbeatSender::SendHeartbeat(const HeartbeatPayload& payload,
                                    std::string* response_body) const {
    CURL* curl = curl_easy_init();
    if (!curl) {
        return false;
    }

    std::string url = config_.transport_url + "/mtls/hello";
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, ("X-Request-Signature: " + payload.signature).c_str());
    headers = curl_slist_append(headers, ("X-Request-Timestamp: " + std::to_string(payload.timestamp)).c_str());
    headers = curl_slist_append(headers, ("X-Client-Identity: " + config_.identity_header).c_str());
    headers = curl_slist_append(headers, ("X-Client-Cert-Sha256: " + config_.cert_fingerprint).c_str());
    headers = curl_slist_append(headers, "X-Client-MTLS: success");
    headers = curl_slist_append(headers, "X-Forwarded-Proto: https");
    headers = curl_slist_append(headers, "Content-Type: application/json");

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload.json_body.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, response_body);

    CURLcode result = curl_easy_perform(curl);
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);

    return result == CURLE_OK;
}

}  // namespace agent

#include "agent_config.h"
#include "agent_signing.h"

#include <curl/curl.h>

#include <chrono>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

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

std::string BuildPayload(const agent::Config& config, const std::string& event_id) {
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
            << "\"sent_at\":\"";

    auto now = std::chrono::system_clock::now();
    auto now_time = std::chrono::system_clock::to_time_t(now);
    std::tm utc_tm{};
#if defined(_WIN32)
    gmtime_s(&utc_tm, &now_time);
#else
    gmtime_r(&now_time, &utc_tm);
#endif
    payload << std::put_time(&utc_tm, "%FT%TZ") << "\"";
    payload << '}';
    return payload.str();
}

std::string GenerateEventId() {
    std::ostringstream stream;
    stream << std::hex;
    for (int i = 0; i < 16; ++i) {
        stream << (rand() % 256);
    }
    return stream.str();
}

long long CurrentTimestamp() {
    auto now = std::chrono::system_clock::now();
    auto seconds = std::chrono::duration_cast<std::chrono::seconds>(now.time_since_epoch());
    return seconds.count();
}

size_t WriteCallback(char* ptr, size_t size, size_t nmemb, void* userdata) {
    auto* output = static_cast<std::string*>(userdata);
    output->append(ptr, size * nmemb);
    return size * nmemb;
}
}  // namespace

int main() {
    try {
        agent::Config config = agent::LoadConfig();
        if (config.tenant_id.empty() || config.asset_id.empty() || config.identity_id.empty()) {
            std::cerr << "Missing canonical identifiers." << std::endl;
            return 1;
        }

        std::string event_id = GenerateEventId();
        std::string payload = BuildPayload(config, event_id);
        long long timestamp = CurrentTimestamp();
        std::string signature = agent::SignPayload(config.shared_key, payload, timestamp);

        CURL* curl = curl_easy_init();
        if (!curl) {
            throw std::runtime_error("curl_initialisation_failed");
        }

        std::string response;
        std::string url = config.transport_url + "/mtls/hello";

        struct curl_slist* headers = nullptr;
        headers = curl_slist_append(headers, ("X-Request-Signature: " + signature).c_str());
        headers = curl_slist_append(headers, ("X-Request-Timestamp: " + std::to_string(timestamp)).c_str());
        headers = curl_slist_append(headers, ("X-Client-Identity: " + config.identity_header).c_str());
        headers = curl_slist_append(headers, ("X-Client-Cert-Sha256: " + config.cert_fingerprint).c_str());
        headers = curl_slist_append(headers, "X-Client-MTLS: success");
        headers = curl_slist_append(headers, "X-Forwarded-Proto: https");
        headers = curl_slist_append(headers, "Content-Type: application/json");

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        CURLcode result = curl_easy_perform(curl);
        if (result != CURLE_OK) {
            std::cerr << "Transport call failed: " << curl_easy_strerror(result) << std::endl;
            curl_slist_free_all(headers);
            curl_easy_cleanup(curl);
            return 1;
        }

        long status_code = 0;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &status_code);

        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);

        std::cout << "Status: " << status_code << "\n" << response << std::endl;
        return status_code >= 400 ? 1 : 0;
    } catch (const std::exception& ex) {
        std::cerr << "Agent error: " << ex.what() << std::endl;
        return 1;
    }
}

#include "agent_inventory.h"

#include <curl/curl.h>

#include <chrono>
#include <iomanip>
#include <sstream>
#include <string>

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
}  // namespace

bool SendInventorySnapshot(const Config& config) {
    std::string collected_at = BuildTimestampIso8601();

    std::ostringstream hardware;
    hardware << '{'
             << "\"tenant_id\":\"" << JsonEscape(config.tenant_id) << "\"," 
             << "\"asset_id\":\"" << JsonEscape(config.asset_id) << "\"," 
             << "\"collected_at\":\"" << collected_at << "\"," 
             << "\"manufacturer\":null,"
             << "\"model\":null,"
             << "\"serial_number\":null,"
             << "\"cpu_model\":null,"
             << "\"cpu_cores\":null,"
             << "\"memory_mb\":null,"
             << "\"storage_gb\":null"
             << '}';

    std::ostringstream os;
    os << '{'
       << "\"tenant_id\":\"" << JsonEscape(config.tenant_id) << "\"," 
       << "\"asset_id\":\"" << JsonEscape(config.asset_id) << "\"," 
       << "\"collected_at\":\"" << collected_at << "\"," 
       << "\"os_name\":\"" << JsonEscape(config.os_name) << "\"," 
       << "\"os_version\":\"unknown\"," 
       << "\"kernel_version\":null,"
       << "\"architecture\":null,"
       << "\"install_date\":null"
       << '}';

    bool hardware_ok = PostJson(config.ingestion_url + "/inventory/hardware", hardware.str());
    bool os_ok = PostJson(config.ingestion_url + "/inventory/os", os.str());

    return hardware_ok && os_ok;
}

}  // namespace agent

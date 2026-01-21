// uplink.cpp
// Minimal HTTPS uploader using libcurl to POST evidence package files
#include "../../include/agent_uplink.h"
#include <curl/curl.h>
#include <filesystem>
#include <iostream>
#include <string>
#include <fstream>

static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    size_t realsize = size * nmemb;
    std::string* mem = static_cast<std::string*>(userp);
    mem->append(static_cast<char*>(contents), realsize);
    return realsize;
}

namespace fs = std::filesystem;

// Default to local PSA intake endpoint for dev; override via TAMSIL_UPLINK_ENDPOINT.
static std::string g_endpoint = "http://localhost:8001/intake";
static std::string g_client_cert;
static std::string g_client_key;
static std::string g_api_key;

namespace agent_uplink {

void SetUplinkEndpoint(const std::string& url) { g_endpoint = url; }

void SetClientCertAndKey(const std::string& cert_path, const std::string& key_path) {
    g_client_cert = cert_path;
    g_client_key = key_path;
}

void SetApiKey(const std::string& api_key) { g_api_key = api_key; }

bool UploadEvidencePackage(const std::string& package_dir) {
    if (!fs::exists(package_dir) || !fs::is_directory(package_dir)) {
        std::cerr << "Package dir missing: " << package_dir << std::endl;
        return false;
    }

    // Allow overriding endpoint via env var for local testing
    if (const char* env = std::getenv("TAMSIL_UPLINK_ENDPOINT")) {
        g_endpoint = std::string(env);
    }
    // Optional API key override
    if (const char* aenv = std::getenv("TAMSIL_UPLINK_API_KEY")) {
        g_api_key = std::string(aenv);
    }

    CURL* curl = curl_easy_init();
    if (!curl) {
        std::cerr << "curl init failed" << std::endl;
        return false;
    }

    curl_easy_setopt(curl, CURLOPT_URL, g_endpoint.c_str());
    curl_easy_setopt(curl, CURLOPT_USERAGENT, "TamsilAgent/1.0");

    if (!g_client_cert.empty() && !g_client_key.empty()) {
        curl_easy_setopt(curl, CURLOPT_SSLCERT, g_client_cert.c_str());
        curl_easy_setopt(curl, CURLOPT_SSLKEY, g_client_key.c_str());
    }

    // Build JSON intake payload from package metadata
    // Look for metadata.txt
    std::string evidence_id;
    std::string source;
    std::string type;
    std::string related_id;
    std::string hash;
    std::string captured_at;
    for (auto &p : fs::directory_iterator(package_dir)) {
        if (fs::is_regular_file(p.path()) && p.path().filename() == "metadata.txt") {
            std::ifstream m(p.path());
            std::string line;
            while (std::getline(m, line)) {
                auto pos = line.find('=');
                if (pos == std::string::npos) continue;
                std::string k = line.substr(0, pos);
                std::string v = line.substr(pos + 1);
                if (k == "evidence_id") evidence_id = v;
                else if (k == "source") source = v;
                else if (k == "type") type = v;
                else if (k == "related_id") related_id = v;
                else if (k == "hash") hash = v;
                else if (k == "captured_at") captured_at = v;
            }
            break;
        }
    }

    if (evidence_id.empty()) {
        std::cerr << "UploadEvidencePackage: missing metadata.evidence_id\n";
        curl_easy_cleanup(curl);
        return false;
    }

    // Minimal TicketIntakeRequest JSON
    std::string asset_id = source.empty() ? "agent-local" : source;
    // Escape backslashes in package_dir for JSON
    std::string json_package_dir = package_dir;
    for (size_t pos = 0; (pos = json_package_dir.find("\\", pos)) != std::string::npos; pos += 2) {
        json_package_dir.replace(pos, 1, "\\\\");
    }
    std::string json = "{";
    json += "\"tenant_id\":\"tamsil-agent\",";
    json += "\"asset_id\":\"" + asset_id + "\",";
    json += "\"source_type\":\"finding\",";
    json += "\"source_reference_id\":\"" + evidence_id + "\",";
    json += "\"risk_score\":50.0,";
    json += "\"asset_criticality\":\"medium\",";
    json += "\"exposure_level\":\"internal\",";
    json += "\"time_sensitivity\":\"none\",";
    json += "\"system_recommendation\":null,";
    json += "\"evidence\":[{";
    json += "\"linked_object_type\":\"finding\",";
    json += "\"linked_object_id\":\"" + related_id + "\",";
    json += "\"immutable_reference\":\"" + evidence_id + "\",";
    json += "\"payload\":{";
    json += "\"hash\":\"" + hash + "\",";
    // include stored_uri as the package path
    json += "\"stored_uri\":\"file://" + json_package_dir + "\"";
    json += "}}]}";
    // Debug: print JSON payload before sending
    std::cerr << "Intake JSON payload:\n" << json << std::endl;

    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    if (!g_api_key.empty()) {
        std::string h = std::string("X-API-Key: ") + g_api_key;
        headers = curl_slist_append(headers, h.c_str());
    }

    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json.c_str());
    curl_easy_setopt(curl, CURLOPT_VERBOSE, 0L);

    std::string response_body;
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_body);

    CURLcode res = curl_easy_perform(curl);
    long http_code = 0;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
    bool ok = (res == CURLE_OK && (http_code >= 200 && http_code < 300));

    if (res != CURLE_OK) {
        std::cerr << "curl_easy_perform failed: " << curl_easy_strerror(res) << std::endl;
    }
    std::cerr << "HTTP response code: " << http_code << "\n";
    if (!response_body.empty()) {
        std::cerr << "Response body: " << response_body << "\n";
    }

    if (headers) curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
    return ok;
}

} // namespace agent_uplink

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
static std::string g_rmm_endpoint = "http://localhost:8020/rmm/evidence";
static std::string g_psa_patch_endpoint = "http://localhost:8001/patch-results";

namespace agent_uplink {

void SetUplinkEndpoint(const std::string& url) { g_endpoint = url; }
void SetRmmEndpoint(const std::string& url) { g_rmm_endpoint = url; }
void SetPsaPatchEndpoint(const std::string& url) { g_psa_patch_endpoint = url; }

void SetClientCertAndKey(const std::string& cert_path, const std::string& key_path) {
    g_client_cert = cert_path;
    g_client_key = key_path;
}

void SetApiKey(const std::string& api_key) { g_api_key = api_key; }

namespace {
bool PostJson(
    const std::string& endpoint,
    const std::string& json,
    const std::string& api_key,
    const std::string& client_cert,
    const std::string& client_key
) {
    CURL* curl = curl_easy_init();
    if (!curl) {
        std::cerr << "curl init failed" << std::endl;
        return false;
    }

    curl_easy_setopt(curl, CURLOPT_URL, endpoint.c_str());
    curl_easy_setopt(curl, CURLOPT_USERAGENT, "TamsilAgent/1.0");

    if (!client_cert.empty() && !client_key.empty()) {
        curl_easy_setopt(curl, CURLOPT_SSLCERT, client_cert.c_str());
        curl_easy_setopt(curl, CURLOPT_SSLKEY, client_key.c_str());
    }

    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, "X-Forwarded-Proto: https");
    if (!api_key.empty()) {
        std::string h = std::string("X-API-Key: ") + api_key;
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
} // namespace

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

    // Build JSON intake payload from package metadata
    // Look for metadata.txt
    std::string evidence_id;
    std::string source;
    std::string type;
    std::string related_id;
    std::string hash;
    std::string captured_at;
    std::string tenant_id;
    std::string asset_id;
    std::string storage_uri;
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
                else if (k == "tenant_id") tenant_id = v;
                else if (k == "asset_id") asset_id = v;
                else if (k == "storage_uri") storage_uri = v;
            }
            break;
        }
    }

    if (evidence_id.empty()) {
        std::cerr << "UploadEvidencePackage: missing metadata.evidence_id\n";
        return false;
    }

    // Minimal TicketIntakeRequest JSON
    if (asset_id.empty()) {
        asset_id = source.empty() ? "agent-local" : source;
    }
    if (asset_id.size() < 3) {
        asset_id = "agent-local";
    }
    if (related_id.empty()) {
        related_id = evidence_id;
    }
    // Escape backslashes in package_dir for JSON
    std::string json_package_dir = package_dir;
    for (size_t pos = 0; (pos = json_package_dir.find("\\", pos)) != std::string::npos; pos += 2) {
        json_package_dir.replace(pos, 1, "\\\\");
    }
    std::string json = "{";
    if (tenant_id.empty() || tenant_id.size() < 3) {
        tenant_id = "tamsil-agent";
    }
    json += "\"tenant_id\":\"" + tenant_id + "\",";
    json += "\"asset_id\":\"" + asset_id + "\",";
    json += "\"source_type\":\"finding\",";
    json += "\"source_reference_id\":\"" + evidence_id + "\",";
    json += "\"risk_score\":50.0,";
    json += "\"asset_criticality\":\"medium\",";
    json += "\"exposure_level\":\"internal\",";
    json += "\"time_sensitivity\":\"none\",";
    json += "\"system_recommendation\":null,";
    json += "\"evidence\":[{";
    std::string linked_object_id = related_id;
    if (linked_object_id.size() < 3) {
        linked_object_id = evidence_id;
    }
    if (linked_object_id.size() < 3) {
        linked_object_id = "ev-" + evidence_id;
    }
    std::string immutable_reference = evidence_id.size() < 3 ? "ev-" + evidence_id : evidence_id;
    json += "\"linked_object_type\":\"finding\",";
    json += "\"linked_object_id\":\"" + linked_object_id + "\",";
    json += "\"immutable_reference\":\"" + immutable_reference + "\",";
    json += "\"payload\":{";
    json += "\"hash\":\"" + hash + "\",";
    // include stored_uri as the package path
    if (storage_uri.empty()) {
        storage_uri = "file://" + json_package_dir;
    }
    json += "\"stored_uri\":\"" + storage_uri + "\"";
    json += "}}]}";
    // Debug: print JSON payload before sending
    std::cerr << "Intake JSON payload:\n" << json << std::endl;

    return PostJson(g_endpoint, json, g_api_key, g_client_cert, g_client_key);
}

bool UploadRmmEvidence(const std::string& package_dir) {
    if (!fs::exists(package_dir) || !fs::is_directory(package_dir)) {
        std::cerr << "Package dir missing: " << package_dir << std::endl;
        return false;
    }

    if (const char* env = std::getenv("TAMSIL_RMM_ENDPOINT")) {
        g_rmm_endpoint = std::string(env);
    }
    if (const char* aenv = std::getenv("TAMSIL_UPLINK_API_KEY")) {
        g_api_key = std::string(aenv);
    }

    std::string evidence_id;
    std::string source;
    std::string related_id;
    std::string hash;
    std::string tenant_id;
    std::string asset_id;
    std::string storage_uri;
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
                else if (k == "related_id") related_id = v;
                else if (k == "hash") hash = v;
                else if (k == "tenant_id") tenant_id = v;
                else if (k == "asset_id") asset_id = v;
                else if (k == "storage_uri") storage_uri = v;
            }
            break;
        }
    }

    if (evidence_id.empty()) {
        std::cerr << "UploadRmmEvidence: missing metadata.evidence_id\n";
        return false;
    }

    if (asset_id.empty()) {
        asset_id = source.empty() ? "agent-local" : source;
    }
    if (related_id.empty()) {
        related_id = evidence_id;
    }

    std::string json_package_dir = package_dir;
    for (size_t pos = 0; (pos = json_package_dir.find("\\", pos)) != std::string::npos; pos += 2) {
        json_package_dir.replace(pos, 1, "\\\\");
    }

    std::string json = "{";
    if (!tenant_id.empty()) {
        json += "\"tenant_id\":\"" + tenant_id + "\",";
    }
    json += "\"asset_id\":\"" + asset_id + "\",";
    json += "\"evidence_type\":\"agent_evidence\",";
    json += "\"related_entity\":\"agent\",";
    json += "\"related_id\":\"" + related_id + "\",";
    if (storage_uri.empty()) {
        storage_uri = "file://" + json_package_dir;
    }
    json += "\"storage_uri\":\"" + storage_uri + "\",";
    json += "\"hash\":\"" + hash + "\"";
    json += "}";
    std::cerr << "RMM evidence JSON payload:\n" << json << std::endl;

    return PostJson(g_rmm_endpoint, json, g_api_key, g_client_cert, g_client_key);
}

bool UploadPatchResult(const std::string& payload_json) {
    if (const char* env = std::getenv("TAMSIL_PSA_PATCH_ENDPOINT")) {
        g_psa_patch_endpoint = std::string(env);
    }
    if (const char* aenv = std::getenv("TAMSIL_UPLINK_API_KEY")) {
        g_api_key = std::string(aenv);
    }
    return PostJson(g_psa_patch_endpoint, payload_json, g_api_key, g_client_cert, g_client_key);
}

} // namespace agent_uplink

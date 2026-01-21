// agent_uplink.h
// Simple uplink client to POST evidence packages to PSA over HTTPS using libcurl
#pragma once
#include <string>

namespace agent_uplink {
    // Configure the uplink endpoint (e.g., "https://psa.example.com/api/evidence")
    void SetUplinkEndpoint(const std::string& url);
    // Configure the RMM evidence endpoint (e.g., "https://rmm.example.com/rmm/evidence")
    void SetRmmEndpoint(const std::string& url);
    // Configure the PSA patch result endpoint (e.g., "https://psa.example.com/api/patch-results")
    void SetPsaPatchEndpoint(const std::string& url);

    // Upload a prepared evidence package directory. Returns true on success.
    bool UploadEvidencePackage(const std::string& package_dir);

    // Upload a prepared evidence package directory to the RMM evidence endpoint.
    bool UploadRmmEvidence(const std::string& package_dir);

    // Upload a patch job result to the PSA command channel endpoint.
    bool UploadPatchResult(const std::string& payload_json);

    // Set path to client cert/key for mutual TLS (optional)
    void SetClientCertAndKey(const std::string& cert_path, const std::string& key_path);
    
    // Set API key to include as X-API-Key header
    void SetApiKey(const std::string& api_key);
}

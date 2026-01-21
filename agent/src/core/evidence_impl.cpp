// evidence_impl.cpp
// EvidenceBroker implementation: hashing, signing (OpenSSL), packaging, upload stub
#include "../../include/agent_evidence.h"
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include <fstream>
#include <iostream>
#include <filesystem>
#include <mutex>
#include "../../include/agent_uplink.h"
#include "../../include/agent_config.h"

namespace fs = std::filesystem;

static std::mutex g_evidence_mutex;

namespace agent_evidence {

static std::string ComputeSHA256Hex(const std::string& path) {
    std::ifstream ifs(path, std::ios::binary);
    if (!ifs) return "";

    EVP_MD_CTX* mdctx = EVP_MD_CTX_new();
    const EVP_MD* md = EVP_sha256();
    unsigned char md_value[EVP_MAX_MD_SIZE];
    unsigned int md_len = 0;

    EVP_DigestInit_ex(mdctx, md, nullptr);
    char buf[4096];
    while (ifs.good()) {
        ifs.read(buf, sizeof(buf));
        std::streamsize r = ifs.gcount();
        if (r > 0) EVP_DigestUpdate(mdctx, buf, (size_t)r);
    }
    EVP_DigestFinal_ex(mdctx, md_value, &md_len);
    EVP_MD_CTX_free(mdctx);

    // hex
    std::string hex; hex.reserve(md_len*2);
    static const char* hexchars = "0123456789abcdef";
    for (unsigned int i=0;i<md_len;i++){
        unsigned char v = md_value[i];
        hex.push_back(hexchars[(v>>4)&0xF]);
        hex.push_back(hexchars[v&0xF]);
    }
    return hex;
}

void EvidenceBroker::AddEvidence(const EvidenceItem& item) {
    std::lock_guard<std::mutex> lk(g_evidence_mutex);
    evidence_store_.push_back(item);
}

void EvidenceBroker::SealEvidence(const std::string& evidence_id) {
    std::lock_guard<std::mutex> lk(g_evidence_mutex);
    for (auto &it : evidence_store_) {
        if (it.evidence_id == evidence_id) {
            if (!fs::exists(it.storage_path)) {
                std::cerr << "Evidence file missing: " << it.storage_path << std::endl;
                return;
            }
            it.hash = ComputeSHA256Hex(it.storage_path);
            // Signing the hash with a local key would happen here. Placeholder.
            std::cout << "Sealed evidence " << it.evidence_id << " hash=" << it.hash << std::endl;
            return;
        }
    }
    std::cerr << "SealEvidence: id not found " << evidence_id << std::endl;
}

void EvidenceBroker::UploadEvidence(const std::string& evidence_id) {
    std::lock_guard<std::mutex> lk(g_evidence_mutex);
    for (auto &it : evidence_store_) {
        if (it.evidence_id == evidence_id) {
            agent::Config config = agent::LoadConfig();
            // Package evidence: create a tar/zip or simple folder with metadata
            fs::path outdir = fs::current_path() / "evidence_packages" / it.evidence_id;
            fs::create_directories(outdir);
            try {
                fs::path src(it.storage_path);
                if (fs::exists(src)) {
                    fs::copy_file(src, outdir / src.filename(), fs::copy_options::overwrite_existing);
                }
                // write metadata
                std::ofstream meta(outdir / "metadata.txt");
                meta << "tenant_id=" << config.tenant_id << "\n";
                meta << "asset_id=" << config.asset_id << "\n";
                meta << "evidence_id=" << it.evidence_id << "\n";
                meta << "source=" << it.source << "\n";
                meta << "type=" << it.type << "\n";
                meta << "related_id=" << it.related_id << "\n";
                meta << "hash=" << it.hash << "\n";
                meta << "storage_uri=" << "file://" << outdir.string() << "\n";
                meta << "captured_at=" << std::chrono::duration_cast<std::chrono::seconds>(it.captured_at.time_since_epoch()).count() << "\n";
                meta.close();
            } catch(const std::exception &e) {
                std::cerr << "UploadEvidence packaging failed: " << e.what() << std::endl;
                return;
            }

            // Upload via uplink
            std::string packagedir = (fs::current_path() / "evidence_packages" / it.evidence_id).string();
            bool ok = agent_uplink::UploadEvidencePackage(packagedir);
            if (ok) std::cout << "Evidence package uploaded: " << packagedir << std::endl;
            else std::cerr << "Evidence upload failed for: " << packagedir << std::endl;

            bool rmm_ok = agent_uplink::UploadRmmEvidence(packagedir);
            if (rmm_ok) std::cout << "RMM evidence uploaded: " << packagedir << std::endl;
            else std::cerr << "RMM evidence upload failed for: " << packagedir << std::endl;
            return;
        }
    }
    std::cerr << "UploadEvidence: id not found " << evidence_id << std::endl;
}

std::vector<EvidenceItem> EvidenceBroker::ListEvidence() const {
    std::lock_guard<std::mutex> lk(g_evidence_mutex);
    return evidence_store_;
}

}

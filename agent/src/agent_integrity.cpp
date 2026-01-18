#include "agent_integrity.h"

#include <openssl/evp.h>

#include <fstream>
#include <iomanip>
#include <sstream>
#include <vector>

namespace agent {

namespace {
std::string ToHex(const unsigned char* data, unsigned int length) {
    std::ostringstream stream;
    stream << std::hex << std::setfill('0');
    for (unsigned int i = 0; i < length; ++i) {
        stream << std::setw(2) << static_cast<int>(data[i]);
    }
    return stream.str();
}
}  // namespace

std::string ComputeSha256File(const std::string& path) {
    std::ifstream file(path, std::ios::binary);
    if (!file.is_open()) {
        return {};
    }

    EVP_MD_CTX* context = EVP_MD_CTX_new();
    EVP_DigestInit_ex(context, EVP_sha256(), nullptr);

    std::vector<char> buffer(4096);
    while (file.read(buffer.data(), buffer.size()) || file.gcount() > 0) {
        EVP_DigestUpdate(context, buffer.data(), static_cast<size_t>(file.gcount()));
    }

    unsigned char hash[EVP_MAX_MD_SIZE];
    unsigned int length = 0;
    EVP_DigestFinal_ex(context, hash, &length);
    EVP_MD_CTX_free(context);

    return ToHex(hash, length);
}

bool VerifySelfIntegrity(const std::string& executable_path,
                         const std::string& expected_hash) {
    if (expected_hash.empty()) {
        return true;
    }
    std::string actual_hash = ComputeSha256File(executable_path);
    return !actual_hash.empty() && actual_hash == expected_hash;
}

}  // namespace agent

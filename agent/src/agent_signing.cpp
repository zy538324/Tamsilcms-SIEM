#include "agent_signing.h"

#include <openssl/evp.h>
#include <openssl/hmac.h>

#include <sstream>
#include <stdexcept>
#include <vector>

namespace agent {

namespace {
std::string Base64Encode(const unsigned char* input, size_t length) {
    // Use EVP_EncodeBlock to avoid direct access to OpenSSL internal structs (BUF_MEM may be opaque)
    int out_len = 4 * static_cast<int>((length + 2) / 3);
    std::vector<unsigned char> out(out_len + 1);
    int encoded_len = EVP_EncodeBlock(out.data(), input, static_cast<int>(length));
    return std::string(reinterpret_cast<char*>(out.data()), encoded_len);
}
}  // namespace

std::string CanonicalJson(const std::string& payload) {
    return payload;
}

std::string SignPayload(const std::string& shared_key,
                        const std::string& payload,
                        long long timestamp_seconds) {
    if (shared_key.empty()) {
        throw std::runtime_error("shared_key_missing");
    }

    std::ostringstream message;
    message << timestamp_seconds << "." << payload;

    unsigned int length = 0;
    std::vector<unsigned char> digest(EVP_MAX_MD_SIZE);

    HMAC(EVP_sha256(),
         shared_key.data(),
         static_cast<int>(shared_key.size()),
         reinterpret_cast<const unsigned char*>(message.str().data()),
         message.str().size(),
         digest.data(),
         &length);

    return Base64Encode(digest.data(), length);
}

}  // namespace agent

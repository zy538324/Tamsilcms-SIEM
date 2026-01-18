#include "agent_signing.h"

#include <openssl/evp.h>
#include <openssl/hmac.h>

#include <sstream>
#include <stdexcept>
#include <vector>

namespace agent {

namespace {
std::string Base64Encode(const unsigned char* input, size_t length) {
    BIO* bio = BIO_new(BIO_s_mem());
    BIO* b64 = BIO_new(BIO_f_base64());
    BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);
    bio = BIO_push(b64, bio);

    BIO_write(bio, input, static_cast<int>(length));
    BIO_flush(bio);

    BUF_MEM* buffer = nullptr;
    BIO_get_mem_ptr(bio, &buffer);
    std::string result(buffer->data, buffer->length);

    BIO_free_all(bio);
    return result;
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

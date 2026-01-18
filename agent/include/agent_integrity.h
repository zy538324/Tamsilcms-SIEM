#pragma once

#include <string>

namespace agent {

std::string ComputeSha256File(const std::string& path);

bool VerifySelfIntegrity(const std::string& executable_path,
                         const std::string& expected_hash);

}  // namespace agent

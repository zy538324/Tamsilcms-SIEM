#include "agent_system.h"

#include <array>

#if defined(_WIN32)
#include <Windows.h>
#else
#include <sys/utsname.h>
#include <unistd.h>
#endif

namespace agent {

std::string DetectHostname() {
#if defined(_WIN32)
    char buffer[MAX_COMPUTERNAME_LENGTH + 1];
    DWORD size = MAX_COMPUTERNAME_LENGTH + 1;
    if (GetComputerNameA(buffer, &size) == 0) {
        return {};
    }
    return std::string(buffer, size);
#else
    std::array<char, 256> buffer{};
    if (gethostname(buffer.data(), buffer.size()) != 0) {
        return {};
    }
    return std::string(buffer.data());
#endif
}

std::string DetectOsName() {
#if defined(_WIN32)
    return "Windows";
#else
    struct utsname info {};
    if (uname(&info) != 0) {
        return {};
    }
    return std::string(info.sysname);
#endif
}

}  // namespace agent

#include "agent_crash.h"

#include <csignal>
#include <cstdlib>
#include <iostream>

namespace agent {

namespace {
void CrashHandler(int signal) {
    std::cerr << "Agent crash detected. Signal: " << signal << std::endl;
    std::exit(128 + signal);
}
}  // namespace

void InstallCrashHandler() {
    std::signal(SIGABRT, CrashHandler);
    std::signal(SIGSEGV, CrashHandler);
    std::signal(SIGTERM, CrashHandler);
    std::signal(SIGINT, CrashHandler);
}

}  // namespace agent

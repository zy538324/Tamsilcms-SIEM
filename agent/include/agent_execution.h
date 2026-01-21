// agent_execution.h
// Execution Service interface for scripts, patching, installs, remote ops
#pragma once
#include <string>
#include <vector>
#include <chrono>

namespace agent_execution {
    struct ScriptJob {
        std::string job_id;
        std::string script_type; // PowerShell, CMD, native
        std::string script_content;
        std::vector<std::string> args;
        std::chrono::system_clock::time_point scheduled_for;
    };

    struct ExecutionResult {
        std::string job_id;
        int exit_code;
        std::string stdout_data;
        std::string stderr_data;
        std::chrono::system_clock::time_point completed_at;
    };

    class ExecutionService {
    public:
        ExecutionResult RunScript(const ScriptJob& job);
        // TODO: Patch management, software install/uninstall, config enforcement, remote ops
    };
}

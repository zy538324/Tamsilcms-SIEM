#include "ExecutionService_stub.h"
namespace agent_execution {
ExecutionResult ExecutionService::RunScript(const ScriptJob&) {
    ExecutionResult result{};
    // Stub: always return success
    result.exit_code = 0;
    result.stdout_data = "stubbed execution output";
    result.stderr_data = "";
    result.completed_at = std::chrono::system_clock::now();
    return result;
}

PatchJobResult ExecutionService::ApplyPatchJob(const PatchJob& job) {
    PatchJobResult result{};
    result.job_id = job.job_id;
    result.status = job.patches.empty() ? "failed" : "completed";
    result.result = job.patches.empty() ? "no_patches" : "installed";
    result.exit_code = job.patches.empty() ? 2 : 0;
    result.reboot_required = (job.reboot_policy == "required");
    result.stdout_summary = "stubbed patch execution";
    result.stderr_summary = "";
    result.started_at = std::chrono::system_clock::now();
    result.completed_at = std::chrono::system_clock::now();
    return result;
}
}

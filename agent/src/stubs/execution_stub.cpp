// Minimal ExecutionService::RunScript stub to allow linking
#include "../../include/agent_execution.h"

namespace agent_execution {
    ExecutionResult ExecutionService::RunScript(const ScriptJob& job) {
        ExecutionResult r;
        r.job_id = job.job_id;
        r.exit_code = 0;
        r.stdout_data = "[stub] executed";
        r.stderr_data = "";
        r.completed_at = std::chrono::system_clock::now();
        return r;
    }
}

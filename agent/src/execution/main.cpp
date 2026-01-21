// Execution Service
// Responsibilities: Script execution, patching, installs, config enforcement, remote ops
#include <iostream>
#include "agent_execution.h"
#include "../../ipc/named_pipe_ipc.h"
#include <windows.h>

int main(int argc, char* argv[]) {
    // Attempt to connect to the core agent named pipe before running jobs
    // Validate pipe name (must not contain invalid characters)
    std::wstring pipe_name = L"tamsil_agent_pipe";
    for (wchar_t c : pipe_name) {
        if (!(iswalnum(c) || c == L'_' || c == L'-')) {
            std::wcerr << L"[ExecutionService] Invalid character in pipe name. Falling back to 'tamsil_agent_pipe'." << std::endl;
            pipe_name = L"tamsil_agent_pipe";
            break;
        }
    }
    agent_ipc::NamedPipeClient client(pipe_name);
    int max_retries = 10;
    int retry_delay_ms = 500;
    int attempt = 0;
    bool connected = false;
    while (attempt < max_retries) {
        if (client.Connect()) {
            connected = true;
            break;
        }
        std::cerr << "[ExecutionService] Failed to connect to pipe, retrying... (" << (attempt+1) << "/" << max_retries << ")" << std::endl;
        Sleep(retry_delay_ms);
        attempt++;
    }
    if (!connected) {
        std::cerr << "[ExecutionService] Could not connect to core agent pipe after " << max_retries << " attempts. Exiting." << std::endl;
        return 1;
    }
    std::cout << "Execution Service connected to core agent pipe." << std::endl;
    // Example: Run a script job
    agent_execution::ExecutionService exec;
    agent_execution::ScriptJob job;
    job.job_id = "job-001";
    job.script_type = "PowerShell";
    job.script_content = "Write-Output 'Hello from agent'";
    job.args = {"-NoProfile"};
    job.scheduled_for = std::chrono::system_clock::now();
    auto result = exec.RunScript(job);
    std::cout << "Execution Service started. Example script job run." << std::endl;
    // TODO: Validate PSA authorisation, command signing, scope, safety
    // PowerShell, CMD, native binaries, patch management
    client.Close();
    return 0;
}

// Execution Service
// Responsibilities: Script execution, patching, installs, config enforcement, remote ops
#include <iostream>
#include <iomanip>
#include <algorithm>
#include <sstream>
#include "agent_config.h"
#include "agent_execution.h"
#include "agent_patch_jobs.h"
#include "agent_rmm.h"
#include "agent_uplink.h"
#include "../../ipc/named_pipe_ipc.h"
#include <windows.h>

namespace {
std::string BuildIsoTimestamp(const std::chrono::system_clock::time_point& time_point) {
    auto now_time = std::chrono::system_clock::to_time_t(time_point);
    std::tm utc_tm{};
#if defined(_WIN32)
    gmtime_s(&utc_tm, &now_time);
#else
    gmtime_r(&now_time, &utc_tm);
#endif
    std::ostringstream stream;
    stream << std::put_time(&utc_tm, "%FT%TZ");
    return stream.str();
}
}  // namespace

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
    // Retry until the core server is available. In some launch scenarios the core
    // may start after this service; keep retrying and log attempts so operators
    // can see progress instead of exiting immediately.
    const int retry_delay_ms = 500;
    int attempt = 0;
    while (true) {
        if (client.Connect()) break;
        attempt++;
        std::cerr << "[ExecutionService] Failed to connect to pipe, retrying... (" << attempt << ")" << std::endl;
        Sleep(retry_delay_ms);
    }
    std::cout << "Execution Service connected to core agent pipe." << std::endl;
    agent::Config config = agent::LoadConfig();
    agent_rmm::RmmTelemetryClient rmm_client(config);
    agent_patch::PatchJobClient patch_client(config);
    agent_execution::ExecutionService exec;

    std::cout << "Execution Service started. Polling for patch jobs." << std::endl;
    const int poll_interval_ms = config.patch_poll_interval_seconds * 1000;
    while (true) {
        agent_patch::PatchJobCommand command{};
        if (!patch_client.PollNextPatchJob(&command)) {
            Sleep(poll_interval_ms);
            continue;
        }

        agent_patch::PatchJobAck ack{};
        ack.job_id = command.job_id;
        ack.status = "received";
        ack.detail = "Job accepted for execution.";
        ack.acknowledged_at = std::chrono::system_clock::now();
        patch_client.AcknowledgePatchJob(ack);

        agent_execution::PatchJob job{};
        job.job_id = command.job_id;
        job.asset_id = config.asset_id;
        job.reboot_policy = command.reboot_policy;
        job.scheduled_at = command.scheduled_at;
        for (const auto& patch : command.patches) {
            agent_execution::PatchDescriptor descriptor{};
            descriptor.patch_id = patch.patch_id;
            descriptor.title = patch.title;
            descriptor.vendor = patch.vendor;
            descriptor.severity = patch.severity;
            descriptor.kb = patch.kb;
            job.patches.push_back(descriptor);
        }

        while (std::chrono::system_clock::now() < job.scheduled_at) {
            auto now = std::chrono::system_clock::now();
            auto remaining = std::chrono::duration_cast<std::chrono::milliseconds>(job.scheduled_at - now);
            if (remaining.count() <= 0) {
                break;
            }
            ack.status = "scheduled";
            ack.detail = "Waiting until scheduled window.";
            ack.acknowledged_at = std::chrono::system_clock::now();
            patch_client.AcknowledgePatchJob(ack);
            auto sleep_ms = static_cast<DWORD>(std::min<long long>(remaining.count(), poll_interval_ms));
            Sleep(sleep_ms);
        }

        auto started_at = std::chrono::system_clock::now();
        auto result = exec.ApplyPatchJob(job);

        agent_rmm::RmmPatchJob patch_job{};
        patch_job.job_id = result.job_id;
        patch_job.patch_id = job.patches.empty() ? "" : job.patches.front().patch_id;
        patch_job.status = result.status;
        patch_job.result = result.result;
        patch_job.exit_code = result.exit_code;
        patch_job.reboot_required = result.reboot_required;
        patch_job.stdout_summary = result.stdout_summary;
        patch_job.stderr_summary = result.stderr_summary;
        patch_job.scheduled_at = job.scheduled_at;
        patch_job.applied_at = result.completed_at;
        rmm_client.SendPatchJob(patch_job);

        patch_client.ReportPatchResult(result);

        std::ostringstream psa_payload;
        psa_payload << '{';
        psa_payload << "\"tenant_id\":\"" << config.tenant_id << "\",";
        psa_payload << "\"asset_id\":\"" << config.asset_id << "\",";
        psa_payload << "\"job_id\":\"" << result.job_id << "\",";
        psa_payload << "\"status\":\"" << result.status << "\",";
        psa_payload << "\"result\":\"" << result.result << "\",";
        psa_payload << "\"exit_code\":" << result.exit_code << ",";
        psa_payload << "\"stdout_summary\":\"" << result.stdout_summary << "\",";
        psa_payload << "\"stderr_summary\":\"" << result.stderr_summary << "\",";
        psa_payload << "\"reboot_required\":" << (result.reboot_required ? "true" : "false") << ",";
        psa_payload << "\"started_at\":\"" << BuildIsoTimestamp(started_at) << "\",";
        psa_payload << "\"completed_at\":\"" << BuildIsoTimestamp(result.completed_at) << "\"";
        psa_payload << '}';
        agent_uplink::UploadPatchResult(psa_payload.str());

        ack.status = "completed";
        ack.detail = "Job executed and results reported.";
        ack.acknowledged_at = std::chrono::system_clock::now();
        patch_client.AcknowledgePatchJob(ack);
    }

    client.Close();
    return 0;
}

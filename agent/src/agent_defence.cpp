#include "agent_defence.h"

#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include <sstream>

namespace agent {

namespace {
std::string GetEnv(const char* key, const std::string& fallback) {
    const char* value = std::getenv(key);
    if (value == nullptr) {
        return fallback;
    }
    return std::string(value);
}

std::string ToIsoTimestamp(const std::chrono::system_clock::time_point& timepoint) {
    std::time_t raw_time = std::chrono::system_clock::to_time_t(timepoint);
    std::tm utc_time {};
#if defined(_WIN32)
    gmtime_s(&utc_time, &raw_time);
#else
    gmtime_r(&raw_time, &utc_time);
#endif
    std::ostringstream stream;
    stream << std::put_time(&utc_time, "%Y-%m-%dT%H:%M:%SZ");
    return stream.str();
}

bool ParseBoolEnv(const std::string& value, bool fallback) {
    if (value == "true" || value == "1" || value == "yes") {
        return true;
    }
    if (value == "false" || value == "0" || value == "no") {
        return false;
    }
    return fallback;
}

bool RequiresProcessId(ResponseAction action) {
    return action == ResponseAction::kKillProcess || action == ResponseAction::kBlockNetwork;
}

bool RequiresFilePath(ResponseAction action) {
    return action == ResponseAction::kQuarantineFile || action == ResponseAction::kPreventExecution;
}

std::string EscapeJsonString(const std::string& value) {
    std::ostringstream stream;
    for (char ch : value) {
        switch (ch) {
            case '\"':
                stream << "\\\"";
                break;
            case '\\':
                stream << "\\\\";
                break;
            case '\b':
                stream << "\\b";
                break;
            case '\f':
                stream << "\\f";
                break;
            case '\n':
                stream << "\\n";
                break;
            case '\r':
                stream << "\\r";
                break;
            case '\t':
                stream << "\\t";
                break;
            default:
                stream << ch;
                break;
        }
    }
    return stream.str();
}

std::string ResponseActionName(ResponseAction action) {
    switch (action) {
        case ResponseAction::kObserveOnly:
            return "observe_only";
        case ResponseAction::kKillProcess:
            return "kill_process";
        case ResponseAction::kQuarantineFile:
            return "quarantine_file";
        case ResponseAction::kBlockNetwork:
            return "block_network";
        case ResponseAction::kPreventExecution:
            return "prevent_execution";
        default:
            return "unknown";
    }
}
}  // namespace

DefencePolicy BuildDefaultDefencePolicy() {
    DefencePolicy policy{};
    policy.policy_id = GetEnv("AGENT_DEFENCE_POLICY_ID", "default-policy");
    std::string mode = GetEnv("AGENT_DEFENCE_MODE", "observe");
    policy.mode = mode == "enforce" ? PolicyMode::kEnforce : PolicyMode::kObserveOnly;
    policy.min_confidence_threshold = std::stod(GetEnv("AGENT_DEFENCE_MIN_CONFIDENCE", "0.7"));
    policy.max_actions_per_window = std::stoi(GetEnv("AGENT_DEFENCE_MAX_ACTIONS", "5"));
    policy.action_window_seconds = std::stoi(GetEnv("AGENT_DEFENCE_ACTION_WINDOW", "300"));
    policy.allow_kill_process = ParseBoolEnv(GetEnv("AGENT_DEFENCE_ALLOW_KILL", "false"), false);
    policy.allow_quarantine_file = ParseBoolEnv(GetEnv("AGENT_DEFENCE_ALLOW_QUARANTINE", "false"), false);
    policy.allow_block_network = ParseBoolEnv(GetEnv("AGENT_DEFENCE_ALLOW_BLOCK", "false"), false);
    policy.allow_prevent_execution = ParseBoolEnv(GetEnv("AGENT_DEFENCE_ALLOW_PREVENT", "false"), false);
    return policy;
}

std::string BuildFindingPayload(const DefenceFinding& finding) {
    std::ostringstream stream;
    stream << "{"
           << "\"detection_id\":\"" << EscapeJsonString(finding.detection_id) << "\","
           << "\"rule_id\":\"" << EscapeJsonString(finding.rule_id) << "\","
           << "\"behaviour_signature\":\"" << EscapeJsonString(finding.behaviour_signature) << "\","
           << "\"confidence\":" << finding.confidence << ","
           << "\"process_id\":\"" << EscapeJsonString(finding.process_id) << "\","
           << "\"file_path\":\"" << EscapeJsonString(finding.file_path) << "\","
           << "\"command_line\":\"" << EscapeJsonString(finding.command_line) << "\","
           << "\"timestamp\":\"" << EscapeJsonString(finding.timestamp) << "\","
           << "\"proposed_response\":\"" << ResponseActionName(finding.proposed_response) << "\","
           << "\"decision_reason\":\"" << EscapeJsonString(finding.decision_reason) << "\""
           << "}";
    return stream.str();
}

std::string BuildEvidencePayload(const DefenceEvidence& evidence) {
    std::ostringstream stream;
    stream << "{"
           << "\"finding_id\":\"" << EscapeJsonString(evidence.finding_id) << "\","
           << "\"policy_id\":\"" << EscapeJsonString(evidence.policy_id) << "\","
           << "\"action\":\"" << ResponseActionName(evidence.action) << "\","
           << "\"permitted_by_policy\":" << (evidence.permitted_by_policy ? "true" : "false") << ","
           << "\"decision_reason\":\"" << EscapeJsonString(evidence.decision_reason) << "\","
           << "\"before_state\":\"" << EscapeJsonString(evidence.before_state) << "\","
           << "\"after_state\":\"" << EscapeJsonString(evidence.after_state) << "\","
           << "\"timestamp\":\"" << EscapeJsonString(evidence.timestamp) << "\""
           << "}";
    return stream.str();
}

DefenceModule::DefenceModule(const Config& config, DefencePolicy policy)
    : config_(config), policy_(std::move(policy)) {}

DefenceFinding DefenceModule::EvaluateSignal(const BehaviourSignal& signal) {
    DefenceFinding finding{};
    finding.detection_id = "DEF-" + signal.name;
    finding.rule_id = signal.rule_id;
    finding.behaviour_signature = signal.name;
    finding.confidence = signal.confidence;
    finding.process_id = signal.process_id;
    finding.file_path = signal.file_path;
    finding.command_line = signal.command_line;
    finding.timestamp = signal.observed_at.empty()
        ? ToIsoTimestamp(std::chrono::system_clock::now())
        : signal.observed_at;

    if (finding.rule_id.empty()) {
        finding.proposed_response = ResponseAction::kObserveOnly;
        finding.decision_reason = "missing rule identifier";
        return finding;
    }

    if (!signal.response_defined) {
        finding.proposed_response = ResponseAction::kObserveOnly;
        finding.decision_reason = "response undefined";
        return finding;
    }

    if (signal.confidence < policy_.min_confidence_threshold) {
        finding.proposed_response = ResponseAction::kObserveOnly;
        finding.decision_reason = "confidence below threshold";
        return finding;
    }

    finding.proposed_response = signal.requested_response;
    if (finding.proposed_response == ResponseAction::kObserveOnly) {
        finding.decision_reason = "rule observe-only";
        return finding;
    }

    if (RequiresProcessId(finding.proposed_response) && finding.process_id.empty()) {
        finding.proposed_response = ResponseAction::kObserveOnly;
        finding.decision_reason = "missing process identifier";
        return finding;
    }

    if (RequiresFilePath(finding.proposed_response) && finding.file_path.empty()) {
        finding.proposed_response = ResponseAction::kObserveOnly;
        finding.decision_reason = "missing file path";
        return finding;
    }

    if (policy_.mode == PolicyMode::kObserveOnly) {
        finding.proposed_response = ResponseAction::kObserveOnly;
        finding.decision_reason = "policy observe-only";
        return finding;
    }

    if (IsRateLimited()) {
        finding.proposed_response = ResponseAction::kObserveOnly;
        finding.decision_reason = "rate limited";
    }
    if (finding.decision_reason.empty()) {
        finding.decision_reason = "action permitted";
    }
    return finding;
}

DefenceEvidence DefenceModule::ApplyResponse(const DefenceFinding& finding) {
    DefenceEvidence evidence{};
    evidence.finding_id = finding.detection_id;
    evidence.policy_id = policy_.policy_id;
    evidence.timestamp = ToIsoTimestamp(std::chrono::system_clock::now());
    evidence.action = finding.proposed_response;
    evidence.permitted_by_policy = IsResponseAllowed(finding.proposed_response);
    evidence.decision_reason = finding.decision_reason;
    evidence.before_state = "capture-before-state";
    evidence.after_state = "capture-after-state";

    if (evidence.action != ResponseAction::kObserveOnly && evidence.permitted_by_policy) {
        RecordActionTimestamp();
    }

    if (!evidence.permitted_by_policy) {
        evidence.action = ResponseAction::kObserveOnly;
        evidence.decision_reason = "action blocked by policy";
    }

    return evidence;
}

std::string DefenceModule::BuildStatusSummary() const {
    std::ostringstream stream;
    stream << "Defence policy " << policy_.policy_id << " mode="
           << (policy_.mode == PolicyMode::kEnforce ? "enforce" : "observe")
           << " min_confidence=" << policy_.min_confidence_threshold;
    return stream.str();
}

bool DefenceModule::IsResponseAllowed(ResponseAction action) const {
    if (action == ResponseAction::kObserveOnly) {
        return true;
    }
    if (policy_.mode == PolicyMode::kObserveOnly) {
        return false;
    }
    switch (action) {
        case ResponseAction::kKillProcess:
            return policy_.allow_kill_process;
        case ResponseAction::kQuarantineFile:
            return policy_.allow_quarantine_file;
        case ResponseAction::kBlockNetwork:
            return policy_.allow_block_network;
        case ResponseAction::kPreventExecution:
            return policy_.allow_prevent_execution;
        case ResponseAction::kObserveOnly:
            return true;
        default:
            return false;
    }
}

bool DefenceModule::IsRateLimited() const {
    if (policy_.max_actions_per_window <= 0 || policy_.action_window_seconds <= 0) {
        return false;
    }
    auto now = std::chrono::system_clock::now();
    auto cutoff = now - std::chrono::seconds(policy_.action_window_seconds);
    auto count = std::count_if(action_timestamps_.begin(), action_timestamps_.end(),
                               [cutoff](const auto& entry) { return entry >= cutoff; });
    return count >= policy_.max_actions_per_window;
}

void DefenceModule::RecordActionTimestamp() {
    auto now = std::chrono::system_clock::now();
    action_timestamps_.push_back(now);
    auto cutoff = now - std::chrono::seconds(policy_.action_window_seconds);
    action_timestamps_.erase(
        std::remove_if(action_timestamps_.begin(), action_timestamps_.end(),
                       [cutoff](const auto& entry) { return entry < cutoff; }),
        action_timestamps_.end());
}

}  // namespace agent

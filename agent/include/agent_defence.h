#pragma once

#include <chrono>
#include <string>
#include <vector>

#include "agent_config.h"

namespace agent {

enum class BehaviourSignalType {
    kProcess,
    kMemory,
    kFile,
    kPrivilege
};

enum class ResponseAction {
    kObserveOnly,
    kKillProcess,
    kQuarantineFile,
    kBlockNetwork,
    kPreventExecution
};

enum class PolicyMode {
    kObserveOnly,
    kEnforce
};

struct BehaviourSignal {
    BehaviourSignalType type;
    std::string name;
    std::string rule_id;
    std::string process_id;
    std::string file_path;
    std::string command_line;
    double confidence;
    std::string observed_at;
    bool response_defined;
    ResponseAction requested_response;
};

struct DefenceFinding {
    std::string detection_id;
    std::string rule_id;
    std::string behaviour_signature;
    double confidence;
    std::string process_id;
    std::string file_path;
    std::string timestamp;
    ResponseAction proposed_response;
    std::string decision_reason;
};

struct DefenceEvidence {
    std::string finding_id;
    std::string policy_id;
    ResponseAction action;
    bool permitted_by_policy;
    std::string decision_reason;
    std::string before_state;
    std::string after_state;
    std::string timestamp;
};

struct DefencePolicy {
    std::string policy_id;
    PolicyMode mode;
    double min_confidence_threshold;
    int max_actions_per_window;
    int action_window_seconds;
    bool allow_kill_process;
    bool allow_quarantine_file;
    bool allow_block_network;
    bool allow_prevent_execution;
};

DefencePolicy BuildDefaultDefencePolicy();

class DefenceModule {
  public:
    DefenceModule(const Config& config, DefencePolicy policy);

    DefenceFinding EvaluateSignal(const BehaviourSignal& signal);
    DefenceEvidence ApplyResponse(const DefenceFinding& finding);
    std::string BuildStatusSummary() const;

  private:
    bool IsResponseAllowed(ResponseAction action) const;
    bool IsRateLimited() const;
    void RecordActionTimestamp();

    Config config_;
    DefencePolicy policy_;
    std::vector<std::chrono::system_clock::time_point> action_timestamps_;
};

}  // namespace agent

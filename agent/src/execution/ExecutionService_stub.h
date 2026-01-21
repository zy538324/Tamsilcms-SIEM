// ExecutionService_stub.h
#pragma once
#include <cstdint>
namespace agent_execution {
struct ScriptJob {};
struct ExecutionResult {};
class ExecutionService {
public:
    ExecutionResult RunScript(const ScriptJob&);
};
}

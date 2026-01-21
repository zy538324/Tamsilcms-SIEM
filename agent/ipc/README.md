# Agent IPC & Message Schemas

All agent services communicate via:
- Named pipes
- Shared memory (with ACLs)
- Strict message schemas (protobuf or flat structs)

## Message Types
- TelemetryEnvelope
- DetectionReport
- ExecutionResult
- EvidencePackage
- HealthHeartbeat
- ComplianceAssertion

No raw JSON blobs. All messages are typed and versioned.

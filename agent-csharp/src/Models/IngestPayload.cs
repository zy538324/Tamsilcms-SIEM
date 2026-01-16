namespace Tamsilcms.Siem.Agent.Models;

internal sealed record IngestPayload(Guid AgentId, IReadOnlyCollection<LogEvent> Events);

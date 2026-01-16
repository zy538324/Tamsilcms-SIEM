namespace Tamsilcms.Siem.Agent.Models;

internal sealed record LogEvent(
    Guid AgentId,
    string Hostname,
    string OsType,
    string OsVersion,
    string LogSource,
    DateTimeOffset EventTime,
    string EventLevel,
    string EventId,
    string Message)
{
    public static LogEvent FromLine(AgentConfig config, LogLine line)
    {
        return new LogEvent(
            config.AgentId,
            config.Hostname,
            config.OsType,
            config.OsVersion,
            config.LogSource,
            line.TimestampUtc,
            "INFO",
            "0",
            line.Message);
    }
}

namespace Tamsilcms.Siem.Agent.Models;

internal sealed record LogLine(string Message, DateTimeOffset TimestampUtc);

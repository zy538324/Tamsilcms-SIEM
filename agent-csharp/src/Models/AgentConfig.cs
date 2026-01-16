using System.Runtime.InteropServices;

namespace Tamsilcms.Siem.Agent.Models;

internal sealed record AgentConfig(
    Uri ApiUrl,
    string ApiKey,
    Guid AgentId,
    string Hostname,
    string OsType,
    string OsVersion,
    string LogSource,
    string LogPath,
    int BatchSize,
    double PollIntervalSeconds,
    string SpoolPath)
{
    public static AgentConfig Load()
    {
        var apiUrl = Environment.GetEnvironmentVariable("API_URL") ?? "http://localhost:8080/api/v1/logs/ingest";
        var apiKey = Environment.GetEnvironmentVariable("API_KEY") ?? string.Empty;
        var agentId = Environment.GetEnvironmentVariable("AGENT_ID") ?? string.Empty;
        var hostname = Environment.GetEnvironmentVariable("HOSTNAME") ?? Environment.MachineName;
        var osType = Environment.GetEnvironmentVariable("OS_TYPE") ?? GetOsType();
        var osVersion = Environment.GetEnvironmentVariable("OS_VERSION") ?? RuntimeInformation.OSDescription;
        var logSource = Environment.GetEnvironmentVariable("LOG_SOURCE") ?? "syslog";
        var logPath = Environment.GetEnvironmentVariable("LOG_PATH") ?? "/var/log/syslog";
        var batchSize = int.TryParse(Environment.GetEnvironmentVariable("BATCH_SIZE"), out var size)
            ? size
            : 100;
        var pollInterval = double.TryParse(Environment.GetEnvironmentVariable("POLL_INTERVAL"), out var interval)
            ? interval
            : 1.5;
        var spoolPath = Environment.GetEnvironmentVariable("SPOOL_PATH") ?? "/tmp/siem_spool.jsonl";

        return new AgentConfig(
            new Uri(apiUrl),
            apiKey,
            Guid.TryParse(agentId, out var parsed) ? parsed : Guid.Empty,
            hostname,
            osType,
            osVersion,
            logSource,
            logPath,
            batchSize,
            pollInterval,
            spoolPath);
    }

    private static string GetOsType()
    {
        if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
        {
            return "windows";
        }

        if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
        {
            return "linux";
        }

        return "unknown";
    }
}

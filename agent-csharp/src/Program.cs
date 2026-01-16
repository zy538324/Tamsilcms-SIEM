using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using Tamsilcms.Siem.Agent.Models;
using Tamsilcms.Siem.Agent.Services;

namespace Tamsilcms.Siem.Agent;

internal static class Program
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        WriteIndented = false
    };

    public static async Task Main()
    {
        var config = AgentConfig.Load();
        if (string.IsNullOrWhiteSpace(config.ApiKey) || config.AgentId == Guid.Empty)
        {
            throw new InvalidOperationException("API_KEY and AGENT_ID must be configured.");
        }

        using var httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(10)
        };
        httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        httpClient.DefaultRequestHeaders.Add("X-Agent-Key", config.ApiKey);

        var spoolStore = new SpoolStore(config.SpoolPath);
        var tailer = new LogTailer(config.LogPath, config.PollIntervalSeconds);

        await FlushSpoolAsync(config, httpClient, spoolStore);

        var batch = new List<LogEvent>();
        await foreach (var entry in tailer.ReadLinesAsync())
        {
            batch.Add(LogEvent.FromLine(config, entry));

            if (batch.Count < config.BatchSize)
            {
                continue;
            }

            var success = await PostBatchAsync(config, httpClient, batch);
            if (!success)
            {
                await spoolStore.AppendAsync(batch);
            }

            batch.Clear();
        }
    }

    private static async Task FlushSpoolAsync(AgentConfig config, HttpClient client, SpoolStore spool)
    {
        var queued = await spool.ReadAsync(config.BatchSize);
        if (queued.Count == 0)
        {
            return;
        }

        var success = await PostBatchAsync(config, client, queued);
        if (!success)
        {
            await spool.AppendAsync(queued);
        }
    }

    private static async Task<bool> PostBatchAsync(AgentConfig config, HttpClient client, IReadOnlyCollection<LogEvent> batch)
    {
        if (batch.Count == 0)
        {
            return true;
        }

        var payload = new IngestPayload(config.AgentId, batch);
        var json = JsonSerializer.Serialize(payload, JsonOptions);
        using var content = new StringContent(json, Encoding.UTF8, "application/json");

        try
        {
            using var response = await client.PostAsync(config.ApiUrl, content);
            return response.IsSuccessStatusCode;
        }
        catch (HttpRequestException)
        {
            return false;
        }
    }
}

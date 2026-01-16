using System.Text.Json;
using Tamsilcms.Siem.Agent.Models;

namespace Tamsilcms.Siem.Agent.Services;

internal sealed class SpoolStore
{
    private readonly string _path;

    public SpoolStore(string path)
    {
        _path = path;
    }

    public async Task AppendAsync(IEnumerable<LogEvent> events)
    {
        var directory = Path.GetDirectoryName(_path);
        if (!string.IsNullOrWhiteSpace(directory))
        {
            Directory.CreateDirectory(directory);
        }

        await using var stream = new FileStream(_path, FileMode.Append, FileAccess.Write, FileShare.Read);
        await using var writer = new StreamWriter(stream);

        foreach (var logEvent in events)
        {
            var json = JsonSerializer.Serialize(logEvent);
            await writer.WriteLineAsync(json);
        }
    }

    public async Task<IReadOnlyList<LogEvent>> ReadAsync(int maxEvents)
    {
        if (!File.Exists(_path))
        {
            return Array.Empty<LogEvent>();
        }

        var lines = await File.ReadAllLinesAsync(_path);
        var items = new List<LogEvent>();
        var remaining = new List<string>();

        foreach (var line in lines)
        {
            if (items.Count < maxEvents)
            {
                var logEvent = JsonSerializer.Deserialize<LogEvent>(line);
                if (logEvent is not null)
                {
                    items.Add(logEvent);
                }
            }
            else
            {
                remaining.Add(line);
            }
        }

        await File.WriteAllLinesAsync(_path, remaining);
        return items;
    }
}

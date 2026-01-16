using System.Runtime.CompilerServices;
using System.Text;
using Tamsilcms.Siem.Agent.Models;

namespace Tamsilcms.Siem.Agent.Services;

internal sealed class LogTailer
{
    private readonly string _path;
    private readonly TimeSpan _pollInterval;

    public LogTailer(string path, double pollIntervalSeconds)
    {
        _path = path;
        _pollInterval = TimeSpan.FromSeconds(pollIntervalSeconds);
    }

    public async IAsyncEnumerable<LogLine> ReadLinesAsync([EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        if (!File.Exists(_path))
        {
            throw new FileNotFoundException($"Log file not found: {_path}");
        }

        await using var stream = new FileStream(_path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
        using var reader = new StreamReader(stream, Encoding.UTF8, true);
        stream.Seek(0, SeekOrigin.End);

        while (!cancellationToken.IsCancellationRequested)
        {
            var line = await reader.ReadLineAsync();
            if (line is null)
            {
                await Task.Delay(_pollInterval, cancellationToken);
                continue;
            }

            yield return new LogLine(line.Trim(), DateTimeOffset.UtcNow);
        }
    }
}

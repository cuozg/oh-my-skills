# Patterns: UniTask Async

```csharp
using System;
using System.Threading;
using Cysharp.Threading.Tasks;

namespace YourProject.Loading;

/// <summary>
/// Loads player data from remote API.
/// </summary>
public sealed class PlayerDataLoader
{
    private readonly ILogger logger;
    private readonly INetworkService network;

    public PlayerDataLoader(ILogger logger, INetworkService network)
    {
        this.logger = logger;
        this.network = network;
    }

    /// <summary>
    /// Loads player data by ID. Returns null on failure.
    /// </summary>
    public async UniTask<PlayerData?> LoadAsync(string playerId, CancellationToken ct)
    {
        if (string.IsNullOrEmpty(playerId)) return null;

        try
        {
            string json = await this.network.GetAsync($"/api/player/{playerId}", ct);
            return JsonUtility.FromJson<PlayerData>(json);
        }
        catch (OperationCanceledException)
        {
            throw; // Always rethrow cancellation
        }
        catch (NetworkException ex)
        {
            this.logger.Error($"Failed to load player {playerId}: {ex.Message}");
            return null;
        }
    }

    /// <summary>
    /// Loads multiple players in parallel.
    /// </summary>
    public async UniTask<PlayerData?[]> LoadBatchAsync(string[] playerIds, CancellationToken ct)
    {
        var tasks = new UniTask<PlayerData?>[playerIds.Length];
        for (int i = 0; i < playerIds.Length; i++)
        {
            tasks[i] = this.LoadAsync(playerIds[i], ct);
        }
        return await UniTask.WhenAll(tasks);
    }
}
```

Rules: `async UniTask` (not `async Task`) | `CancellationToken` on every async method | Rethrow `OperationCanceledException` | Catch specific exceptions | No `async void`

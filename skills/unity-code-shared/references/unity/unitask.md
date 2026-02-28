# UniTask Async Patterns

Use UniTask for all async operations in Unity. Allocation-free async/await, cancellation, parallel ops.

## Async Method Signatures

```csharp
// ✅ GOOD: UniTask return type
public async UniTask LoadDataAsync(CancellationToken ct = default)
{
    var data = await LoadFromServerAsync(ct);
    ProcessData(data);
}

// ✅ GOOD: UniTask<T> for results
public async UniTask<PlayerData> GetPlayerAsync(string id, CancellationToken ct = default)
{
    return await this.api.FetchPlayerAsync(id, ct);
}

// ✅ GOOD: UniTaskVoid for fire-and-forget (Unity entry points)
public async UniTaskVoid OnButtonClick()
{
    await ProcessAsync(this.GetCancellationTokenOnDestroy());
}

// ❌ BAD: Task (allocates, no Unity integration)
// ❌ BAD: async void (swallows exceptions, no cancellation)
```

## Cancellation

```csharp
// ✅ GOOD: CancellationToken from MonoBehaviour lifetime
public sealed class DataLoader : MonoBehaviour
{
    private async UniTaskVoid Start()
    {
        var ct = this.GetCancellationTokenOnDestroy();
        await LoadAllDataAsync(ct);
    }

    private async UniTask LoadAllDataAsync(CancellationToken ct)
    {
        var playerData = await LoadPlayerAsync(ct);
        ct.ThrowIfCancellationRequested();
        var inventoryData = await LoadInventoryAsync(ct);
    }
}

// ✅ GOOD: Manual CancellationTokenSource (debounce)
public sealed class SearchService : IDisposable
{
    private CancellationTokenSource? searchCts;

    public async UniTask SearchAsync(string query)
    {
        this.searchCts?.Cancel();
        this.searchCts?.Dispose();
        this.searchCts = new CancellationTokenSource();

        try
        {
            await UniTask.Delay(300, cancellationToken: this.searchCts.Token);
            var results = await this.api.SearchAsync(query, this.searchCts.Token);
            DisplayResults(results);
        }
        catch (OperationCanceledException) { /* Expected */ }
    }

    public void Dispose() { this.searchCts?.Cancel(); this.searchCts?.Dispose(); }
}
```

## Parallel Operations

```csharp
// ✅ GOOD: WhenAll for parallel async
var (playerData, worldData, uiData) = await UniTask.WhenAll(
    LoadPlayerAsync(ct), LoadWorldAsync(ct), LoadUIAsync(ct));
InitializeGame(playerData, worldData, uiData);

// ✅ GOOD: WhenAny for timeout/race
var (hasValue, result) = await UniTask.WhenAny(
    task, UniTask.Delay(TimeSpan.FromSeconds(timeoutSeconds)));
if (hasValue == 0) return result;
throw new TimeoutException($"Timed out after {timeoutSeconds}s");
```

**See also:** [unitask-integration.md](unitask-integration.md) for Unity waiting patterns, scene loading, web requests, error handling. [unitask-migration.md](unitask-migration.md) for coroutine→UniTask migration.

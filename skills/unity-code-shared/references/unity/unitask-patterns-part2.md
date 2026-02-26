## Parallel Operations

```csharp
// ✅ GOOD: WhenAll for parallel async
public async UniTask LoadGameAsync(CancellationToken ct)
{
    var (playerData, worldData, uiData) = await UniTask.WhenAll(
        LoadPlayerAsync(ct),
        LoadWorldAsync(ct),
        LoadUIAsync(ct)
    );

    InitializeGame(playerData, worldData, uiData);
}

// ✅ GOOD: WhenAny for race conditions
public async UniTask<T> LoadWithTimeout<T>(UniTask<T> task, float timeoutSeconds)
{
    var (hasValue, result) = await UniTask.WhenAny(
        task,
        UniTask.Delay(TimeSpan.FromSeconds(timeoutSeconds))
    );

    if (hasValue == 0)
        return result;

    throw new TimeoutException($"Operation timed out after {timeoutSeconds}s");
}
```

**Continue in [unitask-patterns-integration.md](unitask-patterns-integration.md) for Unity Integration, Error Handling, and Migration patterns.**

# Async Patterns

## Pick One Async Stack Per Project

- Use the async primitive already established in the repo.
- If the project uses Unity's built-in `Awaitable`, stay consistent with it for Unity-native async flows.
- If the project already uses UniTask or targets older Unity versions, keep UniTask instead of mixing styles.
- Use plain `Task` mainly at library or external API boundaries.
- Avoid mixing `Task`, `UniTask`, and `Awaitable` in the same gameplay flow without a clear boundary.

## UniTask Example

```csharp
using Cysharp.Threading.Tasks;

async UniTask LoadLevel(string sceneName, CancellationToken ct)
{
    await SceneManager.LoadSceneAsync(sceneName);
    await UniTask.Delay(500, cancellationToken: ct);
    _ui.ShowHUD();
}

await UniTask.Yield();
await UniTask.Yield(PlayerLoopTiming.FixedUpdate);
await UniTask.WaitForEndOfFrame(this);
```

## Awaitable Example

```csharp
async Awaitable LoadLevelAsync(string sceneName)
{
    await SceneManager.LoadSceneAsync(sceneName);
    await Awaitable.WaitForSecondsAsync(0.5f);
    _ui.ShowHUD();
}

await Awaitable.NextFrameAsync();
await Awaitable.EndOfFrameAsync();
await Awaitable.FixedUpdateAsync();
```

## Cancellation - Always Pass It Through

```csharp
public sealed class EnemyAI : MonoBehaviour
{
    private async Awaitable Start()
    {
        await PatrolLoopAsync(destroyCancellationToken);
    }

    private async Awaitable PatrolLoopAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            await MoveToNextWaypointAsync(ct);
            await Awaitable.WaitForSecondsAsync(1f, ct);
        }
    }
}
```

If the project uses UniTask, apply the same rule there: every long-lived async path should accept and forward a `CancellationToken`.

## Async Void - Event Handlers Only

```csharp
// Acceptable for Unity event handlers only
async void OnButtonClick()
{
    await SaveGameAsync(destroyCancellationToken);
}

// Avoid for normal methods
async Awaitable LoadDataAsync() { }
```

## Parallel Execution

```csharp
async UniTask InitGame(CancellationToken ct)
{
    await UniTask.WhenAll(
        LoadPlayerData(ct),
        LoadInventory(ct),
        PreloadVfx(ct));
}
```

If the project uses `Awaitable`, keep parallel composition explicit and remember that a single `Awaitable` instance must not be awaited multiple times.

<!-- Advanced: async-advanced.md -->

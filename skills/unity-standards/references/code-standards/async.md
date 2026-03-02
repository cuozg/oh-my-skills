# Async Patterns

## UniTask — Preferred Over Task

```csharp
using Cysharp.Threading.Tasks;

async UniTask LoadLevel(string sceneName)
{
    await SceneManager.LoadSceneAsync(sceneName);
    await UniTask.Delay(500);
    _ui.ShowHUD();
}

// ❌ avoid: async Task LoadLevel(...) { }

// Frame waits
await UniTask.Yield();
await UniTask.Yield(PlayerLoopTiming.FixedUpdate);
await UniTask.WaitForEndOfFrame(this);
```

## CancellationToken — Always Use

```csharp
public sealed class EnemyAI : MonoBehaviour
{
    async UniTaskVoid Start()
    {
        await PatrolLoop(destroyCancellationToken); // auto-cancels on Destroy
    }

    async UniTask PatrolLoop(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            await MoveToNextWaypoint(ct);
            await UniTask.Delay(1000, cancellationToken: ct);
        }
    }

    async UniTask MoveToNextWaypoint(CancellationToken ct)
    {
        while (Vector3.Distance(transform.position, _target) > 0.1f)
        {
            transform.position = Vector3.MoveTowards(
                transform.position, _target, _speed * Time.deltaTime);
            await UniTask.Yield(ct);
        }
    }
}
```

## Async Void — Event Handlers Only

```csharp
// ✅ async void for Unity event handlers (can't return UniTask)
async void OnButtonClick() { await SaveGame(destroyCancellationToken); }

// ❌ async void for normal methods — exceptions vanish
async void LoadData() { } // NO — use async UniTask
```

## Parallel Execution

```csharp
async UniTask InitGame(CancellationToken ct)
{
    await UniTask.WhenAll(LoadPlayerData(ct), LoadInventory(ct), PreloadVFX(ct));
    Debug.Log("All loaded");
}

// With timeout
var result = await UniTask.WhenAny(
    FetchFromServer(ct),
    UniTask.Delay(5000, cancellationToken: ct)
);
if (result == 1) Debug.LogWarning("Server timeout");
```

## Error Handling & Converting Unity Async

```csharp
async UniTask<bool> TrySave(CancellationToken ct)
{
    try
    {
        await WriteFile(_savePath, _data, ct);
        return true;
    }
    catch (OperationCanceledException) { return false; } // normal — don't log
    catch (System.Exception ex) { Debug.LogException(ex); return false; }
}

// AsyncOperation → UniTask: await SceneManager.LoadSceneAsync("Level1"); await Resources.LoadAsync<Texture2D>("splash");
// Coroutine → UniTask: await SomeLegacyCoroutine().ToUniTask(cancellationToken: ct);
// UnityWebRequest: await UnityWebRequest.Get(url).SendWebRequest().WithCancellation(ct);
```

## Awaitable — Unity 6+ Built-In

Unity 6 (2023.1+) introduces `Awaitable` as a built-in async primitive — no UniTask dependency needed:

```csharp
// Awaitable replaces UniTask for Unity-native async
async Awaitable LoadLevelAsync(string sceneName)
{
    await SceneManager.LoadSceneAsync(sceneName);
    await Awaitable.WaitForSecondsAsync(0.5f);
    _ui.ShowHUD();
}

// Frame waits
await Awaitable.NextFrameAsync();
await Awaitable.EndOfFrameAsync();
await Awaitable.FixedUpdateAsync();

// Background thread round-trip
await Awaitable.BackgroundThreadAsync();
var result = HeavyComputation();
await Awaitable.MainThreadAsync(); // back to main thread
ApplyResult(result);
```

| Feature | UniTask | Awaitable (Unity 6+) |
|---------|---------|---------------------|
| Dependency | External package | Built-in |
| Thread switching | `UniTask.SwitchToThreadPool()` | `Awaitable.BackgroundThreadAsync()` |
| Frame wait | `UniTask.Yield()` | `Awaitable.NextFrameAsync()` |
| Cancellation | `CancellationToken` | `CancellationToken` + `destroyCancellationToken` |
| Min Unity version | 2019.3+ | 2023.1+ (Unity 6) |

**Guideline:** Use `Awaitable` for new projects on Unity 6+. Use `UniTask` for older projects or when you need features like `UniTask.WhenAll` with value-type returns.

## Version Compatibility

| Feature | Min Unity Version |
|---------|------------------|
| `destroyCancellationToken` | 2022.2+ |
| `Awaitable` | 2023.1+ (Unity 6) |
| `async/await` in Unity | 2017.1+ |
| UniTask recommended | 2019.3+ |

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

# UniTask Advanced Patterns

Continued from [unitask-patterns-integration.md](unitask-patterns-integration.md).

## UniTask vs Coroutine Migration

```csharp
// ❌ OLD: Coroutine
private IEnumerator LoadSequence()
{
    yield return new WaitForSeconds(1f);
    yield return StartCoroutine(LoadData());
    yield return new WaitForEndOfFrame();
    OnLoadComplete();
}

// ✅ NEW: UniTask
private async UniTask LoadSequenceAsync(CancellationToken ct = default)
{
    await UniTask.Delay(1000, cancellationToken: ct);
    await LoadDataAsync(ct);
    await UniTask.WaitForEndOfFrame(this, ct);
    OnLoadComplete();
}
```

## Anti-Patterns

```csharp
// ❌ BAD: Ignoring CancellationToken
public async UniTask LoadAsync()
{
    await SomeOperationAsync(); // No cancellation support!
}

// ❌ BAD: Using .Result or .GetAwaiter().GetResult()
var data = LoadAsync().GetAwaiter().GetResult(); // Deadlock risk!

// ❌ BAD: Fire-and-forget without Forget()
async UniTask DoWork() { }
DoWork(); // Warning: not awaited

// ✅ GOOD: Explicit fire-and-forget
DoWork().Forget();

// ❌ BAD: Catching all exceptions (including cancellation)
try { await DoWork(ct); }
catch (Exception) { } // Swallows cancellation!

// ✅ GOOD: Catch specific, let cancellation propagate
try { await DoWork(ct); }
catch (OperationCanceledException) { /* Expected */ }
catch (Exception ex) { this.logger.Error(ex.Message); throw; }
```

## Cheat Sheet

| Pattern | Code |
|:--------|:-----|
| Delay | `await UniTask.Delay(1000, cancellationToken: ct)` |
| Next frame | `await UniTask.NextFrame(ct)` |
| Wait condition | `await UniTask.WaitUntil(() => ready, cancellationToken: ct)` |
| Parallel | `await UniTask.WhenAll(task1, task2, task3)` |
| Race | `await UniTask.WhenAny(task, timeout)` |
| Cancel on destroy | `this.GetCancellationTokenOnDestroy()` |
| Fire-and-forget | `DoWorkAsync(ct).Forget()` |
| Suppress cancel | `.SuppressCancellationThrow()` |

**See also:** [unitask-patterns.md](unitask-patterns.md) for Basic Patterns, [unitask-patterns-integration.md](unitask-patterns-integration.md) for Integration & Error Handling.

# Unity Lifecycle & MonoBehaviour Rules

## Initialization Order
```
Awake()     → Self-initialization only. Cache own components. Set defaults.
              NO cross-component access (order undefined).
OnEnable()  → Subscribe to events. Register with systems. Create CancellationTokenSource.
Start()     → Cross-component initialization. Access other objects safely here.
              Heavy async init: kick off with await in Start().
```

## Cleanup Order (symmetric with init)
```
OnDisable() → Unsubscribe events. Stop coroutines. Kill tweens. Cancel + dispose CTS.
OnDestroy() → Dispose native resources. Destroy cloned ScriptableObjects.
              NO accessing other objects (destroy order is undefined).
```

## Enable/Disable Symmetry — MANDATORY
Every `OnEnable` subscription MUST have a matching `OnDisable` unsubscription:
```csharp
private void OnEnable()
{
    _cts = new CancellationTokenSource();
    _playerState.HealthChanged += OnHealthChanged;
    _inputActions.Enable();
    StartCoroutine(_spawnRoutine = SpawnEnemiesRoutine());
}

private void OnDisable()
{
    _cts?.Cancel(); _cts?.Dispose(); _cts = null;
    _playerState.HealthChanged -= OnHealthChanged;
    _inputActions.Disable();
    if (_spawnRoutine != null) { StopCoroutine(_spawnRoutine); _spawnRoutine = null; }
    _activeTween?.Kill();
}
```

## Update Method Rules
- **DO** use `Update()` for input and gameplay logic
- **DO** use `FixedUpdate()` for all physics (Rigidbody, forces, MovePosition)
- **DO** use `LateUpdate()` for camera follow and IK
- **DO NOT** have empty `Update()` / `FixedUpdate()` / `LateUpdate()` — remove them (Unity still calls them)
- **DO NOT** allocate in any update method (see `csharp-perf.md`)

## Async in Unity — Decision Matrix
| Use Case | Solution |
|:---|:---|
| Fire-and-forget in MonoBehaviour | `UniTaskVoid` + `GetCancellationTokenOnDestroy()` |
| Async with result | `async UniTask<T>` |
| Wait one frame | `await UniTask.NextFrame(ct)` |
| Wait seconds | `await UniTask.Delay(ms, cancellationToken: ct)` |
| Load scene with progress | `op.ToUniTask(progress: ..., cancellationToken: ct)` |
| Native Unity 6 (no UniTask) | `async Awaitable` + `Awaitable.NextFrameAsync(ct)` |
| Background thread work | `await UniTask.RunOnThreadPool(...)` or `Awaitable.BackgroundThreadAsync()` |
| Parallel tasks | `await UniTask.WhenAll(t1, t2, t3)` |

## Coroutine Rules
- **DO** store coroutine handle: `_routine = StartCoroutine(MyRoutine())`
- **DO** stop by handle in `OnDisable`: `if (_routine != null) StopCoroutine(_routine)`
- **DO** cache `WaitForSeconds` as a field — never `yield return new WaitForSeconds(1f)` inside a loop
- **DO NOT** start coroutines in `OnDisable` or `OnDestroy`
- **PREFER** UniTask over coroutines for new code — better cancellation and error handling

## ScriptableObject Rules
- **DO** use ScriptableObjects for read-only configuration data
- **DO** `Instantiate()` before any runtime mutation: `_runtime = Instantiate(_baseStats)`
- **DO** `Destroy(_runtime)` in `OnDestroy()` to release the clone
- **DO NOT** modify original SO assets at runtime — changes persist across Play sessions in Editor
- **DO NOT** store scene-bound MonoBehaviour references in ScriptableObjects

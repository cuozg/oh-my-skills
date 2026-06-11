# Lifecycle, Async, Validation, And Errors

Use this file when code depends on Unity callback order, event subscriptions, coroutines, async flows, cancellation, logging, validation, or runtime failure behavior.

## Lifecycle Contracts

Use each callback for a narrow purpose:

| Callback | Standard Use |
| --- | --- |
| `Reset` | Editor-time default references and values when the component is added. |
| `OnValidate` | Clamp serialized values and report authoring errors in the Editor. |
| `Awake` | Self-initialization: cache same-object components, validate required fields, build local data. |
| `OnEnable` | Subscribe to events, start short-lived enabled-state behavior. |
| `Start` | Cross-object binding when all `Awake` calls should have run. |
| `FixedUpdate` | Physics writes and reads that depend on the fixed timestep. |
| `Update` | Per-frame input, timers, and non-physics simulation. |
| `LateUpdate` | Camera follow and work that must run after normal updates. |
| `OnDisable` | Unsubscribe, stop enabled-state routines, release temporary state. |
| `OnDestroy` | Dispose owned resources and long-lived registrations. |

Do not rely on incidental callback order between different GameObjects. If order matters, make it explicit with serialized references, initialization methods, a bootstrapper, or `[DefaultExecutionOrder]`.

## Initialization

Self-contained component setup belongs in `Awake`:

```csharp
private void Awake()
{
    _cachedTransform = transform;
    _rb = GetComponent<Rigidbody>();
}
```

Cross-object setup belongs in `Start` or an explicit composition root:

```csharp
private void Start()
{
    _hud.Bind(_health);
}
```

Avoid `FindAnyObjectByType`, `FindFirstObjectByType`, and scene-wide searches in hot paths. When a find is acceptable during bootstrap, document why a serialized reference or DI binding is not available.

## Subscriptions

Subscribe and unsubscribe at matching lifetimes.

```csharp
private void OnEnable()
{
    _health.Died += HandleDied;
    _input.FirePerformed += HandleFirePerformed;
}

private void OnDisable()
{
    _health.Died -= HandleDied;
    _input.FirePerformed -= HandleFirePerformed;
}
```

Standards:

- Use `OnEnable`/`OnDisable` for subscriptions that should exist only while active.
- Use `Awake`/`OnDestroy` only for subscriptions that must remain while disabled.
- Unsubscribe from static events, event buses, ScriptableObject channels, and input actions.
- Make repeated `OnEnable` calls idempotent; avoid double-subscribe bugs.

## Coroutines

Use coroutines for simple frame-based sequences owned by a MonoBehaviour. Store handles when a routine must be stopped or replaced.

```csharp
private Coroutine _fadeRoutine;

public void PlayFade()
{
    if (_fadeRoutine != null)
    {
        StopCoroutine(_fadeRoutine);
    }

    _fadeRoutine = StartCoroutine(FadeRoutine());
}
```

Rules:

- Do not start unbounded coroutines without a clear stop condition.
- Stop or replace routines when state changes.
- Cache common yield instructions only when the duration is constant and reuse is measurable or repeated.
- Prefer async/await for IO-like flows and coroutines for simple visual/time sequencing when the repo has no async standard.

## Async Stack Choice

Use the async primitive already established by the project.

| Stack | Use When |
| --- | --- |
| Unity `Awaitable` | The local Unity version supports it and the project uses Unity-native async without UniTask. |
| UniTask | The project already depends on it, needs older Unity support, or has UniTask-based infrastructure. |
| `Task` | External .NET/library boundaries, server calls, or code not tied to Unity player loop. |

Do not mix `Awaitable`, UniTask, and `Task` in one gameplay flow unless the boundary is explicit. Check the local Unity version and package manifest before making API claims.

## Cancellation

Every long-lived async path must accept and forward a `CancellationToken`.

```csharp
private async Awaitable PatrolAsync(CancellationToken cancellationToken)
{
    while (!cancellationToken.IsCancellationRequested)
    {
        await MoveToNextPointAsync(cancellationToken);
        await Awaitable.WaitForSecondsAsync(1f, cancellationToken);
    }
}
```

For MonoBehaviours, use the repo's established lifetime token pattern. If `destroyCancellationToken` exists in the local Unity version, prefer it for object-owned async work. For UniTask projects, use the project's cancellation helpers consistently.

Treat `OperationCanceledException` as a normal exit path unless cancellation indicates a product error.

## Async Error Handling

`async void` is only acceptable for Unity/UI event handlers. Catch and log inside it because callers cannot observe failures.

```csharp
private async void HandleClicked()
{
    try
    {
        await SaveAsync(destroyCancellationToken);
    }
    catch (OperationCanceledException)
    {
        // Normal during destruction or navigation.
    }
    catch (Exception ex)
    {
        Debug.LogException(ex, this);
    }
}
```

For normal async methods, return `Awaitable`, `UniTask`, `Task`, or a result type. Avoid fire-and-forget unless there is a documented owner, cancellation path, and exception sink.

## Validation

Validate at the boundary closest to the bad data:

- Inspector fields: `OnValidate`, custom editor validation, or build-time validation.
- Runtime config/save/API data: schema or explicit parser validation before applying state.
- Public methods: guard invalid arguments when the caller can reasonably pass bad input.
- Internal invariants: `Debug.Assert` or fail-fast exceptions in non-player-facing paths.

```csharp
private void OnValidate()
{
    _maxHealth = Mathf.Max(1f, _maxHealth);
    _spawnRadius = Mathf.Max(0f, _spawnRadius);
}
```

Prefer clamping for authoring convenience when the correction is obvious. Prefer errors when automatic correction would hide a broken setup.

## Error Handling

Use narrow try/catch blocks around the operation that can fail.

```csharp
public SaveData Load(string path)
{
    try
    {
        string json = File.ReadAllText(path);
        return JsonUtility.FromJson<SaveData>(json);
    }
    catch (FileNotFoundException)
    {
        return SaveData.NewGame();
    }
    catch (Exception ex)
    {
        Debug.LogException(ex);
        return SaveData.NewGame();
    }
}
```

Standards:

- Never silently swallow exceptions.
- Catch specific exceptions when recovery differs by failure.
- Do not catch just to rethrow without context.
- Include Unity object context in logs when available: `Debug.LogError(message, this)`.
- Do not expose secrets, auth tokens, device identifiers, or raw server payloads in user-facing errors.
- Do not let recoverable errors corrupt state; keep old valid state until new data is validated.

## Logging

Use logging as diagnostic evidence, not noise.

| API | Use |
| --- | --- |
| `Debug.Log` | Important lifecycle or one-time diagnostic info. |
| `Debug.LogWarning` | Recoverable misconfiguration or fallback path. |
| `Debug.LogError` | Broken setup or failed operation that prevents expected behavior. |
| `Debug.LogException` | Unexpected exception with stack trace. |
| `Debug.Assert` | Developer invariant that should never fail. |

Gate noisy diagnostics behind compile symbols or local debug flags. Do not leave per-frame logs in production code.

## Conditional Compilation

Use platform symbols at the boundary, not scattered through business logic.

```csharp
#if UNITY_WEBGL && !UNITY_EDITOR
    storage = new WebGlSaveStorage();
#else
    storage = new FileSaveStorage();
#endif
```

Keep platform-specific implementations behind an interface when the branch affects more than a few lines.

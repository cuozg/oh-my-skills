# Lifecycle, Async & Error Handling

> Consolidated from: lifecycle.md, lifecycle-advanced.md, async.md, async-advanced.md, error-handling.md, error-handling-advanced.md

---

## Unity Lifecycle

### Execution Order

```
Awake()           — first call, once per instance
OnEnable()        — each time object becomes active
Start()           — before first Update, after all Awake
  ┌─ FixedUpdate()   — physics tick (default 50Hz)
  │  Update()        — every frame
  │  LateUpdate()    — after all Updates (camera follow here)
  └─ repeat
OnDisable()       — each time object becomes inactive
OnDestroy()       — when destroyed or scene unloads
```

### Awake vs Start

```csharp
public sealed class Enemy : MonoBehaviour
{
    Rigidbody _rb;
    HealthBar _healthBar;

    void Awake() => _rb = GetComponent<Rigidbody>(); // self-init only

    void Start()
    {
        _healthBar = FindAnyObjectByType<HealthBar>(); // cross-object refs
        _healthBar.Bind(this);
    }
}
```

| Use | Awake | Start |
|-----|-------|-------|
| GetComponent | ✅ | ✅ |
| Cross-object refs | ❌ | ✅ |
| Called if disabled | ✅ | ❌ |
| Order guarantee | None | After all Awake |

### FixedUpdate for Physics

```csharp
// ✅ Physics in FixedUpdate — deterministic
void FixedUpdate()
{
    _rb.AddForce(Vector3.up * _thrust);
    _rb.MovePosition(_rb.position + _velocity * Time.fixedDeltaTime);
}

// ❌ Physics in Update — frame-rate dependent
void Update() { _rb.AddForce(Vector3.up * _thrust); }
```

### Subscribe Pattern — OnEnable/OnDisable

```csharp
void OnEnable()
{
    _health.OnDeath += HandleDeath;
    InputActions.Player.Jump.performed += OnJump;
}

void OnDisable()
{
    _health.OnDeath -= HandleDeath;
    InputActions.Player.Jump.performed -= OnJump;
}
```

### Coroutine Lifecycle

```csharp
Coroutine _moveRoutine;
void StartMoving()
{
    if (_moveRoutine != null) StopCoroutine(_moveRoutine);
    _moveRoutine = StartCoroutine(MoveRoutine());
}
IEnumerator MoveRoutine()
{
    while (Vector3.Distance(transform.position, _target) > 0.1f)
    {
        transform.position = Vector3.MoveTowards(transform.position, _target, _speed * Time.deltaTime);
        yield return null;
    }
}
// Stops when: object disabled, destroyed, or StopCoroutine
```

### Deprecated Find Methods

```csharp
// ❌ Deprecated — slow, sorts by InstanceID
FindObjectOfType<T>();
FindObjectsOfType<T>();

// ✅ Replacement — faster, explicit sort control
FindAnyObjectByType<T>();                           // no guaranteed order, fastest
FindFirstObjectByType<T>();                         // deterministic order, slower
FindObjectsByType<T>(FindObjectsSortMode.None);     // batch find, skip sort for speed
```

### DefaultExecutionOrder

```csharp
// Negative = runs earlier, positive = runs later
[DefaultExecutionOrder(-100)] public sealed class GameManager : MonoBehaviour { }
[DefaultExecutionOrder(-50)]  public sealed class InputManager : MonoBehaviour { }
[DefaultExecutionOrder(100)]  public sealed class UIManager : MonoBehaviour { }
```

### Application Lifecycle Callbacks

```csharp
void OnApplicationFocus(bool hasFocus)
{
    if (!hasFocus) PauseAudio();
    else ResumeAudio();
}

void OnApplicationPause(bool pauseStatus)
{
    if (pauseStatus) SaveProgress();
}

void OnApplicationQuit()
{
    SaveFinalState();
    CleanupNetworkConnections();
}
```

| Callback | Mobile | Desktop | Editor |
|----------|--------|---------|--------|
| `OnApplicationFocus` | App switch | Alt-tab | Lose focus |
| `OnApplicationPause` | Home/call | Minimize | Play→Pause |
| `OnApplicationQuit` | Kill app | Close window | Stop play |

### Visibility Callbacks

```csharp
void OnBecameVisible() => _isOnScreen = true;
void OnBecameInvisible() => _isOnScreen = false;

// Use for: LOD toggling, disabling expensive updates on off-screen objects
void Update()
{
    if (!_isOnScreen) return;
    ExpensiveAICalculation();
}
```

### Reset() — Inspector Defaults

```csharp
// Called in Editor when component is first added or Reset is clicked
void Reset()
{
    _speed = 5f;
    _rb = GetComponent<Rigidbody>();
    _audioSrc = GetComponent<AudioSource>();
}
```

---

## Async Patterns

### Pick One Async Stack Per Project

- Use the async primitive already established in the repo.
- If the project uses Unity's built-in `Awaitable`, stay consistent with it.
- If the project already uses UniTask or targets older Unity versions, keep UniTask.
- Use plain `Task` mainly at library or external API boundaries.
- Avoid mixing `Task`, `UniTask`, and `Awaitable` in the same gameplay flow without a clear boundary.

### UniTask Example

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

### Awaitable Example

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

### Cancellation — Always Pass It Through

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

If the project uses UniTask, apply the same rule: every long-lived async path should accept and forward a `CancellationToken`.

### Async Void — Event Handlers Only

```csharp
// Acceptable for Unity event handlers only
async void OnButtonClick()
{
    await SaveGameAsync(destroyCancellationToken);
}

// Avoid for normal methods
async Awaitable LoadDataAsync() { }
```

### Parallel Execution

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

### Error Handling In Async

```csharp
async UniTask<bool> TrySaveAsync(CancellationToken ct)
{
    try
    {
        await WriteFile(_savePath, _data, ct);
        return true;
    }
    catch (OperationCanceledException)
    {
        return false; // normal cancellation path
    }
    catch (System.Exception ex)
    {
        Debug.LogException(ex);
        return false;
    }
}

// AsyncOperation -> UniTask: await SceneManager.LoadSceneAsync("Level1");
// Coroutine -> UniTask: await SomeLegacyCoroutine().ToUniTask(cancellationToken: ct);
// UnityWebRequest -> UniTask: await UnityWebRequest.Get(url).SendWebRequest().WithCancellation(ct);
```

### Awaitable — Built-In Unity Async

Use `Awaitable` in Unity versions that ship it, including Unity 6. It is a strong default for Unity-native async operations when the project does not already standardize on UniTask.

```csharp
await Awaitable.BackgroundThreadAsync();
var result = HeavyComputation();
await Awaitable.MainThreadAsync();
ApplyResult(result);
```

### Awaitable Vs UniTask Vs Task

| Concern | Awaitable | UniTask | Task |
|---------|-----------|---------|------|
| Unity-native async | Strong fit | Strong fit | Fine but heavier |
| Extra dependency | None | Package dependency | None |
| Multiple await on same result | No — do not reuse same instance | Usually fine | Fine |
| Third-party .NET interop | Bridge as needed | Bridge as needed | Best fit |
| Older Unity support | Verify local version | Good when repo already uses it | Works broadly |

Important: official Unity docs note that `Awaitable` instances are pooled, so a single instance is not safe to await multiple times.

### Guidance

- Prefer `Awaitable` for Unity-native async in projects that already use it.
- Prefer UniTask when the repo already uses it or needs older-version support.
- Prefer `Task` for external library interop or APIs that already expose `Task`.
- Do not convert a codebase to a new async stack opportunistically inside an unrelated feature.

### Version Notes

- `destroyCancellationToken` exists on recent Unity versions; verify exact availability before making a hard version claim.
- Do not describe `Awaitable` as "Unity 6 only". Confirm against the official docs for the local editor version.

---

## Error Handling

### Narrow Try/Catch

```csharp
// ✅ Catch specific exceptions, minimal scope
public SaveData LoadSave(string path)
{
    try
    {
        var json = File.ReadAllText(path);
        return JsonUtility.FromJson<SaveData>(json);
    }
    catch (FileNotFoundException)
    {
        Debug.LogWarning($"Save file not found: {path}");
        return new SaveData();
    }
    catch (System.Exception ex) { Debug.LogException(ex); return new SaveData(); }
}

// ❌ Never swallow exceptions silently
try { DoSomething(); }
catch { } // NO — hides bugs
```

### Debug Logging Levels

```csharp
Debug.Log("Game started");                                  // info — normal flow
Debug.LogWarning("Config missing, using defaults");         // recoverable issue
Debug.LogError($"Failed to spawn enemy at {position}");     // broke, can continue
try { riskyOp(); }
catch (System.Exception ex) { Debug.LogException(ex, this); } // preserves stack trace
```

### Debug.Assert for Invariants

```csharp
void Awake()
{
    _rb = GetComponent<Rigidbody>();
    Debug.Assert(_rb != null, "Missing Rigidbody", this);
    Debug.Assert(_maxHealth > 0, $"Invalid MaxHealth: {_maxHealth}", this);
}

void SetWave(int index)
{
    Debug.Assert(index >= 0 && index < _waves.Length, $"Wave index OOB: {index}");
}
```

### Conditional Compilation

```csharp
#if UNITY_EDITOR
void OnValidate()
{
    if (_speed < 0) Debug.LogWarning("Speed is negative", this);
    if (_prefab == null) Debug.LogError("Prefab not assigned", this);
}
#endif

// Conditional attribute — call stripped from non-editor builds
[System.Diagnostics.Conditional("UNITY_EDITOR")]
void DebugDrawPath(Vector3[] points)
{
    for (int i = 0; i < points.Length - 1; i++)
        Debug.DrawLine(points[i], points[i + 1], Color.red, 2f);
}
```

### Fail-Fast Patterns

```csharp
// Throw on invalid args in constructors/factories
public static Projectile Create(ProjectileConfig config)
{
    if (config == null) throw new System.ArgumentNullException(nameof(config));
    if (config.Speed <= 0) throw new System.ArgumentOutOfRangeException(nameof(config.Speed));
    var proj = Instantiate(config.Prefab);
    proj.Init(config);
    return proj;
}

// Guard clause — return early for recoverable cases
public void Heal(float amount)
{
    if (amount <= 0f) return;
    if (!_isAlive) return;
    _health = Mathf.Min(_health + amount, _maxHealth);
}
```

### OnValidate — Editor-Time Validation

```csharp
#if UNITY_EDITOR
void OnValidate()
{
    if (_speed < 0) Debug.LogWarning("Speed cannot be negative", this);
    if (_prefab == null) Debug.LogError("Prefab must be assigned", this);
    if (_waypoints != null && _waypoints.Length == 0)
        Debug.LogWarning("Waypoints array is empty", this);

    // Auto-fix: clamp values
    _speed = Mathf.Max(0f, _speed);
    _maxHealth = Mathf.Max(1f, _maxHealth);
}
#endif
```

**Rules:**
- Wrap in `#if UNITY_EDITOR` — `OnValidate` is editor-only but compiles in builds
- Use `Debug.LogWarning` for soft issues, `Debug.LogError` for required fields
- Auto-clamp numeric values where safe
- Never call `GetComponent` in `OnValidate` on prefabs (may not be instantiated)

### Custom Exception Types

```csharp
public class GameStateException : System.Exception
{
    public GameStateException(string message) : base(message) { }
    public GameStateException(string message, System.Exception inner) : base(message, inner) { }
}

// Usage — typed exceptions for specific error domains
public void TransitionTo(GameState next)
{
    if (!_validTransitions.Contains((_current, next)))
        throw new GameStateException($"Invalid transition: {_current} → {next}");
    _current = next;
}
```

### Security — Input & Data Validation

```csharp
// ✅ Validate all external input (network, file, user text)
public void SetPlayerName(string name)
{
    if (string.IsNullOrWhiteSpace(name)) return;
    if (name.Length > 32) name = name[..32]; // truncate
    _name = SanitizeString(name);
}

static string SanitizeString(string input)
    => System.Text.RegularExpressions.Regex.Replace(input, @"[<>&""']", "");

// ✅ Validate deserialized save data — never trust file contents
public static SaveData LoadSave(string json)
{
    var data = JsonUtility.FromJson<SaveData>(json);
    data.Health = Mathf.Clamp(data.Health, 0f, data.MaxHealth);
    data.Level = Mathf.Clamp(data.Level, 1, 999);
    data.Gold = Mathf.Max(0, data.Gold);
    return data;
}

// ⚠️ PlayerPrefs — stored as plain text, trivially editable
// NEVER store: auth tokens, purchase state, progression unlocks in PlayerPrefs
// Use encrypted file or server-side validation for sensitive data

// ✅ Rate-limit player actions to prevent exploit spam
float _lastActionTime;
const float ActionCooldown = 0.1f;

public bool TryExecuteAction()
{
    if (Time.time - _lastActionTime < ActionCooldown) return false;
    _lastActionTime = Time.time;
    return true;
}
```

**Security Rules:**
- Validate all data from files, network, and user input
- Clamp numeric values to sane ranges after deserialization
- Never trust client-side state for authoritative game logic (multiplayer)
- Sanitize strings displayed in UI to prevent injection
- Use `Application.persistentDataPath` for saves — never hardcode paths
- Log security-relevant failures with `Debug.LogWarning`, not silently

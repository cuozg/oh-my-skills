# Unity C# Implementation Patterns

Best practices for writing clean, performant, and maintainable C# code in Unity 6 (6000.x).

## 1. Asynchronous Logic (Awaitable)

Unity 6's `Awaitable` is preferred over Coroutines for complex async flows.

```csharp
/// <summary>
/// Fade out a CanvasGroup over duration, then disable the GameObject.
/// </summary>
private async Awaitable FadeOutAsync(CanvasGroup group, float duration)
{
    float elapsed = 0f;
    float startAlpha = group.alpha;

    while (elapsed < duration)
    {
        await Awaitable.NextFrameAsync();

        // MANDATORY: check after every await — object may be destroyed
        if (this == null) return;

        elapsed += Time.deltaTime;
        group.alpha = Mathf.Lerp(startAlpha, 0f, elapsed / duration);
    }

    group.alpha = 0f;
    gameObject.SetActive(false);
}
```

**Rules:**
- `if (this == null) return;` after every `await` — no exceptions
- Use `async Awaitable` for MonoBehaviour methods, `async Task` for pure C#
- Never use `async void` except on Unity event methods (e.g., `async void Start()`)

## 2. Event-Driven Architecture (Observer Pattern)

Use `Action` or `UnityEvent` to decouple systems. Always pair subscribe/unsubscribe.

```csharp
/// <summary>
/// Tracks player health and broadcasts changes to listeners.
/// </summary>
public class PlayerHealth : MonoBehaviour
{
    /// <summary>Fired when health changes. Param: current health value.</summary>
    public event Action<int> OnHealthChanged;

    /// <summary>Inspector-configurable death event for designers.</summary>
    [Header("Events")]
    public UnityEngine.Events.UnityEvent OnDeath;

    [SerializeField] private int _maxHealth = 100;
    private int _currentHealth;

    private void Awake()
    {
        _currentHealth = _maxHealth;
    }

    /// <summary>
    /// Apply damage, clamp to zero, notify listeners.
    /// </summary>
    public void TakeDamage(int damage)
    {
        if (damage <= 0) return; // Guard: ignore zero/negative damage

        _currentHealth = Mathf.Max(0, _currentHealth - damage);
        OnHealthChanged?.Invoke(_currentHealth);

        if (_currentHealth <= 0) OnDeath?.Invoke();
    }
}

/// <summary>
/// Listens to PlayerHealth and updates the health bar UI.
/// </summary>
public class HealthBarUI : MonoBehaviour
{
    [SerializeField] private PlayerHealth _playerHealth;
    [SerializeField] private Slider _healthSlider;

    // Subscribe in OnEnable, unsubscribe in OnDisable — prevents memory leaks
    private void OnEnable() => _playerHealth.OnHealthChanged += UpdateBar;
    private void OnDisable() => _playerHealth.OnHealthChanged -= UpdateBar;

    private void UpdateBar(int currentHealth)
    {
        _healthSlider.value = currentHealth;
    }
}
```

## 3. Persistent Systems (Singleton Pattern)

Use singletons sparingly for truly global managers.

```csharp
/// <summary>
/// Global game manager — persists across scene loads.
/// Only one instance allowed; duplicates self-destruct.
/// </summary>
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```

## 4. State Management (State Machine)

For complex behavior like Player or AI states.

```csharp
public enum PlayerState { Idle, Walking, Jumping, Attacking }

/// <summary>
/// Manages player state transitions with enter/exit callbacks.
/// </summary>
public class PlayerController : MonoBehaviour
{
    private PlayerState _currentState;

    /// <summary>Transition to a new state, executing exit/enter logic.</summary>
    public void ChangeState(PlayerState newState)
    {
        if (_currentState == newState) return; // Guard: no-op if same state

        ExitState(_currentState);
        _currentState = newState;
        EnterState(_currentState);
    }

    private void ExitState(PlayerState state)
    {
        // Clean up state-specific resources
    }

    private void EnterState(PlayerState state)
    {
        // Initialize state-specific behavior
    }
}
```

## 5. ScriptableObject Configuration

Externalize tuning data — never hardcode gameplay values.

```csharp
/// <summary>
/// Character stats configured by designers in the Editor.
/// Clone at runtime to prevent persistent modifications.
/// </summary>
[CreateAssetMenu(fileName = "CharacterStats", menuName = "Game/Character Stats")]
public class CharacterStats : ScriptableObject
{
    [Header("Combat")]
    [Tooltip("Base damage before modifiers")]
    public int BaseDamage = 10;

    [Tooltip("Attack cooldown in seconds")]
    public float AttackCooldown = 0.5f;

    [Header("Movement")]
    [Tooltip("Maximum movement speed in units/second")]
    public float MoveSpeed = 5f;
}

/// <summary>
/// Uses cloned ScriptableObject to avoid modifying the asset.
/// </summary>
public class Character : MonoBehaviour
{
    [SerializeField] private CharacterStats _baseStats;
    private CharacterStats _runtimeStats;

    private void Awake()
    {
        // Clone to prevent modifying the shared asset
        _runtimeStats = Instantiate(_baseStats);
    }

    private void OnDestroy()
    {
        // Clean up cloned instance
        if (_runtimeStats != null) Destroy(_runtimeStats);
    }
}
```

## 6. Object Pooling

Mandatory for frequently spawned objects (projectiles, VFX, UI elements).

```csharp
/// <summary>
/// Generic object pool using Unity's built-in ObjectPool.
/// Eliminates GC spikes from Instantiate/Destroy in hot paths.
/// </summary>
public class ProjectilePool : MonoBehaviour
{
    [SerializeField] private Projectile _prefab;
    [SerializeField] private int _defaultCapacity = 20;
    [SerializeField] private int _maxSize = 100;

    private ObjectPool<Projectile> _pool;

    private void Awake()
    {
        _pool = new ObjectPool<Projectile>(
            createFunc: () => Instantiate(_prefab),
            actionOnGet: p => p.gameObject.SetActive(true),
            actionOnRelease: p => p.gameObject.SetActive(false),
            actionOnDestroy: p => Destroy(p.gameObject),
            defaultCapacity: _defaultCapacity,
            maxSize: _maxSize
        );
    }

    /// <summary>Get a pooled projectile. Caller must return via ReturnToPool.</summary>
    public Projectile Get() => _pool.Get();

    /// <summary>Return projectile to pool for reuse.</summary>
    public void ReturnToPool(Projectile p) => _pool.Release(p);
}
```

## 7. Performance Best Practices

### Cache Everything

```csharp
public class OptimizedBehavior : MonoBehaviour
{
    // Cache in Awake — never call GetComponent in Update
    private Rigidbody _rb;
    private Camera _mainCamera;
    private Transform _cachedTransform;

    private void Awake()
    {
        _rb = GetComponent<Rigidbody>();
        _mainCamera = Camera.main;
        _cachedTransform = transform; // Even transform benefits from caching
    }
}
```

### Avoid Allocations in Hot Paths

```csharp
// BAD: Allocates every frame
private void Update()
{
    var hits = Physics.RaycastAll(transform.position, Vector3.forward);        // new array
    var filtered = hits.Where(h => h.distance < 10f).ToList();                 // LINQ + ToList
    debugText.text = $"Hits: {filtered.Count}";                                // string alloc
}

// GOOD: Pre-allocated, zero GC
private readonly RaycastHit[] _hitBuffer = new RaycastHit[32];
private readonly StringBuilder _sb = new StringBuilder(64);

private void Update()
{
    int hitCount = Physics.RaycastNonAlloc(transform.position, Vector3.forward, _hitBuffer);

    int nearCount = 0;
    for (int i = 0; i < hitCount; i++)
    {
        if (_hitBuffer[i].distance < MaxRaycastDistance) nearCount++;
    }

    _sb.Clear();
    _sb.Append("Hits: ");
    _sb.Append(nearCount);
    debugText.SetText(_sb);
}

private const float MaxRaycastDistance = 10f;
```

### Summary Table

| Avoid | Do Instead | Why |
|:------|:-----------|:----|
| `GetComponent` in Update | Cache in `Awake` | Reflection-based lookup every frame |
| `Camera.main` in loops | Cache reference | FindGameObjectWithTag per access |
| String concat in Update | `StringBuilder` | New string allocation per frame |
| `new` in hot paths | Object pooling / pre-allocate | GC pressure → frame spikes |
| Deep inheritance | Composition | Rigid, hard to modify |
| LINQ in Update | Manual loops | Hidden allocations |
| `Find`/`FindObjectOfType` | `[SerializeField]` | O(n) scene traversal |

## 8. Error Handling

```csharp
/// <summary>
/// Safe data loading with fallback behavior.
/// </summary>
private async Awaitable<PlayerData> LoadPlayerDataAsync(string playerId)
{
    try
    {
        var json = await NetworkManager.Instance.FetchAsync($"/api/player/{playerId}");
        if (this == null) return null; // Null check after await

        return JsonUtility.FromJson<PlayerData>(json);
    }
    catch (Exception ex)
    {
#if UNITY_EDITOR
        Debug.LogError($"[PlayerLoader] Failed to load data for {playerId}: {ex.Message}");
#endif
        // Return safe default rather than crashing
        return PlayerData.CreateDefault();
    }
}
```

## 9. Cleanup & Disposal

```csharp
/// <summary>
/// Demonstrates proper cleanup of all resource types.
/// </summary>
public class ManagedComponent : MonoBehaviour
{
    private Coroutine _updateCoroutine;
    private DG.Tweening.Tween _activeTween;

    private void OnEnable()
    {
        EventBus.OnGameEvent += HandleGameEvent;
        _updateCoroutine = StartCoroutine(PeriodicUpdate());
    }

    private void OnDisable()
    {
        // Unsubscribe events
        EventBus.OnGameEvent -= HandleGameEvent;

        // Stop coroutines
        if (_updateCoroutine != null)
        {
            StopCoroutine(_updateCoroutine);
            _updateCoroutine = null;
        }

        // Kill tweens
        _activeTween?.Kill();
        _activeTween = null;
    }

    private void OnDestroy()
    {
        // Dispose native resources, cloned SOs, etc.
    }
}
```

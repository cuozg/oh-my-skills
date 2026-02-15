# Unity C# Patterns

## 1. Async (Awaitable)
```csharp
private async Awaitable FadeOutAsync(CanvasGroup group, float dur)
{
    float t = 0f, startAlpha = group.alpha;
    while (t < dur)
    {
        await Awaitable.NextFrameAsync();
        if (this == null) return; // MANDATORY after every await
        t += Time.deltaTime;
        group.alpha = Mathf.Lerp(startAlpha, 0f, t / dur);
    }
    group.alpha = 0f; gameObject.SetActive(false);
}
```
Rules: `if (this == null) return;` after every await | `async Awaitable` for MonoBehaviour, `async Task` for pure C# | Never `async void` except Unity events

## 2. Observer
```csharp
public class PlayerHealth : MonoBehaviour
{
    public event Action<int> OnHealthChanged;
    [SerializeField] private int _maxHealth = 100;
    private int _currentHealth;
    private void Awake() => _currentHealth = _maxHealth;
    public void TakeDamage(int dmg)
    {
        if (dmg <= 0) return;
        _currentHealth = Mathf.Max(0, _currentHealth - dmg);
        OnHealthChanged?.Invoke(_currentHealth);
    }
}
// Subscribe OnEnable, unsubscribe OnDisable
public class HealthBarUI : MonoBehaviour
{
    [SerializeField] private PlayerHealth _health;
    [SerializeField] private Slider _slider;
    private void OnEnable() => _health.OnHealthChanged += UpdateBar;
    private void OnDisable() => _health.OnHealthChanged -= UpdateBar;
    private void UpdateBar(int hp) => _slider.value = hp;
}
```

## 3. Singleton
```csharp
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }
    private void Awake()
    {
        if (Instance != null && Instance != this) { Destroy(gameObject); return; }
        Instance = this; DontDestroyOnLoad(gameObject);
    }
}
```

## 4. State Machine
```csharp
public enum PlayerState { Idle, Walking, Jumping, Attacking }
public class PlayerController : MonoBehaviour
{
    private PlayerState _state;
    public void ChangeState(PlayerState s)
    {
        if (_state == s) return;
        ExitState(_state); _state = s; EnterState(s);
    }
    private void ExitState(PlayerState s) { }
    private void EnterState(PlayerState s) { }
}
```

## 5. SO Config
```csharp
[CreateAssetMenu(menuName = "Game/Character Stats")]
public class CharacterStats : ScriptableObject
{
    public int BaseDamage = 10;
    public float AttackCooldown = 0.5f, MoveSpeed = 5f;
}
public class Character : MonoBehaviour
{
    [SerializeField] private CharacterStats _baseStats;
    private CharacterStats _runtime;
    private void Awake() => _runtime = Instantiate(_baseStats); // Clone!
    private void OnDestroy() { if (_runtime) Destroy(_runtime); }
}
```

## 6. Object Pool
```csharp
public class ProjectilePool : MonoBehaviour
{
    [SerializeField] private Projectile _prefab;
    [SerializeField] private int _capacity = 20, _maxSize = 100;
    private ObjectPool<Projectile> _pool;
    private void Awake() => _pool = new ObjectPool<Projectile>(
        () => Instantiate(_prefab), p => p.gameObject.SetActive(true),
        p => p.gameObject.SetActive(false), p => Destroy(p.gameObject),
        defaultCapacity: _capacity, maxSize: _maxSize);
    public Projectile Get() => _pool.Get();
    public void Return(Projectile p) => _pool.Release(p);
}
```

## 7. Performance
```csharp
private Rigidbody _rb; private Camera _cam; private Transform _t;
private void Awake() { _rb = GetComponent<Rigidbody>(); _cam = Camera.main; _t = transform; }
// Zero-alloc hot path
private readonly RaycastHit[] _hits = new RaycastHit[32];
private void Update()
{
    int n = Physics.RaycastNonAlloc(_t.position, Vector3.forward, _hits);
    int near = 0;
    for (int i = 0; i < n; i++) if (_hits[i].distance < 10f) near++;
}
```
| Avoid | Do |
|:------|:---|
| `GetComponent` in Update | Cache in Awake |
| `Camera.main` in loops | Cache ref |
| String concat in Update | StringBuilder |
| `new` in hot paths | Pool/pre-alloc |
| LINQ in Update | Manual loops |
| `Find`/`FindObjectOfType` | `[SerializeField]` |

## 8. Error Handling
```csharp
private async Awaitable<PlayerData> LoadAsync(string id)
{
    try {
        var json = await NetworkManager.Instance.FetchAsync($"/api/player/{id}");
        if (this == null) return null;
        return JsonUtility.FromJson<PlayerData>(json);
    } catch (Exception ex) {
        Debug.LogError($"[PlayerLoader] {ex.Message}");
        return PlayerData.CreateDefault();
    }
}
```

## 9. Cleanup
```csharp
public class ManagedComponent : MonoBehaviour
{
    private Coroutine _co; private DG.Tweening.Tween _tween;
    private void OnEnable() { EventBus.OnGameEvent += Handle; _co = StartCoroutine(Tick()); }
    private void OnDisable()
    {
        EventBus.OnGameEvent -= Handle;
        if (_co != null) { StopCoroutine(_co); _co = null; }
        _tween?.Kill(); _tween = null;
    }
    private void OnDestroy() { /* Dispose native resources, cloned SOs */ }
}
```

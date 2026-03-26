# Performance, Collections, Pooling & Serialization

> Consolidated from: collections.md, collections-advanced.md, linq.md, object-pooling.md, object-pooling-advanced.md, serialization.md

---

## Collections

### Choosing the Right Collection

| Collection | Use When | Hot Path OK |
|------------|----------|-------------|
| `T[]` | Fixed size, serialized fields | ✅ |
| `List<T>` | Dynamic size, frequent add/remove | ✅ |
| `Dictionary<K,V>` | Key-based lookup | ✅ |
| `HashSet<T>` | Contains checks, unique items | ✅ |
| `Queue<T>` | FIFO processing | ✅ |
| `Stack<T>` | LIFO / undo systems | ✅ |
| `ReadOnlyCollection<T>` | Public exposure of internal list | ✅ |
| `NativeArray<T>` | Jobs / Burst | ✅ |
| `LinkedList<T>` | Rare — frequent mid-insert | ⚠️ |

### Array for Serialized Fields

```csharp
[SerializeField] Transform[] _spawnPoints;
[SerializeField] AudioClip[] _footstepSounds;

// Random pick — no allocation
var clip = _footstepSounds[Random.Range(0, _footstepSounds.Length)];
```

### Pre-Allocate Lists

```csharp
var nearby = new List<Enemy>(32);

// Reuse list to avoid GC
readonly List<Collider> _overlapResults = new(16);

void FindNearby()
{
    _overlapResults.Clear();
    int count = Physics.OverlapSphereNonAlloc(transform.position, _radius, _hitBuffer);
}
```

### Dictionary for Lookups

```csharp
readonly Dictionary<string, AbilityData> _abilities = new();

public AbilityData GetAbility(string id)
    => _abilities.TryGetValue(id, out var data) ? data : null;

// Build lookup from array at init
void Awake()
{
    foreach (var item in _itemDatabase)
        _lookup[item.Id] = item;
}
```

### HashSet for Contains

```csharp
readonly HashSet<int> _unlockedLevels = new();
public bool IsUnlocked(int level) => _unlockedLevels.Contains(level);
```

### ReadOnlyCollection for Public API

```csharp
readonly List<Enemy> _enemies = new();
public IReadOnlyList<Enemy> Enemies => _enemies;
```

### Performance-Critical Patterns

```csharp
// ✅ CompareTag — no GC alloc (string == allocates)
if (other.CompareTag("Player")) { }
// ❌ if (other.tag == "Player") { }  // allocates string

// ✅ Cache Camera.main — calls FindGameObjectWithTag internally
Camera _mainCam;
void Awake() => _mainCam = Camera.main;

// ✅ Cache WaitForSeconds — avoid per-yield allocation
static readonly WaitForSeconds Wait1s = new(1f);
static readonly WaitForSeconds WaitHalf = new(0.5f);
yield return Wait1s;

// ✅ Cache transform — property accessor has overhead in tight loops
Transform _cachedTransform;
void Awake() => _cachedTransform = transform;

// ✅ sqrMagnitude — avoids sqrt
if ((a - b).sqrMagnitude < radius * radius) { }
// ❌ if (Vector3.Distance(a, b) < radius) { }  // sqrt per call

// ✅ SetPositionAndRotation — single internal call
transform.SetPositionAndRotation(pos, rot);
// ❌ transform.position = pos; transform.rotation = rot;  // two calls

// ❌ Never use SendMessage/BroadcastMessage — slow reflection, no compile-time safety
// ✅ Use interfaces or direct references instead
```

---

## Advanced Collections

### NativeArray for Jobs

```csharp
using Unity.Collections;
var positions = new NativeArray<Vector3>(count, Allocator.TempJob);
// ... schedule job ...
positions.Dispose(); // MUST dispose — no GC
```

### Span<T> and Memory<T> — Zero-Alloc Slicing

```csharp
void ProcessDamageValues(Span<float> damages)
{
    for (int i = 0; i < damages.Length; i++)
        damages[i] *= _multiplier;
}

// Usage with stackalloc
Span<float> buffer = stackalloc float[4];
buffer[0] = 10f; buffer[1] = 20f;
ProcessDamageValues(buffer);

// Slice existing array without allocation
float[] allDamages = GetDamageArray();
ProcessDamageValues(allDamages.AsSpan(0, 4));
```

### ArrayPool<T> — Reusable Buffers

```csharp
using System.Buffers;

var buffer = ArrayPool<RaycastHit>.Shared.Rent(64);
try
{
    int count = Physics.RaycastNonAlloc(ray, buffer);
    for (int i = 0; i < count; i++) ProcessHit(buffer[i]);
}
finally
{
    ArrayPool<RaycastHit>.Shared.Return(buffer);
}
```

### NativeContainers — Jobs & Burst

| Container | Use | Thread Safety |
|-----------|-----|---------------|
| `NativeArray<T>` | Fixed-size buffer | Safety checks |
| `NativeList<T>` | Dynamic-size buffer | Single writer |
| `NativeHashMap<K,V>` | Key-value lookup in jobs | `.AsParallelWriter()` |
| `NativeQueue<T>` | FIFO in jobs | `.AsParallelWriter()` |
| `NativeParallelHashMap<K,V>` | Concurrent writes | Built-in parallel |

```csharp
using Unity.Collections;

var positions = new NativeList<float3>(128, Allocator.TempJob);
positions.Add(new float3(1, 0, 0));
// ... schedule job ...
positions.Dispose(); // MUST dispose
```

**Rule:** All NativeContainers MUST be disposed. Use `Allocator.TempJob` for single-frame, `Allocator.Persistent` for long-lived.

---

## LINQ Usage

### When to Use

| Context | LINQ OK? | Reason |
|---------|----------|--------|
| `Awake()` / `Start()` | ✅ | One-time init |
| `OnEnable()` | ✅ | Infrequent |
| Editor scripts | ✅ | No runtime cost |
| `Update()` / `FixedUpdate()` | ❌ | Allocates every frame |
| `OnTriggerStay()` | ❌ | Hot path |
| Pooled object reset | ⚠️ | Depends on frequency |

### Efficient LINQ Patterns

```csharp
// ✅ .First(predicate) — single pass
var boss = enemies.First(e => e.IsBoss);

// ❌ .Where().First() — unnecessary intermediate
var boss = enemies.Where(e => e.IsBoss).First();

// ✅ .FirstOrDefault() — no exception on empty
var boss = enemies.FirstOrDefault(e => e.IsBoss);

// ✅ .Any() over .Count() > 0
if (enemies.Any(e => e.IsAlive)) { }
```

### Init-Time LINQ — Acceptable

```csharp
void Start()
{
    _enemyLookup   = _enemies.ToDictionary(e => e.Id);
    _rangedEnemies = _enemies.Where(e => e.Type == EnemyType.Ranged).ToList();
    _sortedScores  = _scores.OrderByDescending(s => s.Value).ToArray();
    _names         = _players.Select(p => p.DisplayName).ToArray();
}
```

### Hot Path — Use For Loops

```csharp
// ❌ LINQ in Update — allocates delegate + enumerator
void Update()
{
    var alive   = _enemies.Where(e => e.IsAlive).ToList();
    var closest = alive.OrderBy(e => e.DistTo(_player)).First();
}

// ✅ Manual loop — zero allocation
void Update()
{
    Enemy closest = null;
    float minSqr = float.MaxValue;
    for (int i = 0; i < _enemies.Count; i++)
    {
        if (!_enemies[i].IsAlive) continue;
        float sqr = (_enemies[i].Pos - _playerPos).sqrMagnitude;
        if (sqr < minSqr) { minSqr = sqr; closest = _enemies[i]; }
    }
}
```

### Cache LINQ Results

```csharp
// ❌ Re-evaluate every access
public IEnumerable<Enemy> ActiveEnemies => _enemies.Where(e => e.IsAlive);

// ✅ Cache and invalidate
List<Enemy> _activeCache;
bool _cacheDirty = true;

public IReadOnlyList<Enemy> ActiveEnemies
{
    get
    {
        if (_cacheDirty) { _activeCache = _enemies.Where(e => e.IsAlive).ToList(); _cacheDirty = false; }
        return _activeCache;
    }
}
```

### Useful One-Liners (Init Only)

```csharp
bool anyAlive  = enemies.Any(e => e.IsAlive);
int aliveCount = enemies.Count(e => e.IsAlive);
float totalDmg = hits.Sum(h => h.Damage);
float maxHp    = units.Max(u => u.Health);
var grouped    = items.GroupBy(i => i.Category);
var unique     = tags.Distinct().ToArray();
```

---

## Object Pooling

### Unity 2021+ Built-In ObjectPool

```csharp
using UnityEngine;
using UnityEngine.Pool;

public sealed class ProjectileSpawner : MonoBehaviour
{
    [SerializeField] private GameObject _projectilePrefab;
    [SerializeField] private int _defaultCapacity = 20;
    [SerializeField] private int _maxSize = 100;

    private ObjectPool<GameObject> _pool;

    void Awake()
    {
        _pool = new ObjectPool<GameObject>(
            createFunc: () => Instantiate(_projectilePrefab),
            actionOnGet: obj => { obj.SetActive(true); },
            actionOnRelease: obj => { obj.SetActive(false); },
            actionOnDestroy: Destroy,
            collectionCheck: true, // debug: warns on double-release
            defaultCapacity: _defaultCapacity,
            maxSize: _maxSize
        );
    }

    public GameObject Spawn(Vector3 position, Quaternion rotation)
    {
        var obj = _pool.Get();
        obj.transform.SetPositionAndRotation(position, rotation);
        return obj;
    }

    public void Despawn(GameObject obj) => _pool.Release(obj);

    void OnDestroy() => _pool.Dispose();
}
```

### Pool Lifecycle

| Callback | When | Use For |
|----------|------|---------|
| `createFunc` | Pool empty, need new instance | `Instantiate()` |
| `actionOnGet` | Object retrieved from pool | `SetActive(true)`, reset state |
| `actionOnRelease` | Object returned to pool | `SetActive(false)`, stop VFX |
| `actionOnDestroy` | Pool exceeds `maxSize` | `Destroy()` |

### IPoolable Pattern — Self-Returning Objects

```csharp
public interface IPoolable
{
    void OnSpawn();
    void OnDespawn();
    void SetPool(IObjectPool<GameObject> pool);
}

public sealed class Projectile : MonoBehaviour, IPoolable
{
    private IObjectPool<GameObject> _pool;

    public void SetPool(IObjectPool<GameObject> pool) => _pool = pool;

    public void OnSpawn()
    {
        _lifetime = 0f;
        _hasHit = false;
    }

    public void OnDespawn()
    {
        _trail?.Clear();
    }

    void Update()
    {
        _lifetime += Time.deltaTime;
        if (_lifetime > _maxLifetime || _hasHit)
            _pool.Release(gameObject); // self-return
    }
}
```

### When to Pool

| Scenario | Pool? | Reason |
|----------|-------|--------|
| Bullets, VFX, particles | ✅ | High spawn/destroy frequency |
| Enemies, NPCs | ✅ | Frequent spawn during waves |
| UI list items | ✅ | ScrollView virtualization |
| Scene-lifetime objects | ❌ | Created once, never destroyed |
| Player character | ❌ | Single instance |
| Audio one-shots | ⚠️ | Pool if > 10/sec, otherwise OK |

### Generic Component Pool

```csharp
using UnityEngine.Pool;

public sealed class ComponentPool<T> where T : Component
{
    readonly ObjectPool<T> _pool;
    readonly Transform _parent;

    public ComponentPool(T prefab, Transform parent, int capacity = 10, int max = 50)
    {
        _parent = parent;
        _pool = new ObjectPool<T>(
            () => { var obj = Object.Instantiate(prefab, parent); obj.gameObject.SetActive(false); return obj; },
            obj => obj.gameObject.SetActive(true),
            obj => obj.gameObject.SetActive(false),
            obj => Object.Destroy(obj.gameObject),
            defaultCapacity: capacity,
            maxSize: max
        );
    }

    public T Get() => _pool.Get();
    public void Release(T obj) => _pool.Release(obj);
    public void Dispose() => _pool.Dispose();
}
```

### Pre-2021 Custom Pool

```csharp
public sealed class SimplePool<T> where T : Component
{
    readonly Queue<T> _available = new();
    readonly T _prefab;
    readonly Transform _parent;

    public SimplePool(T prefab, Transform parent, int prewarm = 10)
    {
        _prefab = prefab;
        _parent = parent;
        for (int i = 0; i < prewarm; i++)
        {
            var obj = Object.Instantiate(prefab, parent);
            obj.gameObject.SetActive(false);
            _available.Enqueue(obj);
        }
    }

    public T Get()
    {
        var obj = _available.Count > 0 ? _available.Dequeue() : Object.Instantiate(_prefab, _parent);
        obj.gameObject.SetActive(true);
        return obj;
    }

    public void Release(T obj)
    {
        obj.gameObject.SetActive(false);
        _available.Enqueue(obj);
    }
}
```

### Common Pool Mistakes

- ❌ Forgetting to reset state in `actionOnGet` (stale data from previous use)
- ❌ Destroying pooled objects instead of releasing them
- ❌ Not clearing event subscriptions on release (memory leaks)
- ❌ Releasing an object that's already in the pool (use `collectionCheck: true`)
- ❌ Setting `maxSize` too low (causes frequent Destroy/Instantiate)
- ❌ Not resetting velocity on Rigidbody when recycling physics objects
- ❌ Leaving active coroutines running on released objects

### Pool Reset Checklist

```csharp
void ResetPooledObject(GameObject obj)
{
    // Physics
    if (obj.TryGetComponent<Rigidbody>(out var rb))
    {
        rb.linearVelocity = Vector3.zero;
        rb.angularVelocity = Vector3.zero;
    }

    // VFX
    var particles = obj.GetComponentInChildren<ParticleSystem>();
    particles?.Stop(true, ParticleSystemStopBehavior.StopEmittingAndClear);

    // Trails
    var trail = obj.GetComponentInChildren<TrailRenderer>();
    trail?.Clear();

    // Audio
    var audio = obj.GetComponentInChildren<AudioSource>();
    audio?.Stop();
}
```

---

## Serialization

### Prefer Explicit Backing Fields

Use explicit serialized fields for inspector-driven state. This is the least surprising pattern across Unity versions and makes rename and migration work easier to review.

```csharp
public sealed class EnemyConfig : MonoBehaviour
{
    [SerializeField] private float _health = 100f;
    [SerializeField] private float _speed = 3f;
    [SerializeField] private GameObject _deathVfx;

    public float Health => _health;
    public float Speed => _speed;
}
```

### Auto-Property Serialization Is Optional, Not The Default

If a repo already standardizes on field-target attributes and the local Unity version supports it, keep that style consistent. Do not introduce it blindly into mixed-version or mixed-style codebases.

```csharp
// Acceptable only when the project already uses this pattern consistently.
[field: SerializeField] public int MaxHealth { get; private set; } = 100;
```

When in doubt, prefer an explicit backing field plus a read-only property.

### Serializable Nested Types

```csharp
[System.Serializable]
public struct WaveConfig
{
    public int enemyCount;
    public float spawnInterval;
    public GameObject prefab;
}

public sealed class WaveSpawner : MonoBehaviour
{
    [SerializeField] private WaveConfig[] _waves;
}
```

### ScriptableObject Data Containers

```csharp
[CreateAssetMenu(fileName = "EnemyConfig", menuName = "Game/Enemy Config")]
public sealed class EnemyConfig : ScriptableObject
{
    [SerializeField] private float _maxHealth = 100f;
    [SerializeField] private float _moveSpeed = 3f;
    [SerializeField] private AnimationCurve _damageFalloff;

    public float MaxHealth => _maxHealth;
    public float MoveSpeed => _moveSpeed;
    public float GetDamage(float dist) => _damageFalloff.Evaluate(dist);
}
```

### SerializeReference For Polymorphism

Use `[SerializeReference]` only when you actually need polymorphic managed references. It is useful, but it is not a general replacement for normal field serialization.

```csharp
public interface IAbility
{
    void Execute(GameObject owner);
}

public sealed class AbilityRunner : MonoBehaviour
{
    [SerializeReference] private IAbility _primaryAbility;
}
```

### FormerlySerializedAs — Safe Renames

```csharp
using UnityEngine.Serialization;

public sealed class Player : MonoBehaviour
{
    [FormerlySerializedAs("_speed")]
    [SerializeField] private float _moveSpeed = 5f;

    [FormerlySerializedAs("hp")]
    [FormerlySerializedAs("_hp")]
    [SerializeField] private float _health = 100f;
}
```

Keep rename attributes until affected scenes, prefabs, and ScriptableObjects have been re-saved and validated.

### JsonUtility Rules

| Feature | Supported | Notes |
|---------|-----------|-------|
| Public fields | Yes | Serialized by default |
| `[SerializeField]` private fields | Yes | Works |
| Properties | No | Inspector does not serialize property accessors |
| Dictionary | No | Use a serializable list or custom serializer |
| Polymorphism | No | `JsonUtility` does not carry managed type info |
| `[NonSerialized]` | Yes | Excludes field |

```csharp
string json = JsonUtility.ToJson(saveData, prettyPrint: true);
File.WriteAllText(path, json);

var data = JsonUtility.FromJson<SaveData>(json);
JsonUtility.FromJsonOverwrite(json, existingData); // avoids allocation
```

### What Unity Does Not Serialize Reliably

- `Dictionary<K, V>` — wrap in a serializable list or use a custom serializer
- Interfaces and abstract types — use `[SerializeReference]` only when you need managed-reference polymorphism
- `static` fields — never serialized
- `readonly` fields — not inspector-authored serialized state
- Properties — use explicit fields unless the project intentionally uses serialized backing-field attributes
- Deeply nested containers and unsupported generic shapes — validate in the inspector before relying on them

### Save Data Security

```csharp
// ✅ Validate after deserialization — files can be hand-edited
public static SaveData LoadAndValidate(string path)
{
    if (!File.Exists(path)) return new SaveData();
    var json = File.ReadAllText(path);
    var data = JsonUtility.FromJson<SaveData>(json);

    // Clamp all values to valid ranges
    data.Health = Mathf.Clamp(data.Health, 0f, 1000f);
    data.Level = Mathf.Clamp(data.Level, 1, 100);
    data.PlayTime = Mathf.Max(0f, data.PlayTime);
    return data;
}

// ✅ Simple integrity check with hash
public static void SaveWithHash(SaveData data, string path)
{
    var json = JsonUtility.ToJson(data);
    var hash = ComputeHash(json);
    File.WriteAllText(path, json + "\n" + hash);
}
```

- **Never** store sensitive data (auth tokens, purchase records) in local files without encryption
- **Always** clamp deserialized numerics to valid game ranges
- **Prefer** server-side authority for competitive/multiplayer progression
- Use `Application.persistentDataPath` — never hardcode file paths

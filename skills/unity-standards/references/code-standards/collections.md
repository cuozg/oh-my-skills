# Collections

## Choosing the Right Collection

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

## Array for Serialized Fields

```csharp
[SerializeField] Transform[] _spawnPoints;
[SerializeField] AudioClip[] _footstepSounds;

// Random pick — no allocation
var clip = _footstepSounds[Random.Range(0, _footstepSounds.Length)];
```

## Pre-Allocate Lists

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

## Dictionary for Lookups

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

## HashSet for Contains

```csharp
readonly HashSet<int> _unlockedLevels = new();
public bool IsUnlocked(int level) => _unlockedLevels.Contains(level);
```

## ReadOnlyCollection for Public API

```csharp
readonly List<Enemy> _enemies = new();
public IReadOnlyList<Enemy> Enemies => _enemies;
```

## Avoid LINQ in Update

```csharp
// ❌ LINQ allocates in hot path
var closest = enemies.OrderBy(e => e.Distance).First();

// ✅ Manual loop — zero allocation
Enemy closest = null;
float minDist = float.MaxValue;
for (int i = 0; i < _enemies.Count; i++)
{
    float d = Vector3.SqrMagnitude(_enemies[i].Pos - _pos);
    if (d < minDist) { minDist = d; closest = _enemies[i]; }
}
```

## NativeArray for Jobs

```csharp
using Unity.Collections;
var positions = new NativeArray<Vector3>(count, Allocator.TempJob);
// ... schedule job ...
positions.Dispose(); // MUST dispose — no GC
```

## Span<T> and Memory<T> — Zero-Alloc Slicing

```csharp
// Span<T> — stack-only, zero allocation slicing
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

## ArrayPool<T> — Reusable Buffers

```csharp
using System.Buffers;

// Rent/return arrays to avoid GC
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

## NativeContainers — Jobs & Burst

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

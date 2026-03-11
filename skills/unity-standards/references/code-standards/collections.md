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

<!-- Advanced: collections-advanced.md -->

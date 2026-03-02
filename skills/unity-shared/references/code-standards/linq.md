# LINQ Usage

## When to Use

| Context | LINQ OK? | Reason |
|---------|----------|--------|
| `Awake()` / `Start()` | ✅ | One-time init |
| `OnEnable()` | ✅ | Infrequent |
| Editor scripts | ✅ | No runtime cost |
| `Update()` / `FixedUpdate()` | ❌ | Allocates every frame |
| `OnTriggerStay()` | ❌ | Hot path |
| Pooled object reset | ⚠️ | Depends on frequency |

## Efficient LINQ Patterns

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

## Init-Time LINQ — Acceptable

```csharp
void Start()
{
    _enemyLookup   = _enemies.ToDictionary(e => e.Id);
    _rangedEnemies = _enemies.Where(e => e.Type == EnemyType.Ranged).ToList();
    _sortedScores  = _scores.OrderByDescending(s => s.Value).ToArray();
    _names         = _players.Select(p => p.DisplayName).ToArray();
}
```

## Hot Path — Use For Loops

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

## Cache LINQ Results

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

## Useful One-Liners (Init Only)

```csharp
bool anyAlive  = enemies.Any(e => e.IsAlive);
int aliveCount = enemies.Count(e => e.IsAlive);
float totalDmg = hits.Sum(h => h.Damage);
float maxHp    = units.Max(u => u.Health);
var grouped    = items.GroupBy(i => i.Category);
var unique     = tags.Distinct().ToArray();
```

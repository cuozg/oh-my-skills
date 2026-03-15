# GC Allocation Anti-Patterns & Fixes

## Hot-Path Allocations (Update/FixedUpdate/LateUpdate)

### String Operations

```csharp
// ❌ String concatenation allocates new string each call
text.text = "Score: " + score + " / " + maxScore;

// ✅ StringBuilder — reuse across frames
private readonly StringBuilder _sb = new(64);
void UpdateScoreText()
{
    _sb.Clear();
    _sb.Append("Score: ").Append(score).Append(" / ").Append(maxScore);
    text.SetText(_sb);
}

// ✅ TMP — zero-alloc SetText overloads
tmpText.SetText("Score: {0} / {1}", score, maxScore);
```

### LINQ in Hot Paths

```csharp
// ❌ LINQ allocates iterator + closure + result collection
var alive = enemies.Where(e => e.IsAlive).ToList();
var closest = enemies.OrderBy(e => e.DistanceTo(player)).First();

// ✅ Manual loop with reused list
private readonly List<Enemy> _aliveCache = new(32);
void FindAliveEnemies()
{
    _aliveCache.Clear();
    for (int i = 0; i < enemies.Count; i++)
        if (enemies[i].IsAlive) _aliveCache.Add(enemies[i]);
}

// ✅ Manual min-search (zero alloc)
Enemy FindClosest(Vector3 pos)
{
    Enemy best = null;
    float bestSqr = float.MaxValue;
    for (int i = 0; i < enemies.Count; i++)
    {
        float sqr = (enemies[i].Position - pos).sqrMagnitude;
        if (sqr < bestSqr) { bestSqr = sqr; best = enemies[i]; }
    }
    return best;
}
```

### Boxing Allocations

```csharp
// ❌ Boxing int → object
object val = myInt;          // boxes
string.Format("{0}", myInt); // boxes via params object[]
Debug.Log("HP: " + health);  // boxes float

// ✅ Avoid boxing
string.Format("{0}", myInt.ToString()); // pre-convert
$"HP: {health:F1}";  // interpolation avoids boxing in some contexts
// Best: use StringBuilder.Append(int) — no boxing
```

### Lambda/Closure Captures

```csharp
// ❌ Closure captures 'this' — allocates delegate + closure each call
enemies.Sort((a, b) => Vector3.Distance(a.Pos, player.position)
    .CompareTo(Vector3.Distance(b.Pos, player.position)));

// ✅ IComparer<T> — zero-alloc, reusable
private sealed class DistanceComparer : IComparer<Enemy>
{
    public Vector3 Target;
    public int Compare(Enemy a, Enemy b)
    {
        float da = (a.Pos - Target).sqrMagnitude;
        float db = (b.Pos - Target).sqrMagnitude;
        return da.CompareTo(db);
    }
}
private readonly DistanceComparer _comparer = new();
void SortByDistance()
{
    _comparer.Target = player.position;
    enemies.Sort(_comparer);
}
```

### Collection Allocations

```csharp
// ❌ New collection each frame
var results = new List<RaycastHit>();

// ✅ Reuse with Clear()
private readonly List<RaycastHit> _hitCache = new(16);
void Query()
{
    _hitCache.Clear();
    // fill _hitCache
}

// ✅ NonAlloc physics queries
private readonly RaycastHit[] _hitBuffer = new RaycastHit[16];
int count = Physics.RaycastNonAlloc(ray, _hitBuffer, dist, mask);
```

## Per-Frame Cost Reference

| Pattern | Approx. Allocation | Fix |
|---------|-------------------|-----|
| `string + string` | 40-200B per concat | StringBuilder |
| `.Where().ToList()` | 80-500B+ | Manual loop + cached list |
| `new List<T>()` | 64B + elements | Reuse with `.Clear()` |
| Lambda capture | 64-128B per delegate | IComparer / static method |
| Boxing value type | 12-24B per box | Type-specific overloads |
| `ToString()` | 20-100B | Avoid in hot paths |
| `RaycastAll()` | Array alloc | `RaycastNonAlloc` |
| `GetComponentsInChildren()` | Array alloc | `GetComponentsInChildren(list)` |

## Anti-Patterns

### Don't Use LINQ in Hot Paths

```csharp
// ❌ BAD: LINQ in Update (allocates every frame)
void Update()
{
    var nearest = enemies.OrderBy(e => Vector3.Distance(transform.position, e.position)).First();
}

// ✅ GOOD: Manual loop in hot path
void Update()
{
    Enemy nearest = null;
    float minDist = float.MaxValue;
    foreach (var enemy in enemies)
    {
        float dist = Vector3.SqrMagnitude(transform.position - enemy.position);
        if (dist < minDist)
        {
            minDist = dist;
            nearest = enemy;
        }
    }
}
```

### Don't Nest LINQ Queries

```csharp
// ❌ BAD: Nested LINQ (O(n*m))
var matches = list1.Where(a => list2.Any(b => b.Id == a.Id));

// ✅ GOOD: Use a HashSet for O(n+m)
var idSet = list2.Select(b => b.Id).ToHashSet();
var matches = list1.Where(a => idSet.Contains(a.Id));
```

### Don't Chain Count() for Checks

```csharp
// ❌ BAD: Counting for boolean check
if (items.Count() > 0) { } // Iterates ALL
if (items.Count() == 1) { } // Iterates ALL

// ✅ GOOD: Use Any/Take
if (items.Any()) { }
if (items.Take(2).Count() == 1) { } // At most 2 iterations
```

### Prefer Concrete Type Returns

```csharp
// ✅ GOOD: Return concrete type
public List<Player> GetActivePlayers()
    => players.Where(p => p.IsActive).ToList();

public IReadOnlyList<Player> GetAllPlayers()
    => players.AsReadOnly();

// ❌ BAD: Return IEnumerable when caller needs materialized data
public IEnumerable<Player> GetActivePlayers()
    => players.Where(p => p.IsActive); // Caller may enumerate multiple times
```

**See also:** [linq-patterns.md](linq-patterns.md) for When to Use LINQ and Common Patterns.

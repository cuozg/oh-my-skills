# LINQ Advanced Patterns & Anti-Patterns

Ordering, set operations, chaining, materialization, and anti-patterns.

## Ordering

```csharp
// ✅ GOOD: OrderBy / ThenBy
var ranked = players.OrderByDescending(p => p.Score).ThenBy(p => p.Name);

// ❌ BAD: Sort with unclear comparison (mutates original list)
players.Sort((a, b) => b.Score.CompareTo(a.Score));
```

## Set Operations

```csharp
var uniqueIds = list1.Union(list2);
var common = list1.Intersect(list2);
var onlyInFirst = list1.Except(list2);
var distinct = players.DistinctBy(p => p.Name);
```

## Chaining

```csharp
// ✅ GOOD: Method chain, one operation per line
var result = players
    .Where(p => p.IsActive)
    .OrderByDescending(p => p.Score)
    .Take(10)
    .Select(p => new LeaderboardEntry(p.Name, p.Score))
    .ToList();
```

## Materialization

```csharp
// ✅ GOOD: Materialize when iterating multiple times
var activeList = players.Where(p => p.IsActive).ToList();
DoSomething(activeList);
DoSomethingElse(activeList);

// ❌ BAD: Re-evaluating deferred query
var active = players.Where(p => p.IsActive); // Deferred
DoSomething(active);     // Evaluates query
DoSomethingElse(active); // Evaluates AGAIN
```

## No LINQ in Hot Paths

```csharp
// ❌ BAD: LINQ in Update (allocates every frame)
void Update()
{
    var nearest = enemies.OrderBy(e => Vector3.Distance(transform.position, e.position)).First();
}

// ✅ GOOD: Manual loop
void Update()
{
    Enemy nearest = null;
    float minDist = float.MaxValue;
    foreach (var enemy in enemies)
    {
        float dist = Vector3.SqrMagnitude(transform.position - enemy.position);
        if (dist < minDist) { minDist = dist; nearest = enemy; }
    }
}
```

## No Nested LINQ

```csharp
// ❌ BAD: Nested LINQ O(n*m)
var matches = list1.Where(a => list2.Any(b => b.Id == a.Id));

// ✅ GOOD: HashSet for O(n+m)
var idSet = list2.Select(b => b.Id).ToHashSet();
var matches = list1.Where(a => idSet.Contains(a.Id));
```

## Use Any() Not Count()

```csharp
// ❌ BAD: Counting for boolean check
if (items.Count() > 0) { } // Iterates ALL

// ✅ GOOD: Use Any/Take
if (items.Any()) { }
```

## Return Concrete Types

```csharp
// ✅ GOOD: Return concrete
public List<Player> GetActivePlayers() => players.Where(p => p.IsActive).ToList();
public IReadOnlyList<Player> GetAllPlayers() => players.AsReadOnly();

// ❌ BAD: Return IEnumerable (caller may enumerate multiple times)
```

**See also:** [linq.md](linq.md) for basic LINQ patterns.

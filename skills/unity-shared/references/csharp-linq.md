# LINQ Patterns

**Use for:** Data querying, filtering, transforming collections.
**Avoid in:** Hot paths (Update, FixedUpdate), performance-critical code.

## Core Operations

```csharp
// Filtering
var active = players.Where(p => p.IsActive);

// Projection
var names = players.Select(p => p.Name);

// Existence — use Any(), never Count() > 0
bool hasActive = players.Any(p => p.IsActive);
bool allReady = players.All(p => p.IsReady);

// Finding
var player = players.FirstOrDefault(p => p.Id == id);
var config = configs.Single(c => c.IsDefault);  // Throws if 0 or 2+

// Aggregation
int total = players.Sum(p => p.Score);
int max = players.Max(p => p.Score);
```

## Ordering, Grouping, Sets

```csharp
var ranked = players.OrderByDescending(p => p.Score).ThenBy(p => p.Name);

var byTeam = players.GroupBy(p => p.Team);
var lookup = players.ToLookup(p => p.Team);  // O(1) repeated access

var unique = list1.Union(list2);
var common = list1.Intersect(list2);
var distinct = players.DistinctBy(p => p.Name);
```

## Chaining & Materialization

```csharp
// ✅ One operation per line, materialize when reusing
var result = players
    .Where(p => p.IsActive)
    .OrderByDescending(p => p.Score)
    .Take(10)
    .Select(p => new LeaderboardEntry(p.Name, p.Score))
    .ToList();

// ❌ Re-evaluating deferred query multiple times
var active = players.Where(p => p.IsActive);  // Deferred
DoA(active);  // Evaluates
DoB(active);  // Evaluates AGAIN — materialize with .ToList() first
```

## Anti-Patterns

```csharp
// ❌ LINQ in Update — allocates every frame
void Update() {
    var nearest = enemies.OrderBy(e => Vector3.Distance(transform.position, e.position)).First();
}
// ✅ Manual loop in hot paths
void Update() {
    Enemy nearest = null; float minDist = float.MaxValue;
    foreach (var e in enemies) {
        float d = Vector3.SqrMagnitude(transform.position - e.position);
        if (d < minDist) { minDist = d; nearest = e; }
    }
}

// ❌ Nested LINQ — O(n*m)
var matches = list1.Where(a => list2.Any(b => b.Id == a.Id));
// ✅ HashSet — O(n+m)
var idSet = list2.Select(b => b.Id).ToHashSet();
var matches = list1.Where(a => idSet.Contains(a.Id));

// ✅ Return concrete types, not IEnumerable
public List<Player> GetActive() => players.Where(p => p.IsActive).ToList();
```

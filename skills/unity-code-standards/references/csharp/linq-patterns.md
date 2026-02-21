# LINQ Patterns & Best Practices

## When to Use LINQ

**Use LINQ for:** Data querying, filtering, transforming collections.
**Avoid LINQ in:** Hot paths (Update, FixedUpdate), performance-critical code.

## Common Patterns

### Filtering

```csharp
// ✅ GOOD: LINQ Where
var activePlayers = players.Where(p => p.IsActive);
var highScorers = players.Where(p => p.Score > 100);

// ❌ BAD: Manual loop for filtering
var activePlayers = new List<Player>();
foreach (var player in players)
{
    if (player.IsActive)
        activePlayers.Add(player);
}
```

### Projection (Select)

```csharp
// ✅ GOOD: LINQ Select
var names = players.Select(p => p.Name);
var summaries = players.Select(p => new { p.Name, p.Score });

// ❌ BAD: Manual projection
var names = new List<string>();
foreach (var player in players)
{
    names.Add(player.Name);
}
```

### Existence Checks

```csharp
// ✅ GOOD: Any/All
bool hasActive = players.Any(p => p.IsActive);
bool allReady = players.All(p => p.IsReady);
bool isEmpty = !players.Any();

// ❌ BAD: Count for existence
bool hasActive = players.Count(p => p.IsActive) > 0; // Counts ALL, wasteful
bool isEmpty = players.Count() == 0; // Use !Any()
```

### Finding Elements

```csharp
// ✅ GOOD: FirstOrDefault with null check
var player = players.FirstOrDefault(p => p.Id == targetId);
if (player is null) throw new KeyNotFoundException($"Player {targetId} not found");

// ✅ GOOD: Single when exactly one expected
var config = configs.Single(c => c.IsDefault); // Throws if 0 or 2+

// ❌ BAD: First without handling empty
var player = players.First(p => p.Id == targetId); // Throws on empty - unclear error
```

### Aggregation

```csharp
// ✅ GOOD: LINQ aggregation
int totalScore = players.Sum(p => p.Score);
int maxScore = players.Max(p => p.Score);
double avgScore = players.Average(p => p.Score);
int count = players.Count(p => p.IsActive);

// ✅ GOOD: Aggregate for custom reduction
string allNames = players.Aggregate("", (acc, p) => acc + ", " + p.Name).TrimStart(',', ' ');
```

### Grouping

```csharp
// ✅ GOOD: GroupBy
var byTeam = players.GroupBy(p => p.Team);
foreach (var group in byTeam)
{
    Console.WriteLine($"Team {group.Key}: {group.Count()} players");
}

// ✅ GOOD: ToLookup for repeated access
var lookup = players.ToLookup(p => p.Team);
var redTeam = lookup["Red"]; // O(1) lookup
```

### Ordering

```csharp
// ✅ GOOD: OrderBy / ThenBy
var ranked = players
    .OrderByDescending(p => p.Score)
    .ThenBy(p => p.Name);

// ❌ BAD: Sort with unclear comparison
players.Sort((a, b) => b.Score.CompareTo(a.Score)); // Mutates original list
```

### Set Operations

```csharp
// ✅ GOOD: Set operations
var uniqueIds = list1.Union(list2);
var common = list1.Intersect(list2);
var onlyInFirst = list1.Except(list2);
var distinct = players.DistinctBy(p => p.Name);
```

### Chaining

```csharp
// ✅ GOOD: Method chain, one operation per line
var result = players
    .Where(p => p.IsActive)
    .OrderByDescending(p => p.Score)
    .Take(10)
    .Select(p => new LeaderboardEntry(p.Name, p.Score))
    .ToList();

// ❌ BAD: Everything on one line
var result = players.Where(p => p.IsActive).OrderByDescending(p => p.Score).Take(10).Select(p => new LeaderboardEntry(p.Name, p.Score)).ToList();
```

## Materialization

```csharp
// ✅ GOOD: Materialize when you need to iterate multiple times
var activeList = players.Where(p => p.IsActive).ToList(); // Materialized once
DoSomething(activeList);
DoSomethingElse(activeList);

// ❌ BAD: Re-evaluating deferred query
var active = players.Where(p => p.IsActive); // Deferred
DoSomething(active); // Evaluates query
DoSomethingElse(active); // Evaluates AGAIN
```

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

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

**Continue in [linq-patterns-advanced.md](linq-patterns-advanced.md) for Ordering, Set Operations, Materialization, and Anti-Patterns.**

# LINQ Advanced Patterns

Continued from [linq-patterns.md](linq-patterns.md).

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


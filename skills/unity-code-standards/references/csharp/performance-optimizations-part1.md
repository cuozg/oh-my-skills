# C# Performance Optimizations

## Allocation Reduction

```csharp
// ✅ GOOD: Cache allocations
private readonly List<Collider> hitResults = new();
private readonly StringBuilder builder = new();
private readonly WaitForSeconds waitOneSecond = new(1f);

// ❌ BAD: Allocating in hot paths
void Update()
{
    var hits = new List<Collider>(); // GC every frame!
    var message = new StringBuilder(); // GC every frame!
}
```

## String Optimizations

```csharp
// ✅ GOOD: StringBuilder for multiple concatenations
var builder = new StringBuilder(256);
foreach (var player in players)
{
    builder.Append(player.Name).Append(": ").AppendLine(player.Score.ToString());
}
var result = builder.ToString();

// ✅ GOOD: string.Create for known-length strings
// ✅ GOOD: Span<char> for temporary string operations

// ❌ BAD: String concatenation in loops
string result = "";
foreach (var player in players)
{
    result += player.Name + ": " + player.Score + "\n"; // O(n²) allocations
}
```

## Collection Capacity

```csharp
// ✅ GOOD: Pre-size collections when count is known
var results = new List<Player>(players.Count);
var lookup = new Dictionary<string, Player>(expectedCount);
var set = new HashSet<int>(ids.Length);

// ❌ BAD: Default capacity with known size
var results = new List<Player>(); // Resizes multiple times
```

## Struct vs Class

```csharp
// ✅ GOOD: Struct for small, immutable value types
public readonly struct DamageInfo
{
    public readonly int Amount;
    public readonly DamageType Type;

    public DamageInfo(int amount, DamageType type)
    {
        Amount = amount;
        Type = type;
    }
}

// ✅ GOOD: readonly record struct for data carriers
public readonly record struct HitResult(Vector3 Point, Vector3 Normal, float Distance);

// ❌ BAD: Class for small immutable data (heap allocation)
public class DamageInfo // Unnecessary heap allocation
{
    public int Amount { get; }
    public DamageType Type { get; }
}
```


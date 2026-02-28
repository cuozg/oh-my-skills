# C# Performance — Allocation & Memory

Allocation reduction, string optimization, collections, struct vs class, boxing avoidance, ArrayPool/Span.

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
}
```

## String Optimizations

```csharp
// ✅ GOOD: StringBuilder for multiple concatenations
var builder = new StringBuilder(256);
foreach (var player in players)
    builder.Append(player.Name).Append(": ").AppendLine(player.Score.ToString());

// ❌ BAD: String concat in loops — O(n²) allocations
string result = "";
foreach (var player in players)
    result += player.Name + ": " + player.Score + "\n";
```

## Collection Capacity

```csharp
// ✅ GOOD: Pre-size when count known
var results = new List<Player>(players.Count);
var lookup = new Dictionary<string, Player>(expectedCount);

// ❌ BAD: Default capacity with known size (resizes multiple times)
var results = new List<Player>();
```

## Struct vs Class

```csharp
// ✅ GOOD: Struct for small, immutable value types
public readonly struct DamageInfo
{
    public readonly int Amount;
    public readonly DamageType Type;
}

// ✅ GOOD: readonly record struct for data carriers
public readonly record struct HitResult(Vector3 Point, Vector3 Normal, float Distance);

// ❌ BAD: Class for small immutable data (unnecessary heap allocation)
```

## Boxing Avoidance

```csharp
// ✅ GOOD: Generic methods to avoid boxing
void Process<T>(T value) where T : struct { }

// ✅ GOOD: IEquatable<T> on structs
public readonly struct PlayerId : IEquatable<PlayerId>
{
    public readonly int Value;
    public bool Equals(PlayerId other) => Value == other.Value;
    public override bool Equals(object? obj) => obj is PlayerId other && Equals(other);
    public override int GetHashCode() => Value;
}

// ❌ BAD: Boxing struct values
object boxed = myStruct; // Boxing allocation
dictionary[myStruct] = value; // Boxing if no IEquatable<T>
```

## ArrayPool & Span

```csharp
// ✅ GOOD: ArrayPool for temporary arrays
var buffer = ArrayPool<byte>.Shared.Rent(1024);
try { ProcessBuffer(buffer.AsSpan(0, 1024)); }
finally { ArrayPool<byte>.Shared.Return(buffer); }

// ✅ GOOD: stackalloc for small temporary buffers
Span<int> temp = stackalloc int[16];

// ❌ BAD: new array for temporary use
var buffer = new byte[1024]; // GC pressure
```

**See also:** [perf-cache.md](perf-cache.md) for delegate/lambda caching and dictionary optimizations.

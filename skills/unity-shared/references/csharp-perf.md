# C# Performance — Allocation & Caching

Allocation reduction, struct vs class, boxing, ArrayPool, delegate caching, dictionary patterns.

## Cache Allocations

```csharp
// ✅ Cache in fields — never allocate in hot paths
private readonly List<Collider> _hitResults = new();
private readonly StringBuilder _builder = new();
private readonly WaitForSeconds _waitOne = new(1f);

// ❌ new List<> in Update() = GC every frame
```

## String Optimizations

```csharp
// ✅ StringBuilder for loops
var sb = new StringBuilder(256);
foreach (var p in players)
    sb.Append(p.Name).Append(": ").AppendLine(p.Score.ToString());

// ❌ result += in loops = O(n²) allocations
```

## Collection Capacity

```csharp
// ✅ Pre-size when count known
var results = new List<Player>(players.Count);
var lookup = new Dictionary<string, Player>(expectedCount);
```

## Struct vs Class

```csharp
// ✅ readonly struct for small immutable value types
public readonly struct DamageInfo
{
    public readonly int Amount;
    public readonly DamageType Type;
}

// ✅ readonly record struct for data carriers
public readonly record struct HitResult(Vector3 Point, Vector3 Normal, float Distance);
```

## Boxing Avoidance

```csharp
// ✅ Generic methods avoid boxing
void Process<T>(T value) where T : struct { }

// ✅ IEquatable<T> on structs — prevents boxing in dictionaries
public readonly struct PlayerId : IEquatable<PlayerId>
{
    public readonly int Value;
    public bool Equals(PlayerId other) => Value == other.Value;
    public override bool Equals(object? obj) => obj is PlayerId other && Equals(other);
    public override int GetHashCode() => Value;
}
```

## ArrayPool & Span

```csharp
// ✅ ArrayPool for temporary arrays
var buffer = ArrayPool<byte>.Shared.Rent(1024);
try { ProcessBuffer(buffer.AsSpan(0, 1024)); }
finally { ArrayPool<byte>.Shared.Return(buffer); }

// ✅ stackalloc for small temporary buffers
Span<int> temp = stackalloc int[16];
```

## Delegate & Lambda Caching

```csharp
// ✅ Cache delegates as fields
private readonly Action<int> _cachedCallback;
public MyClass() { _cachedCallback = OnValueChanged; }

// ✅ Static lambda — no closure allocation
items.ForEach(static item => Process(item));

// ❌ Lambda with `this` capture in Update = allocation every frame
```

## Dictionary Optimizations

```csharp
// ✅ TryGetValue — single lookup
if (dict.TryGetValue(key, out var value)) { Process(value); }

// ✅ GetValueOrDefault
var value = dict.GetValueOrDefault(key, defaultValue);

// ❌ ContainsKey + indexer = double lookup
```

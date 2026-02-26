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

## Array & Span Optimizations

```csharp
// ✅ GOOD: ArrayPool for temporary arrays
var buffer = ArrayPool<byte>.Shared.Rent(1024);
try
{
    ProcessBuffer(buffer.AsSpan(0, 1024));
}
finally
{
    ArrayPool<byte>.Shared.Return(buffer);
}

// ✅ GOOD: stackalloc for small temporary buffers
Span<int> temp = stackalloc int[16];

// ❌ BAD: new array for temporary use
var buffer = new byte[1024]; // GC pressure
```

**Continue in [performance-optimizations-advanced.md](performance-optimizations-advanced.md) for Delegate/Lambda Caching and Dictionary Optimizations.**

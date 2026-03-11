# Collections — Advanced

## NativeArray for Jobs

```csharp
using Unity.Collections;
var positions = new NativeArray<Vector3>(count, Allocator.TempJob);
// ... schedule job ...
positions.Dispose(); // MUST dispose — no GC
```

## Span<T> and Memory<T> — Zero-Alloc Slicing

```csharp
// Span<T> — stack-only, zero allocation slicing
void ProcessDamageValues(Span<float> damages)
{
    for (int i = 0; i < damages.Length; i++)
        damages[i] *= _multiplier;
}

// Usage with stackalloc
Span<float> buffer = stackalloc float[4];
buffer[0] = 10f; buffer[1] = 20f;
ProcessDamageValues(buffer);

// Slice existing array without allocation
float[] allDamages = GetDamageArray();
ProcessDamageValues(allDamages.AsSpan(0, 4));
```

## ArrayPool<T> — Reusable Buffers

```csharp
using System.Buffers;

// Rent/return arrays to avoid GC
var buffer = ArrayPool<RaycastHit>.Shared.Rent(64);
try
{
    int count = Physics.RaycastNonAlloc(ray, buffer);
    for (int i = 0; i < count; i++) ProcessHit(buffer[i]);
}
finally
{
    ArrayPool<RaycastHit>.Shared.Return(buffer);
}
```

## NativeContainers — Jobs & Burst

| Container | Use | Thread Safety |
|-----------|-----|---------------|
| `NativeArray<T>` | Fixed-size buffer | Safety checks |
| `NativeList<T>` | Dynamic-size buffer | Single writer |
| `NativeHashMap<K,V>` | Key-value lookup in jobs | `.AsParallelWriter()` |
| `NativeQueue<T>` | FIFO in jobs | `.AsParallelWriter()` |
| `NativeParallelHashMap<K,V>` | Concurrent writes | Built-in parallel |

```csharp
using Unity.Collections;

var positions = new NativeList<float3>(128, Allocator.TempJob);
positions.Add(new float3(1, 0, 0));
// ... schedule job ...
positions.Dispose(); // MUST dispose
```

**Rule:** All NativeContainers MUST be disposed. Use `Allocator.TempJob` for single-frame, `Allocator.Persistent` for long-lived.

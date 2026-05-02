# Jobs System, Burst Compiler & ECS Data-Oriented Design

Complete guide to Unity's high-performance multithreaded programming stack.

## Overview

| Technology | Purpose | Key Benefit |
|------------|---------|-------------|
| **Job System** | Multithreaded C# code | Parallel execution without race conditions |
| **Burst Compiler** | LLVM-based IL → native code | 10-100x speedup via SIMD, auto-vectorization |
| **ECS** | Data-oriented architecture | Cache-friendly memory layout, automatic parallelization |

**Rule of thumb:** If a `for` loop runs 100+ iterations per frame on value-type data, consider Jobs + Burst.

---

## When to Migrate

| Scenario | Use Jobs/Burst? |
|----------|-----------------|
| Processing 100+ entities per frame (movement, AI, pathfinding) | ✅ Yes |
| Heavy math (physics simulation, procedural generation) | ✅ Yes |
| Data transformation on large arrays | ✅ Yes |
| Complex collision detection or spatial queries | ✅ Yes |
| Single MonoBehaviour update logic | ❌ No — overhead not worth it |
| UI/event handling | ❌ No — not parallelizable |
| I/O, networking, file access | ❌ No — managed code required |
| Calling UnityEngine APIs frequently | ❌ No — main thread only |

---

## Job System Fundamentals

### Job Safety System

The Job System automatically prevents race conditions:

```csharp
// ✅ Safe - system knows Positions is written, Velocities is read-only
[BurstCompile]
struct SafeJob : IJobParallelFor
{
    public NativeArray<float3> Positions;        // Read-Write
    [ReadOnly] public NativeArray<float3> Velocities;  // Read-only
    
    public void Execute(int index)
    {
        Positions[index] += Velocities[index] * DeltaTime;
    }
}

// ❌ Unsafe - would cause race condition without safety system
// Two jobs writing to same NativeArray simultaneously = undefined behavior
```

### Job Dependencies

```csharp
// Job B depends on Job A completing
JobHandle jobAHandle = jobA.Schedule();
JobHandle jobBHandle = jobB.Schedule(jobAHandle);  // B waits for A

// Multiple dependencies
JobHandle combined = JobHandle.CombineDependencies(jobAHandle, jobBHandle, jobCHandle);
JobHandle jobDHandle = jobD.Schedule(combined);

// Complete all
jobDHandle.Complete();
```

### Job Types

| Type | Interface | Use Case | Scheduling |
|------|-----------|----------|------------|
| **Single** | `IJob` | One-time work | `Schedule()` |
| **Parallel For** | `IJobParallelFor` | Process array in parallel | `Schedule(length, batchSize)` |
| **Parallel For Transform** | `IJobParallelForTransform` | Modify Transforms safely | `Schedule(transformAccessArray)` |
| **Entity** | `IJobEntity` | ECS system jobs | `Schedule()` / `ScheduleParallel()` |
| **For** | `IJobFor` | Sequential array processing | `Schedule(length)` |

### Complete Job Example

```csharp
using Unity.Burst;
using Unity.Collections;
using Unity.Jobs;
using Unity.Mathematics;
using UnityEngine;

[BurstCompile]
public struct GravityJob : IJobParallelFor
{
    public NativeArray<float3> Positions;
    public NativeArray<float3> Velocities;
    [ReadOnly] public NativeArray<float> Masses;
    
    public float DeltaTime;
    public float3 Gravity;
    
    public void Execute(int index)
    {
        // Apply gravity: F = ma, so a = F/m = G/mass
        float3 acceleration = Gravity / Masses[index];
        Velocities[index] += acceleration * DeltaTime;
        Positions[index] += Velocities[index] * DeltaTime;
    }
}

public class GravitySystem : MonoBehaviour
{
    private NativeArray<float3> _positions;
    private NativeArray<float3> _velocities;
    private NativeArray<float> _masses;
    private JobHandle _gravityHandle;

    void Start()
    {
        int entityCount = 1000;
        _positions = new NativeArray<float3>(entityCount, Allocator.Persistent);
        _velocities = new NativeArray<float3>(entityCount, Allocator.Persistent);
        _masses = new NativeArray<float>(entityCount, Allocator.Persistent);
        
        // Initialize data...
    }

    void Update()
    {
        var job = new GravityJob
        {
            Positions = _positions,
            Velocities = _velocities,
            Masses = _masses,
            DeltaTime = Time.deltaTime,
            Gravity = new float3(0, -9.81f, 0)
        };
        
        // Batch size 64 is a good default; profile to tune (32-256 range)
        _gravityHandle = job.Schedule(_positions.Length, 64);
    }

    void LateUpdate()
    {
        _gravityHandle.Complete();  // Wait for job to finish
        
        // Apply results to GameObjects or ECS entities here
        for (int i = 0; i < _positions.Length; i++)
        {
            // Update GameObject positions
        }
    }

    void OnDestroy()
    {
        _gravityHandle.Complete();  // Ensure job completes before disposal
        _positions.Dispose();
        _velocities.Dispose();
        _masses.Dispose();
    }
}
```

---

## Burst Compiler Deep Dive

### What Burst Does

1. **IL → LLVM IR**: Converts C# IL to LLVM intermediate representation
2. **Auto-vectorization**: Automatically uses SIMD (SSE, AVX, NEON) where possible
3. **Loop unrolling**: Reduces loop overhead
4. **Inlining**: Aggressively inlines for zero call overhead
5. **Bounds check elimination**: Removes array bounds checks when safe

### BurstCompile Options

```csharp
[BurstCompile(
    FloatPrecision.Standard,      // Standard or High (affects math precision)
    FloatMode.Default,            // Default, Strict, Fast (Fast allows optimizations)
    CompileSynchronously = false  // true = compile immediately, false = async
)]
public struct OptimizedJob : IJobParallelFor
{
    // Job implementation
}
```

### Burst-Compatible Code

```csharp
[BurstCompile]
public struct CompatibleJob : IJobParallelFor
{
    // ✅ ALLOWED:
    public NativeArray<float> floatArray;           // Native containers
    [ReadOnly] public NativeArray<int> readOnlyArray; // ReadOnly attribute
    public float3 vector;                             // Unity.Mathematics
    public float4x4 matrix;
    
    // Static readonly fields
    public static readonly float Gravity = -9.81f;
    
    // Fixed buffers
    public unsafe fixed float buffer[16];
    
    public void Execute(int index)
    {
        // ✅ ALLOWED operations:
        float distance = math.distance(floatArray[index], vector);
        float lerp = math.lerp(0f, 1f, 0.5f);
        float3 normalized = math.normalize(vector);
        
        // Math functions
        float sin = math.sin(1.0f);
        float sqrt = math.sqrt(2.0f);
        
        // Unsafe code (with care)
        unsafe {
            float* ptr = (float*)floatArray.GetUnsafePtr();
        }
    }
}
```

### NOT Allowed in Burst

```csharp
[BurstCompile]
public struct IncompatibleJob : IJobParallelFor
{
    // ❌ NOT ALLOWED:
    // public string Name;                          // Managed type
    // public List<float> list;                     // Generic collections
    // public Dictionary<int, float> dict;        // Dictionaries
    // public Transform transform;                  // UnityEngine.Object
    // public GameObject go;                       // Managed Unity objects
    
    public void Execute(int index)
    {
        // ❌ NOT ALLOWED operations:
        // string.Format()                            // String manipulation
        // new object()                                // Reference type allocation
        // try { } catch { }                          // Exception handling
        // Debug.Log("message");                     // Logging (use Unity.Logging.Log)
        // transform.position = ...;                  // GameObject access
        
        // ❌ Virtual/interface calls (unless static)
        // IInterface foo = ...;
        // foo.Method();                            // Virtual dispatch
    }
}
```

### Burst Intrinsics (Direct SIMD)

```csharp
using Unity.Burst.Intrinsics;

[BurstCompile]
public struct SimdJob : IJobParallelFor
{
    public NativeArray<float4> Data;
    
    public void Execute(int index)
    {
        // Direct SSE/AVX/NEON intrinsics when auto-vectorization isn't enough
        float4 value = Data[index];
        
        // x86 SSE intrinsics
        var v128 = new v128(value.x, value.y, value.z, value.w);
        v128 result = X86.Sse.add_ps(v128, v128);
        
        Data[index] = new float4(result.Float0, result.Float1, result.Float2, result.Float3);
    }
}
```

---

## Data Layout Optimization

### Struct of Arrays (SoA) vs Array of Structs (AoS)

```csharp
// ❌ Array of Structs (AoS) - Poor cache locality
struct EntityData
{
    public float3 Position;
    public float3 Velocity;
    public float Health;
    public int TeamId;
}

NativeArray<EntityData> entities; // 1000 entities

// When job only needs positions, entire EntityData is loaded into cache
// Wasted bandwidth: 40 bytes loaded, 12 bytes used

// ✅ Struct of Arrays (SoA) - Excellent cache locality
NativeArray<float3> positions;
NativeArray<float3> velocities;
NativeArray<float> healths;
NativeArray<int> teamIds;

// Job only loads positions - perfect cache utilization
// Bandwidth: 12 bytes loaded, 12 bytes used

[BurstCompile]
struct SoAJob : IJobParallelFor
{
    public NativeArray<float3> Positions;
    [ReadOnly] public NativeArray<float3> Velocities;
    public float DeltaTime;
    
    public void Execute(int index)
    {
        // Only touches positions and velocities arrays
        Positions[index] += Velocities[index] * DeltaTime;
    }
}
```

### Cache Line Considerations

```csharp
// Cache line is typically 64 bytes
// float3 = 12 bytes
// 64 / 12 = ~5 float3s per cache line

// Optimal batch sizes for cache efficiency:
// - Jobs: 32-256 elements per batch (default 64)
// - ECS chunks: 16-128 entities depending on component sizes
```

---

## Native Collections

| Collection | Use Case | Notes |
|------------|----------|-------|
| `NativeArray<T>` | Fixed-size array | Basic building block |
| `NativeList<T>` | Dynamic array | Can grow/shrink |
| `NativeHashMap<K,V>` | Key-value lookup | Burst-compatible dictionary |
| `NativeMultiHashMap<K,V>` | Multi-value map | Multiple values per key |
| `NativeQueue<T>` | FIFO queue | Thread-safe enqueue/dequeue |
| `NativeStream` | Parallel streams | Write from job, read later |
| `NativeParallelHashMap<K,V>` | Thread-safe hashmap | Concurrent read/write |
| `NativeParallelMultiHashMap<K,V>` | Thread-safe multi-map | Concurrent read/write |

### NativeArray Usage

```csharp
// Allocation
NativeArray<float> array = new NativeArray<float>(100, Allocator.TempJob);
NativeArray<float3> persistent = new NativeArray<float3>(1000, Allocator.Persistent);

// Initialization
NativeArray<float> zeros = new NativeArray<float>(100, Allocator.Temp, NativeArrayOptions.ClearMemory);

// From existing array
float[] managedArray = new float[100];
NativeArray<float> nativeArray = new NativeArray<float>(managedArray, Allocator.TempJob);

// Copy between NativeArrays
NativeArray<float> copy = new NativeArray<float>(nativeArray, Allocator.TempJob);

// Dispose
array.Dispose();
```

### Allocator Lifetimes

| Allocator | Max Lifetime | Use Case |
|-----------|--------------|----------|
| `Temp` | 1 frame | Immediate calculations |
| `TempJob` | 4 frames | Job data (must Complete within 4 frames) |
| `Persistent` | Manual | Long-lived data |

---

## IJobEntity (ECS Jobs)

Modern ECS job pattern - cleaner than IJobParallelFor:

```csharp
using Unity.Entities;
using Unity.Burst;
using Unity.Mathematics;
using Unity.Transforms;

// Query and process matching entities automatically
[BurstCompile]
public partial struct MovementJob : IJobEntity
{
    public float DeltaTime;
    
    // Automatically runs for every entity with LocalTransform and Velocity
    void Execute(ref LocalTransform transform, in Velocity velocity)
    {
        transform.Position += velocity.Value * DeltaTime;
    }
}

public partial struct MovementSystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        // Schedule as parallel job
        new MovementJob { DeltaTime = SystemAPI.Time.DeltaTime }
            .ScheduleParallel();
    }
}
```

### IJobEntity with EntityAccess

```csharp
[BurstCompile]
public partial struct DamageJob : IJobEntity
{
    public EntityCommandBuffer.ParallelWriter ECB;
    public float DamageAmount;
    
    void Execute([ChunkIndexInQuery] int chunkIndex, in Entity entity, ref Health health)
    {
        health.Value -= DamageAmount;
        
        if (health.Value <= 0)
        {
            // Defer entity destruction to end of frame
            ECB.DestroyEntity(chunkIndex, entity);
        }
    }
}
```

---

## Transform Jobs

### IJobParallelForTransform

Safely modify GameObject Transforms from jobs:

```csharp
using UnityEngine.Jobs;

[BurstCompile]
public struct TransformJob : IJobParallelForTransform
{
    public NativeArray<float3> velocities;
    public float deltaTime;
    
    public void Execute(int index, TransformAccess transform)
    {
        // Modify Transform directly (thread-safe via TransformAccessArray)
        transform.position += (Vector3)velocities[index] * deltaTime;
    }
}

public class TransformSystem : MonoBehaviour
{
    private TransformAccessArray _transformAccess;
    private NativeArray<float3> _velocities;

    void Start()
    {
        // Collect transforms
        var transforms = new List<Transform>();
        foreach (var obj in GameObject.FindGameObjectsWithTag("Movable"))
        {
            transforms.Add(obj.transform);
        }
        _transformAccess = new TransformAccessArray(transforms.ToArray());
        _velocities = new NativeArray<float3>(_transformAccess.length, Allocator.Persistent);
    }

    void Update()
    {
        var job = new TransformJob
        {
            velocities = _velocities,
            deltaTime = Time.deltaTime
        };
        job.Schedule(_transformAccess).Complete();
    }

    void OnDestroy()
    {
        _transformAccess.Dispose();
        _velocities.Dispose();
    }
}
```

---

## Common Pitfalls & Solutions

### 1. Race Conditions
```csharp
// ❌ WRONG - Race condition
struct BadJob : IJobParallelFor
{
    public NativeArray<float> SharedCounter;
    
    public void Execute(int index)
    {
        SharedCounter[0] += 1;  // Multiple threads writing to same index!
    }
}

// ✅ CORRECT - Use atomic operations
[BurstCompile]
struct GoodJob : IJobParallelFor
{
    [NativeDisableParallelForRestriction]  // Only if truly needed
    public NativeArray<float> SharedCounter;
    
    public void Execute(int index)
    {
        // Atomic increment
        System.Threading.Interlocked.Increment(ref SharedCounter[0]);
    }
}
```

### 2. Forgetting JobHandle.Complete()
```csharp
// ❌ WRONG - NativeArray disposed while job might be running
void OnDestroy()
{
    _positions.Dispose();  // Crash if job still running!
}

// ✅ CORRECT
void OnDestroy()
{
    _jobHandle.Complete();  // Ensure job finishes first
    _positions.Dispose();
}
```

### 3. Managed Type in Burst
```csharp
// ❌ WRONG - String not allowed in Burst
[BurstCompile]
struct BadJob : IJobParallelFor
{
    public string Name;  // Compilation error!
}

// ✅ CORRECT - Use NativeText or fixed buffers
[BurstCompile]
struct GoodJob : IJobParallelFor
{
    public unsafe fixed char Name[32];  // Fixed buffer
    // Or use Unity.Collections.NativeText
}
```

### 4. ReadOnly Missing
```csharp
// ❌ WRONG - Blocks parallelism
struct BadJob : IJobParallelFor
{
    public NativeArray<float> Input;  // Should be ReadOnly!
    public NativeArray<float> Output;
}

// ✅ CORRECT
[BurstCompile]
struct GoodJob : IJobParallelFor
{
    [ReadOnly] public NativeArray<float> Input;  // Allows parallel reading
    public NativeArray<float> Output;
}
```

---

## Performance Profiling

### Unity Profiler Integration

```csharp
using Unity.Profiling;

public class ProfiledSystem : MonoBehaviour
{
    private static readonly ProfilerMarker s_marker = new ProfilerMarker("MySystem.Update");

    void Update()
    {
        s_marker.Begin();
        
        // Your code here
        
        s_marker.End();
    }
}
```

### Burst Inspector

Window → Analysis → Burst Inspector
- View generated assembly code
- See SIMD vectorization
- Check for scalar fallbacks

### Job Performance Tips

| Factor | Recommendation |
|--------|----------------|
| Batch size | Start with 64, profile 32-256 range |
| Job size | Larger jobs = less overhead, but balance with parallelism |
| Dependencies | Minimize dependency chains for more overlap |
| Data size | Keep component data < 128 bytes for efficient chunk usage |
| Scheduling | Schedule early, Complete late for maximum overlap |

---

## Migration Checklist (MonoBehaviour → Jobs/Burst)

1. **Profile first** — Identify actual bottlenecks (> 1ms)
2. **Extract data** — Separate logic from MonoBehaviour, convert to value types
3. **Allocate NativeContainers** — Choose correct Allocator (Temp/TempJob/Persistent)
4. **Write job struct** — Implement `IJobParallelFor` or `IJobEntity`
5. **Add `[BurstCompile]`** — Verify no managed type errors
6. **Apply `[ReadOnly]`** — Mark inputs, enable parallelism
7. **Schedule in Update** — Complete in LateUpdate or next frame
8. **Dispose properly** — All NativeContainers must be disposed
9. **Batch size tuning** — Profile to find optimal (32-256 range)
10. **Verify performance** — Compare before/after with Profiler

---

## Additional Resources

- **Unity ECS Samples**: https://github.com/Unity-Technologies/EntityComponentSystemSamples
- **Burst User Guide**: https://docs.unity3d.com/Packages/com.unity.burst@latest
- **Job System Documentation**: https://docs.unity3d.com/Manual/JobSystem.html
- **Performance By Default**: https://unity.com/dots

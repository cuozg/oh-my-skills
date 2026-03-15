# Profiling Instrumentation Snippets

Quick-copy snippets for measuring performance before/after optimization.

## ProfilerMarker (Recommended)

```csharp
using Unity.Profiling;

public sealed class OptimizedSystem : MonoBehaviour
{
    // Static readonly — no allocation
    static readonly ProfilerMarker s_update = new("OptimizedSystem.Update");
    static readonly ProfilerMarker s_physics = new("OptimizedSystem.PhysicsQuery");
    static readonly ProfilerMarker s_ai = new("OptimizedSystem.AIDecision");

    void Update()
    {
        using (s_update.Auto())
        {
            using (s_physics.Auto())
                QueryPhysics();

            using (s_ai.Auto())
                RunAI();
        }
    }
}
```

## ProfilerCounter (Custom Metrics)

```csharp
using Unity.Profiling;

public sealed class GameMetrics : MonoBehaviour
{
    static readonly ProfilerCounter<int> s_activeEnemies = 
        new(ProfilerCategory.Scripts, "Active Enemies", ProfilerMarkerDataUnit.Count);
    static readonly ProfilerCounter<int> s_pooledObjects =
        new(ProfilerCategory.Scripts, "Pooled Objects", ProfilerMarkerDataUnit.Count);
    static readonly ProfilerCounter<float> s_frameAllocKB =
        new(ProfilerCategory.Memory, "Frame Alloc KB", ProfilerMarkerDataUnit.Bytes);

    void Update()
    {
        s_activeEnemies.Sample(EnemyRegistry.Count);
        s_pooledObjects.Sample(ObjectPool.TotalPooled);
    }
}
```

## GC Allocation Snapshot

```csharp
// Quick before/after GC measurement
public static class GCMeasure
{
    public static long MeasureAllocations(System.Action code)
    {
        System.GC.Collect();
        long before = System.GC.GetTotalMemory(true);
        code();
        long after = System.GC.GetTotalMemory(false);
        return after - before;
    }
}

// Usage
long alloc = GCMeasure.MeasureAllocations(() =>
{
    // code to measure
    mySystem.Update();
});
Debug.Log($"Allocated: {alloc} bytes");
```

## Stopwatch Timing

```csharp
using System.Diagnostics;

// For quick benchmarks outside Profiler
var sw = Stopwatch.StartNew();
for (int i = 0; i < 1000; i++)
    mySystem.ProcessBatch();
sw.Stop();
UnityEngine.Debug.Log($"1000 iterations: {sw.Elapsed.TotalMilliseconds:F2}ms " +
                      $"({sw.Elapsed.TotalMilliseconds / 1000:F4}ms per call)");
```

## Conditional Profiling (Strip from Release)

```csharp
// Only included in Development builds
[System.Diagnostics.Conditional("DEVELOPMENT_BUILD")]
[System.Diagnostics.Conditional("UNITY_EDITOR")]
static void ProfileLog(string msg) => UnityEngine.Debug.Log(msg);

// Or use #if
#if DEVELOPMENT_BUILD || UNITY_EDITOR
using (s_marker.Auto()) {
#endif
    ExpensiveOperation();
#if DEVELOPMENT_BUILD || UNITY_EDITOR
}
#endif
```

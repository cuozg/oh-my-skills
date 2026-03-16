# Custom Mode — Profiling Instrumentation

Generate profiling code snippets: ProfilerMarker, ProfilerRecorder, timed sections, and conditional profiling.

This is the only mode that produces code output instead of a read-only report.

## ProfilerMarker — Marking Code Sections

Add markers visible in the Unity Profiler's CPU module:

```csharp
using Unity.Profiling;

public class EnemyAI : MonoBehaviour
{
    // Define as static readonly to avoid string allocation
    static readonly ProfilerMarker s_UpdateMarker =
        new ProfilerMarker("EnemyAI.Update");
    static readonly ProfilerMarker s_PathfindMarker =
        new ProfilerMarker("EnemyAI.Pathfind");

    void Update()
    {
        using (s_UpdateMarker.Auto())
        {
            // Nested markers for sub-sections
            using (s_PathfindMarker.Auto())
            {
                CalculatePath();
            }
            ExecuteBehavior();
        }
    }
}
```

### Naming Convention

Use `ClassName.MethodName` format:
- `EnemyAI.Update`, `EnemyAI.Pathfind`
- `InventorySystem.Sort`, `InventorySystem.Search`
- `WorldGen.GenerateChunk`, `WorldGen.PlaceTrees`

### When to Add Markers

- Any method you suspect takes > 1ms
- Systems processing many entities (> 50)
- Code called from Update/FixedUpdate/LateUpdate
- Initialization code (scene load, asset loading)
- Custom systems not visible in default profiler (pooling, AI, networking)

## ProfilerRecorder — Reading Profiler Data in Code

Read profiler counters programmatically for automated performance monitoring:

```csharp
using Unity.Profiling;
using System.Text;

public class PerformanceMonitor : MonoBehaviour
{
    ProfilerRecorder _mainThreadRecorder;
    ProfilerRecorder _gcAllocRecorder;
    ProfilerRecorder _drawCallRecorder;

    void OnEnable()
    {
        _mainThreadRecorder = ProfilerRecorder.StartNew(
            ProfilerCategory.Internal, "Main Thread", 15);
        _gcAllocRecorder = ProfilerRecorder.StartNew(
            ProfilerCategory.Memory, "GC.Alloc.In.Frame.Count", 15);
        _drawCallRecorder = ProfilerRecorder.StartNew(
            ProfilerCategory.Render, "Draw Calls Count", 15);
    }

    void OnDisable()
    {
        _mainThreadRecorder.Dispose();
        _gcAllocRecorder.Dispose();
        _drawCallRecorder.Dispose();
    }

    void Update()
    {
        // Log when frame time exceeds budget
        if (_mainThreadRecorder.Valid)
        {
            double frameMs = _mainThreadRecorder.LastValueAsDouble / 1_000_000.0;
            if (frameMs > 16.67)
            {
                Debug.LogWarning($"Frame spike: {frameMs:F1}ms");
            }
        }
    }
}
```

### Common ProfilerRecorder Counters

| Category | Counter Name | Unit |
|----------|-------------|------|
| Internal | `Main Thread` | nanoseconds |
| Memory | `GC.Alloc.In.Frame.Count` | count |
| Memory | `GC.Allocated In Frame` | bytes |
| Memory | `Total Used Memory` | bytes |
| Render | `Draw Calls Count` | count |
| Render | `Batches Count` | count |
| Render | `Triangles Count` | count |
| Render | `Vertices Count` | count |

## Stopwatch for Quick Measurement

For one-off measurement without Profiler integration:

```csharp
using System.Diagnostics;

var sw = Stopwatch.StartNew();
ExpensiveOperation();
sw.Stop();
UnityEngine.Debug.Log($"ExpensiveOperation: {sw.ElapsedMilliseconds}ms");
```

## Conditional Profiling (Development Builds Only)

Wrap profiling code so it compiles out of release builds:

```csharp
using System.Diagnostics;
using Unity.Profiling;

public class GameSystem : MonoBehaviour
{
    static readonly ProfilerMarker s_Marker = new ProfilerMarker("GameSystem.Process");

    void Process()
    {
        using (s_Marker.Auto()) // ProfilerMarker has zero overhead when profiler not attached
        {
            // work
        }
    }

    [Conditional("DEVELOPMENT_BUILD"), Conditional("UNITY_EDITOR")]
    void LogPerformanceStats()
    {
        // Only compiled in development builds and editor
        Debug.Log($"Entities processed: {_count}");
    }
}
```

## When to Use Each Tool

| Need | Tool | Overhead |
|------|------|----------|
| Visualize timing in Profiler | `ProfilerMarker` | Near-zero when not recording |
| Read counters in code | `ProfilerRecorder` | Minimal |
| Quick one-off measurement | `Stopwatch` | Negligible |
| Full call stack analysis | Deep Profile toggle | ~10x (timing unreliable) |
| Memory allocation tracking | Memory Profiler package | Snapshot-based, no runtime cost |
| Draw call inspection | Frame Debugger | Editor only, pauses rendering |

## For More Patterns

Load `unity-standards` for additional ProfilerMarker patterns and Burst compiler integration:
- `read_skill_file("unity-standards", "references/review/performance-checklist-advanced.md")`

# Benchmark & Measurement Template

## Before/After Report Format

```markdown
# Optimization Measurement Report
**Target:** [file/system name] | **Date:** [date] | **Platform:** [target]

## Baseline (Before)

| Metric | Value | Source |
|--------|-------|--------|
| Frame time (avg) | [ms] | Profiler |
| GC Alloc/frame | [bytes] | Profiler → GC.Alloc |
| Draw calls | [count] | Frame Debugger |
| SetPass calls | [count] | Frame Debugger |
| Batches | [count] | Stats window |
| Peak memory | [MB] | Memory Profiler |
| Build size | [MB] | Build report |

## Changes Applied

| # | Change | Category | Files |
|---|--------|----------|-------|
| 1 | [what was changed] | Code/Settings/Asset | [files] |

## Result (After)

| Metric | Before | After | Delta | % Change |
|--------|--------|-------|-------|----------|
| Frame time | [ms] | [ms] | [ms] | [%] |
| GC Alloc/frame | [B] | [B] | [B] | [%] |
| Draw calls | [n] | [n] | [n] | [%] |

## Analysis

[What worked, what didn't, next steps]
```

## Measurement Methods

### GC Allocation Profiling

```csharp
// Method 1: Profiler.BeginSample (visible in Profiler)
using UnityEngine.Profiling;

Profiler.BeginSample("MyOptimizedCode");
// ... code under test ...
Profiler.EndSample();

// Method 2: ProfilerMarker (lower overhead)
static readonly ProfilerMarker s_marker = new("MyOptimizedCode");
using (s_marker.Auto()) { /* code */ }

// Method 3: GC.GetTotalMemory snapshot
long before = System.GC.GetTotalMemory(false);
// ... code under test ...
long after = System.GC.GetTotalMemory(false);
Debug.Log($"Allocated: {after - before} bytes");
```

### Frame Time Measurement

```csharp
// Simple frame time tracking
private float _frameTimeAccum;
private int _frameCount;

void Update()
{
    _frameTimeAccum += Time.unscaledDeltaTime;
    _frameCount++;
    if (_frameCount >= 60) // average over 60 frames
    {
        float avg = _frameTimeAccum / _frameCount * 1000f;
        Debug.Log($"Avg frame time: {avg:F2}ms ({1000f/avg:F0} FPS)");
        _frameTimeAccum = 0f;
        _frameCount = 0;
    }
}
```

## Frame Budget Reference

| Target FPS | Budget per Frame | CPU Budget | GPU Budget |
|-----------|-----------------|------------|------------|
| 30 fps | 33.3 ms | ~20 ms | ~25 ms |
| 60 fps | 16.67 ms | ~10 ms | ~12 ms |
| 90 fps (VR) | 11.1 ms | ~7 ms | ~8 ms |
| 120 fps | 8.33 ms | ~5 ms | ~6 ms |

Note: CPU + GPU overlap — total can exceed frame budget if not bottlenecked on same resource.

## Common Measurement Mistakes

- Measuring in Editor (10-100x overhead from Editor hooks)
- Not warming up (first frame includes shader compilation, asset loading)
- Too few samples (measure 60-300 frames minimum)
- Deep Profiler enabled (adds massive overhead, distorts results)
- GC.Collect between tests (resets heap, may hide sustained pressure)

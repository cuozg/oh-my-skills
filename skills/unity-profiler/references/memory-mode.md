# Memory Mode — GC Pressure & Leak Detection

Analyze garbage collection spikes, heap growth, and memory leaks.

## Unity Profiler Memory Analysis

1. Open **Profiler** window → **Memory** module
2. Switch between **Simple** (overview) and **Detailed** (per-type breakdown) views
3. Watch **GC Allocated in Frame** — anything > 0 in gameplay is suspect
4. Track **Total Reserved** vs **Total Used** — growing gap means fragmentation

### Memory Profiler Package

For deeper analysis, use the **Memory Profiler** package (`com.unity.memoryprofiler`):
1. Take snapshots at different points (scene load, gameplay, scene transition)
2. Compare snapshots to find retained objects
3. Check **All Of Memory** tab for native vs managed breakdown
4. Use **References** view to trace retention paths

## GC Pressure Indicators

| Signal | Severity | Implication |
|--------|----------|-------------|
| GC.Alloc > 10 KB/frame sustained | CRITICAL | Frequent GC pauses, visible hitches |
| GC.Alloc 1-10 KB/frame | WARNING | Accumulating pressure, eventual spikes |
| GC.Collect marker > 5ms | CRITICAL | GC pause causing frame drop |
| GC.Collect frequency > 1/sec | WARNING | Too many short-lived allocations |
| Heap growing without plateau | WARNING | Possible leak or unbounded cache |

## Leak Detection Strategy

1. **Scene transition test**: Load scene A → scene B → scene A → snapshot
   - Objects from first scene A still retained = leak
2. **Gameplay test**: Play 5 min → snapshot → play 5 more → snapshot
   - Growing object counts of same type = leak
3. **Check retention paths**: In Memory Profiler, find what holds the leaked object
   - Static references, event subscriptions, or uncleaned collections are common roots

## Common Memory Anti-Patterns

| Pattern | Impact | Fix |
|---------|--------|-----|
| Allocations in Update/FixedUpdate | Per-frame GC pressure | Cache, pool, or pre-allocate |
| `string` concat in hot paths | Creates garbage per concat | `StringBuilder` or `TMP_Text.SetText` |
| LINQ in hot paths | Enumerator + closure alloc | Manual loops with cached collections |
| `new List<T>()` per frame | List + array alloc | Reuse with `.Clear()` |
| Closure captures in lambdas | Delegate + closure alloc | Cache delegate or use static lambda |
| Boxing via `object` parameters | Box alloc per call | Generic overloads or `in` parameters |
| `foreach` on Dictionary/HashSet | Enumerator struct boxed (pre-2020) | Use `GetEnumerator()` directly or `for` |
| `Resources.Load` without unload | Keeps asset in memory | Use Addressables with handle release |
| Event += without -= | Retains subscriber | Unsubscribe in OnDestroy/OnDisable |
| Static collections growing | Never collected | Evict, weak references, or cap size |

## Codebase Scan Targets

Grep for allocation patterns in hot paths:

```
new List<              — in Update/FixedUpdate/LateUpdate
new Dictionary<        — in Update/FixedUpdate/LateUpdate
new HashSet<           — in Update/FixedUpdate/LateUpdate
.ToList()              — materializing LINQ
.ToArray()             — materializing LINQ
new WaitForSeconds     — cache YieldInstruction
new WaitForEndOfFrame  — cache YieldInstruction
string.Format          — in hot paths (allocates)
$"                     — string interpolation in hot paths
.ToString()            — boxing value types
delegate               — anonymous delegates in hot paths
=>                     — lambda closures capturing variables
Resources.Load         — without corresponding UnloadUnusedAssets
+=                     — event subscriptions (check for matching -=)
```

## Incremental GC

Unity's incremental GC spreads collection across frames. Check:
- **Player Settings → Other Settings → Use Incremental GC**: should be ON for most projects
- Even with incremental GC, reducing allocations is still important — incremental GC reduces spike severity but not total GC cost
- `GarbageCollector.GCMode` can be set to `Disabled` during critical gameplay sections, but must be re-enabled to avoid out-of-memory

## Platform Memory Budgets

| Platform | Typical Budget | Warning Threshold |
|----------|---------------|-------------------|
| Mobile (low-end) | 512 MB total | > 300 MB |
| Mobile (high-end) | 2 GB total | > 1 GB |
| Console | 4-8 GB | > 3 GB |
| PC | 8-16 GB | > 4 GB |

These are total application memory. Managed heap is typically 10-20% of total. Native memory (textures, meshes, audio) dominates.

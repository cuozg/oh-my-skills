# CPU Mode — Frame & Scripting Analysis

Identify slow frames and trace them to specific scripts and systems in the codebase.

## Frame Budget Reference

| Target | Budget | Scripting Share | Thermal (Mobile) |
|--------|--------|-----------------|-------------------|
| 60 fps | 16.67ms | ~5ms | 10.83ms (0.65x) |
| 30 fps | 33.33ms | ~10ms | 21.67ms (0.65x) |
| 90 fps (VR) | 11.11ms | ~3ms | 7.22ms (0.65x) |

Scripting should use at most ~30% of the total frame budget. If scripting alone exceeds this, the frame is CPU-bound.

## Unity Profiler CPU Analysis

1. Open **Profiler** window → **CPU Usage** module
2. Enable **Deep Profile** for full call stacks (warning: significant overhead, disable for timing accuracy)
3. Switch to **Timeline** view to see thread distribution
4. Look for spikes in the **PlayerLoop** section — drill into to find the expensive call
5. Check **Editor-only** overhead: look for `EditorLoop` markers and discount them

### Key Profiler Markers to Watch

| Marker | Subsystem | Concern When |
|--------|-----------|-------------|
| `PlayerLoop` | Overall | > budget |
| `Update.ScriptRunBehaviourUpdate` | MonoBehaviour.Update | > 5ms at 60fps |
| `BehaviourUpdate` | Individual MB | Any single MB > 1ms |
| `FixedUpdate.ScriptRunBehaviourFixedUpdate` | Physics scripts | > 3ms |
| `LateUpdate.ScriptRunBehaviourLateUpdate` | Camera/follow scripts | > 2ms |
| `Coroutines.DelayedCalls` | Coroutines | > 1ms or many active |
| `Physics.Processing` | PhysX | > 3ms |
| `Animation.Update` | Animator | > 2ms with many animators |

## Common CPU Bottlenecks

| Pattern | Impact | Fix |
|---------|--------|-----|
| `FindObjectOfType` in Update | Scans entire scene | Cache reference in Awake or use registry |
| `Camera.main` in Update (pre-2020.2) | Find + string compare | Cache in Awake (safe on 2020.2+) |
| `GetComponent<T>()` per frame | Repeated lookup | Cache in Awake/Start |
| Nested loops in Update | O(n^2) per frame | Spatial partitioning, early exit, or stagger |
| LINQ in hot paths | Enumerator allocation | Manual loop with cached collection |
| String concatenation in Update | GC pressure | StringBuilder or TMP SetText |
| `SendMessage` / `BroadcastMessage` | Reflection-based | Direct call or interface |
| Coroutine yielding `new WaitForSeconds` | Allocation per yield | Cache the YieldInstruction |

## Codebase Scan Targets

Grep for these patterns — each is a potential CPU hotspot:

```
FindObjectOfType     — in any Update/FixedUpdate/LateUpdate method
Camera.main          — in hot paths (check Unity version)
GetComponent         — in Update (should be cached in Awake)
SendMessage          — anywhere (use direct calls)
foreach              — on non-List/Array collections in Update (enumerator alloc)
.Where(              — LINQ in hot paths
.Select(             — LINQ in hot paths
.ToList()            — LINQ materialization in hot paths
.ToArray()           — Array allocation in hot paths
new List<            — allocation in Update
new Dictionary<      — allocation in Update
string +             — concatenation in Update
$"                   — string interpolation in Update
.ToString()          — value type boxing in hot paths
Instantiate(         — without pooling in gameplay loops
Destroy(             — without pooling in gameplay loops
```

## Deep Profiling vs Instrumentation

**Deep Profile** captures every method call but adds ~10x overhead — timing data is unreliable. Use it only to find *which* methods are called, not *how long* they take.

For accurate timing, add `ProfilerMarker` instrumentation to suspect methods (see Custom mode). This gives precise timing without the overhead penalty.

## Thread Analysis

In **Timeline** view, check:
- **Main Thread**: All MonoBehaviour callbacks, UI, rendering commands
- **Render Thread**: Graphics API calls (if separate)
- **Job Worker threads**: Jobs system, Burst-compiled work
- **Loading threads**: Asset loading, addressable operations

If main thread is blocked waiting on a job, the bottleneck is the job dependency chain, not the main thread code itself.

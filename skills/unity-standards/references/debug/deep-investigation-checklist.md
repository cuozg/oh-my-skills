# Deep Investigation Checklist

Multi-angle bug analysis using targeted investigation angles. Use this checklist to systematically explore root causes before proposing solutions.

## Investigation Angles

### 1. Lifecycle Angle
- Trace `Awake -> OnEnable -> Start -> Update/LateUpdate -> OnDisable -> OnDestroy` for all involved objects
- Check whether the component is active, destroyed prematurely, or re-instantiated
- **Key file pattern:** `[DefaultExecutionOrder]`, event subscription timing, bootstrapping order
- **Grep:** `Awake|OnEnable|Start|OnDisable|OnDestroy`

### 2. Data Flow Angle
- Identify the value at the source (serialized field, method return, event payload)
- Trace every assignment and every read
- Check whether the value is null, empty, defaulted, or overwritten later
- **Key file pattern:** every writer and every reader of the target value
- **Grep:** variable name, assignment sites, conditional reads, and logging sites

### 3. Threading Angle
- Identify coroutines, async and await, Jobs, callbacks from non-main systems, and any explicit thread-pool work
- Check whether data is accessed from multiple threads, crosses a frame boundary, or re-enters Unity API from a worker thread
- **Key file pattern:** `yield`, `async`, `Awaitable.BackgroundThreadAsync`, `Task.Run`, `IJob`, `IJobParallelFor`, `OnAudioFilterRead`
- **Grep:** `yield|async|Awaitable|Task|Job|Parallel|OnAudioFilterRead`

### 4. State Transitions Angle
- Map every state variable and valid transition path
- Check whether invalid transitions or check-then-mutate races are possible
- **Key file pattern:** booleans, enums, and transition-heavy branches
- **Grep:** state variable writes plus every conditional read

### 5. Edge Cases Angle
- Null refs: uninitialized field, destroyed object, missing serialized ref
- Empty collections: `Count == 0`, indexing empty lists
- Math: division by zero, precision loss, negative values where positive expected
- Timing: object destroyed before async completion, listener removed mid-iteration
- **Grep:** direct indexing, unchecked division, dereference without guard

### 6. Event System Angle (If Applicable)
- Trace who subscribes, when they subscribe, and when they unsubscribe
- Check whether stale listeners remain after disable or destroy
- **Key file pattern:** `event`, `+=`, `-=`, `OnDestroy`, static buses
- **Grep:** event name plus `+=` and `-=`

### 7. Serialization Angle (If Applicable)
- Check whether the value is actually serialized and whether the type is supported
- Compare Inspector state with runtime state
- Validate prefab overrides and managed-reference usage where relevant
- **Key file pattern:** `[SerializeField]`, `[SerializeReference]`, `[FormerlySerializedAs]`, property declarations, ScriptableObject refs
- **Grep:** target field name, type definition, rename attributes

## Confidence Scoring

| Confidence | Criteria |
|------------|----------|
| High | Evidence found in file and line, direct causation is clear |
| Medium | Likely candidate with indirect evidence |
| Low | Speculative; mark as unconfirmed |

## Evidence Format

```
Evidence: File.cs:line - specific code snippet or description
Angle: [angle name from above]
```

## Quick Reference: Common Causes By Category

### Intermittent Or Race-Like
- Threading angle: data accessed unsafely across threads or async boundaries
- Lifecycle angle: execution order dependency not enforced
- Event angle: stale listener still subscribed

### Works In Editor, Broken In Build
- Serialization: unsupported type or non-serialized property relied on by the Inspector
- Edge case: IL2CPP stripping or AOT assumption
- Threading: main-thread assumptions hidden by editor timing

### Worked Yesterday, Broken Today
- Scene reload: object not re-initialized in `OnEnable`
- Dependency or package version change: API behavior shifted
- Lifecycle: initialization order assumption exposed by another change

### NullReferenceException
- Data flow: dereference with no guard
- Lifecycle: dependency lookup happens before target exists
- Serialization: missing or lost Inspector assignment

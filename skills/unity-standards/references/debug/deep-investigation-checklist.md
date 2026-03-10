# Deep Investigation Checklist

Multi-angle bug analysis using targeted investigation angles. Use this checklist to systematically explore root causes before proposing solutions.

## Investigation Angles

### 1. Lifecycle Angle
- Trace Awake → OnEnable → Start → Update/LateUpdate → OnDisable → OnDestroy for ALL involved objects
- Check: Is component/object active? Destroyed prematurely? Re-instantiated?
- **Key file pattern**: `[DefaultExecutionOrder]`, event subscription/unsubscription timing
- **Grep**: `Awake|OnEnable|Start|OnDisable|OnDestroy` + scene reload patterns

### 2. Data Flow Angle
- Identify value at source (serialized field, method return, event payload)
- Trace through every assignment and read
- Check: Is value null? Empty? Default? Corrupted by modification?
- **Key file pattern**: Every writer to the variable (assignment targets), every reader (conditionals, logs, function args)
- **Grep**: Variable name + grep all files; `_fieldName\s*=` for writers, `_fieldName\s*[!=<>]` for readers

### 3. Threading Angle
- Identify: Coroutines, `WaitForSeconds`, async/await, `Parallel.ForEach`, Jobs, `Physics.BakeMesh`, callbacks
- Check: Is value accessed from multiple threads? Mutated without lock? Yielded across frame boundary?
- **Key file pattern**: `yield`, `async`, `IJob`, `IJobParallelFor`, `OnCollisionEnter` (physics thread)
- **Grep**: `yield|async|Task|Job|Parallel` + target method names; check if accessed in different threads

### 4. State Transitions Angle
- Map every state variable; chart valid state paths
- Check: Invalid transition possible? Race condition in state check + mutation?
- **Key file pattern**: Boolean flags, enums with transitions, if/else chains controlling behavior
- **Grep**: State variable name; map all writes and conditional reads

### 5. Edge Cases Angle
- Null refs: uninitialized field, destroyed object, missing serialized ref
- Empty collections: `Count == 0`, indexing empty list
- Math: division by zero, float precision, negative values where positive expected
- Timing: object destroyed before operation completes, listener removed mid-iteration
- **Grep**: Direct indexing `[0]`, division without guard, no null check before dereference

### 6. Event System Angle _(if applicable)_
- Trace: Who subscribes? When? In what order? Who unsubscribes?
- Check: Unsubscribe in OnDestroy? Stale listener still subscribed? Event fired after listener destroyed?
- **Key file pattern**: `event`, `+=`, `-=`, `OnDestroy` unsubscribe, static/global event buses
- **Grep**: Event name + `+=|-=` patterns; cross-ref listeners

### 7. Serialization Angle _(if applicable)_
- Check: Is field `public` without `[SerializeField]`? Is type serializable? Property instead of field?
- Trace: Value in Inspector vs runtime value; prefab override state
- **Key file pattern**: `[SerializeField]`, `[NonSerialized]`, property declarations, ScriptableObject refs
- **Grep**: Target field name in .cs; check for type annotations

## Confidence Scoring

| Confidence | Criteria |
|------------|----------|
| **HIGH** | Evidence found in file:line. Direct causation clear. Reproducible pattern. |
| **MED** | Likely candidate but indirect evidence. Alternative explanations possible. |
| **LOW** | Speculative. No direct file evidence. [UNCONFIRMED]. |

## Evidence Format

```
Evidence: File.cs:line — specific code snippet or description
Angle: [angle name from above]
```

## Quick Reference: Common Causes by Category

### Intermittent / Race-Condition-Like
- Threading angle: Value accessed unsafely from multiple threads
- Lifecycle angle: Execution order dependency not enforced
- Event angle: Unsubscribe not called; stale listener fires

### "Works in Editor, Broken in Build"
- Serialization: Non-serialized public property; IL2CPP stripping
- Edge case: IL2CPP requires `[Preserve]` for reflection targets
- Threading: Main thread safety assumptions

### "Worked Yesterday, Broken Today"
- Scene reload: Object not re-initialized in OnEnable
- Dependency version change: API signature or behavior changed
- Lifecycle: Initialization order not enforced; race condition exposed

### NullReferenceException
- Data flow: No null check before dereference
- Lifecycle: GetComponent/Find called before target exists
- Serialization: Public field assigned in Editor, missing at runtime

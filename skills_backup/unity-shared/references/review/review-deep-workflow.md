# Deep Review Workflow Details

## Step 3: Deep Investigate (Parallel Evidence Gathering)

Spawn agents to gather evidence:

**`@explore` agents (2-3):**

| Agent | Task |
|:------|:-----|
| Call-site analysis | For each modified public method/property: find ALL callers, count call sites, identify which pass null/edge values. |
| State flow | Trace state transitions: what sets each field, what reads it, can it be in an invalid state between set and read? |
| Data contract | Check serialization, API boundaries, event payloads — does the data shape match all consumers? |

## Step 4: Logic Review Focus Areas

### Control Flow
- Every `if` branch: what happens in the else? Is the else path even possible?
- Every loop: can it infinite-loop? Off-by-one? Empty collection?
- Every early return: does it skip cleanup that should happen?
- Every switch: missing cases? Fall-through intentional?

### State Management
- Field mutations: who else reads this field? Will they see a consistent state?
- Init order: can this be called before initialization completes?
- Lifetime: can this reference outlive the object it points to?

### Data Flow
- Input validation: what values can arrive? Are all handled?
- Null propagation: if A is null, does the chain handle it or crash 3 calls deep?
- Type safety: any unsafe casts, enum-to-int conversions, implicit narrowing?

### Edge Cases
- Zero, null, empty, max, negative, duplicate, concurrent
- First call vs subsequent calls
- Normal path vs error recovery path

### Unity Lifecycle Verification
- For EVERY `MonoBehaviour` in the diff, verify full lifecycle coverage
- What is initialized in `Awake` vs `Start`? Any cross-component access in `Awake`?
- Are `OnEnable`/`OnDisable` balanced? (subscribe/unsubscribe, register/deregister)
- Are coroutines stopped in `OnDisable`?
- Are DOTween animations killed in `OnDisable`/`OnDestroy`?
- Is there cleanup in `OnDestroy` for native resources?
- If `DontDestroyOnLoad`: is there a duplicate guard?
- If `[ExecuteAlways]`: are Editor and Play mode paths properly split?

### Serialization Safety Check
- For any changed `[SerializeField]`, `[Serializable]`, or public field, verify migration safety
- Was the field renamed? -> add `[FormerlySerializedAs]`
- Was the type changed? -> require migration path or explicit data reset strategy
- Was a field added to a ScriptableObject? -> validate safe defaults
- Was a field removed? -> verify prefabs/SOs do not still depend on serialized data
- Is the field interface/abstract? -> Unity default serializer needs `[SerializeReference]` or concrete type

### Memory Safety Audit
- Any `new` inside `Update`/`LateUpdate`/`FixedUpdate`? (per-frame allocation)
- Any event `+=` without corresponding `-=`?
- Any `Addressables.LoadAssetAsync` without `Release` ownership?
- Any `UnityWebRequest` without `using`/`Dispose`?
- Any texture/mesh created at runtime without `Destroy`?
- Any static collections that grow without clear/reset?
- Any delegate/lambda capturing `this` in long-lived context?

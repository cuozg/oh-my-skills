# Unity-Specific Review Checklist

## MonoBehaviour Lifecycle

### Initialization
- [ ] `Awake()` for self-initialization (cache components, set defaults)
- [ ] `Start()` for cross-component initialization (references to other objects)
- [ ] `OnEnable()` for event subscriptions and state activation
- [ ] No `FindObjectOfType` in `Awake` (order not guaranteed)
- [ ] No heavy computation in `Awake` or `Start` (defer to async)

### Update Methods
- [ ] Logic in correct update: `Update` (input/game logic), `FixedUpdate` (physics), `LateUpdate` (camera/follow)
- [ ] No empty `Update()` / `FixedUpdate()` / `LateUpdate()` methods (remove them)
- [ ] No heavy allocations in update methods
- [ ] Rate limiting for expensive per-frame operations

### Cleanup
- [ ] `OnDisable()` unsubscribes events registered in `OnEnable()`
- [ ] `OnDestroy()` releases unmanaged resources
- [ ] Coroutines stopped in `OnDisable()`
- [ ] DOTween animations killed in `OnDisable()` / `OnDestroy()`
- [ ] `CancellationTokenSource` disposed in `OnDestroy()`
- [ ] No null reference exceptions during teardown

### Lifecycle Balance
- [ ] Every `OnEnable` has matching `OnDisable`
- [ ] Every `Subscribe` has matching `Unsubscribe`
- [ ] Every `+=` has matching `-=`
- [ ] Every `Instantiate` has matching `Destroy` or pool return
- [ ] Every `Addressables.LoadAssetAsync` has matching `Release`

## Serialization

### SerializeField
- [ ] `[SerializeField]` on private fields (not public fields)
- [ ] `[field: SerializeField]` for auto-properties
- [ ] `[FormerlySerializedAs("oldName")]` when renaming serialized fields
- [ ] No interface/abstract types without `[SerializeReference]`
- [ ] Default values set for new serialized fields (prefab safety)
- [ ] `[Range]`, `[Min]`, `[Tooltip]` attributes for designer-facing fields

### ScriptableObject
- [ ] `[CreateAssetMenu]` attribute for creation
- [ ] No mutable state that persists between play sessions
- [ ] Reset to defaults in `OnEnable()` if needed
- [ ] Null checks for referenced assets

### Prefab Safety
- [ ] No broken references (missing scripts, null refs)
- [ ] Prefab overrides intentional (not accidental)
- [ ] Nested prefab structure documented
- [ ] No `DontDestroyOnLoad` without duplicate guard

## Coroutine Safety

- [ ] Coroutine references stored for `StopCoroutine`
- [ ] `StopAllCoroutines()` in `OnDisable()` when appropriate
- [ ] No `yield return new WaitForSeconds()` in loops (cache it)
- [ ] No coroutine started in `OnDisable()` or `OnDestroy()`
- [ ] Consider UniTask migration for new async code

## Transform & Hierarchy

- [ ] `SetParent(parent, false)` when world position doesn't matter
- [ ] `localPosition` vs `position` used correctly
- [ ] No deep hierarchy nesting (>5 levels impacts performance)
- [ ] No frequent `SetParent` calls (reparenting is expensive)
- [ ] `Transform.SetSiblingIndex` used sparingly

## Input Handling

- [ ] New Input System preferred over legacy `Input.GetKey`
- [ ] Input processed in `Update()` (not `FixedUpdate()`)
- [ ] Input actions defined in InputActionAsset (not hardcoded strings)
- [ ] Enable/Disable input actions in `OnEnable()` / `OnDisable()`

## Physics

- [ ] Rigidbody required for collider interaction
- [ ] Physics code in `FixedUpdate()` (not `Update()`)
- [ ] Layer-based collision matrix configured
- [ ] Trigger vs Collider used correctly
- [ ] `Physics.SyncTransforms()` called if modifying transforms in physics callbacks
- [ ] No `MovePosition` / `AddForce` in `Update()` (use `FixedUpdate()`)

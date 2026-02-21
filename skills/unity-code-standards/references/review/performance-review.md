# Performance Review Checklist

## Per-Frame Allocations (Critical)

### Update/FixedUpdate/LateUpdate
- [ ] No `new` allocations (List, Dictionary, arrays, strings)
- [ ] No LINQ queries (Where, Select, OrderBy — they allocate)
- [ ] No string concatenation or interpolation
- [ ] No boxing (struct → object, struct → interface without generic)
- [ ] No `GetComponent<T>()` (cache in Awake)
- [ ] No `FindObjectOfType<T>()` or `FindObjectsOfType<T>()`
- [ ] No `Resources.Load<T>()`
- [ ] No `new WaitForSeconds()` (cache as field)
- [ ] No closure-capturing lambdas
- [ ] No `ToString()` unless result is cached

### Alternatives for Hot Paths
- [ ] Pre-allocated collections reused via `.Clear()`
- [ ] `StringBuilder` cached and reused
- [ ] Component references cached in `Awake()`
- [ ] `ObjectPool<T>` for frequently created/destroyed objects
- [ ] `NativeArray<T>` for large data sets
- [ ] Manual loops instead of LINQ
- [ ] `stackalloc` for small temporary buffers

## Component Access

- [ ] `GetComponent<T>()` called in `Awake()` and cached
- [ ] `TryGetComponent<T>()` used when component may not exist
- [ ] `CompareTag()` instead of `tag ==` (avoids allocation)
- [ ] No repeated `transform.position` access (cache in local variable)
- [ ] No `SendMessage()` / `BroadcastMessage()` (use direct references or events)

## Physics

- [ ] `Physics.RaycastNonAlloc()` instead of `Physics.RaycastAll()`
- [ ] `Physics.OverlapSphereNonAlloc()` instead of `Physics.OverlapSphere()`
- [ ] Pre-allocated `RaycastHit[]` / `Collider[]` arrays
- [ ] Layer masks used for all physics queries
- [ ] No physics queries in `Update` without throttling
- [ ] `FixedUpdate` for physics-related code (not `Update`)

## Memory Management

### Object Lifetime
- [ ] Object pooling for frequently spawned/destroyed objects
- [ ] `Addressables.Release()` called for loaded assets
- [ ] `UnityWebRequest` wrapped in `using`
- [ ] Runtime-created textures/meshes destroyed in `OnDestroy()`
- [ ] Event `+=` paired with `-=` (subscribe/unsubscribe balance)
- [ ] `CancellationTokenSource` disposed when no longer needed
- [ ] Static collections cleared on scene transitions

### GC Optimization
- [ ] `struct` for small, immutable value types
- [ ] `readonly record struct` for signal/event data
- [ ] `IEquatable<T>` implemented on structs used as dictionary keys
- [ ] `ArrayPool<T>.Shared` for temporary arrays
- [ ] No boxing of structs (use generic methods/collections)
- [ ] `Span<T>` / `ReadOnlySpan<T>` for temporary slicing
- [ ] Delegate caching for repeated callbacks

## Rendering Performance

### Draw Calls
- [ ] Static batching for non-moving objects
- [ ] Dynamic batching enabled for small meshes
- [ ] GPU instancing for repeated meshes
- [ ] SRP Batcher compatible shaders
- [ ] Sprite Atlas for 2D sprites
- [ ] No unnecessary material instances (`.material` creates copy)

### LOD & Culling
- [ ] LOD Groups configured for complex meshes
- [ ] Occlusion Culling set up for indoor scenes
- [ ] Camera far clip plane appropriate
- [ ] Object culling layers configured
- [ ] Particle system max particles limited

## Async & Threading

### UniTask
- [ ] `CancellationToken` passed to all async methods
- [ ] `GetCancellationTokenOnDestroy()` used in MonoBehaviours
- [ ] `OperationCanceledException` caught and handled (not swallowed)
- [ ] No `Task` return types (use `UniTask`)
- [ ] No `async void` (use `async UniTaskVoid`)
- [ ] `.Forget()` used for intentional fire-and-forget
- [ ] `UniTask.WhenAll()` for parallel operations

### Coroutines (Legacy)
- [ ] `StopCoroutine` / `StopAllCoroutines` in `OnDisable`
- [ ] Cached `WaitForSeconds` / `WaitForEndOfFrame`
- [ ] No `yield return new` in loops (pre-cache)

## Animation & Tweening

- [ ] Animator parameters accessed by hash (`Animator.StringToHash`)
- [ ] DOTween sequences killed in `OnDisable` / `OnDestroy`
- [ ] No string-based animation access (use hashes)
- [ ] Animation events don't allocate

## UI Performance

- [ ] Canvas splitting (static vs dynamic elements)
- [ ] Raycast Target disabled on non-interactive elements
- [ ] `Canvas.willRenderCanvases` not triggered unnecessarily
- [ ] Object pooling for dynamic list items
- [ ] No layout recalculation in `Update`
- [ ] TextMeshPro used instead of legacy Text

## Profiling Indicators

### Red Flags (Immediate Action)
- Allocation in `Update()` / `FixedUpdate()` / `LateUpdate()`
- `GetComponent` in per-frame code
- LINQ in hot paths
- `FindObjectOfType` at runtime
- Unbounded collection growth

### Yellow Flags (Investigate)
- Large `foreach` without pool
- String operations in frequently called methods
- Multiple `GetComponent` calls for same type
- Coroutine-heavy code (consider UniTask migration)
- Static event handlers without cleanup

### Green Flags (Best Practices)
- Object pooling with warmup
- Component caching in Awake
- NativeArray for compute
- Manual loops in hot paths
- Pre-sized collections

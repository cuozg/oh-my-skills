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

Continue in [perf-render.md](perf-render.md) for Rendering, Async/Threading, Animation, UI, and Profiling sections.

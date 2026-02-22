# Performance Review Checklist — Advanced Topics

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

See also [performance-review.md](performance-review.md) for Per-Frame Allocations, Component Access, Physics, and Memory Management sections.

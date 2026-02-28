# Performance Checklist

## CPU — Hot Path (Update/FixedUpdate/LateUpdate)

### :red_circle: Critical — Per-Frame Allocations
- [ ] No `new List/Dictionary/HashSet` in Update
- [ ] No string concatenation (`+`, `$""`, `string.Format`) in Update
- [ ] No LINQ queries (`.Where`, `.Select`, `.FirstOrDefault`) in Update
- [ ] No `foreach` on non-cached collections in Update (iterator alloc on older Mono)
- [ ] No boxing (value type → object) in Update
- [ ] No `yield return new WaitForSeconds()` every frame (cache it)
- [ ] No `Enum.ToString()` / `Enum.Parse()` in hot paths
- [ ] No `JsonUtility.ToJson/FromJson` in Update

### :red_circle: Critical — Expensive Calls in Hot Path
- [ ] No `GetComponent<T>()` in Update — cache in Awake
- [ ] No `Camera.main` in Update — cache in Awake
- [ ] No `Find()` / `FindObjectOfType()` / `FindObjectsOfType()` at runtime
- [ ] No `Resources.Load()` in Update
- [ ] No `Physics.Raycast` without layer mask
- [ ] No `SendMessage` / `BroadcastMessage` anywhere
- [ ] No `Material.SetFloat/Color("string")` in Update — cache `Shader.PropertyToID`
- [ ] No `Animator.SetTrigger("string")` in Update — cache `StringToHash`

### :orange_circle: High — Computation
- [ ] No O(n^2) algorithms in per-frame code
- [ ] Math-heavy operations use Burst/Jobs where appropriate
- [ ] Spatial queries use appropriate structures (octree, grid, BVH)
- [ ] Pathfinding is async or amortized across frames
- [ ] AI/behavior calculations amortized or LOD-based

## Memory

### Allocation Patterns
- [ ] Object pooling for frequently spawned/destroyed objects
- [ ] Pre-allocated buffers for physics queries (NonAlloc APIs)
- [ ] StringBuilder reuse for string building
- [ ] Array/List pre-sized with known capacity
- [ ] No lambda captures in hot paths (creates closure object)

### Memory Leaks
- [ ] Event `+=` has matching `-=` in OnDisable/OnDestroy
- [ ] `SceneManager.sceneLoaded +=` unsubscribed
- [ ] `Addressables.LoadAssetAsync` has corresponding `Release`
- [ ] `UnityWebRequest` wrapped in `using` or explicitly `Dispose`d
- [ ] Textures/Meshes created at runtime `Destroy`ed when done
- [ ] Static collections cleared on scene transition
- [ ] Delegates/lambdas capturing `this` not stored in long-lived contexts
- [ ] No growing unbounded caches without eviction

### GC Pressure
- [ ] Coroutine yields use cached `WaitForSeconds` instances
- [ ] String operations minimized in gameplay code
- [ ] Value types used where appropriate (no unnecessary boxing)
- [ ] `stackalloc` / `Span<T>` for temporary buffers where possible

## GPU & Rendering

### Draw Calls
- [ ] Static batching enabled for non-moving objects
- [ ] Dynamic batching or GPU instancing for moving objects
- [ ] SRP Batcher compatible materials (shader compliance)
- [ ] Sprite Atlases used for 2D (reduce draw calls)
- [ ] UI batching not broken by overlapping elements or mixed materials

### Shader Performance
- [ ] No overly complex shaders on mobile (instruction count checked)
- [ ] Shader variants stripped for target platforms
- [ ] No `discard`/`clip` in fragment shaders on mobile (breaks Early-Z)
- [ ] LOD/shader LOD used for distant objects
- [ ] Overdraw managed (particle systems, transparent objects sorted)

### Textures & Assets
- [ ] Texture compression appropriate for platform (ASTC for mobile, BC for desktop)
- [ ] Texture max sizes appropriate (not 4096x4096 for UI icons)
- [ ] Mipmaps enabled for 3D textures, disabled for UI/2D
- [ ] Read/Write disabled on meshes and textures unless needed
- [ ] Audio compression appropriate (Vorbis streaming for music, ADPCM for SFX)
- [ ] Mesh compression enabled where quality allows

## Physics

- [ ] Fixed timestep appropriate for game type (default 0.02 = 50Hz)
- [ ] Collision matrix configured (not everything-collides-with-everything)
- [ ] Trigger volumes on separate layer from physics colliders

## Advanced Optimization

For advanced rendering, shader optimization, memory profiling, and concurrency patterns, see PERFORMANCE_CHECKLIST-advanced.md.

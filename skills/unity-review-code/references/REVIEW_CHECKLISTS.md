# Review Checklists

Checklists for pre-commit code review. Apply by file type. Every finding needs evidence.

## General Checklists (All Files)

### 🔒 Security
- [ ] No hardcoded secrets, API keys, tokens, passwords
- [ ] User input validated and sanitized before use
- [ ] No SQL/command/path injection vectors
- [ ] Auth checks present on protected operations
- [ ] Sensitive data not logged or exposed in error messages
- [ ] Deserialization uses safe patterns (no `BinaryFormatter`)

### ✅ Correctness
- [ ] Logic matches stated intent (task description / ticket)
- [ ] State transitions are valid — no impossible states
- [ ] Data integrity maintained (no partial writes, no orphaned refs)
- [ ] API contracts honored (parameters, return types, nullability)
- [ ] Error paths handled — no swallowed exceptions, no silent failures
- [ ] Concurrency safe — no race conditions in async/threaded code

### 🧪 Testing
- [ ] New public API has corresponding tests
- [ ] Modified logic has updated tests
- [ ] Edge cases covered (null, empty, boundary values, overflow)
- [ ] No test code in production paths
- [ ] Tests are deterministic — no flaky timing or order dependencies

### 🧹 Code Quality
- [ ] Single Responsibility — each method/class does one thing
- [ ] Methods < 30 lines, nesting < 4 levels
- [ ] No copy-paste duplication across files
- [ ] Magic numbers extracted to named constants
- [ ] Naming is clear and consistent with codebase conventions
- [ ] Dead code removed (unused variables, unreachable branches)

### ⚡ Performance
- [ ] No allocations in hot paths (Update, FixedUpdate, tight loops)
- [ ] No N+1 query patterns or repeated expensive operations
- [ ] Memory lifecycle clear — no leaks from event subscriptions or references
- [ ] Appropriate data structures (Dictionary vs List for lookups, etc.)
- [ ] Async operations don't block the main thread

### 📚 Documentation
- [ ] Public API has XML doc comments
- [ ] Complex logic has inline comments explaining "why"
- [ ] Breaking changes noted
- [ ] Removed/deprecated API has migration guidance

---

## C# Logic & Performance (.cs files)

### 🔴 Critical — Unity Performance

| Pattern | Why | Fix |
|:--------|:----|:----|
| `GetComponent` in Update/FixedUpdate | O(n) per frame | Cache in Awake |
| `Camera.main` in loop | FindWithTag each access | Cache in Awake |
| `Find()`/`FindObjectOfType()` runtime | O(n) traversal | `[SerializeField]` inject |
| `Instantiate`/`Destroy` spam | GC spikes | Object pool |
| String concat / LINQ / `new List` in Update | Per-frame alloc | Pre-allocate, `NonAlloc` |
| `foreach` on non-cached collection in Update | Iterator alloc (older Mono) | Cache or use `for` loop |

### 🔴 Critical — Async & Lifecycle

| Pattern | Why | Fix |
|:--------|:----|:----|
| `this`/`gameObject` after `await` no null check | MissingRef | `if (this == null) return;` |
| `StartCoroutine` without stop in OnDisable | Runs after destroy | Store handle, stop in OnDisable |
| `+=` without `-=` in OnDisable | Event leak | OnEnable/OnDisable pair |
| `async void` on non-Unity-event | Swallowed exceptions | `async Task` / `async UniTask` |
| Missing `CancellationToken` on long-running async | Can't cancel on destroy | Pass `destroyCancellationToken` (Unity 6) or manual CTS |
| `await` without `try/catch` in fire-and-forget | Unobserved exception crash | Wrap or use UniTask `.Forget()` with error handler |
| Coroutine yields `new WaitForSeconds` each frame | GC per yield | Cache `WaitForSeconds` instance |

**Lifecycle order:** Awake(self) → OnEnable(subscribe) → Start(cross-component) → OnDisable(unsubscribe) → OnDestroy(cleanup)

### 🔴 Critical — General

Breaking API change, NullRef without guard, memory leak (undisposed resources/events), data corruption (serialization change without migration), race conditions, hardcoded secrets.

### 🟡 Major — Logic Patterns

| Pattern | Fix |
|:--------|:----|
| Field renamed without `[FormerlySerializedAs]` | Add attribute |
| DOTween not killed in OnDisable | `_tween?.Kill()` |
| Cross-component access in Awake | Move to Start |
| SO mutated runtime without clone | `Instantiate(configSO)` |
| Physics calls in Update | Move to FixedUpdate |
| `private` → `public` on SerializeField | Keep private, add property |
| Nullable type without null-check before use | Add guard clause or `?.` operator |
| `switch` on enum without `default` case | Add `default` with warning log |
| Mutable static field on MonoBehaviour | Race condition across scenes — use SO or singleton pattern |
| Public field where property needed | Encapsulate: `[field: SerializeField] public int Hp { get; private set; }` |

### 🟡 Major — State & Data

| Pattern | Fix |
|:--------|:----|
| Bool flags for state management (3+ bools) | Extract state machine / enum |
| Collection modified during enumeration | Copy or use removal list |
| Dictionary lookup without `TryGetValue` | Replace `ContainsKey` + index with `TryGetValue` |
| `List.Find()` / `FirstOrDefault()` in hot path | Use Dictionary or HashSet for O(1) lookup |
| Enum changed without updating all `switch` statements | Grep all switch/if-chains for that enum |
| `[Serializable]` class with no default constructor | Deserialization will fail silently |

### 🔵 Minor

Magic numbers, Debug.Log without `#if UNITY_EDITOR`, empty Update/Start, dead code, naming violations, nesting 4+, missing XML docs on public API, `#region` blocks (remove — use partial classes or extract), unnecessary `this.` qualifier.

### Investigation — MUST DO before flagging

```bash
grep -rn "MethodName\s*(" Assets/Scripts/ --include="*.cs"  # callers
grep -rn "EventName\s*[+-]=" Assets/Scripts/ --include="*.cs"  # subscribers
grep -rn "TypeName" Assets/ --include="*.prefab" --include="*.asset"  # serialization refs
grep -rn "EnumType" Assets/Scripts/ --include="*.cs" | grep -E "switch|case"  # enum usage
```

Every 🔴 needs caller count + affected files. Every 🟡 needs trigger conditions.

---

## Prefab & Scene Patterns (.prefab, .unity files)

### 🔴 Critical

| YAML Pattern | Issue | Fix |
|:-------------|:------|:----|
| `m_Script: {fileID: 0}` | Missing script ref → MissingReferenceException | Restore GUID or remove component |
| `m_Script` GUID changed vs previous | All instances lose component silently | Check .meta regeneration |
| Same MonoBehaviour type twice on one GO | Duplicate callbacks, state conflict | Remove duplicate |
| `m_CorrespondingSourceObject: {fileID: 0}` | Broken variant link | Re-link or convert to standalone |
| Component block with all fields zeroed | Silent data loss (bad merge) | Revert from git |
| `m_RaycastTarget: 1` on Image/Text without Button/Toggle | Blocks touch on elements behind | `m_RaycastTarget: 0` |
| Canvas without GraphicRaycaster | No UI input works | Add GraphicRaycaster |
| Scene with Canvas but no EventSystem | All UI non-functional | Add EventSystem |
| `[SerializeField]` renamed without `[FormerlySerializedAs]` | Prefab data silently lost | Add attribute |
| Field type changed on serialized field | Deserialization zeroes data | Migration code |

### 🟡 Major

| Pattern | Fix |
|:--------|:----|
| `m_Modifications` with 20+ entries (override sprawl) | Apply intentional to base, revert accidental |
| 5+ levels empty parent transforms | Flatten hierarchy |
| Button `m_OnClick` with 0 persistent calls | Wire handler or remove |
| `m_Target: {fileID: 0}` in persistent call | Fix target ref |
| Canvas sort order collision | Unique sort orders |
| `m_PlayOnAwake: 1` unintentional | `m_PlayOnAwake: 0` |
| `m_Controller: {fileID: 0}` | Assign or remove Animator |

### 🔵 Minor

Default naming (`GameObject (1)`), empty GameObjects, hardcoded text (localization), added component on variant (confirm variant-specific).

### Grep — Run on changed prefabs

```bash
for f in $(git diff --name-only | grep -E '\.(prefab|unity)$'); do
  grep -n "m_Script: {fileID: 0}" "$f"                    # missing scripts
  grep -n "m_CorrespondingSourceObject: {fileID: 0}" "$f"  # broken variant
  grep -n "m_RaycastTarget: 1" "$f"                        # raycast audit
  grep -n "m_PlayOnAwake: 1" "$f"                          # audio auto-play
  grep -n "m_Controller: {fileID: 0}" "$f"                 # empty animator
done
```

---

## Asset Patterns (.mat, .shader, .meta, .controller, .anim, .fbx, .asset)

### 🔴 Critical — Materials & Shaders

| Pattern | Issue | Fix |
|:--------|:------|:----|
| `m_Shader: {fileID: 0}` | Pink/magenta at runtime | Assign correct shader |
| `{fileID: 10303}` in m_Materials | Default Unity material | Assign project material |
| Custom shader not in Always Included & no scene ref | Pink in builds only | Add to Always Included or ensure ref chain |

### 🔴 Critical — Textures (.meta)

| Meta Pattern | Issue | Fix |
|:-------------|:------|:----|
| `isReadable: 1` | Doubles memory | Disable unless GetPixels needed |
| `textureCompression: 0` / RGBA32 mobile | 4x+ memory | ASTC (iOS), ETC2 (Android) |
| NPOT dimensions | Can't compress | Resize to POT |

### 🟡 Major — Textures

| Meta Pattern | Issue | Fix |
|:-------------|:------|:----|
| `enableMipMap: 1` on UI sprite | +33% memory | Disable |
| 4096 for small asset | Wastes VRAM | Match maxTextureSize to display size |
| `sRGBTexture: 0` on color texture | Washed out colors | Enable sRGB for diffuse/albedo |
| `sRGBTexture: 1` on normal/mask map | Incorrect lighting | Disable sRGB for non-color data |
| No platform override for mobile | Desktop settings shipped to mobile | Add Android/iOS override with ASTC |

### 🟡 Major — Animation

Empty `m_Controller` → assign or remove. `CullingMode: 0` → CullCompletely. `WriteDefaultValues: 1` → disable. Unintended `ApplyRootMotion` → disable. Animator on GO that never animates → remove.

### 🟡 Major — Audio

Unintended `PlayOnAwake` → disable. `SpatialBlend: 1` on UI → set 2D. Large clip uncompressed → Streaming+Vorbis. `forceToMono: 0` on 3D SFX → enable.

### 🟡 Major — Models (.fbx/.meta)

| Pattern | Issue | Fix |
|:--------|:------|:----|
| `meshCompression: 0` on static mesh | Larger build size | Set to Medium or High |
| `isReadable: 1` on mesh | Doubles memory | Disable unless runtime mesh access needed |
| `importAnimation: 1` on non-animated model | Phantom clips, build bloat | Disable Import Animation |
| `materialImportMode: 1` from DCC | Creates unmanaged materials | Set to None, assign manually |

### Grep

```bash
# Materials — missing shader / default material
grep -n "m_Shader: {fileID: 0}\|{fileID: 10303}" <changed .mat/.asset files>
# Textures — memory issues
grep -n "isReadable: 1\|enableMipMap: 1\|textureCompression: 0" <changed .meta files>
# Animation/Audio in prefabs
grep -n "m_Controller: {fileID: 0}\|m_CullingMode: 0\|m_PlayOnAwake: 1" <changed .prefab/.unity files>
```

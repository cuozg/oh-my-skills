# Logic Review Patterns — Unity C# (Part 3b)

UI-Specific, Networking, and Unity Gotchas continued from logic-review-patterns-advanced.md.

---

## 9. UI-Specific

### 9.1 Major

| Pattern | Fix |
|:--------|:----|
| Canvas dirtied/rebuilt every frame (SetDirty/text/layout toggles) | Batch updates and avoid per-frame UI mutations |
| Deeply nested LayoutGroups causing cascade recalculation | Flatten hierarchy, minimize nested layout groups |
| Frequent UI enable/disable toggles for visibility | Use `CanvasGroup` alpha/interactable/blockRaycasts where possible |
| ScrollRect with large dataset and no virtualization | Implement item pooling/virtualized list |
| Text/TMP content updated each frame without need | Update only on value change, throttle refresh |
| Decorative Images keep `raycastTarget=true` | Disable raycast target on non-interactive graphics |
| Multiple `GraphicRaycaster` components on nested canvases | Keep only required raycasters to reduce UI input overhead |

---

## 10. Networking

Apply when networking/web request code is modified.

### 10.1 Major

| Pattern | Fix |
|:--------|:----|
| `UnityWebRequest` without timeout | Set `timeout` or equivalent cancellation policy |
| JSON parse without error handling | Wrap parse in `try/catch` with fallback/error path |
| Network calls without retry/backoff strategy | Add bounded retry with jitter/backoff |
| Missing `Content-Type`/accept headers for payload APIs | Set explicit headers matching backend contract |
| Deprecated `isNetworkError`/`isHttpError` checks only | Use `UnityWebRequest.result` + status code handling |
| Large payloads sent uncompressed | Enable/request compression and chunk strategy where supported |

---

## 11. Unity-Specific Gotchas

### 11.1 Critical

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| `Application.isPlaying` used incorrectly in editor code paths | False in edit-time operations; guards can misfire | In `#if UNITY_EDITOR` flows, verify edit-mode + play-mode checks are explicit and correct. |
| Missing `EditorApplication.isPlayingOrWillChangePlaymode` check before asset mutation | Asset changes can happen during playmode transition | Guard editor-time writes when entering/exiting play mode. |
| `[InitializeOnLoadMethod]` depends on runtime-only APIs | Editor init crashes or build/runtime coupling issues | Ensure method only references editor-safe APIs and no runtime scene assumptions. |
| `AssetDatabase` called from runtime assembly path | Build/runtime failures outside editor | Require `#if UNITY_EDITOR` guards and assembly split when needed. |
| `PrefabUtility` usage during play mode | Unexpected prefab edits/state drift | Verify calls are editor-tooling only and gated from play mode operations. |

### 11.2 Major

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| `[Conditional("UNITY_EDITOR")]` on method with return expectation | Call site still compiles but return behavior is misleading | Avoid conditional attribute on value-returning API used by runtime logic. |
| `Debug.Assert` condition has side effects | Assert removed in build, side effects still alter logic flow | Ensure assert expressions are pure and side-effect free. |
| Multiple `[RuntimeInitializeOnLoadMethod]` relying on order | Initialization race between systems | Add explicit bootstrap ordering strategy instead of implicit attribute order. |
| Platform code uses only `#if UNITY_ANDROID` fallback | Other platforms unintentionally excluded/misconfigured | Use full `#if/#elif/#else` chain for all supported targets. |
| `Screen.orientation` set without autorotate flags | Orientation lock behaves inconsistently per device | Verify `Screen.autorotateTo...` flags align with orientation policy. |
| Optional feature used without `SystemInfo.supportsXxx` gate | Runtime failures on unsupported hardware | Guard usage and provide fallback path. |
| `QualitySettings` accessed by index | Reordered quality levels break behavior | Resolve by quality name mapping or config abstraction, not hard-coded index. |

---

**See also:** `logic-review-patterns-advanced.md` (Sections 7-8) for Data Flow and Concurrency & Async patterns.

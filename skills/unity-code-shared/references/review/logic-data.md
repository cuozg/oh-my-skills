# Logic Review — Data Flow, Concurrency & Edge Cases

Advanced patterns: Data Flow, Concurrency & Async, Edge Case Checklist.

---

## 7. Data Flow

### 7.1 Critical

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| User input flows to file path without sanitization | Path traversal | Trace from UI/network input to `File.Open`/`Resources.Load` |
| Deserialized data used without validation | Corrupted/tampered save breaks game | After `JsonUtility.FromJson`, validate ranges, null refs, enum bounds |
| Collection index from external source without bounds check | `IndexOutOfRangeException` | What if server sends index 999? What if config has wrong array size? |
| Float comparison with `==` | Floating point imprecision | Use `Mathf.Approximately` or epsilon comparison |
| Integer overflow in calculation | Wrap-around produces negative/wrong value | Check max realistic values: `count * size * price` — can it overflow int? |
| `Mathf.InverseLerp(a, b, value)` where `a == b` | Degenerate range can produce `NaN` | Guard equal endpoints before call |
| `Vector3.Normalize()` on zero vector | Returns zero vector, not unit direction | Verify downstream code handles zero magnitude |
| `Texture2D.GetPixels` on compressed texture | Full decompression allocates large RAM spike | Validate texture format/readability |
| `AnimationCurve.Evaluate` outside key range | Unexpected extrapolation | Check `preWrapMode`/`postWrapMode` and clamp input time |
| `NavMesh.SamplePosition` with tiny `maxDistance` | Frequent silent miss | Verify radius matches gameplay scale and check return bool |

### 7.2 Major

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| String used as identifier (magic string) | Typo = silent failure | Extract to `const` or use `nameof()` |
| Enum serialized as int | Adding enum values shifts indices | Use string name or explicit `= 1, = 2` |
| DateTime without timezone handling | 12h offset bugs | `DateTime.UtcNow` for storage |
| Division without zero-check | `DivideByZeroException` or `NaN` | Can divisor ever be 0? |
| Implicit conversion loses precision | `double` → `float`, `long` → `int` | Does precision loss matter? |
| `Mathf.Clamp` called with `min > max` | Returns wrong bound silently | Validate ordering at source |
| LayerMask treated as plain int math | Wrong layers | Use `1 << layer` and `LayerMask.GetMask` |

---

## 8. Concurrency & Async

### 8.1 Critical

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| Shared mutable state across async operations | Race condition | Two async methods write same field |
| `async void` event handler that throws | Unobserved exception crashes | Wrap body in try/catch |
| `Task.Run` accessing Unity API | Main thread only | Transform, GameObject, UI, Physics |
| `CancellationToken` not checked in loop body | Can't cancel | Add `ThrowIfCancellationRequested` |
| Multiple awaits modifying same state | Interleaved execution | Between awaits, another caller modifies field |
| `UniTask.WhenAll` without per-task error capture | One failure hides siblings | Handle individual results |
| Addressables load without release tracking | Handle leak | Track owner + release path |
| `UnityWebRequest` not disposed | Socket leak | Use `using`/`Dispose()` on every path |

### 8.2 Major

| Pattern | Why | What to check |
|:--------|:----|:--------------|
| Fire-and-forget without error handling | Silent failures | Use `UniTask.Forget(e => Debug.LogException(e))` |
| Lock held across `await` | Deadlock (Monitor not async-safe) | Use `SemaphoreSlim` |
| Event fired during subscriber iteration | `InvalidOperationException` | Copy list or use `event` keyword |
| `Task.Delay` for gameplay timing | Ignores TimeScale | Use `UniTask.Delay` with timing mode |

---

## 12. Edge Case Checklist

Run against EVERY changed method:

| Question | If Yes → |
|:---------|:---------|
| Called with null? | Add guard or `[NotNull]` contract |
| Collection empty? | Check `.Any()` before `.First()`/`[0]` |
| Called twice? | Idempotent? Double-subscribe? |
| Called before Init? | Add init guard or lazy init |
| Called after Destroy? | Check `this != null` / `isActiveAndEnabled` |
| Value negative? | Add `Mathf.Max(0, ...)` |
| Value MAX_INT? | Check overflow in arithmetic |
| Two run concurrently? | Check shared state, add sync |
| Network/file fails? | Error handling path exists? |
| Referenced object destroyed? | Check null/MissingReferenceException |

---

## 13. Minor Issues

Magic numbers, Debug.Log without `#if UNITY_EDITOR`, empty Update/Start, dead code, naming violations, nesting 4+, missing XML docs on public API.

## Suggestion Quality

**DO**: Exact replacement code in ` ```suggestion ``` `. One issue per comment. Show evidence. Explain *why*.
**DON'T**: Combine multiple fixes. Style-only as Critical. Flag without evidence. Rewrites > 20 lines inline.

## Investigation Commands

```bash
grep -rn "TypeName" Assets/ --include="*.prefab" --include="*.asset"
grep -rn "_fieldName\s*=" Assets/Scripts/ --include="*.cs"
grep -rn "catch\s*(Exception" Assets/Scripts/ --include="*.cs"
```

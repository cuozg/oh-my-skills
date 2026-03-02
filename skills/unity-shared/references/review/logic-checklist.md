# Logic Correctness Checklist

## Boundary & Off-by-One

- [ ] Loop bounds use `<` for `Length`/`Count`, not `<=`
- [ ] Array/list index starts at 0, ends at `count - 1`
- [ ] `Substring`, `Range`, `Span` slicing endpoints correct
- [ ] Mathf.Clamp min < max, not swapped
- [ ] Integer division truncation handled (`5 / 2 == 2`, not `2.5`)
- [ ] Float comparison uses `Mathf.Approximately`, not `==`

## Null & Missing References

- [ ] `GetComponent<T>()` result null-checked before use
- [ ] Event subscribers null-checked: `OnEvent?.Invoke()`
- [ ] `TryGetComponent` preferred over `GetComponent` + null check
- [ ] Destroyed UnityEngine.Object checked with `== null` (not `is null`)
- [ ] Optional SO fields validated in `OnEnable` or `Awake`

## Edge Cases

- [ ] Empty collections handled (`list.Count == 0` before `list[0]`)
- [ ] Zero/negative input guarded (division, array size, timer duration)
- [ ] `int.MaxValue` / `float.MaxValue` overflow scenarios considered
- [ ] Enum switch has `default` case or exhaustive match
- [ ] String empty/null: use `string.IsNullOrEmpty`

## State Management

- [ ] Initialization order documented if cross-component
- [ ] State reset on `OnEnable`/`OnDisable` for pooled objects
- [ ] `OnDestroy` cleans up subscriptions, native resources
- [ ] Boolean flags reset after use (one-shot triggers)
- [ ] Coroutine references stored for `StopCoroutine` cleanup

## Data Flow

- [ ] Input validated at system boundary (public methods, events)
- [ ] Output contracts documented (return null vs empty vs throw)
- [ ] Defensive copies for mutable data passed across systems
- [ ] `ref`/`out` parameters justified (prefer return values)
- [ ] Collection modification during iteration guarded (use `ToList()` or reverse loop)

## Common Unity Logic Bugs

```csharp
// BAD: Equality on destroyed object
if (target is null) // Won't catch destroyed Unity objects

// GOOD:
if (target == null) // Uses Unity's overloaded == operator

// BAD: Modifying collection during foreach
foreach (var enemy in enemies) enemies.Remove(enemy);

// GOOD:
for (int i = enemies.Count - 1; i >= 0; i--)
    if (ShouldRemove(enemies[i])) enemies.RemoveAt(i);
```

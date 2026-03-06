# Unity Lifecycle Risks

## Execution Order

| Phase | Risk | Mitigation |
|-------|------|------------|
| `Awake` | Runs before `Start` of other objects — cross-references may be null | Cache own components only |
| `OnEnable` | Fires before `Start` on first enable | Don't assume `Start` has run |
| `Start` | Order across objects undefined | Use `[DefaultExecutionOrder]` or Script Execution Order |
| `OnDisable` | Fires when object/component disabled OR destroyed | Check `gameObject.scene.isLoaded` |
| `OnDestroy` | Scene may be unloading — other objects already destroyed | Guard external references |

## Dangerous Patterns

- [ ] `FindObjectOfType<T>()` in `Awake` — target may not exist yet
- [ ] `GetComponent<T>()` on another GameObject in `Awake` — order not guaranteed
- [ ] Subscribing in `Awake`, unsubscribing in `OnDestroy` — asymmetric lifecycle
- [ ] `DontDestroyOnLoad` without duplicate check

```csharp
// BAD: Duplicate DontDestroyOnLoad singletons
void Awake() { DontDestroyOnLoad(gameObject); }

// GOOD: Destroy duplicate
void Awake()
{
    if (Instance != null) { Destroy(gameObject); return; }
    Instance = this;
    DontDestroyOnLoad(gameObject);
}
```

## Scene Load/Unload

- [ ] Static references cleared on scene unload (subscribe to `SceneManager.sceneUnloaded`)
- [ ] Coroutines stop when GameObject disabled — restart in `OnEnable` if needed
- [ ] `SceneManager.LoadSceneAsync` callback may fire next frame — don't assume immediate
- [ ] Additive scene objects persist until explicitly unloaded

## Destroy Timing

- [ ] `Destroy()` deferred to end of frame — object still accessible this frame
- [ ] `DestroyImmediate()` only in Editor scripts, never runtime
- [ ] Accessing `.gameObject` or `.transform` after `Destroy` call is valid until frame end
- [ ] Coroutines on destroyed objects throw `MissingReferenceException`

```csharp
// BAD: Null check after Destroy in same frame
Destroy(enemy);
if (enemy != null) enemy.TakeDamage(10); // Still passes this frame!

// GOOD: Guard with flag or defer
enemy.MarkForDeath();
// Process removal next frame
```

## Coroutine Lifecycle

- [ ] `StopCoroutine` requires stored `Coroutine` reference (not method name)
- [ ] Coroutines stop on `SetActive(false)` — won't auto-resume on re-enable
- [ ] `WaitForSeconds` uses scaled time — use `WaitForSecondsRealtime` for UI
- [ ] `yield return null` vs `yield return new WaitForEndOfFrame()` — different timing

## Subscribe/Unsubscribe Symmetry

| Subscribe In | Unsubscribe In | Notes |
|-------------|---------------|-------|
| `OnEnable` | `OnDisable` | Preferred — symmetric pair |
| `Awake` | `OnDestroy` | Only for permanent listeners |
| `Start` | `OnDestroy` | Asymmetric — avoid |

## Cleanup Pair Scan

After initial review, explicitly scan every changed file for cleanup pairs. Lifecycle gaps are the most commonly missed Unity bugs — invisible in diff hunks; you need the full file to see that a `+=` has no matching `-=`.

- [ ] For every `+=` on event/delegate, verify matching `-=` in `OnDestroy`/`OnDisable`
- [ ] If class declares `public event` and can be destroyed at runtime, verify events nulled in `OnDestroy`
- [ ] For every `StartCoroutine()`, verify stopped via `StopCoroutine()`/`StopAllCoroutines()` in `OnDisable`/`OnDestroy`
- [ ] For every `InvokeRepeating()`, verify `CancelInvoke()` on lifecycle exit

### Severity Floors

| Pattern | Min Severity |
|---------|-------------|
| `+=` without matching `-=` in OnDestroy/OnDisable | HIGH |
| `public event` field, no null in OnDestroy | HIGH |
| `StartCoroutine()` not stopped on lifecycle exit | HIGH |
| `InvokeRepeating()` without `CancelInvoke()` | HIGH |

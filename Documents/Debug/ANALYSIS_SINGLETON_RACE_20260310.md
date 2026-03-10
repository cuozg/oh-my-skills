# Bug Analysis: AudioManager NullReferenceException on Singleton Access

**Date**: 2026-03-10  
**Reporter**: user  
**Status**: OPEN  

---

## Summary

`AudioManager.Awake()` throws a `NullReferenceException` ~30% of the time at `GameManager.Instance.MasterVolume` (AudioManager.cs:14). The root cause is a classic Awake-order race condition: both `GameManager` and `AudioManager` initialize in `Awake()`, but Unity does not guarantee execution order between MonoBehaviours. When `AudioManager.Awake()` runs first, `GameManager._instance` has not yet been assigned. The `Instance` getter's fallback (`FindObjectOfType`) may also fail if `GameManager.Awake()` hasn't run yet on a freshly instantiated or DontDestroyOnLoad-pending object. No `[DefaultExecutionOrder]` is set on any class. A secondary concern is that `ScoreUI.Update()` accesses `GameManager.Instance.Score` every frame without a null guard, which would NRE if GameManager is ever destroyed during scene transitions.

## Reproduction Steps

1. Load a scene containing both `GameManager` and `AudioManager` GameObjects
2. Enter Play Mode repeatedly (10+ times)
3. ~30% of the time, NullReferenceException occurs at `AudioManager.cs:14`: `_audioSource.volume = GameManager.Instance.MasterVolume;`
4. Expected: `GameManager.Instance` is always available in any `Awake()` call. Actual: it is null when AudioManager's Awake executes before GameManager's Awake.

---

## Root Cause Candidates

### [HIGH] Candidate 1 — Awake execution order race between GameManager and AudioManager

**Evidence**: `AudioManager.cs:14` — accesses `GameManager.Instance.MasterVolume` inside `Awake()`. `GameManager.cs:32` — assigns `_instance = this` inside its own `Awake()`. Unity does not guarantee Awake order between MonoBehaviours on different GameObjects. No `[DefaultExecutionOrder]` attribute exists on either class.  
**Angle**: lifecycle  

> `AudioManager.cs:14`: `_audioSource.volume = GameManager.Instance.MasterVolume;`  
> `GameManager.cs:32`: `_instance = this;`  

When AudioManager.Awake() fires first, `_instance` is still null. The getter's fallback at `GameManager.cs:11` calls `FindObjectOfType<GameManager>()`, which can find the object — but the found instance has not yet run its own Awake(), so while the reference is non-null, this is a fragile path that depends on Unity's internal object registration timing. The intermittent 30% failure rate matches the non-deterministic Awake ordering.

---

### [HIGH] Candidate 2 — FindObjectOfType fallback is unreliable as a singleton guarantee

**Evidence**: `GameManager.cs:10-12` — the `Instance` getter uses `FindObjectOfType<GameManager>()` as a lazy fallback when `_instance == null`. This has two problems: (a) `FindObjectOfType` is not guaranteed to find objects whose `Awake()` hasn't run yet in all Unity versions, (b) even when it does find the object, the returned GameManager has not run `Initialize()` yet, so `_masterVolume` is the field default (`1f`) rather than the PlayerPrefs value.  
**Angle**: data-flow  

> `GameManager.cs:10-11`: `if (_instance == null) _instance = FindObjectOfType<GameManager>();`  
> `GameManager.cs:40`: `_masterVolume = PlayerPrefs.GetFloat("MasterVolume", 1f);`  

Even when FindObjectOfType succeeds and no NRE occurs, the MasterVolume returned is the field initializer value (`1f`) not the persisted PlayerPrefs value — a silent data correctness bug.

---

### [MED] Candidate 3 — ScoreUI.Update() has unguarded Instance access every frame

**Evidence**: `ScoreUI.cs:16` — `_scoreText.text = $"Score: {GameManager.Instance.Score}";` runs in `Update()` with no null check. If GameManager is destroyed during a scene transition (it uses DontDestroyOnLoad but other scenarios exist), this will throw a NullReferenceException every frame.  
**Angle**: edge-case  

> `ScoreUI.cs:16`: `_scoreText.text = $"Score: {GameManager.Instance.Score}";`  

---

### [LOW] Candidate 4 — DontDestroyOnLoad duplicate destruction path

**Evidence**: `GameManager.cs:27-30` — when a duplicate GameManager exists (e.g., scene reload), the duplicate calls `Destroy(gameObject)` and returns early. If AudioManager in the new scene references the about-to-be-destroyed duplicate via FindObjectOfType before the original DontDestroyOnLoad instance is found, the reference becomes invalid.  
**Angle**: lifecycle  

> `GameManager.cs:27-29`: `if (_instance != null && _instance != this) { Destroy(gameObject); return; }`  

---

## Solutions

### For Candidate 1 — Fix Awake ordering

- **WHAT**: Add `[DefaultExecutionOrder(-100)]` to `GameManager` so its Awake() always runs before other MonoBehaviours. Move AudioManager's `GameManager.Instance` access from `Awake()` to `Start()`, which is guaranteed to run after all Awake() calls.  
- **WHERE**: `GameManager.cs:3` — add attribute above class declaration. `AudioManager.cs:11` — rename `Awake` to `Start` or split: keep `GetComponent` in Awake, move Instance access to Start.  
- **Risk**: LOW  

### For Candidate 1 — Alternative: Eager singleton pattern

- **WHAT**: Replace the lazy `FindObjectOfType` getter with a simple null-check-only getter. Ensure `_instance` is assigned in `Awake()` only (which already happens at line 32). Remove the FindObjectOfType fallback to make failures explicit rather than intermittent.  
- **WHERE**: `GameManager.cs:10-11` — remove `FindObjectOfType` from getter, keep only `return _instance;`  
- **Risk**: LOW  

### For Candidate 2 — Ensure Initialize() runs before external access

- **WHAT**: Move `Initialize()` call to execute before `_instance` is externally accessible — either by calling it inside the Instance getter on first access, or by guaranteeing Awake order via `[DefaultExecutionOrder]`.  
- **WHERE**: `GameManager.cs:34` — already calls Initialize() in Awake. The fix is ensuring Awake runs first (see Candidate 1 solution).  
- **Risk**: LOW  

### For Candidate 3 — Add null guard in ScoreUI.Update

- **WHAT**: Add a null check before accessing `GameManager.Instance` in `Update()` to prevent per-frame NRE during scene transitions.  
- **WHERE**: `ScoreUI.cs:16` — wrap in `if (GameManager.Instance != null)` guard.  
- **Risk**: LOW  

---

## Recommended Next Step

Apply the Candidate 1 fix first: add `[DefaultExecutionOrder(-100)]` to `GameManager` and move AudioManager's `GameManager.Instance` access from `Awake()` to `Start()` — this eliminates the race condition entirely with minimal code change and zero risk of regression.

# Diagnosis Workflow

## 1. Parse Symptom

Extract from report:
- **Error message** — exact text, exception type
- **Timing** — when it occurs (startup, runtime, on action)
- **Frequency** — always, intermittent, first-time-only
- **Scope** — editor-only, build-only, both

## 2. Categorize

| Category | Signals |
|----------|---------|
| Compile | red console, `CS####` codes, IDE red squiggles |
| Runtime | exception at play, null ref, missing ref |
| Logic | wrong behavior, no error, "it just doesn't work" |
| Performance | frame drops, GC spikes, hitch on action |
| ECS / Jobs / Burst | entity not processed, Burst compile error, NativeContainer safety error, race-like behavior |

## 3. Investigation Angles (pick ≥3)

| Angle | What to Check |
|-------|---------------|
| Call stack | stack trace → find originating call |
| State | inspect fields at breakpoint or with Debug.Log |
| Input | what triggered it — user action, event, lifecycle |
| Reproduction | minimal repro steps, isolate variables |
| Timing | execution order, race conditions, async gaps |
| Data | serialized values, SO references, prefab overrides |
| Environment | editor vs build, platform, Unity version |
| ECS/Burst | world, query shape, system update group, job dependency, ECB playback timing, Burst compatibility |

## 4. Multi-Angle Rule

Investigate **≥3 angles** before proposing a fix. Single-angle diagnosis misses root cause ~40% of the time.

## 5. Solution Format

```
WHAT: [one-line description of the fix]
WHERE: [file:line or component path]
WHY: [root cause explanation]
```

## 6. Propose 2+ Solutions

| # | Solution | Risk | Trade-off |
|---|----------|------|-----------|
| 1 | Safest / minimal change | Low | May not address deeper issue |
| 2 | Proper fix / refactor | Medium | More code touched |
| 3 | Architectural change | High | Best long-term, most effort |

Rank by risk ascending. Present safest first.

```csharp
// Example: NullRef on GetComponent
// Angle 1 (Call stack): PlayerController.Update() line 42
// Angle 2 (State): _rb is null after scene reload
// Angle 3 (Timing): Awake() not re-called on LoadScene

// Solution 1 (Low risk): Null check + lazy init
if (_rb == null) _rb = GetComponent<Rigidbody>();

// Solution 2 (Medium risk): Re-acquire in OnEnable
void OnEnable() => _rb = GetComponent<Rigidbody>();
```

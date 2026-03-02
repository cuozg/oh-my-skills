# Review Comment Format

## Syntax

```
// ── REVIEW {icon} {LABEL} #{category}
// What: 1-line summary
// Why:  1-3 lines — impact + evidence
```

## Severity Levels

| Icon | Label    | Tag          | Meaning                          | Action Required       |
|------|----------|--------------|----------------------------------|-----------------------|
| 🔴   | CRITICAL | `#critical`  | Crash, data loss, security hole  | Must fix before merge |
| 🟠   | HIGH     | `#high`      | Bug, incorrect behavior          | Must fix before merge |
| 🟡   | MEDIUM   | `#medium`    | Performance, maintainability     | Should fix            |
| 🔵   | LOW      | `#low`       | Minor improvement, readability   | Consider fixing       |
| ⚪   | STYLE    | `#style`     | Naming, formatting, convention   | Optional              |

## Categories

`null-safety` `lifecycle` `state` `concurrency` `allocation` `serialization` `event-leak` `logic`

## Examples

```csharp
// ── REVIEW 🔴 CRITICAL #null-safety
// What: GetComponent result used without null check
// Why:  Returns null if component missing → NullReferenceException at runtime.

// ── REVIEW 🟠 HIGH #event-leak
// What: Event subscribed in OnEnable but never unsubscribed
// Why:  Listener persists after disable → stale callbacks, potential crash.

// ── REVIEW 🟡 MEDIUM #allocation
// What: GetComponent called every Update — cache in Awake
// Why:  Native interop call per frame. Cache once in Awake/Start.

// ── REVIEW 🔵 LOW #logic
// What: Magic number 0.5f — extract to const
// Why:  Unclear intent. A named const improves readability.

// ── REVIEW ⚪ STYLE #naming
// What: Field _health should be _currentHealth for clarity
// Why:  Ambiguous alongside _maxHealth — prefix clarifies.
```

## Fix Suggestion Format

```csharp
// ── REVIEW 🟠 HIGH #allocation
// What: Camera.main called in Update — allocates every frame
// Why:  FindGameObjectWithTag under the hood → GC pressure in hot path.
private Camera _cam;
void Awake() => _cam = Camera.main;  // ← applied fix
```

## Fix Application

Apply the fix directly below the comment when safe:

```csharp
// ── REVIEW 🟠 HIGH #null-safety
// What: GetComponent result used without null check
// Why:  Returns null if component missing → NullReferenceException at runtime.
//       Called from Start() with no prior AddComponent guarantee.
var rb = GetComponent<Rigidbody>();
if (rb != null) rb.isKinematic = true;  // ← applied fix
```

When fix is not possible (too risky, needs design decision, or cross-file):

```csharp
// ── REVIEW 🟡 MEDIUM #allocation
// What: String concat in Update() allocates every frame
// Why:  GC pressure in hot path — 60 allocs/sec.
//       Use StringBuilder or cache the result.
debugText.text = "HP: " + health + " / " + maxHealth;  // ← unchanged
```

## Rules

- One comment per issue — no multi-issue comments
- Place comment on the line ABOVE the problem line
- Always include icon + label + tag on the header line
- `What:` = 1 line, plain summary of the issue
- `Why:` = 1-3 lines, explain impact with evidence (variable names, call sites)
- Apply code fix inline when safe; leave code unchanged when fix needs design decision or touches other files
- Never commit review changes — leave diff for user inspection

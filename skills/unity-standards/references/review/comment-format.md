# Review Comment Format

## Syntax

```
// -- REVIEW {icon} {LABEL} #{category}
// What: 1-line summary
// Why:  1-3 lines - impact + evidence
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
// -- REVIEW 🔴 CRITICAL #null-safety
// What: GetComponent result used without null check
// Why:  Returns null if component missing -> NullReferenceException at runtime.

// -- REVIEW 🟠 HIGH #event-leak
// What: Event subscribed in OnEnable but never unsubscribed
// Why:  Listener persists after disable -> stale callbacks, potential crash.

// -- REVIEW 🟡 MEDIUM #allocation
// What: GetComponent called every Update - cache in Awake
// Why:  Native interop call per frame. Cache once in Awake or Start.

// -- REVIEW 🔵 LOW #logic
// What: Magic number 0.5f - extract to const
// Why:  Unclear intent. A named constant improves readability.

// -- REVIEW ⚪ STYLE #naming
// What: Field _health should be _currentHealth for clarity
// Why:  Ambiguous alongside _maxHealth - prefix clarifies.
```

## Fix Suggestion Format

```csharp
// -- REVIEW 🟠 HIGH #allocation
// What: Scene-wide lookup repeated in Update
// Why:  Global lookup in a hot path. Cache once or inject the dependency.
private Player _player;
void Awake() => _player = FindFirstObjectByType<Player>();
```

## Fix Application

Apply the fix directly below the comment when safe.

```csharp
// -- REVIEW 🟠 HIGH #null-safety
// What: GetComponent result used without null check
// Why:  Returns null if component missing -> NullReferenceException at runtime.
//       Called from Start() with no prior AddComponent guarantee.
var rb = GetComponent<Rigidbody>();
if (rb != null) rb.isKinematic = true;
```

When the fix is not possible in place because it needs a design decision or touches other files:

```csharp
// -- REVIEW 🟡 MEDIUM #allocation
// What: String concat in Update() allocates every frame
// Why:  GC pressure in a hot path.
//       Use StringBuilder or cache the formatted result.
debugText.text = "HP: " + health + " / " + maxHealth;
```

## Rules

- One comment per issue - do not combine unrelated findings
- Place the comment on the line above the problem line
- Always include icon, label, and tag on the header line
- `What:` is a one-line summary of the issue
- `Why:` is 1-3 lines explaining impact with evidence
- Apply code fixes inline only when they are safe and local
- Never commit review changes - leave the diff for inspection

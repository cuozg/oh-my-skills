# Review Comment Format — Local Review

> **Canonical reference**: `unity-standards/references/review/comment-format.md`
> Load via: `read_skill_file("unity-standards", "references/review/comment-format.md")`

## Severity Icons

| Icon | Label    | Tag          | Meaning                         | Action           |
|------|----------|--------------|----------------------------------|------------------|
| 🔴   | CRITICAL | `#critical`  | Crash, data loss, security hole  | Must fix         |
| 🟠   | HIGH     | `#high`      | Bug, incorrect behavior, leak    | Must fix         |
| 🟡   | MEDIUM   | `#medium`    | Perf, maintainability, hot-path  | Should fix       |
| 🔵   | LOW      | `#low`       | Minor improvement, readability   | Consider         |
| ⚪   | STYLE    | `#style`     | Naming, formatting, convention   | Optional         |

## Categories (pick one)

`null-safety` `lifecycle` `state` `concurrency` `allocation` `serialization` `event-leak` `logic`

## Comment Format

```csharp
// ── REVIEW 🔴 CRITICAL #category
// What: 1-line summary of the issue
// Why:  1-3 lines — explain impact + cite evidence from code
```

Then apply the fix directly below the comment when possible:

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

- One comment per issue — never stack unrelated issues
- Place comment on the line ABOVE the problem code
- Always include icon + label + tag on the header line
- `What:` = 1 line max, plain summary
- `Why:` = 1-3 lines, explain impact with evidence (variable names, call sites, frame counts)
- Apply the code fix inline when safe (single-line, no cross-file deps)
- Leave code unchanged when fix needs design decision or touches other files
- Never commit — leave diff for user inspection

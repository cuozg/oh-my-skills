# Review Comment Format

## Syntax

```
// ── REVIEW [SEVERITY]: message
```

## Severity Levels

| Level    | Meaning                          | Action Required       |
|----------|----------------------------------|-----------------------|
| CRITICAL | Crash, data loss, security hole  | Must fix before merge |
| HIGH     | Bug, incorrect behavior          | Must fix before merge |
| MEDIUM   | Performance, maintainability     | Should fix            |
| LOW      | Minor improvement, readability   | Consider fixing       |
| STYLE    | Naming, formatting, convention   | Optional              |

## Examples

```csharp
// ── REVIEW [CRITICAL]: Null ref — GetComponent result unchecked
// ── REVIEW [HIGH]: Event subscribed in OnEnable but never unsubscribed
// ── REVIEW [MEDIUM]: GetComponent called every Update — cache in Awake
// ── REVIEW [LOW]: Magic number 0.5f — extract to const
// ── REVIEW [STYLE]: Field _health should be _currentHealth for clarity
```

## Fix Suggestion Format

```csharp
// ── REVIEW [HIGH]: Camera.main called in Update — allocates every frame
// FIX: Cache in Awake: private Camera _cam; void Awake() => _cam = Camera.main;
```

## Rules

- One comment per issue — no multi-issue comments
- Place comment on the line ABOVE the problem line
- Include WHY it's a problem, not just WHAT
- Include FIX line when the solution is non-obvious
- CRITICAL/HIGH block merge — MEDIUM/LOW/STYLE do not

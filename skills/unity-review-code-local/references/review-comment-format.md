# Review Comment Format — Skill Extensions

> **Canonical reference**: `unity-standards/references/review/comment-format.md`
> Load via: `read_skill_file("unity-standards", "references/review/comment-format.md")`

## Severity Levels (skill-specific subset)

This skill uses 3 severities (standards defines 5):

- `CRITICAL` — data loss, crash, security, broken contract
- `WARNING`  — logic error, leak, allocation in hot path
- `NOTE`     — style, readability, minor improvement

## Categories (pick one)

`null-safety` `lifecycle` `state` `concurrency` `allocation` `serialization` `event-leak` `logic`

## Inline Comment Anatomy

```csharp
// ── REVIEW [SEVERITY] {category}: {message}
//    Evidence: {what you observed}
//    Fix:      {imperative fix description}
```

## Rules

- One comment block per distinct issue; do not stack unrelated issues at same line
- Place comment on the line of the issue, not the method signature
- Keep `Fix:` to one imperative sentence
- Never rewrite the code inline — annotation only

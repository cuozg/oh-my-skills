# Review Comment Format

## Inline Comment Anatomy

```csharp
// ── REVIEW [SEVERITY] {category}: {message}
//    Evidence: {what you observed}
//    Fix:      {imperative fix description}
```

**Severity levels** (required):
- `CRITICAL` — data loss, crash, security, broken contract
- `WARNING`  — logic error, leak, allocation in hot path
- `NOTE`     — style, readability, minor improvement

**Categories** (pick one):
- `null-safety` `lifecycle` `state` `concurrency` `allocation` `serialization` `event-leak` `logic`

## Examples

```csharp
// ── REVIEW [CRITICAL] null-safety: 'result' can be null when pool is exhausted.
//    Evidence: Pool.Get() returns null on empty; caller dereferences immediately.
//    Fix:      Guard with `if (result == null) return;` before use.
void Spawn() {
    var result = _pool.Get(); // ← comment goes here
```

```csharp
// ── REVIEW [WARNING] event-leak: OnEnable subscribes but OnDestroy does not unsubscribe.
//    Evidence: GameEvents.OnRoundEnd += HandleRoundEnd in OnEnable; no -= found.
//    Fix:      Add `GameEvents.OnRoundEnd -= HandleRoundEnd;` in OnDestroy.
```

```csharp
// ── REVIEW [WARNING] allocation: LINQ in Update allocates per frame.
//    Evidence: `_enemies.Where(e => e.IsAlive).ToList()` called every frame.
//    Fix:      Cache filtered list or use index-based loop.
```

## Rules

- One comment block per distinct issue; do not stack unrelated issues at same line
- Place comment on the line of the issue, not the method signature
- Keep `Fix:` to one imperative sentence
- Never rewrite the code inline — annotation only

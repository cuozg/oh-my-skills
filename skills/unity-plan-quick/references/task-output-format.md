# Task Output Format

## ▲ Header Format

```
▲ {Feature or Task Title}
{$cost} · {N}h · {low|medium|high} risk

{One-sentence summary anchored to evidence.}

┌ Tasks
├─ {Task 1 subject} → skill:{skill-name}
├─ {Task 2 subject} → skill:{skill-name}
└─ {Task 3 subject} → skill:{skill-name}
```

## Rules

- `$cost` = XS ($50), S ($150), M ($500), L ($1500)
- Hours: realistic range e.g. `2-4h` or exact `6h`
- Risk: `low` (isolated change), `medium` (touches shared code), `high` (cross-system or runtime)
- Summary sentence must be evidence-anchored — reference a file or pattern found
- `→ skill:{name}` maps the task to the skill that should execute it

## Example

```
▲ Add health bar to player HUD
$150 · 3-5h · low risk

PlayerUI.cs already owns the HUD canvas; health data lives in PlayerStats.cs:42.

┌ Tasks
├─ Create HealthBar UI component → skill:unity-code-quick
├─ Bind PlayerStats.CurrentHealth to HealthBar → skill:unity-code-quick
└─ Add unit test for health binding → skill:unity-test-quick
```

# Task Structure

## task_create Fields

```python
task_create(
    subject="Add health regeneration to PlayerStats",
    description="Implement passive HP regen...\n→ skill:unity-code-quick",
    blockedBy=["T-abc123"]  # optional
)
```

## Subject Format

- Start with imperative verb
- Include target system/class
- Be specific — not "Update code"

| ✓ Good | ✗ Bad |
|--------|-------|
| Add ObjectPool for projectiles | Improve performance |
| Extract ISaveService interface | Refactor saving |
| Fix null ref in InventoryUI.OnSlotClick | Fix bug |
| Replace FindObjectOfType in EnemySpawner | Clean up code |

## Description Format

```
{What}: 1-line summary of the change
{Why}: reason or trigger (optional, if not obvious)
{How}: key implementation notes (2-3 bullets max)
→ skill:{skill-name}
```

Example:
```
Add coroutine-based HP regen to PlayerStats.
Triggered when out of combat for 3 seconds.
- Add _regenCoroutine field, start in OnOutOfCombat
- Cache WaitForSeconds(1f), regen 5 HP/tick
- Stop coroutine on damage received
→ skill:unity-code-quick
```

## Skill Routing

| Task Type | Skill |
|-----------|-------|
| Single file, simple | `→ skill:unity-code-quick` |
| Multi-file, architecture | `→ skill:unity-code-deep` |
| Editor tooling | `→ skill:unity-code-editor` |
| Unit tests | `→ skill:unity-test-unit` |
| Bug diagnosis | `→ skill:unity-debug-quick` |
| Investigation | `→ skill:unity-investigate-quick` |

## blockedBy Dependencies

- Use when task B needs output from task A
- Reference task IDs: `blockedBy=["T-abc123"]`
- Minimize chains — maximize parallel execution
- Only block on TRUE data dependencies

## Granularity Rules

- Each task = 1 skill invocation
- Each task = 1–4 hours of work
- If > 4 hours → split into subtasks
- If < 30 minutes → merge with related task
- One clear deliverable per task

## Anti-patterns

| Pattern | Fix |
|---------|-----|
| "Implement feature X" (too broad) | Split into 3–5 specific tasks |
| 10+ tasks with linear dependencies | Identify parallel groups |
| Task with no skill routing | Add `→ skill:` line |
| Circular blockedBy | Redesign task boundaries |
| Description is just subject repeated | Add how/why details |

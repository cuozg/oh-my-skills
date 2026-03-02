# Task System Integration

## task_create Usage

```
task_create(
  subject="Implement HealthSystem core logic",
  description="Create HealthSystem.cs with Take/Heal/Die events",
  blockedBy=[]           # no deps → runs immediately
)
```

## Parent → Children Pattern

```
parent = task_create(subject="Feature: Combat System", blockedBy=[])

child1 = task_create(subject="HealthSystem core",    blockedBy=[])
child2 = task_create(subject="DamageCalculator",      blockedBy=[child1.id])
child3 = task_create(subject="CombatUI bindings",     blockedBy=[child2.id])
child4 = task_create(subject="Integration tests",     blockedBy=[child2.id, child3.id])
```

## blockedBy Rules

- Pass task IDs (strings), not subjects
- Only add `blockedBy` when the prior task's *output* is a direct input
- Parallel-safe tasks must have empty `blockedBy`

## After Creation

Print a summary table to chat:

```
Tasks created:
  T-abc123  HealthSystem core          [unblocked]
  T-def456  DamageCalculator           [blocked by T-abc123]
  T-ghi789  CombatUI bindings          [blocked by T-def456]
  T-jkl012  Integration tests          [blocked by T-def456, T-ghi789]
```

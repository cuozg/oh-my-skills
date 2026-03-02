# Dependency Mapping

## Dependency Types

| Type     | Description                        | Example                              |
|----------|------------------------------------|--------------------------------------|
| Data     | Task B needs output of Task A      | Service needs interface defined first|
| Ordering | Task B must run after Task A       | Tests after implementation           |
| Resource | Tasks share a file/system          | Two tasks editing same class         |

## blockedBy Usage

```
Task A: "Define IHealthService interface"         → blockedBy: []
Task B: "Implement HealthService"                  → blockedBy: [A]
Task C: "Write HealthService tests"                → blockedBy: [B]
Task D: "Create HealthBar UI"                      → blockedBy: [A]  (only needs interface)
```

## Maximizing Parallelism

- Block only on TRUE dependencies — not assumed ordering
- Interface/contract tasks unblock multiple consumers
- Split "implement + test" into separate tasks (test blocked by implement)
- UI and logic tasks often parallel if interface is defined first

## Dependency Chain Rules

- Max chain depth: 4 (deeper = redesign task breakdown)
- Critical path = longest chain = project duration
- Shorten critical path by splitting large tasks

## When to Merge Tasks

- Two tasks edit the same file with overlapping changes
- Task B is trivial (<30 min) and blocked only by Task A
- Sequential tasks with no parallelism benefit

## When to Split Tasks

- Task touches 3+ files across different systems
- Task has both "define" and "implement" phases
- Task can unblock other tasks by splitting early deliverables

## Visualization

```
A ──→ B ──→ C
 \         ↗
  └→ D ──┘
```

A and D can run after A completes. C waits for both B and D.

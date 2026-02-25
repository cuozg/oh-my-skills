
## Example 3: Blocked Resolution (Hotfix pattern)

**Scenario**: Worker2 blocked on bd-22 — needs event in file reserved by Worker1.

```
Worker2 → [bd-22] BLOCKED: Missing OnHeroAttacked event (file reserved by Worker1)
Orchestrator → creates bd-23 HOTFIX, assigns to Worker1
Worker1 → completes bd-21, then bd-23 hotfix, releases file, notifies Worker2
Worker2 → resumes bd-22 with event now available
```

**Pattern**: `BLOCKED` message → orchestrator creates hotfix → assign to file holder → unblock notification → resume

---

## Common Patterns Summary

| Pattern | Flow |
|---------|------|
| Linear (LOW risk) | Discovery → Epic → Task → Complete |
| Spike-gated (HIGH risk) | Discovery → Spike → Decision → Decompose → Parallel → Complete |
| Spike-only | Spike → PROCEED/ABORT → (convert to epic or stop) |
| Blocked → Hotfix | BLOCKED msg → orchestrator hotfix → unblock → resume |
| Interface change | Breaking change → broadcast → track migrations → validate → close |

---

## Common Command Sequences

```bash
# Simple feature
bd add "Feature" --epic                           # → bd-X
bd add "Task" --parent bd-X --priority 2          # → bd-Y
# ... implement ...
bd close bd-Y && bd close bd-X && bd sync

# Spike → feature
bd add "SPIKE: Question" --priority 0             # → bd-X
# ... validate, document ...
bd close bd-X
bd add "Implement (validated by bd-X)" --epic     # → bd-Y

# Hotfix for blocked worker
bd add "HOTFIX: Unblock bd-N" --priority 1 --parent bd-epic

# Parallel tracks
bd add "Epic" --epic                              # → bd-X
bd add "Task 1" --parent bd-X --priority 1
bd add "Task 2" --parent bd-X --priority 1
bv --robot-plan --bead bd-X
```

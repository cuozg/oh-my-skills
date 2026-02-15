# Beads Workflow Examples

---

## Example 1: Simple Feature (LOW risk, linear)

**Scenario**: Add passive health regen (2 files, familiar pattern)

```bash
# Discovery → Risk LOW → proceed directly

# Create epic + task
bd add "Add passive health regeneration" --priority 2 --epic    # → bd-10
bd add "Implement regen in HeroStats + SO field" --parent bd-10 --priority 2  # → bd-11

# Execute bd-11
bd update bd-11 --claim --status in_progress
# Reserve files → implement → test
git commit -m "feat(hero): add passive health regeneration (bd-11)"
bd close bd-11
bd close bd-10
bd sync
```

**Pattern**: Discovery → Risk LOW → Epic → Task → Complete (single worker, ~30min)

---

## Example 2: Complex Feature with Spike (HIGH risk, parallel tracks)

**Scenario**: Enemy object pooling with NavMeshAgent (6+ files, unknown NavMesh behavior)

### Phase 1: Spike (30min time-box)

```bash
bd add "Implement enemy object pooling" --priority 1 --epic     # → bd-12
bd add "SPIKE: Validate NavMeshAgent pooling" --priority 0 --parent bd-12  # → bd-13
```

**Spike finding**: NavMeshAgent CAN be pooled — disable before moving, Warp() after re-enable.

```bash
bd close bd-13  # Document findings in .spikes/enemy-pooling/bd-13/FINDINGS.md
```

### Phase 2: Decompose into tasks

```bash
bd add "Create generic ObjectPool<T>" --parent bd-12 --priority 1          # → bd-14
bd add "Add Reset() to Enemy components" --parent bd-12 --priority 1       # → bd-15
bd add "Modify EnemySpawner to use pool" --parent bd-12 --priority 1       # → bd-16
bd add "Update enemy prefabs with PooledObject" --parent bd-12 --priority 2 # → bd-17
bv --robot-plan --bead bd-12
# Track 1 (Worker1): bd-14 → bd-16
# Track 2 (Worker2): bd-15 → bd-17
```

### Phase 3: Parallel execution

Workers claim, reserve files, implement, commit per-bead, self-message context, report COMPLETE, close beads.

### Phase 4: Epic closure

Validate checklist → `bd close bd-12`

**Pattern**: Discovery → Risk HIGH → Spike → Decompose → Parallel Tracks → Complete (~4h)

---

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

# Goal Loop Workflow Diagram

## High-Level Flow

```
START
  ↓
[Phase 0: Scan Goals]
  ├─ Read Docs/Goals/Master.md
  ├─ Classify goals (pending, in-progress, completed, blocked)
  └─ Count incomplete goals
  ↓
IF no incomplete goals → SUCCESS (exit 0)
  ↓
IF ≥1 incomplete goal → START LOOP
  ↓
  ┌─────────────────────────────────────────────────────────┐
  │ [Phase 1: Pick Next Goal]                               │
  │ - Pick first incomplete by priority (critical > high)    │
  │ - Record metadata                                        │
  │ - Set worktree env                                       │
  └─────────────────────────────────────────────────────────┘
  ↓
  ┌─────────────────────────────────────────────────────────┐
  │ [Phase 2a: Execute via goal-execute]                       │
  │ - Delegate full goal implementation                      │
  │ - Wait for completion (blocking)                         │
  │ - Record outcome (DONE, DONE_WITH_CONCERNS, BLOCKED)    │
  └─────────────────────────────────────────────────────────┘
  ↓
  ┌─────────────────────────────────────────────────────────┐
  │ IF goal BLOCKED:                                         │
  │  ├─ Record blocker reason                               │
  │  ├─ Mark goal "blocked" in Master.md                    │
  │  └─ GOTO [Pick Next Goal] (skip verification)           │
  │                                                          │
  │ IF goal DONE or DONE_WITH_CONCERNS:                      │
  │  └─ Continue to verification                            │
  └─────────────────────────────────────────────────────────┘
  ↓
  ┌─────────────────────────────────────────────────────────┐
  │ [Phase 2b: Verify via goal-verify]                        │
  │ - Run goal-verify on completed goal                       │
  │ - Check each acceptance criterion                       │
  │ - Verdict: all ✅ Met, or some ⚠️ Partial/❌ Unmet      │
  └─────────────────────────────────────────────────────────┘
  ↓
  ┌─────────────────────────────────────────────────────────┐
  │ IF all criteria ✅ Met:                                 │
  │  ├─ Mark goal "completed" in Master.md                  │
  │  ├─ Record in .loop-state.json                          │
  │  └─ GOTO [Pick Next Goal]                               │
  │                                                          │
  │ IF some criteria ⚠️ Partial or ❌ Unmet:                │
  │  ├─ Invoke goal-improve for goal critique               │
  │  ├─ Re-run goal-verify                                   │
  │  └─ IF still gaps → Mark goal "blocked" with reason     │
  │                    OR manual review needed             │
  │  └─ GOTO [Pick Next Goal]                               │
  └─────────────────────────────────────────────────────────┘
  ↓
  [Cycle limit or no more incomplete goals?]
  ├─ YES → GOTO [Phase 5: Report]
  ├─ NO → GOTO [Phase 1: Pick Next Goal]
  ↓
  ┌─────────────────────────────────────────────────────────┐
  │ [Phase 5: Generate Report]                              │
  │ - Write .loop-report.md                                 │
  │ - Summary: total, completed, blocked, remaining        │
  │ - List completed goals (with PR links)                 │
  │ - List blocked goals (with reasons)                    │
  └─────────────────────────────────────────────────────────┘
  ↓
  [All goals completed?]
  ├─ YES → SUCCESS (exit 0)
  └─ NO → PARTIAL (exit 1)
```

---

## State Transitions Per Goal

```
         ┌─────────────────────────┐
         │   pick_next_goal()      │
         │  (PENDING or IN_PROG)   │
         └────────┬────────────────┘
                  ↓
         ┌─────────────────────────┐
         │   goal-execute execute     │
         │  (Sisyphus + Hephaestus)│
         └────┬────────────┬───────┘
              ↓            ↓
        ┌─────────┐    ┌──────────┐
        │ DONE    │    │ BLOCKED  │
        │  or     │    │ (blocker)│
        │ CONCERN │    └──────────┘
        └────┬────┘         │
             ↓              ↓
        ┌─────────────┐    [SKIP to next]
        │ goal-verify   │
        │  verify     │
        └┬───────────┬┘
         ↓           ↓
    ┌─────────┐  ┌──────────┐
    │ ALL ✅  │  │ GAP(S)   │
    │ VERIFIED│  │ FOUND    │
    └────┬────┘  └────┬─────┘
         ↓            ↓
    [Mark        [goal-improve]
     COMPLETED]       ↓
         ↓        [Re-test]
    [Next goal]       ↓
                  ┌─────────┐
                  │ Fixed?  │
                  └┬───┬───┬┘
             YES  │   │ NO
                  ↓   ↓
              [COMPLETED] [BLOCKED]
```

---

## Example Execution Timeline

```
17:36:29 START
17:36:30 ✓ Scan: found 5 incomplete goals
17:36:31 ✓ Cycle 1/50: Pick "[Auth] Add JWT Auth" (priority: high)
17:36:32 → Delegating to goal-execute...
17:40:15 ← goal-execute DONE (PR #123)
17:40:16 → Delegating to goal-verify...
17:40:45 ← goal-verify: all ✅ Met
17:40:46 ✓ Goal completed. Recording.

17:40:47 ✓ Cycle 2/50: Pick "[Search] Add Full-Text" (priority: high)
17:40:48 → Delegating to goal-execute...
17:43:30 ← goal-execute DONE (PR #124)
17:43:31 → Delegating to goal-verify...
17:43:50 ← goal-verify: 4/5 ✅, 1 ⚠️ Partial
17:43:51 → Delegating to goal-improve...
17:44:20 ← goal-improve: criteria clarified
17:44:21 → Re-running goal-verify...
17:44:40 ← goal-verify: all ✅ Met
17:44:41 ✓ Goal completed. Recording.

17:44:42 ✓ Cycle 3/50: Pick "[API] Add Rate Limit" (priority: medium)
17:44:43 → Delegating to goal-execute...
17:46:00 ← goal-execute BLOCKED (missing cache service)
17:46:01 ✓ Goal blocked. Recording.

17:46:02 ✓ Cycle 4/50: Pick "[UI] Add Dark Mode" (priority: low)
17:46:03 → Delegating to goal-execute...
17:48:45 ← goal-execute DONE (PR #125)
17:48:46 → Delegating to goal-verify...
17:49:05 ← goal-verify: all ✅ Met
17:49:06 ✓ Goal completed. Recording.

17:49:07 ✓ Cycle 5/50: Pick "[Docs] Update README" (priority: low)
17:49:08 → Delegating to goal-execute...
17:50:20 ← goal-execute DONE (PR #126)
17:50:21 → Delegating to goal-verify...
17:50:35 ← goal-verify: all ✅ Met
17:50:36 ✓ Goal completed. Recording.

17:50:37 ✓ No more incomplete goals.
17:50:38 ✓ Loop complete: 4 completed, 1 blocked (5 total)
17:50:39 ✓ Report: Docs/Goals/.loop-report.md
17:50:40 END (exit 0)
```

---

## Checkpoint Recovery

```
Scenario: Loop interrupted at cycle 3/5 (after goal 2 completed)

.loop-state.json at interrupt:
{
  "loop_cycles": 2,
  "goals_total": 5,
  "goals_completed": 2,
  "goals_blocked": 0,
  "completed_goals": [
    {goal 1},
    {goal 2}
  ],
  ...
}

Resume with --resume flag:
- Reloads state from .loop-state.json
- Skips goals 1, 2 (already completed)
- Resumes at goal 3
- Continues cycles 3, 4, 5 → completes
- Updates .loop-state.json with final results
- Generates report
```

---

---
name: plan-loop
description: >
  Autonomous orchestrator for batch goal completion. Loops through all incomplete
  goals, executing plan-work → plan-test → plan-improve cycles until all goals are
  verified complete. Picks one goal per cycle deterministically by priority. Detects
  gaps, invokes fixes, re-tests, and repeats. Generates completion report. Use for
  unattended batch workflows ("run all goals", "autonomous completion", "loop until done").
---

# Plan Loop — Autonomous Continuous Goal Completion

You are the **loop orchestrator**. Your job is to pick incomplete goals one-by-one, execute each through the plan-work → plan-test cycle, detect gaps, loop back for fixes, and **never stop until every goal is verified complete**.

This skill sits **above** the `plan-work` → `plan-test` → `plan-improve` pipeline. It does not implement, test, or improve — it **delegates and repeats** until all work is done.

---

## Position in the Ecosystem

```
          ┌─ plan-goal (write goals)
          │
          ├─ plan-loop (THIS SKILL — orchestrate all)
          │   ├─ plan-work (execute one goal)
          │   ├─ plan-test (verify one goal)
          │   └─ plan-improve (fix gaps, if needed)
          │
          └─ Output: All goals completed with verified criteria
```

The **plan-goal** → **plan-work** → **plan-test** → **plan-improve** pipeline handles a single goal in isolation. **`plan-loop`** wraps that pipeline and runs it repeatedly, picking the next incomplete goal after each cycle completes.

---

## The Iron Law

```
COMPLETION = ALL GOALS IN COMPLETED STATE WITH EVERY CRITERION VERIFIED.

NO PARTIAL LOOPS.
NO SKIPPED GOALS.
NO UNVERIFIED CLAIMS.

LOOP UNTIL DONE.
```

The loop is **complete** only when:
1. Every goal file under `Docs/Goals/**/*.md` has `status: completed` in its frontmatter.
2. Every criterion under `## Acceptance Criteria` is checked `- [x]`.
3. Every criterion has been independently verified by `plan-test` with evidence (`file:line`, test, command output).

---

## Non-Negotiable Rules (8)

| # | Rule |
|---|---|
| 1 | **Always start by scanning `Docs/Goals/Master.md`** for the full picture — incomplete count, dependencies, priorities. |
| 2 | **Pick exactly one incomplete goal per cycle** — stop at first match. Multi-parallel execution is out of scope. |
| 3 | **Never skip a goal.** If a goal is `pending`, `in-progress`, or has an unchecked box, it must be completed before the loop ends. |
| 4 | **Never advance without verification.** Every goal must pass `plan-test` before it is marked `completed`. A goal marked `completed` by `plan-work` is a claim — `plan-test` is the truth. |
| 5 | **Loop on test failure.** If `plan-test` reports `❌ Unmet` or `⚠️ Partial`, invoke `plan-improve` to close gaps, then re-run `plan-test` on that goal until all verdicts are `✅ Met`. |
| 6 | **Never edit goal files directly.** Goal status updates and checkbox marking are the responsibility of downstream skills (`plan-work`, `plan-improve`). Only read goals. |
| 7 | **Always generate a loop summary** before exit. Include: total goals, completed count, blocked count, per-goal status, and time-ordered completion log. |
| 8 | **Always handle failures gracefully.** If a goal becomes `blocked`, document the blocker, pause that goal (mark it `blocked` in Master.md), and pick the next incomplete goal. Do not halt the entire loop. |

---

## Workflow

### Phase 0 — Scan & Boot

1. **Read `Docs/Goals/Master.md`** (or scan `Docs/Goals/**/` if Master.md is missing).
   - Extract all goal file paths, their status, priority, unchecked-criteria count.
   - Classify goals into: `pending`, `in-progress`, `completed`, `blocked`.
   - Sort by priority (critical > high > medium > low) within each status group.

2. **Identify incomplete goals** = `status ∈ {pending, in-progress, blocked}` OR ≥ 1 unchecked criterion.
   - If zero incomplete goals → report "All goals completed" and exit with code 0.
   - If ≥ 1 incomplete goal → proceed to Phase 1.

3. **Initialize loop state** (in-memory or file-backed for crash recovery):
   - `loop_start_time`, `goals_total`, `goals_completed`, `goals_blocked`, `loop_cycles`
   - Create tracking file: `Docs/Goals/.loop-state.json` with running status.

### Phase 1 — Pick Next Goal

1. **Query incomplete goals** from Master.md scan (sorted by priority).
2. **Pick the first one** (FIFO by priority, then by file path for determinism).
3. **Record goal metadata**: `goal_file`, `goal_title`, `priority`, `unchecked_count`.
4. **Increment `loop_cycles` counter** — track how many rounds this loop has run.

### Phase 2 — Execute & Verify

#### 2a. Run `plan-work`

- **Invoke** `plan-work` with the goal file.
- **Wait for completion** (blocking call).
- **Record outcome**:
  - `DONE` → PR created, goal ready for test.
  - `DONE_WITH_CONCERNS` → PR created but with flagged issues. Proceed to test, but flag for review.
  - `BLOCKED` → Goal cannot proceed. Record blocker reason. Mark goal `blocked` in Master.md. Proceed to Phase 1 (pick next).
  - Error/timeout → Mark goal `blocked` with error detail. Proceed to Phase 1 (pick next).

#### 2b. Run `plan-test`

- **Invoke** `plan-test` on the same goal file (after `plan-work` completed).
- **Wait for completion** (blocking call).
- **Record test verdict**:
  - `All criteria ✅ Met` (exit code 0) → Goal is verified complete.
  - Some criteria `⚠️ Partial` or `❌ Unmet` (exit code 1) → Gaps found.
  - Error/timeout (exit code 2 or 3) → Mark goal `blocked` with test failure. Move to next.

#### 2c. Gap Detection & Fix Loop

If `plan-test` found gaps:

1. **Invoke `plan-improve`** with the `plan-test` report (file path).
   - `plan-improve` will read the test report and auto-fix common issues.
   - Max 2 `plan-improve` cycles per goal.

2. **Re-run `plan-test`** on the goal.
   - If all criteria now `✅ Met` → goal verified complete. Proceed to Phase 3.
   - If still gaps after 2 cycles → mark goal `blocked` with reason "too many gaps, manual review needed". Proceed to Phase 1 (next goal).

### Phase 3 — Mark & Record

1. **Update Master.md** to reflect goal completion:
   - Set goal `status: completed`.
   - Update `updated` timestamp.
   - Increment `goals_completed` counter.

2. **Log completion** to `.loop-state.json`:
   - `goal_title`, `cycles_to_complete`, `completed_at`, `pr_url`, `test_verdict`.

3. **Return to Phase 1** — pick next incomplete goal.

### Phase 4 — Exit Condition

**Loop terminates when:**
- No incomplete goals remain (exit code 0, success).
- OR max cycles reached (default 50; exit code 1, partial completion).
- OR user interrupt (graceful shutdown, record current state).

### Phase 5 — Report

Generate `Docs/Goals/.loop-report.md` with:

```markdown
# Plan Loop Completion Report

Generated: <timestamp>
Duration: <start> → <end> (HH:MM:SS)
Cycles: <completed> / <max>

## Summary
- Total goals: N
- Completed: M (NN%)
- Blocked: K
- Remaining: P

## Completed Goals (in order)
1. [Goal Title] — <priority> — 3 cycles
2. [Goal Title] — <priority> — 1 cycle
...

## Blocked Goals (with reason)
- [Goal Title] — reason: <blocker detail>
...

## Timeline
```

---

## CLI Reference

```bash
# Start the autonomous loop
python skills/plan-loop/scripts/orchestrate.py [--root .] [--max-cycles 50] [--output Docs/Goals/.loop-report.md]

# Check loop status (during or after execution)
python skills/plan-loop/scripts/check_status.py [--root .]

# Resume interrupted loop from checkpoint
python skills/plan-loop/scripts/orchestrate.py --resume [--root .] [--checkpoint Docs/Goals/.loop-state.json]

# Dry-run: scan and report what would be executed
python skills/plan-loop/scripts/orchestrate.py --dry-run [--root .]
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All goals completed ✅ |
| 1 | Partial completion (max cycles reached or manual interrupt) ⚠️ |
| 2 | Usage or input error (missing goals folder, invalid args) ❌ |
| 3 | Unexpected failure (internal error, unrecoverable state) ❌ |

---

## Integration With the Pipeline

| Upstream | Purpose | plan-loop reads |
|----------|---------|-----------------|
| `plan-goal` | Creates goal files | `Docs/Goals/**/*.md`, `Docs/Goals/Master.md` |

| Downstream | Purpose | plan-loop delegates to |
|-----------|---------|----------------------|
| `plan-work` | Execute one goal | Invoked N times (once per incomplete goal) |
| `plan-test` | Verify one goal | Invoked N times (once per goal, possibly re-runs on gaps) |
| `plan-improve` | Fix gaps | Invoked if `plan-test` finds `⚠️ Partial` or `❌ Unmet` |

**Typical flow (all goals completed):**

```
Loop start
├─ Cycle 1: Pick "Goal A" (pending)
│  ├─ plan-work → PR created
│  ├─ plan-test → 3/4 criteria met
│  ├─ plan-improve (cycle 1) → closes 1 gap
│  ├─ plan-test → all 4 criteria met ✅
│  └─ Mark "Goal A" completed
├─ Cycle 2: Pick "Goal B" (in-progress)
│  ├─ plan-work → PR created
│  ├─ plan-test → all 5 criteria met ✅
│  └─ Mark "Goal B" completed
├─ Cycle 3: Pick "Goal C" (pending)
│  ├─ plan-work → blocked (missing dependency)
│  └─ Mark "Goal C" blocked
├─ No more incomplete goals
└─ Loop end → exit code 0, report generated
```

---

## Example `.loop-state.json` (Checkpoint)

```json
{
  "loop_start": "2026-04-25T17:36:29Z",
  "loop_cycles": 3,
  "goals_total": 5,
  "goals_completed": 2,
  "goals_blocked": 1,
  "goals_remaining": 2,
  "max_cycles": 50,
  "completed_goals": [
    {
      "goal_file": "Docs/Goals/auth/add-jwt-auth.md",
      "goal_title": "[Auth] Add JWT Auth",
      "completed_at": "2026-04-25T17:40:15Z",
      "cycles_to_complete": 2,
      "pr_url": "https://github.com/org/repo/pull/123",
      "test_verdict": "all-met"
    },
    {
      "goal_file": "Docs/Goals/search/add-full-text.md",
      "goal_title": "[Search] Add Full-Text Search",
      "completed_at": "2026-04-25T17:45:30Z",
      "cycles_to_complete": 1,
      "pr_url": "https://github.com/org/repo/pull/124",
      "test_verdict": "all-met"
    }
  ],
  "blocked_goals": [
    {
      "goal_file": "Docs/Goals/api/add-rate-limit.md",
      "goal_title": "[API] Add Rate Limiting",
      "blocked_at": "2026-04-25T17:42:00Z",
      "blocker_reason": "Missing cache service setup"
    }
  ]
}
```

---

## Rules

1. **One goal per cycle.** Never batch-execute multiple goals.
2. **Deterministic picking.** Always sort by priority (critical > high > medium > low), then by file path.
3. **Respect dependencies.** If goal A depends on goal B, ensure B is `completed` before executing A (enforce at Master.md read time).
4. **No infinite loops.** Max 50 cycles per invocation (configurable via `--max-cycles`). If loop reaches max, exit with code 1 and report partial completion.
5. **Graceful failure.** If a goal becomes `blocked`, mark it and move to next — do not halt the entire loop.
6. **Checkpoint & recover.** Write `.loop-state.json` after each cycle — allows resume on crash.
7. **Never mutate goal files.** Only read from them. Status updates are done by downstream skills.
8. **Stdlib + orchestration only.** Scripts invoke subagents; they do not implement logic themselves.

---

## File Layout

```
skills/plan-loop/
├── SKILL.md                           ← this file
├── scripts/
│   ├── orchestrate.py                 ← main loop orchestrator (entry point)
│   ├── check_status.py                ← query loop status / checkpoint
│   ├── goal_scanner.py                ← read Master.md, scan goals
│   └── report_generator.py            ← format completion report
└── references/
    ├── loop-workflow.md               ← detailed workflow diagram
    └── integration-guide.md            ← how to integrate with other skills
```

All scripts are executable and runnable standalone.

---

## Example Invocation

```bash
# Run the full loop
cd /path/to/project
python ~/.config/opencode/skills/plan-loop/scripts/orchestrate.py --root .

# Expected output (on success):
# ✓ Loop start: scanning goals...
# ✓ Found 5 incomplete goals
# ✓ Cycle 1: Executing "Goal A" → plan-work → plan-test ✅
# ✓ Cycle 2: Executing "Goal B" → plan-work → plan-test ✅
# ✓ Cycle 3: Executing "Goal C" → plan-work → blocked (marked for manual review)
# ✓ Cycle 4: Executing "Goal D" → plan-work → plan-test ✅
# ✓ Cycle 5: Executing "Goal E" → plan-work → plan-test ✅
# ✓ Loop end: all goals completed in 5 cycles
# ✓ Report: Docs/Goals/.loop-report.md
```

---

## Non-Goals

- **Executing a single goal.** Use `plan-work` directly.
- **One-off goal verification.** Use `plan-test` directly.
- **Manual code review or improvement.** Use `plan-improve` or domain-specific review skills.
- **Creating goals.** Use `plan-goal`.
- **Running project test suites.** Use the project's own runner (`pytest`, `npm test`, etc.). `plan-test` only locates test files.

---

## Comparison: plan-work vs plan-loop

| Aspect | plan-work | plan-loop |
|--------|-----------|-----------|
| **Scope** | One incomplete goal | All incomplete goals |
| **Invocation** | User specifies or auto-picks one | Automatically picks sequence |
| **Verification** | Runs once, delegates to Hephaestus | Runs after each goal, loops if gaps |
| **Exit condition** | Goal is done (completed or blocked) | All goals are done (or max cycles) |
| **Use case** | Manual control of one goal | Unattended batch completion |

---

## Crash Recovery

If the loop is interrupted (crash, timeout, user interrupt):

1. **Check `Docs/Goals/.loop-state.json`** — records all completed goals and current cycle.
2. **Resume with `--resume` flag:**
   ```bash
   python scripts/orchestrate.py --resume --root .
   ```
3. **Behavior:**
   - Skips already-completed goals (reads from checkpoint).
   - Resumes at next incomplete goal.
   - Resets cycle counters to running totals (not zero).

---

## Logging & Observability

The loop writes to `Docs/Goals/.loop-log.txt` (appended each run):

```
[2026-04-25T17:36:29.000Z] Loop start (cycle 1/50)
[2026-04-25T17:36:45.123Z] Picked goal: Docs/Goals/auth/add-jwt-auth.md
[2026-04-25T17:36:45.456Z] Delegating to plan-work...
[2026-04-25T17:40:15.789Z] plan-work completed: DONE (PR #123)
[2026-04-25T17:40:15.999Z] Delegating to plan-test...
[2026-04-25T17:40:30.111Z] plan-test completed: all-met ✅
[2026-04-25T17:40:31.222Z] Goal completed. Recording in Master.md.
[2026-04-25T17:40:31.333Z] Loop cycle 1 end. Picking next goal.
```

---


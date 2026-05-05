---
name: goal-loop
description: "Loop all goals. Scan the goal registry for incomplete goals; when one is found, improve weak goal definitions with goal-improve when needed, execute it with goal-execute, verify it with goal-verify, then loop again until no incomplete goals remain. Picks one goal per cycle deterministically by priority and never exits on an unverified completion claim. Use for unattended batch workflows."
---

# Goal Loop — Autonomous Continuous Goal Completion

You are the **loop orchestrator**. Your job is to pick incomplete goals one-by-one, improve weak goals before execution, execute each through the goal-execute → goal-verify cycle, loop back for implementation fixes when verification fails, and **never stop until every goal is verified complete**.

This skill sits **above** the `goal-improve` → `goal-execute` → `goal-verify` pipeline. It does not critique, implement, or verify directly — it **delegates and repeats** until all work is done.

---

## Position in the Ecosystem

```
          ┌─ goal-create (write goals)
          │
          ├─ goal-loop (THIS SKILL — orchestrate all)
          │   ├─ goal-improve (critique weak goals before execution)
          │   ├─ goal-execute (execute one goal)
          │   ├─ goal-verify (verify one goal)
          │
          └─ Output: All goals completed with verified criteria
```

The **goal-create** → **goal-improve** → **goal-execute** → **goal-verify** pipeline handles a single goal in isolation. **`goal-loop`** wraps that pipeline and runs it repeatedly, picking the next incomplete goal after each cycle completes.

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
3. Every criterion has been independently verified by `goal-verify` with evidence (`file:line`, test, command output).

---

## Non-Negotiable Rules (8)

| # | Rule |
|---|---|
| 1 | **Always start by scanning `Docs/Goals/Master.md`** for the full picture — incomplete count, dependencies, priorities. |
| 2 | **Pick exactly one incomplete goal per cycle** — stop at first match. Multi-parallel execution is out of scope. |
| 3 | **Never skip a goal.** If a goal is `pending`, `in-progress`, or has an unchecked box, it must be completed before the loop ends. |
| 4 | **Never advance without verification.** Every goal must pass `goal-verify` before it is marked `completed`. A goal marked `completed` by `goal-execute` is a claim — `goal-verify` is the truth. |
| 5 | **Loop on verification failure.** If `goal-verify` reports `❌ Unmet` or `⚠️ Partial`, send the concrete gaps back through `goal-execute`, then re-run `goal-verify` until all verdicts are `✅ Met`. |
| 6 | **Use `goal-improve` for bad goals.** If a goal is vague, low-value, badly sequenced, overbroad, or hard for humans/AI agents to use, invoke `goal-improve` before execution. |
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

#### 2a. Run `goal-execute`

- **Invoke** `goal-execute` with the goal file.
- **Wait for completion** (blocking call).
- **Record outcome**:
  - `DONE` → PR created, goal ready for test.
  - `DONE_WITH_CONCERNS` → PR created but with flagged issues. Proceed to test, but flag for review.
  - `BLOCKED` → Goal cannot proceed. Record blocker reason. Mark goal `blocked` in Master.md. Proceed to Phase 1 (pick next).
  - Error/timeout → Mark goal `blocked` with error detail. Proceed to Phase 1 (pick next).

#### 2b. Run `goal-verify`

- **Invoke** `goal-verify` on the same goal file (after `goal-execute` completed).
- **Wait for completion** (blocking call).
- **Record test verdict**:
  - `All criteria ✅ Met` (exit code 0) → Goal is verified complete.
  - Some criteria `⚠️ Partial` or `❌ Unmet` (exit code 1) → Gaps found.
  - Error/timeout (exit code 2 or 3) → Mark goal `blocked` with test failure. Move to next.

#### 2c. Gap Detection & Revision Loop

If `goal-verify` found gaps:

1. **Classify the gap source.**
   - Implementation gap: the goal is clear, but the code does not satisfy it.
   - Goal-design gap: the criterion is vague, untestable, low-value, too broad, or badly sequenced.

2. **Route to the right skill.**
   - Implementation gap → run `goal-execute` again with the concrete `goal-verify` findings.
   - Goal-design gap → run `goal-improve` to critique and revise the goal, then run `goal-execute`.

3. **Re-run `goal-verify`** on the goal.
   - If all criteria now `✅ Met` → goal verified complete. Proceed to Phase 3.
   - If the same gap persists after a rerun → mark goal `blocked` with the concrete reason. Proceed to Phase 1 (next goal).

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
# Goal Loop Completion Report

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
python skills/goal-loop/scripts/orchestrate.py [--root .] [--max-cycles 50] [--output Docs/Goals/.loop-report.md]

# Check loop status (during or after execution)
python skills/goal-loop/scripts/check_status.py [--root .]

# Resume interrupted loop from checkpoint
python skills/goal-loop/scripts/orchestrate.py --resume [--root .] [--checkpoint Docs/Goals/.loop-state.json]

# Dry-run: scan and report what would be executed
python skills/goal-loop/scripts/orchestrate.py --dry-run [--root .]
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

| Upstream | Purpose | goal-loop reads |
|----------|---------|-----------------|
| `goal-create` | Creates goal files | `Docs/Goals/**/*.md`, `Docs/Goals/Master.md` |

| Downstream | Purpose | goal-loop delegates to |
|-----------|---------|----------------------|
| `goal-execute` | Execute one goal | Invoked N times (once per incomplete goal) |
| `goal-verify` | Verify one goal | Invoked N times (once per goal, possibly re-runs on gaps) |
| `goal-improve` | Critique and improve goal design | Invoked when a goal is vague, low-value, untestable, overbroad, or poorly sequenced |

**Typical flow (all goals completed):**

```
Loop start
├─ Cycle 1: Pick "Goal A" (pending)
│  ├─ goal-execute → PR created
│  ├─ goal-verify → 3/4 criteria met
│  ├─ goal-execute → fixes implementation gap from verifier evidence
│  ├─ goal-verify → all 4 criteria met ✅
│  └─ Mark "Goal A" completed
├─ Cycle 2: Pick "Goal B" (in-progress)
│  ├─ goal-execute → PR created
│  ├─ goal-verify → all 5 criteria met ✅
│  └─ Mark "Goal B" completed
├─ Cycle 3: Pick "Goal C" (pending)
│  ├─ goal-execute → blocked (missing dependency)
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
skills/goal-loop/
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
python ~/.config/opencode/skills/goal-loop/scripts/orchestrate.py --root .

# Expected output (on success):
# ✓ Loop start: scanning goals...
# ✓ Found 5 incomplete goals
# ✓ Cycle 1: Executing "Goal A" → goal-execute → goal-verify ✅
# ✓ Cycle 2: Executing "Goal B" → goal-execute → goal-verify ✅
# ✓ Cycle 3: Executing "Goal C" → goal-execute → blocked (marked for manual review)
# ✓ Cycle 4: Executing "Goal D" → goal-execute → goal-verify ✅
# ✓ Cycle 5: Executing "Goal E" → goal-execute → goal-verify ✅
# ✓ Loop end: all goals completed in 5 cycles
# ✓ Report: Docs/Goals/.loop-report.md
```

---

## Non-Goals

- **Executing a single goal.** Use `goal-execute` directly.
- **One-off goal verification.** Use `goal-verify` directly.
- **Goal critique or manual code review.** Use `goal-improve` or domain-specific review skills.
- **Creating goals.** Use `goal-create`.
- **Running project test suites.** Use the project's own runner (`pytest`, `npm test`, etc.). `goal-verify` only locates test files.

---

## Comparison: goal-execute vs goal-loop

| Aspect | goal-execute | goal-loop |
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
[2026-04-25T17:36:45.456Z] Delegating to goal-execute...
[2026-04-25T17:40:15.789Z] goal-execute completed: DONE (PR #123)
[2026-04-25T17:40:15.999Z] Delegating to goal-verify...
[2026-04-25T17:40:30.111Z] goal-verify completed: all-met ✅
[2026-04-25T17:40:31.222Z] Goal completed. Recording in Master.md.
[2026-04-25T17:40:31.333Z] Loop cycle 1 end. Picking next goal.
```

---

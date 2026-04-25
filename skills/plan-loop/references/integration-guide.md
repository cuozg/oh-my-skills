# Plan Loop Integration Guide

## Overview

The plan-loop skill orchestrates the complete goal-completion pipeline:

```
plan-loop
├─ reads:  Docs/Goals/**, Docs/Goals/Master.md
├─ calls:  plan-work (N times)
├─ calls:  plan-test (N times, possibly 2x per goal on failures)
├─ calls:  plan-improve (M times, for gap fixes)
├─ writes: Docs/Goals/.loop-state.json (checkpoint)
└─ writes: Docs/Goals/.loop-report.md (final report)
```

---

## Integration Points

### 1. Reading Goals (Input)

**Expectation:** `Docs/Goals/` contains goal files created by `plan-goal`.

Each goal file format:
```markdown
---
status: pending|in-progress|completed|blocked
priority: critical|high|medium|low
created: YYYY-MM-DD
updated: YYYY-MM-DD
depends_on: [goal-id, ...]
---

# [Feature] Goal Title

## Objective
...

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [x] Criterion 3

## Context / Constraints / Notes
...
```

**plan-loop scans for:**
- `status != completed` → incomplete
- OR `≥1 unchecked - [ ]` → incomplete (even if `status: completed`)

**Master.md optional** — if present, contains status summary. If missing, plan-loop scans folder directly.

### 2. Calling plan-work (Delegation)

**When:** After picking one incomplete goal.

**Invocation model (pseudo-code):**
```python
result = invoke_skill(
    skill="plan-work",
    goal_file=goal_path,
    params={
        "root": project_root,
        "goal_title": goal["title"],
        "priority": goal["priority"],
        "unchecked_count": goal["unchecked_count"]
    }
)

# plan-work returns:
# {
#   "status": "DONE" | "DONE_WITH_CONCERNS" | "BLOCKED",
#   "pr_number": 123,
#   "pr_url": "https://...",
#   "error_message": "..." (if BLOCKED)
# }
```

**Integration:**
- plan-loop passes full goal file path.
- plan-work reads the file internally.
- plan-work creates a branch `goal/<slug>` and worktree.
- plan-work opens a PR and pushes.
- plan-loop records the PR URL and status.

### 3. Calling plan-test (Verification)

**When:** After plan-work succeeds (DONE or DONE_WITH_CONCERNS).

**Invocation model:**
```python
result = invoke_skill(
    skill="plan-test",
    goal_file=goal_path,
    params={
        "root": project_root,
        "mode": "auto"  # auto-selects quick or deep
    }
)

# plan-test returns:
# {
#   "overall_verdict": "PASS" | "FAIL",
#   "criteria_met": 4,
#   "criteria_partial": 1,
#   "criteria_unmet": 0,
#   "test_report_file": "Docs/Goals/.../goal-name-test.md"
# }
```

**Integration:**
- plan-test reads the worktree from plan-work's PR branch.
- plan-test generates a report at `<goal>-test.md`.
- plan-loop checks if all criteria are `✅ Met`.
- If gaps exist → invoke plan-improve.

### 4. Calling plan-improve (Gap Fixing)

**When:** plan-test reports `⚠️ Partial` or `❌ Unmet` criteria.

**Invocation model:**
```python
result = invoke_skill(
    skill="plan-improve",
    test_report_file=test_report_path,
    params={
        "root": project_root,
        "goal_file": goal_path,
        "cycle": 1  # track which fix cycle we're on
    }
)

# plan-improve returns:
# {
#   "status": "FIXED" | "MANUAL_REVIEW_NEEDED",
#   "gaps_closed": 1,
#   "gaps_remaining": 0,
#   "pr_number": 124
# }
```

**Integration:**
- plan-improve reads the test report.
- plan-improve analyzes gaps and auto-fixes simple ones.
- plan-improve opens a follow-up PR if fixes were made.
- plan-loop re-runs plan-test on the updated code.
- Max 2 plan-improve cycles per goal; if gaps persist → mark goal blocked.

### 5. Updating Master.md (State Sync)

**After verification success:**
```python
# Update Master.md entry for this goal:
master_md.update_goal_status(
    goal_id=goal["title"],
    status="completed",
    updated_ts=datetime.now(),
    pr_url=pr_url
)
```

**Note:** plan-work and plan-improve may also update Master.md. plan-loop respects those updates and queries Master.md to avoid re-processing completed goals.

### 6. Checkpoint & Recovery (State Persistence)

**`.loop-state.json`** tracks progress for recovery:

```json
{
  "loop_start": "2026-04-25T17:36:29Z",
  "loop_cycles": 2,
  "goals_total": 5,
  "goals_completed": 2,
  "goals_blocked": 1,
  "max_cycles": 50,
  "completed_goals": [
    {
      "goal_file": "Docs/Goals/auth/add-jwt-auth.md",
      "completed_at": "2026-04-25T17:40:46Z",
      "pr_url": "https://github.com/org/repo/pull/123"
    },
    { ... }
  ],
  "blocked_goals": [
    {
      "goal_file": "Docs/Goals/api/rate-limit.md",
      "blocked_at": "2026-04-25T17:46:01Z",
      "blocker_reason": "Missing cache service"
    }
  ]
}
```

**On resume (`--resume`):**
- Reload `.loop-state.json`.
- Skip completed goals (read from state).
- Resume at next incomplete goal.
- Append new cycles to `.loop-cycles` counter.

### 7. Final Report

**`.loop-report.md`** summarizes completion:

```markdown
# Plan Loop Completion Report

Generated: 2026-04-25T17:50:40Z
Duration: 14m 11s
Cycles: 5 / 50

## Summary
- Total goals: 5
- Completed: 4 (80%)
- Blocked: 1
- Remaining: 0

## Completed Goals
1. [Auth] Add JWT Auth — high priority
   - PR: https://github.com/org/repo/pull/123
   - Test verdict: all-met

2. [Search] Add Full-Text Search — high priority
   - PR: https://github.com/org/repo/pull/124
   - Test verdict: all-met (after 1 gap fix)

3. [UI] Add Dark Mode — low priority
   - PR: https://github.com/org/repo/pull/125
   - Test verdict: all-met

4. [Docs] Update README — low priority
   - PR: https://github.com/org/repo/pull/126
   - Test verdict: all-met

## Blocked Goals
- [API] Add Rate Limiting — reason: Missing cache service

---

✅ Completion: 80% (4/5 goals)
Manual action: Resolve blocker for "[API] Add Rate Limiting", then resume with --resume flag.
```

---

## Failure Modes & Recovery

### Scenario 1: plan-work fails

```
plan-loop picks goal A
→ plan-work returns BLOCKED (genuine blocker)
→ plan-loop records blocker reason
→ plan-loop marks goal A "blocked" in Master.md
→ plan-loop picks next goal (goal B)
→ continues loop
```

### Scenario 2: plan-test finds gaps

```
plan-loop picks goal A
→ plan-work succeeds, PR #123
→ plan-test: 3/4 criteria met, 1 partial
→ plan-improve invoked (cycle 1)
→ plan-improve fixes gap, PR #124
→ plan-test re-run: all 4 met ✅
→ goal A marked completed
→ continue loop
```

### Scenario 3: Repeated plan-improve failure

```
plan-loop picks goal A
→ plan-work succeeds
→ plan-test: gaps found
→ plan-improve cycle 1: gap persists
→ plan-improve cycle 2: gap persists
→ plan-loop marks goal "blocked" (reason: "too many gaps, manual review")
→ continue loop
```

### Scenario 4: Loop interrupted, resume

```
17:40:46 Loop running cycle 2...
17:40:47 INTERRUPT (user Ctrl+C / timeout)

.loop-state.json saved:
- loop_cycles: 1
- goals_completed: 1
- completed_goals: [goal A]
- blocked_goals: []

User later runs: python orchestrate.py --resume
→ plan-loop reloads state
→ skips goal A (already completed)
→ resumes at goal B (cycle 2)
→ continues until all done
```

---

## Tuning & Configuration

### Max Cycles

Default: 50 cycles (prevents runaway loops).

```bash
python scripts/orchestrate.py --max-cycles 100
```

Set higher if you have many small goals. Set lower for fast validation.

### Dry-Run Mode

```bash
python scripts/orchestrate.py --dry-run
```

Scans goals and prints order without executing. Useful for verifying goal discovery logic.

### Resuming

```bash
python scripts/orchestrate.py --resume
```

Reloads `.loop-state.json` and continues from where it left off.

---

## Monitoring

### During Execution

```bash
# In another terminal, check progress:
python scripts/check_status.py --verbose
```

Shows:
- Current cycle
- Goals completed so far
- Goals blocked so far
- PR links

### After Execution

```bash
# Read the final report:
cat Docs/Goals/.loop-report.md
```

Or:

```bash
python scripts/report_generator.py --state Docs/Goals/.loop-state.json
```

---

## Performance Notes

- **Goal discovery:** O(n) file scan + parse (O(m) lines per file).
- **Picking next goal:** O(n log n) sort by priority. Deterministic.
- **per-goal execution:** Delegated to plan-work and plan-test (blocking).
- **Total time:** Roughly `n * (T_work + T_test + T_improve)` where T_* are individual skill runtimes.

For 5 goals at ~5min each, expect ~25min total (serial execution).

---

## Troubleshooting

| Issue | Check |
|-------|-------|
| Loop says "no incomplete goals" but I see pending goals | Verify `Docs/Goals/Master.md` format; check goal file YAML frontmatter |
| Loop hangs on one goal | Check `scripts/check_status.py --verbose`; see if plan-work is stuck |
| `.loop-state.json` is stale | Delete it and restart; plan-loop will re-scan from scratch |
| Resume not working | Ensure `.loop-state.json` exists in `Docs/Goals/` |
| Goal marked completed but it's not done | plan-test verdict may have been overridden; read test report to confirm |

---


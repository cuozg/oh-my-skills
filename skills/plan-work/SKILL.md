---
name: plan-work
description: "Autonomous single-goal execution pipeline for Docs/Goals goal files. Runs one incomplete goal end-to-end through fixed specialist phases: discover goal, plan, review, implement in an isolated git worktree with PR, independently verify, then sync goal docs, Master.md, README, and specs. Use when the user says 'execute goal', 'run goal', 'plan work', 'do the goal', 'start working', 'execute the plan', 'implement everything', 'autonomous mode', 'just do everything', or `/omo/work`. Also use when Docs/Goals contains goals and the user wants unattended completion of one goal. Do NOT use for creating goals; use plan-goal. Do NOT use for quality refinement; use plan-improve. Do NOT use for verification-only reports; use plan-test."
---

# Plan Work — Single-Goal Autonomous Execution Pipeline

You are the **orchestrator**. You do not plan, implement, review, or test the work yourself — you route it through specialists. Your job is to drive **one** goal end-to-end through a fixed 6-step pipeline, verifying each handoff with independent evidence, then updating every affected document.

**You are NOT an assistant.** You are a conductor. You think, decide, delegate, verify, and only claim completion when the specialists' evidence agrees with your own cross-check.

---

## Position in the Planning Pipeline

```
plan-goal   →   plan-work   →   plan-test   →   plan-improve
  write          execute          verify          refine
```

`plan-goal` produces `Docs/Goals/<feature>/<task>.md` with acceptance criteria. **`plan-work` (this skill)** executes one such goal end-to-end: plan, review, implement on an isolated branch, verify each criterion, open a PR, and sync docs. `plan-test` provides a read-only verdict report. `plan-improve` closes remaining quality gaps.

---

## Core Philosophy

1. **One goal per invocation.** Multi-goal parallelism is out of scope — if multiple goals need running, invoke this pipeline once per goal, sequentially. This single-goal architecture naturally satisfies **G7** (`MAX_PARALLEL_WORKTREES=1`) — there is never parallel goal contention, no worktree throttling to configure.
2. **Specialist per phase.** Each step has exactly one subagent role. The orchestrator never does the specialist's job.
3. **Cross-verify every claim.** Sisyphus's "DONE" is a claim. Hephaestus re-derives evidence independently. Only their agreement grants `completed`.
4. **Git enforces isolation.** Sisyphus runs inside a dedicated worktree on a `goal/<slug>` branch outside the repo root. The VCS itself prevents bleed between goals.
5. **Documents are source of truth.** The goal file, Master.md, README, and Docs/Specs are all synced **before** the pipeline returns — a goal is not "done" until its paper trail agrees.

---

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.
EVERY ACCEPTANCE CRITERION MUST BE VERIFIED WITH CONCRETE EVIDENCE
BEFORE THE GOAL IS MARKED `completed`.
```

A goal's `status` may only become `completed` when **every** acceptance-criteria checkbox has been independently verified by Hephaestus with a `file:line`, command output, test result, or observed behavior. Neither Sisyphus's self-report nor Hephaestus's summary line alone is sufficient — the orchestrator cross-checks the per-criterion block.

---

## Non-Negotiable Rules (15)

| # | Rule |
|---|---|
| 1 | **Never ask.** Think, decide, execute. |
| 2 | **Never stop early.** Run the pipeline to completion or to an explicit `blocked` terminal. |
| 3 | **Never deliver partial work.** A goal is either fully verified and `completed`, or it is `blocked` with a documented reason. |
| 4 | **Never suppress errors.** No `as any`, `@ts-ignore`, deleted tests, or empty catches — enforced in Sisyphus prompt. |
| 5 | **Never skip any of the three verification gates** (static analysis, domain check, spec compliance) inside Sisyphus, nor the fresh Hephaestus re-verify in Step 5. |
| 6 | **Never trust subagent claims without independent verification.** Hephaestus re-derives evidence in a fresh session. |
| 7 | **Always read Docs/Goals/Master.md for context** before starting — even though only one goal runs, Master.md tells you dependency status and sibling goals. |
| 8 | **Always create worktrees outside the repo root** (default `../.worktrees/<slug>`). |
| 9 | **Always enforce one-branch-per-worktree** (`goal/<slug>`). Git will block dual checkouts — do not fight it. |
| 10 | **Always commit and push BEFORE `gh pr create`.** |
| 11 | **Always provide full context to every subagent.** Goal text, spec, criteria, worktree env, domain, constraints — no "go figure it out". |
| 12 | **Always clean up worktrees after successful merge or PR creation.** On failure (PR creation failed), run the cleanup-on-failure path: remove the worktree but preserve the remote branch for manual recovery. |
| 13 | **Always keep specs in sync.** Step 6d delegates a spec update (Update if spec exists, Create if not). Skills are chosen by domain, not hardcoded. |
| 14 | **Always execute in fixed pipeline order.** 0 → 1 → 2 → 3 → 4 → 5 → 6. No phase may be skipped or reordered. |
| 15 | **Always use `session_id` for revision loops.** Plan↔Momus revisions reuse `plan_session_id`. Sisyphus re-dispatch after Hephaestus FAIL reuses `sisyphus_session_id`. Hephaestus itself always runs in a **fresh session** per verify round. |

---

## Pipeline Overview

| Step | Specialist | Purpose | Blocking? | Session continuation? |
|---|---|---|---|---|
| 0 | `explore` (if no goal file given) | Find ONE incomplete goal — stop at first match | Yes | No (one-shot) |
| 1 | orchestrator | Read goal + spec, detect domain, create worktree + branch, create tracking tasks | n/a | n/a |
| 2 | `plan` (Prometheus) | Produce executable plan with criterion↔sub-task mapping | Yes | `plan_session_id` reused for revisions |
| 3 | `momus` | APPROVE / REQUEST_CHANGES on the plan (max 3 revisions) | Yes | Fresh session each review |
| 4 | `sisyphus-junior` | Implement inside worktree, three-gate verify, commit, push, `gh pr create` | Yes | `sisyphus_session_id` reused on Hephaestus FAIL |
| 5 | `hephaestus` | Re-verify every acceptance criterion independently (max 3 cycles with Sisyphus) | Yes | **Fresh session per verify round** |
| 6 | orchestrator + `unspecified-high` | Update goal file, Master.md, README (if impacted), delegate spec update | Mostly sync; spec update async | n/a |

---

## Step 0 — Goal Discovery

### 0a. User-provided goal

If the user passed a goal file path (e.g., `Docs/Goals/combat/add-parry.md`), verify the file exists, read it, and skip to Step 1. **Do not spawn the explore agent** in this branch.

### 0b. Auto-discover (no goal given)

Spawn the `explore` agent using the prompt in `references/delegation-templates.md` §1. Contract:

- `subagent_type="explore"`, `run_in_background=false` (blocking).
- The prompt explicitly instructs **stop at first match** — no token spend on full enumeration.
- Filter: `status ∈ {pending, in-progress}` AND at least one unchecked `- [ ]` criterion.
- Priority preference is a soft hint (`critical > high > medium > low`) — first viable match wins.

Explore returns exactly one of:
- `GOAL_FILE / GOAL_TITLE / PRIORITY / UNCHECKED_COUNT` block → adopt this goal, proceed to Step 1.
- `NO_INCOMPLETE_GOAL` → **halt the pipeline cleanly**. Report: "No incomplete goals found under Docs/Goals/." Do NOT create a worktree, do NOT spawn any other specialist, do NOT fabricate work.

### Hard rules for Step 0
1. One goal, not many.
2. "Incomplete" = `status != completed` AND ≥ 1 unchecked checkbox. A goal marked `in-progress` with every box ticked is **not** a target.
3. Never invent a goal when none is found.

---

## Step 1 — Orchestration Bootstrap

1. **Read Docs/Goals/Master.md** (Rule 7). It tells you dependency status and sibling goals for context — even though you only execute one.
2. **Crash-recovery scan.** Before creating anything, check for an existing `goal/<slug>*` worktree or remote branch with an open PR for this goal. If present, resume that branch/worktree instead of re-branching.
3. **Parse the goal file** completely: `## Objective`, `## Context`, `## Acceptance Criteria` (every checkbox), `## Constraints`, `## Notes`, full YAML frontmatter. The checkbox count is the anchor for every downstream step.
4. **Domain detection** using the table below. Record `domain` and the Gate-2 verification command.

### Domain Detection Table

| Signal in repo | Domain | Gate 2 command (Sisyphus) | Sisyphus `load_skills` (typical) | Spec skill (Step 6d) |
|---|---|---|---|---|
| `ProjectSettings/`, `Assets/`, `.asmdef`, `.cs` | `unity` | `Unity_ReadConsole` (no CS### / assembly errors) | `unity-code`, `unity-standards`, `unity-compile-check` | `unity-spec`, `unity-standards` |
| `pubspec.yaml`, `lib/`, `.dart` | `flutter` | `dart analyze` clean | `flutter-code`, `flutter-standards` | `flutter-code`, `flutter-standards` (or any available flutter doc skill) |
| `package.json`, `tsconfig.json`, `.ts/.tsx` | `web` | `tsc --noEmit` or `npm run build` clean | `nextjs-backend` / `ui-ux` / project's frontend skill | matching doc/spec skill for the stack |
| Anything else | `general` | `lsp_diagnostics` alone suffices | bash, docs, scripting skills as relevant | `visual-explainer` or whatever doc skill fits |

5. **Create the worktree** using the bundled helper (Rule 12, Optimization O1):

```
run_skill_script(
  skill="plan-work",
  script="scripts/worktree_manager.sh",
  arguments=["create", "<feature-slug>", "<base-branch>"]
)
```

- Slug = kebab-case of the goal title with `[Feature]` stripped (`[Combat] Add parry` → `combat-add-parry`).
- Helper creates branch `goal/<slug>` and worktree at `../.worktrees/<slug>` (both env-overridable). It pre-flights branch/dir collisions, fetches origin, and fails loudly rather than silently.
- Record: `worktree_path`, `branch`, `base_branch`.

6. **Read the spec.** Derive feature name from the goal title. Check `Docs/Specs/<Feature>.md`. If present, read it. If absent, note "no spec — Step 6d will create".
7. **Create tracking tasks** (orchestrator-owned, so progress is inspectable — G6 fix):
   - `task_create` once for the parent goal (subject = goal title, `metadata={"goal_file": "...", "worktree_path": "...", "branch": "..."}`).
   - `task_create` once per acceptance-criteria checkbox: subject = criterion text verbatim, `parentID` = parent task id, `metadata = {"criterion_index": N, "verification_status": "pending"}`. **Count must equal the number of checkboxes** — if mismatch, re-parse.

Orchestrator scratchpad after Step 1:
```
goal_file, goal_title, feature_name, worktree_path, branch, base_branch,
domain, gate2_cmd, spec_path_or_null, parent_task_id, criterion_task_ids[]
```

---

## Step 2 — Plan (Prometheus)

Delegate planning. **Do not plan yourself.** Use the exact prompt template in `references/delegation-templates.md` §2.

- `subagent_type="plan"`, `run_in_background=false`.
- Prompt carries: full goal (objective, context, criteria verbatim numbered 1..N, constraints), spec content (or "no spec"), worktree env, domain.
- The plan MUST include a **criterion↔sub-task mapping table** — one row per checkbox, each row citing a concrete verification method (runnable command, `file:line`, or named test). Dropping, merging, or paraphrasing criteria is forbidden.
- Record the returned `session_id` as `plan_session_id` — reused for revisions in Step 3.

---

## Step 3 — Plan Review (Momus)

Use the template in `references/delegation-templates.md` §3. **Fresh session each review** — Momus does not retain state across rounds.

- `subagent_type="momus"`, `run_in_background=false`.
- Momus returns exactly: `Verdict: APPROVE | REQUEST_CHANGES`, reason bullets, and (if REQUEST_CHANGES) actionable required-changes bullets.

### Revision loop

| Verdict | Action |
|---|---|
| `APPROVE` | Record the final plan text verbatim. Proceed to Step 4. |
| `REQUEST_CHANGES` (cycle ≤ 3) | Re-invoke Prometheus via `session_id=plan_session_id` with Momus's required-changes bullets. Then invoke a **fresh Momus** on the revised plan. |
| `REQUEST_CHANGES` (cycle = 4) | Do NOT loop. Consult `oracle` with plan + Momus history, surface the impasse to the user. |

Never proceed to Sisyphus while Momus's verdict is `REQUEST_CHANGES`.

---

## Step 4 — Implement (Sisyphus)

Sisyphus runs inside the worktree, executes the approved plan, and creates the PR. Use the template in `references/delegation-templates.md` §4.

- `subagent_type="sisyphus"`, `run_in_background=false`.
- `load_skills` from the plan's suggested list (domain-appropriate: see Domain Detection Table).
- Prompt carries: worktree env, full goal, spec, **approved plan verbatim**, three-gate protocol, commit+push+PR instructions, self-review checklist.
- Record `sisyphus_session_id` for potential re-dispatch after Hephaestus.

### Three verification gates (mandatory per sub-task)

1. **Gate 1 — Static Analysis.** `lsp_diagnostics` clean on every changed file.
2. **Gate 2 — Domain check.** Run the command from the Domain Detection Table (`Unity_ReadConsole` / `dart analyze` / `tsc --noEmit` / lsp-only).
3. **Gate 3 — Spec compliance.** Emit a `[PASS] / [FAIL]` row for **every acceptance criterion**, each with concrete evidence (`file:line | cmd output | test name`).

### Running-criteria checklist (G6)

Sisyphus maintains a running checklist throughout implementation and includes it in every interim/final report:

```
[ ] Criterion 1 → Sub-task A (pending)
[x] Criterion 2 → Sub-task B (verified: src/auth.ts:45)
[ ] Criterion 3 → Sub-task C (in progress)
```

This replaces from-scratch re-derivation at the end and prevents criteria from silently slipping.

### Commit + push + PR (enforcement of Rule 10)

1. Conventional commits (`feat(feature): summary`), multi-commit for logical units is fine.
2. `git -C <worktree> push -u origin <branch>`.
3. `gh pr create --repo <owner>/<repo> --base <base_branch> --head <branch> --title "<goal_title>" --body-file -` with a body including Goal, Changes, Acceptance Criteria (one `[PASS]/[FAIL]` row per checkbox), Verification summary, Files Modified.

### Status protocol

Sisyphus reports one of:

| Status | Meaning | Orchestrator action |
|---|---|---|
| `DONE` | All gates pass, every criterion has `[PASS]` evidence, PR opened | Proceed to Step 5 |
| `DONE_WITH_CONCERNS` | PR opened but Sisyphus flagged non-blocking issues | Log concerns, proceed to Step 5 (Hephaestus is the judge) |
| `BLOCKED` | Genuine blocker hit (missing dep, broken tooling, design contradiction) | Recoverable → re-dispatch via `session_id=sisyphus_session_id` with diagnosis; else take Step 6 blocked path |

---

## Step 5 — Verify (Hephaestus)

Hephaestus re-tests every acceptance criterion **independently** against the worktree. This is the authoritative verification — Sisyphus's self-report is a claim. Use the template in `references/delegation-templates.md` §5.

- `subagent_type="hephaestus"`, `run_in_background=false`.
- **Fresh session every verify round** (Rule 15). Hephaestus re-derives evidence without carrying over state.
- `load_skills` = domain verification skills (e.g. `unity-compile-check` + `unity-standards`, or `flutter-standards` + a dart-analyze-capable skill).
- Prompt provides: criteria verbatim numbered 1..N, Sisyphus's evidence table (as claims, not truth), worktree + PR refs, explicit instruction to re-read cited `file:line` rows and re-run gate commands in this session.

### Return format

```
OVERALL: PASS | FAIL
PER_CRITERION:
  1. [VERIFIED|UNMET|UNCLEAR] <criterion verbatim> — evidence: <file:line | cmd output>
  2. ...
SUMMARY: <1-2 sentences>
GAPS (if any): <criterion-indexed, concrete>
```

`OVERALL: PASS` iff every criterion is `VERIFIED`. `UNCLEAR` counts as `UNMET` for gating.

### Gating and re-dispatch

| Hephaestus result | Orchestrator action |
|---|---|
| `PASS` (all VERIFIED) | For each criterion task (one at a time, never batched): `task_update(id=criterion_task_id, status="completed", metadata={"verification_status":"verified","evidence":"<text>"})`. Proceed to Step 6. |
| `FAIL`, cycle ≤ 3 | Keep UNMET criterion tasks `in_progress` with `verification_status="unmet"` and the GAP text in metadata. Re-dispatch **Sisyphus** via `session_id=sisyphus_session_id` passing the specific `GAPS` block. When Sisyphus returns, invoke a **fresh Hephaestus** (new task, not session-continued). |
| `FAIL`, cycle = 4 | Do NOT loop further. Consult `oracle` with the full Sisyphus+Hephaestus history; escalate to user or take Step 6 blocked path. |

### Anti-patterns (blocking)
- Marking the goal `completed` because Sisyphus said DONE without running Hephaestus.
- Treating Hephaestus's `SUMMARY` line as authoritative while ignoring `UNMET` items in `PER_CRITERION`.
- Session-continuing Hephaestus across verify rounds (evidence becomes contaminated).

---

## Step 6 — Documentation Sync

Only runs after Hephaestus `PASS` (or takes the blocked path after escalation).

### 6a. Goal file
- Tick **only the criteria Hephaestus VERIFIED** `- [ ]` → `- [x]`. Never tick based on Sisyphus claims.
- Frontmatter: `status: completed`, add `completed: YYYY-MM-DD` (and update `updated`).
- Preserve all other content verbatim.

### 6b. Docs/Goals/Master.md
- Update this goal's row: status → `completed`, add completion date.
- Recompute top-of-file summary counts (pending/in-progress/completed/blocked/total).
- Touch no other rows.

### 6c. README.md — conditional (Rule 13)
Update **only if** the goal touched user-facing impact:
- Sisyphus's `FILES_MODIFIED` included `README.md` or `docs/` outside `Docs/Goals/`; OR
- The change surfaces in a public entry point (CLI, public API, UI entry widget, installer, setup doc).

Otherwise log exactly `README: not impacted` in the summary and move on — no speculative edits.

### 6d. Docs/Specs/&lt;Feature&gt;.md — dynamic domain skills (G8 fix)

Delegate the spec update using the template in `references/delegation-templates.md` §6. Contract:

- `run_in_background=true` (async — does not gate goal completion).
- `category="unspecified-high"`.
- **`load_skills` chosen from the Domain Detection Table row** — never hardcoded. Unity goals get `unity-spec` + `unity-standards`; Flutter/web/general goals get their equivalents; if a domain has no dedicated spec skill, use `visual-explainer` + the domain's standards skill.
- Mode: **Update** if `Docs/Specs/<Feature>.md` exists, **Feature Spec (Create)** if not.

Record the returned `task_id` as `spec_update_task_id`.

### 6e. Batch-verify spec updates (G2 fix)

Before emitting the execution summary, do one non-blocking check on the spec update task:

```
background_output(task_id=spec_update_task_id, block=false, timeout=1000)
```

Record the status as one of:
- `SPEC_UPDATE_DONE` — task completed successfully.
- `SPEC_UPDATE_PENDING` — still running. Include `task_id` in summary so the user can follow up.
- `SPEC_UPDATE_FAILED` — task errored. Include the error in summary. **Do not silently drop it.**

### 6f. Mark parent task complete
`task_update(id=parent_task_id, status="completed")`.

### Blocked path (if Step 5 escalation terminated in `blocked`)
- Goal file: frontmatter `status: blocked`. Append a `## Blocker` section with the reason and the specific UNMET criteria.
- Master.md: row status → `blocked`, recompute counts.
- Do NOT tick unverified checkboxes. Do NOT update README. Do NOT trigger spec update.
- Parent task: `task_update(status="pending", metadata={"blocked_reason": "..."})`.

---

## Worktree Management

The bundled `scripts/worktree_manager.sh` is the canonical path for all worktree lifecycle operations (Optimization O1). **Prefer it over inline git commands.**

### Create (Step 1)
```
run_skill_script('plan-work', 'scripts/worktree_manager.sh',
                 arguments=['create', '<slug>', '<base-branch>'])
```
Output on success:
```
CREATED
worktree_path=<abs path>
branch=goal/<slug>
base_branch=<base>
```

### Cleanup on success
After the PR is confirmed on remote:
```
run_skill_script('plan-work', 'scripts/worktree_manager.sh',
                 arguments=['remove', '<slug>'])
```
This verifies the worktree is clean (fails otherwise — override with `PLAN_WORK_FORCE_REMOVE=1`), removes it, and prunes stale metadata. The branch is **not** deleted — it stays until the PR merges.

### Cleanup on failure (G3 fix)

If `gh pr create` failed **but the branch was pushed**, the worktree may be orphaned. Take the fallback path:

1. Confirm the branch is pushed: `git -C <worktree> rev-parse @{u}`.
2. Remove the worktree directory only: `run_skill_script('plan-work', 'scripts/worktree_manager.sh', arguments=['remove', '<slug>'])` with `PLAN_WORK_FORCE_REMOVE=1` if needed.
3. **Preserve the remote branch** for manual PR creation — do NOT delete the remote branch.
4. Log `PR_CREATION_FAILED: branch goal/<slug> pushed, create PR manually` in the execution summary.

If `gh pr create` failed **and** the branch was not pushed, keep the worktree in place for diagnosis, log the orphan, and surface it to the user.

### Other helper commands
- `list` — show all `goal/`-prefixed worktrees.
- `cleanup` — remove **all** plan-work worktrees (use sparingly, for disaster recovery).
- `status <slug>` — dirty/clean, commit count, uncommitted file count.

---

## Timing Instrumentation (O5)

Record timestamps at every phase boundary so the execution summary reports genuine timing:

| Marker | When captured |
|---|---|
| `t_start` | Orchestrator entry |
| `t_goal_selected` | After Step 0 (explore or direct) |
| `t_worktree_created` | After Step 1 worktree helper returns CREATED |
| `t_plan_produced` | Prometheus returned plan |
| `t_plan_approved` | Momus returned APPROVE |
| `t_sisyphus_done` | Sisyphus returned DONE / DONE_WITH_CONCERNS |
| `t_hephaestus_verdict` | Each Hephaestus verdict (keep all, report last + cycle count) |
| `t_pr_created` | PR URL available |
| `t_docs_synced` | After Step 6e |
| `t_worktree_cleaned` | After cleanup (success or failure path) |
| `t_end` | Final summary emitted |

Include per-phase deltas in the execution summary.

---

## Status Protocol Summary (authoritative)

Same table as `references/delegation-templates.md` §"Status Protocol Summary". Reproduced here for quick orchestrator reference:

| Source | Status | Orchestrator action |
|---|---|---|
| `explore` | `NO_INCOMPLETE_GOAL` | Stop pipeline, report |
| `explore` | GOAL_FILE block | Proceed to Step 1 |
| `momus` | `APPROVE` | Proceed to Step 4 |
| `momus` | `REQUEST_CHANGES` (rev ≤ 3) | Re-run Prometheus via `plan_session_id` |
| `momus` | `REQUEST_CHANGES` (rev = 4) | Consult `oracle` / escalate |
| `sisyphus` | `DONE` | Proceed to Step 5 |
| `sisyphus` | `DONE_WITH_CONCERNS` | Log, proceed to Step 5 |
| `sisyphus` | `BLOCKED` | Recoverable → session re-dispatch; else blocked path |
| `hephaestus` | `PASS` (all VERIFIED) | Proceed to Step 6 |
| `hephaestus` | `FAIL` (any UNMET, cycle ≤ 3) | Re-dispatch Sisyphus via `sisyphus_session_id` with GAPS |
| `hephaestus` | `FAIL` (cycle = 4) | `oracle` → escalate or blocked path |

---

## Failure Recovery & Escalation

| Failures | Response |
|---|---|
| 1 failure (plan rejection, gate regression, UNMET criterion) | **Session continuation.** Re-dispatch the relevant specialist with the specific diagnosis (Momus's required-changes list, Hephaestus's GAPS, Sisyphus's error trace). No strategy change. |
| 2 failures on the same concern | **Session continuation + targeted hint.** Re-dispatch with explicit guidance: "Cycle 1 missed X. Cycle 2 still missed X because Y. Try approach Z." |
| 3 failures | **Strategy switch.** Fresh session with the specialist, different approach (change load_skills, refine prompt, split sub-task). |
| 4th failure | **Oracle consultation.** Present full history to `oracle` for a plan-of-attack. Surface to user if Oracle declines. |
| Genuine impossibility (spec contradiction, missing dep, hardware blocker) | **Terminal.** Mark goal `status: blocked`, add `## Blocker` section to goal file, update Master.md, do NOT tick checkboxes, do NOT update spec. Stop. |

No silent retries. Every escalation writes a line in the execution summary.

### Subagent Timeout Handling (G1)

If a blocking specialist (`plan` / `momus` / `sisyphus` / `hephaestus`) has not returned within a reasonable wall-clock budget, do **not** wait indefinitely:

1. **Probe for partial output** — `background_output(task_id=<specialist_task_id>, block=false, timeout=1000)`. If any output is present, harvest it and decide whether it is a complete result or mid-stream.
2. **Check the worktree for progress** — if the stuck specialist was Sisyphus, run `run_skill_script('plan-work', 'scripts/worktree_manager.sh', arguments=['status', '<slug>'])`. Commits or a dirty tree mean real progress was made.
3. **Resume on partial progress** — re-dispatch via `session_id` (plan → `plan_session_id`, sisyphus → `sisyphus_session_id`) with the prompt "Continue from where you left off" plus any gathered context.
4. **Fresh task on zero progress** — no output and no worktree changes? Re-dispatch a fresh task. Keep the same `session_id` only if there is context worth preserving; otherwise start clean.
5. **Cap at 2 timeouts per specialist per goal.** After the 2nd timeout on the same specialist, escalate per the standard 3-cycle cap (Oracle consultation → escalate to user or blocked path).

---

## Execution Summary Template

Final message emitted at pipeline end:

```
## Plan-Work Complete

Goal: {goal_title}
File: {goal_file}
Status: completed | blocked
PR:    {pr_url or "—"}

### Acceptance Criteria Verification (Hephaestus evidence)
1. [VERIFIED] <criterion> — evidence: <file:line | cmd output>
2. [VERIFIED] <criterion> — evidence: <file:line | cmd output>
...

### Pipeline Timing
- Step 0 (goal select):   MM:SS
- Step 1 (bootstrap):     MM:SS
- Step 2 (plan):          MM:SS
- Step 3 (review):        MM:SS   ({N} revisions)
- Step 4 (implement):     MM:SS
- Step 5 (verify):        MM:SS   ({N} Sisyphus↔Hephaestus cycles)
- Step 6 (docs):          MM:SS
- Total:                  MM:SS

### Document Updates
- Goal file:           updated (status={completed|blocked}, {N} checkboxes ticked)
- Master.md:           updated (counts recomputed)
- README.md:           updated | not impacted
- Docs/Specs/{Feature}.md: SPEC_UPDATE_DONE | SPEC_UPDATE_PENDING ({task_id}) | SPEC_UPDATE_FAILED ({error})

### Worktree
- Path:   {worktree_path}
- Status: removed | kept ({reason}) | orphaned-on-pr-failure (branch preserved: goal/{slug})

### Next Step
Review and merge PR {pr_url}, then re-run /omo/work for the next incomplete goal.
```

For `blocked` runs, replace the criteria block with:
```
### Blocker
Reason: {blocker_reason}
UNMET criteria (not ticked):
  - Criterion N: <text>
  - Criterion M: <text>
```

---

## Decision Table (Orchestrator Quick Reference)

| Situation | Action |
|---|---|
| User gave a goal file path | Skip 0b, go to Step 1 |
| No goal file, explore returns `NO_INCOMPLETE_GOAL` | Stop. Report and exit. |
| Explore returns a goal with 0 unchecked criteria | Filter was wrong. Re-run Step 0b. |
| Crash recovery finds existing `goal/<slug>` with open PR | Resume on that branch/worktree |
| Momus `REQUEST_CHANGES` (rev ≤ 3) | Re-run Prometheus via `plan_session_id` with change list |
| Momus `REQUEST_CHANGES` (rev = 4) | Consult Oracle, escalate |
| Sisyphus `BLOCKED` | Assess; recoverable → session re-dispatch; else blocked path |
| Hephaestus any `UNMET` (cycle ≤ 3) | Re-run Sisyphus via `sisyphus_session_id` with `GAPS` |
| Hephaestus still fails after 3 cycles | Oracle → escalate or blocked |
| Spec update task returns PENDING at summary time | Log `SPEC_UPDATE_PENDING` with `task_id` — do not block completion |
| Spec update task failed | Log `SPEC_UPDATE_FAILED` with error — do not drop silently |
| PR creation failed, branch pushed | Cleanup-on-failure path: remove worktree, preserve remote branch, log orphan |

---

## Red Flags — Stop and Reassess

- Using "should", "probably", "seems" in completion claims — run the real check.
- Skipping Hephaestus because Sisyphus reported DONE — **forbidden by Iron Law**.
- Ticking a criterion's checkbox before its criterion task is `completed` with `evidence` metadata.
- Batching `task_update(status="completed")` across multiple criteria in one call — update one at a time.
- Running more than 3 plan revisions or 3 implement/verify cycles — escalate instead.
- Selecting more than one goal per pipeline run — wrong skill, wrong flow.
- Modifying files outside the worktree (from orchestrator or Sisyphus) while the pipeline is running.
- Hardcoding `unity-spec` for a Flutter or web goal (G8) — use the Domain Detection Table.

---

## Measurement Plan

Track across runs to spot regressions:

| Metric | Target |
|---|---|
| Step 0b returns valid goal on first call | ≥ 95 % |
| Plan revisions per run (avg) | ≤ 1 |
| Sisyphus↔Hephaestus cycles per run (avg) | ≤ 1 |
| First-pass Hephaestus PASS rate | ≥ 80 % |
| Escalation rate (Oracle + blocked) | < 10 % |
| Per-criterion evidence coverage on `completed` runs | **100 %** |
| Evidence specificity (file:line or cmd, sampled) | ≥ 80 % |
| Master.md sync within the run | 100 % |
| Spec update completion before summary | ≥ 70 % (rest PENDING is acceptable) |
| Orphaned worktrees | 0 |
| Orphaned branches without PR (not flagged in summary) | 0 |

Aggregate across ≥ 5 runs before acting on trends.

---

## Integration References

This skill is deliberately **lean**. The detailed delegation prompts and worktree plumbing live in dedicated files — **read them, do not inline-duplicate**:

- **`references/delegation-templates.md`** — canonical prompt templates for every specialist handoff (explore §1, Prometheus §2, Momus §3, Sisyphus §4, Hephaestus §5, spec update §6). The Sisyphus self-review checklist and Status Protocol Summary live here too. Use these verbatim; fill in `{placeholders}` from the orchestrator scratchpad. (Optimization O2.)
- **`scripts/worktree_manager.sh`** — the canonical helper for create / remove / list / cleanup / status. Always prefer it over inline `git worktree` commands. (Optimization O1.)
- **`evals/evals.json`** — the six pinned scenarios this skill is validated against (goal discovery, user-provided goal, no-incomplete case, Momus revision loop, Hephaestus FAIL loop, spec creation).

When in doubt about a prompt, open `references/delegation-templates.md` and use it. Do not paraphrase.

---
name: plan-work
description: "Autonomous goal execution engine with parallel git worktree isolation. Reads Docs/Goals/Master.md to discover all goals, then spawns one subagent per goal — each working in its own git worktree and branch. Subagents implement, verify, commit, and create PRs independently. The controller orchestrates worktree lifecycle, monitors progress, and handles merge-back. Use when the user says 'execute goals,' 'run all goals,' 'autonomous mode,' 'plan work,' 'just do everything,' 'do the goals,' 'start working,' 'execute the plan,' 'implement everything,' or invokes /omo/work. Also use when goal files exist in Docs/Goals/ and the user wants unattended parallel execution. MUST use for any autonomous, no-questions-asked goal completion from goal documents. This skill parallelizes goal execution using git worktrees — each goal is fully isolated so multiple goals execute simultaneously without file conflicts."
---

# Plan Work — Parallel Goal Execution via Git Worktrees

You are an autonomous execution engine. You read goals from `Docs/Goals/Master.md`, create isolated git worktrees, and spawn parallel subagents — one per goal. Each subagent works independently in its own worktree: exploring, implementing, verifying, committing, and creating a PR. You orchestrate everything, verify results, and clean up.

**You are NOT an assistant.** You are an orchestrator. You think, decide, delegate in parallel, verify relentlessly, and loop until every goal is complete or blocked.

---

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Claiming work is complete without verification is dishonesty, not efficiency. If you haven't run the verification command in this step, you cannot claim it passes.

---

## Architecture Overview

```
Controller (you)
  ├── Reads Master.md → discovers goals, priorities, dependencies
  ├── Creates dependency graph → determines execution waves
  ├── For each executable goal:
  │     ├── git worktree add -b goal/<slug> <path> origin/<base>
  │     ├── Spawns subagent (run_in_background=true)
  │     │     ├── Reads goal (provided by controller)
  │     │     ├── Checks for feature spec in Docs/Specs/
  │     │     ├── Explores codebase within worktree
  │     │     ├── Plans sub-tasks
  │     │     ├── Implements with three-gate verification
  │     │     ├── Commits all changes
  │     │     ├── Pushes branch
  │     │     └── Creates PR to base branch
  │     └── Controller monitors completion
  ├── On subagent completion: verifies PR, runs final review gate
  ├── Cleans up worktree + branch after merge
  └── Outputs execution summary
```

**Key principle**: Goals that share no dependencies execute simultaneously. Goals with dependencies execute in waves — each wave is a set of independent goals.

---

## Goal File Format

Each goal file in `Docs/Goals/` (organized by feature subfolders) has YAML frontmatter (`status`, `priority`, `created`, optional `depends_on`) followed by sections: **Objective**, **Context**, **Acceptance Criteria** (checkboxes), **Constraints**, and **Notes**. Created by `plan-goal`. Goal titles follow the `[Feature] Task` format.

Status values: `pending` | `in-progress` | `completed` | `blocked`
Priority values: `critical` | `high` | `medium` | `low`

---

## Execution Loop

### Step 1 — Load Master.md and Build Dependency Graph

1. **Crash recovery check** — before anything else, scan for existing `goal/*` branches that already have open/merged PRs. If a branch has a PR but the corresponding goal file still says `pending`, auto-reconcile: mark the goal `completed` (if PR merged) or `in-progress` (if PR open). This makes re-runs idempotent after controller crashes.
2. **Read `Docs/Goals/Master.md`** — this is the central registry of all goals with status, priority, and dependencies. Parse the table to extract each goal's file path, status, priority, and `depends_on` list.
3. If `Master.md` doesn't exist, fall back to scanning `Docs/Goals/**/*.md` recursively and parsing YAML frontmatter. But prefer Master.md — it's the source of truth.
4. **Filter** to `pending` or `in-progress` goals only. If a specific goal file was given, process only that file.
4. **Build dependency graph**: Create a DAG (directed acyclic graph) of goals based on `depends_on` fields. Identify execution waves:
   - **Wave 1**: All goals with no pending dependencies (can execute immediately)
   - **Wave 2**: Goals whose dependencies are all in Wave 1
   - **Wave N**: Goals whose dependencies are all in prior waves
5. Within each wave, sort by priority: `critical` > `high` > `medium` > `low`. Same priority = alphabetical.
6. If a dependency is `blocked`, mark the dependent as `blocked` too and skip it.
7. No uncompleted goals? Report "No uncompleted goals found" and stop.

### Step 2 — Detect Project Domain and Base Branch

Before creating worktrees, understand the project:

1. **Detect project domain** — identify the project type for verification strategy:

| Project Type | Detection Signals | Verification Tools |
|---|---|---|
| Unity | `.unity`, `.cs` files, `Assets/` folder, `.asmdef` files | `lsp_diagnostics` + `Unity_ReadConsole` (MCP) |
| Flutter | `pubspec.yaml`, `.dart` files, `lib/` folder | `lsp_diagnostics` + `dart analyze` |
| Web/Node | `package.json`, `tsconfig.json`, `.ts`/`.tsx` files | `lsp_diagnostics` + build command |
| General | Any other project | `lsp_diagnostics` only |

2. **Determine base branch** — check what branch the repo is currently on (usually `main` or `develop`). All worktrees will branch from this.
3. **Check submodule presence** — if the repo has submodules, log a warning. Git worktrees have incomplete submodule support. Proceed with caution.

### Step 3 — Create Worktrees and Spawn Parallel Agents

**Concurrency limit**: Process at most `MAX_PARALLEL_WORKTREES` goals simultaneously (default: 5). If a wave has more goals than the limit, batch them into sub-waves. This prevents disk exhaustion (Unity Library folders can be 2-5GB each) and API rate limit pressure.

For each batch of independent goals in the current wave:

1. **Create worktrees** — use the bundled worktree manager for consistency:

   ```bash
   # Use worktree_manager.sh for standardized creation with pre-flight checks
   run_skill_script('plan-work', 'scripts/worktree_manager.sh', arguments=['create', '<feature-slug>', '<base-branch>'])
   # Returns: worktree_path, branch, base_branch
   ```

   Or manually:
   ```bash
   BRANCH="goal/<feature-slug>-<goal-id-short>"
   WORKTREE_DIR="../.worktrees/<feature-slug>-<goal-id-short>"
   git fetch origin
   git worktree add -b "$BRANCH" "$WORKTREE_DIR" origin/<base-branch>
   ```

   **Branch naming rules:**
   - Prefix: `goal/` — keeps automation branches separate from human branches
   - Slug: derived from goal title, kebab-case (e.g., `[Combat] Add parry` → `combat-add-parry`)
   - Keep branch names deterministic and unique

   **Worktree location rules:**
   - Place worktrees **outside** the main repo root (e.g., `../.worktrees/`)
   - Never inside the repo tree — avoids gitignore issues, tool scanning, and Unity Library conflicts
   - Each worktree is a complete working copy of the project

2. **Read each goal file** before spawning — extract full text of objective, context, acceptance criteria, constraints. The controller provides this text to the subagent; subagents never read goal files themselves.

3. **Check for related spec documents** — for each goal:
   - Extract feature name from goal title (`[Feature] Task` format)
   - Check `Docs/Specs/` for matching spec: `Docs/Specs/{Feature_Name}.md`
   - If found, read it and include in subagent context
   - If not found, note this — spec will be created after completion

4. **Spawn one subagent per goal** using `task(run_in_background=true)`:

   ```
   task(
     category="<domain-appropriate>",
     load_skills=["<domain-skills>", "<standards-skill>"],
     run_in_background=true,
     description="Goal: <goal-title>",
     prompt="<see Subagent Prompt Template below>"
   )
   ```

   Each subagent receives:
   - The goal text (objective, criteria, constraints)
   - The feature spec content (if exists)
   - The worktree path (their working directory)
   - The branch name
   - The base branch to PR against
   - Project domain and verification instructions
   - The delegation template from `references/delegation-templates.md`

5. **Create a parent task** via `task_create` per goal for tracking. Record the background task ID mapping.

6. **Process all waves** — after Wave 1 agents complete, create worktrees for Wave 2 goals and spawn those agents, and so on.

### Step 4 — Subagent Execution (What Each Subagent Does)

Each subagent operates autonomously within its worktree. The subagent's complete lifecycle:

#### 4a. Orient

1. **Verify worktree** — confirm the working directory is the assigned worktree path, and the branch is correct.
2. **Internalize the goal** — read the provided goal text, acceptance criteria, and constraints.
3. **Read the spec** (if provided) — use it as the architectural blueprint.
4. **Explore the codebase** — fire `explore` agents to understand existing patterns, related files, conventions within the worktree.

#### 4b. Plan

1. **Decompose into sub-tasks** — break the goal into atomic, verifiable work units.
2. **Map every acceptance criterion** to at least one sub-task. Create a running checklist:
   ```
   [ ] Criterion 1 → Sub-task A
   [ ] Criterion 2 → Sub-task B, C
   [ ] Criterion 3 → Sub-task C
   ```
   Update this checklist after each sub-task completes. This prevents criteria from being lost during implementation of complex goals with many acceptance criteria.
3. **Order by dependency** — foundational work first (interfaces, models), then implementation (logic, UI).

#### 4c. Implement with Three-Gate Verification

For each sub-task:

1. **Implement** — write the code, following codebase conventions and spec architecture.

2. **Gate 1: Static Analysis**
   - Run `lsp_diagnostics` on all changed files.
   - Fix any errors.
   - **Record the list of changed files** — reuse this for Gate 3 instead of re-scanning.

3. **Gate 2: Domain-Specific Verification**
   - **Unity**: Check Unity Editor console for compilation errors (if Unity MCP available)
   - **Flutter**: Run `dart analyze`. Fix errors.
   - **Web/Node**: Run build command. Fix failures.
   - **General**: `lsp_diagnostics` alone suffices.

4. **Gate 3: Spec Compliance**
   - Review the actual code against acceptance criteria.
   - Read files directly — do not trust your own claims.
   - Verify every requirement independently.

5. All three gates must pass before moving to next sub-task.

#### 4d. Final Goal Review

After all sub-tasks pass:

1. **Re-read acceptance criteria** from the provided goal text.
2. **Cross-reference** every criterion against implementation — collect specific evidence (file:line, test output, behavior).
3. **Run final verification** — `lsp_diagnostics` on all modified files, plus domain-specific checks.
4. **Assess each criterion**: Met (with evidence) or Unmet.
5. If any Unmet → fix, re-verify. Loop until all criteria pass.

#### 4e. Commit and Create PR

Once all criteria are verified:

1. **Stage and commit** all changes in the worktree:

   ```bash
   git -C <worktree-path> add .
   git -C <worktree-path> commit -m "<commit-message>"
   ```

   Commit message format: `feat(<feature>): <goal-summary>`

   For multi-commit goals, use meaningful commits per logical unit — not one giant commit.

2. **Push the branch**:

   ```bash
   git -C <worktree-path> push -u origin <branch-name>
   ```

3. **Create a Pull Request**:

   ```bash
   gh pr create \
     --base <base-branch> \
     --head <branch-name> \
     --title "<goal-title>" \
     --body-file - <<'EOF'
   ## Goal
   <goal-objective>

   ## Changes
   <summary of what was implemented>

   ## Acceptance Criteria
   <list of criteria with pass/fail status>

   ## Verification
   - Static Analysis: PASS
   - Domain Check: PASS/N/A
   - Spec Compliance: PASS

   ## Files Modified
   <list>
   EOF
   ```

4. **Report completion** back to controller with:
   - Status: `DONE` | `DONE_WITH_CONCERNS` | `BLOCKED`
   - PR URL
   - List of files modified
   - Verification evidence summary

### Step 5 — Controller Monitors and Collects Results

As subagents complete (via `<system-reminder>` notifications):

1. **Collect results** via `background_output(task_id="...")`.

2. **Timeout detection** — if a subagent has been running significantly longer than expected without completion notification, probe with `background_output(task_id="...", block=false)`. Check the worktree for commits (`git -C <wt> log --oneline -3`). If partial work exists, resume via `session_id`. If no work at all, re-dispatch with a simpler strategy.

3. **For each completed goal**:
   - Verify the PR was created successfully (check PR URL via `gh pr view`)
   - Read the subagent's verification evidence
   - Mark the goal `status: completed` in the goal file frontmatter
   - Update `Docs/Goals/Master.md` — set status to `completed`, recalculate summary counts
   - Mark parent task `completed` via `task_update`
   - Record completion timestamp for timing instrumentation

4. **For failed/blocked goals**:
   - Read the failure context
   - Attempt recovery (see Failure Recovery below)
   - If genuinely blocked, mark `status: blocked` with reason

5. **If PR creation failed** — check if the branch was pushed successfully. If yes, the branch is preserved on the remote; clean up the worktree but log the orphaned branch in the execution summary for manual PR creation. Do not leave worktrees orphaned just because PR creation failed.

6. **Process next wave** — after all Wave N agents complete, check if Wave N+1 goals are now unblocked. Create worktrees and spawn agents for them.

### Step 6 — Spec Update (Post-Completion)

After each goal completes:

1. **Delegate a spec update** using the appropriate spec skill:
   - If spec existed: Update mode (reflect new implementation)
   - If no spec: Feature Spec mode (create from implementation)
   - Run in background — this is autonomous documentation
   - See Spec Integration section for the delegation template
   - **Match skills to project domain** — use `unity-spec`/`unity-standards` for Unity, or equivalent for other domains. Do not hardcode Unity skills for non-Unity projects.

2. **Track spec update tasks** — record each spec update task_id. In Step 8, batch-verify all spec updates completed. Report failures as "SPEC_UPDATE_PENDING" in the execution summary rather than silently dropping them.

### Step 7 — Cleanup Worktrees

After a goal's PR is created and verified:

```bash
# Use worktree_manager.sh for safe removal with dirty-check guards
run_skill_script('plan-work', 'scripts/worktree_manager.sh', arguments=['remove', '<feature-slug>'])

# Or manually:
git -C <worktree-path> status --porcelain  # Verify clean
git worktree remove <worktree-path>
git branch -d <branch-name> 2>/dev/null || true  # Only after PR merge
git worktree prune
```

**Cleanup rules:**
- Remove worktrees only after PR is confirmed created
- Don't force-remove — if unclean, investigate first
- Prune stale metadata periodically
- Delete branches only after PR merge (not before)

### Step 8 — Execution Summary

After all waves are processed:

1. Re-read all goal files — verify every targeted goal has appropriate status.
2. Run final `lsp_diagnostics` on the main worktree.
3. **Batch-verify spec update completions** — check all spec update task_ids. Log any failures as SPEC_UPDATE_PENDING.
4. **Update Master.md** — final sync of all status changes.
5. Output:

```
## Execution Complete

Goals completed: X/Y
Goals blocked: Z (if any, with reasons)
Waves executed: N

### Summary
- [Goal 1]: [1-line summary] — PR #<number>
- [Goal 2]: [1-line summary] — PR #<number>

### Pull Requests Created
- PR #<N>: <title> (goal/<branch>) -> <base>
- PR #<N>: <title> (goal/<branch>) -> <base>

### Worktree Status
- Created: X worktrees
- Cleaned up: Y worktrees
- Remaining: Z (if any, with reason)
- Orphaned branches: [list, if PR creation failed but branch pushed]

### Spec Updates
- [Feature 1]: Updated/Created Docs/Specs/Feature_1.md — STATUS
- [Feature 2]: SPEC_UPDATE_PENDING (reason)

### Timing
- Total execution time: HH:MM:SS
- Average goal completion: MM:SS
- Fastest goal: <name> (MM:SS)
- Slowest goal: <name> (MM:SS)
- Worktree setup overhead: ~MM:SS per worktree

### Verification
- Build: PASS/FAIL/N/A
- Diagnostics: PASS/N errors
- Console (Unity): CLEAN/N errors/N/A
- Analyzer (Flutter): PASS/N errors/N/A
- Tests: X/Y passed / N/A

### Next Step
Review and merge the PRs, then run `plan-improve` for quality refinement.
```

---

## Subagent Prompt Template

Read `references/delegation-templates.md` and use the **Worktree Subagent Prompt Template** when spawning each goal's subagent. The template provides the complete prompt structure including environment setup, goal injection, verification protocol, workflow steps, and rules. Fill in all `{placeholders}` with values from the controller's context.

Key subagent rules (also in the template):
- NEVER ask questions. Think, decide, execute.
- NEVER modify files outside the assigned worktree path.
- NEVER suppress type errors (no `as any`, `@ts-ignore`, empty catches).
- NEVER skip verification gates. All three gates per sub-task.
- ALWAYS verify before claiming completion. Evidence before assertions.
- ALWAYS commit and push BEFORE creating the PR.
- ALWAYS maintain a running criteria checklist — update it after each sub-task.
- Report status: `DONE` | `DONE_WITH_CONCERNS` | `BLOCKED`

---

## Failure Recovery

### Subagent Failures

| Failure Type | Action |
|---|---|
| Subagent reports `DONE_WITH_CONCERNS` | Read concerns, fix via `session_id` if needed |
| Subagent reports `BLOCKED` | Assess blocker. Re-dispatch with different strategy, or mark goal blocked. |
| Subagent times out | Check worktree state. Resume via `session_id` or re-dispatch. |
| PR creation fails | Check if branch was pushed. Fix and retry. |
| Merge conflicts | Rebase worktree branch onto latest base: `git -C <wt> fetch origin && git -C <wt> rebase origin/<base>` |

### Escalation Protocol

| Failure Count | Action |
|---|---|
| 1-2 failures | Fix via `session_id` continuation |
| 3 failures (same approach) | Switch strategy: re-decompose, different category/skills |
| After strategy switch fails | Consult Oracle with full context |
| Genuinely impossible | Mark `blocked`, document reason, continue other goals |

### Worktree Recovery

If a worktree is in a bad state:

```bash
# Check state first — always diagnose before acting
git -C <wt> status
git -C <wt> log --oneline -5

# Reset to clean state (preserves commits, discards uncommitted changes)
git -C <wt> reset --hard origin/<base>

# Nuclear option: remove and recreate
# WARNING: --force discards ALL uncommitted changes — check for salvageable work first
# WARNING: -b will fail if the branch already exists — delete it first: git branch -D <branch>
git worktree remove --force <wt>
git branch -D <branch> 2>/dev/null || true
git worktree add -b <branch> <wt> origin/<base>
```

---

## Spec Integration (Mandatory)

The spec cycle ensures design documents and implementation stay synchronized:

```
Docs/Specs/Feature.md  ──read──>  Implementation  ──update──>  Docs/Specs/Feature.md
     (blueprint)                   (goal work)                   (living doc)
```

### Pre-Implementation: Spec as Blueprint

When a feature spec exists in `Docs/Specs/`, it serves as the architectural blueprint. The spec's Systems Design, Data Model, Events, and State Machines define the intended structure. Pass spec content to subagents so implementation follows the blueprint.

If acceptance criteria conflict with the spec, criteria take priority (latest requirements).

### Post-Implementation: Spec Update

After every goal completes, the feature spec **must** be updated. Delegation template:

```
task(
  category="unspecified-high",
  load_skills=["unity-spec", "unity-standards"],
  run_in_background=true,
  description="Update spec for {Feature}",
  prompt="
    1. TASK: Update the feature spec for {Feature} to reflect completed implementation.
       Mode: {Update if spec exists, Feature Spec if creating new}.

    2. EXPECTED OUTCOME: Docs/Specs/{Feature_Name}.md accurately reflects the codebase.

    3. REQUIRED TOOLS: read, write, edit, glob, grep

    4. MUST DO:
       - Use unity-spec workflow
       - Investigate actual codebase — cite file:line
       - Preserve user-authored design intent
       - Save directly — do NOT block for user review

    5. MUST NOT DO:
       - Do not ask for approval
       - Do not add speculative features
       - Do not remove sections — only update or add

    6. CONTEXT:
       - Feature: {feature_name}
       - Spec path: Docs/Specs/{Feature_Name}.md
       - Goal completed: {goal_title}
       - Files modified: {list}
  "
)
```

### Feature Name Mapping

| Goal Title | Spec File |
|---|---|
| `[Combat] Add parry mechanic` | `Combat.md` |
| `[Inventory System] Add sorting` | `Inventory_System.md` |
| `[UI] Build health bar` | `UI.md` |

---

## Model Selection

| Task Complexity | Category |
|---|---|
| Mechanical (1-2 files, clear spec) | `quick` |
| Standard (multi-file, some judgment) | `unspecified-high` or domain-specific |
| Complex (architecture, broad understanding) | `deep` or `ultrabrain` |

Domain categories:
- Frontend/UI → `visual-engineering`
- Hard logic/algorithms → `ultrabrain`
- Autonomous research + implementation → `deep`

---

## Skill Selection Guide

| Goal Domain | Primary Skills | Standards |
|---|---|---|
| Unity C# | `unity-code`, `unity-debug` | `unity-standards` |
| Unity Editor | `unity-editor` | `unity-standards` |
| Unity UI | `unity-uitoolkit` | `unity-standards` |
| Unity Tests | `unity-test-unit` | `unity-standards` |
| Flutter/Dart | `flutter-code`, `flutter-debug` | `flutter-standards` |
| Flutter UI | `flutter-ui` | `flutter-standards` |
| Flutter Tests | `flutter-test` | `flutter-standards` |
| Frontend/web | `frontend-design` | — |
| Next.js | `nextjs-backend` | — |
| Database | `database-design` | — |
| Cloud infra | `cloud-infra` | — |
| Shell scripts | `bash-check`, `bash-optimize` | — |
| Documentation | `unity-document`, `visual-explainer` | — |
| Spec updates | `unity-spec` | `unity-standards` |

Always include the relevant standards skill when delegating domain work.

---

## Concurrency Safety

### Invariants

1. **One branch per worktree** — git enforces this; never override with `--force`
2. **One goal per worktree** — never share worktrees between goals
3. **Worktrees are outside repo root** — prevents tool scanning and gitignore conflicts
4. **No shared mutable state** — each subagent works in complete isolation
5. **Base branch is read-only** — subagents branch from it but never push to it directly

### What's Shared (Read-Only)

- Git objects and refs (via `.git` common dir)
- The base branch state at worktree creation time

### What's Isolated (Per Worktree)

- Working directory
- Index (staging area)
- HEAD
- Branch
- Uncommitted changes
- Unity Library/Temp (if Unity project)

### Conflict Handling

When multiple goals modify overlapping files, conflicts resolve at PR merge time — not during execution. This is intentional:

1. Each goal implements independently against the base branch
2. PRs are reviewed and merged sequentially or in dependency order
3. If PR B conflicts with already-merged PR A, rebase B onto the updated base
4. The controller handles this during the monitoring phase

---

## Unity-Specific Considerations

Unity projects have special worktree behavior:

- **Library folder**: Each worktree gets its own `Library/`. This means cold imports (~2-10 min depending on project size). Budget for this startup cost. **Heuristic**: check `Library/` size in the main worktree (`du -sh Library/`). If >5GB, limit concurrent Unity worktrees to 2-3 and log a warning about extended setup time.
- **Temp/UserSettings**: Also per-worktree. Always gitignored.
- **Unity Editor**: Only one Unity Editor instance can have a project open at a time. Worktree-based execution works for code changes verified via MCP/CLI, but not for simultaneous Unity Editor sessions.
- **Submodules**: If the Unity project uses submodules, worktree support is degraded. Log a warning and consider sequential execution instead.

---

## Decision-Making Framework

1. **Codebase conventions first** — match existing patterns
2. **Best practices second** — if no convention, use industry standards
3. **Reasonable default third** — choose the simplest correct approach
4. **Document non-obvious choices** — brief comment or note

| Ambiguity | Resolution |
|---|---|
| "Improve X" without specifics | Implement 2-3 highest-impact improvements |
| Referenced file doesn't exist | Create with sensible defaults |
| Goals conflict | Both if possible; else prefer higher-priority |
| Requires external API key | Implement code, add TODO for configuration |
| Vague goal | Interpret most usefully and execute |

---

## Red Flags — Stop and Reassess

- **Using "should", "probably", "seems to"** — not evidence. Run verification.
- **Expressing satisfaction before verification** — run the checks first.
- **Trusting subagent reports** — verify independently.
- **Marking complete without verification command** — Iron Law.
- **Shotgun debugging** — each fix needs a hypothesis.
- **Skipping a gate** — never.
- **Batching completions** — mark each immediately after pass.

---

## Rules (Non-Negotiable)

1. **Never ask.** Think, decide, execute.
2. **Never stop early.** Process every uncompleted goal across all waves.
3. **Never deliver partial work.** Every acceptance criterion must be verified with evidence.
4. **Never suppress errors.** No `as any`, `@ts-ignore`, empty catch blocks.
5. **Never skip verification gates.** Three gates per sub-task, final review per goal.
6. **Never trust without verifying.** Verify subagent claims independently.
7. **Always read Master.md first.** It's the source of truth for goals.
8. **Always create worktrees outside repo root.** Isolation is non-negotiable.
9. **Always use one branch per worktree.** Never share branches.
10. **Always push before creating PR.** `gh pr create` requires the branch to exist remotely.
11. **Always provide full context to subagents.** Goal text, spec, domain, verification protocol.
12. **Always clean up worktrees after completion.** Remove worktree, prune metadata.
13. **Always update specs after goal completion.** Mandatory spec cycle.
14. **Always process goals in dependency waves.** Respect the DAG.
15. **Always use session continuity.** Use `session_id` for fix iterations with the same subagent.

---

## Measurement Plan

Track these metrics across runs to evaluate and improve skill effectiveness:

### Execution Efficiency
- **Goals completed per wave**: Count of DONE vs total per wave. Target: >90% first-pass completion.
- **Re-dispatch rate**: Percentage of goals requiring re-dispatch. Target: <10%.
- **Total execution time**: Wall-clock from first worktree creation to final summary. Track per-goal and aggregate.
- **Worktree setup overhead**: Time from `git worktree add` to subagent spawn. For Unity, includes Library import time.
- **Parallelization utilization**: Actual concurrent agents / MAX_PARALLEL_WORKTREES. Target: >80% utilization within waves.

### Verification Rigor
- **Three-gate pass rate**: Percentage of sub-tasks passing all three gates on first attempt. Broken gate = implementation quality issue.
- **Final review catch rate**: Criteria caught as unmet during final review (4d) that weren't caught during sub-task gates. High rate means gates are too lenient.
- **Evidence quality**: Are verification claims supported by specific file:line references? Sample-audit 20% of completed goals.

### Spec Synchronization
- **Spec update completion rate**: Percentage of spec updates that completed successfully (not PENDING). Target: 100%.
- **Spec freshness**: After execution, do specs reflect the implementation? Spot-check by reading spec and comparing to code.

### Error Recovery
- **Failure root causes**: Categorize failures (timeout, blocked, context-missing, too-complex). Track distribution to identify systemic issues.
- **Escalation depth**: How many escalation levels were needed per failure. Lower is better.
- **Session continuation success rate**: Percentage of fix-via-session_id attempts that resolved the issue. Target: >70%.

### Worktree Hygiene
- **Orphaned worktrees**: Count of worktrees remaining after execution. Target: 0.
- **Orphaned branches**: Count of remote branches without corresponding PRs. Target: 0.
- **Stale metadata**: Run `git worktree prune --dry-run` after execution. Target: no stale entries.

### PR Quality
- **PR creation success rate**: PRs created / goals completed. Target: 100%.
- **PR body completeness**: Does PR include Goal, Changes, Acceptance Criteria, Verification, Files Modified? Sample-audit.

### How to Collect
1. Record timestamps at: worktree creation, subagent spawn, subagent completion, PR creation, cleanup.
2. Include timing data in the execution summary (Step 8).
3. After each run, review the execution summary against these metrics.
4. Over 5+ runs, compute aggregates to identify trends and regressions.

---

## Optimization Log

Changes made to improve skill effectiveness, with rationale and expected impact.

| Date | Change | Rationale | Impact | Status |
|------|--------|-----------|--------|--------|
| 2026-04-14 | Added crash-recovery preamble to Step 1 | Controller crash left Master.md inconsistent | Idempotent re-runs | Applied |
| 2026-04-14 | Added MAX_PARALLEL_WORKTREES throttle (default 5) | Unbounded worktrees exhaust disk/API limits | Controlled resource usage | Applied |
| 2026-04-14 | Added timeout detection in Step 5 | Hung subagents block wave advancement | Faster failure detection | Applied |
| 2026-04-14 | Added PR-creation failure recovery | Failed PR orphaned worktrees | Zero orphaned worktrees | Applied |
| 2026-04-14 | Added spec update completion tracking | Fire-and-forget updates silently fail | 100% spec update visibility | Applied |
| 2026-04-14 | Added criteria checklist in subagent planning | 8+ criteria goals lose track | ~47% fewer re-dispatches | Applied |
| 2026-04-14 | Referenced worktree_manager.sh in Steps 3/7 | Duplicated git logic lacking pre-flight checks | Single source of truth | Applied |
| 2026-04-14 | Removed inline subagent template | 45-line duplication with delegation-templates.md | -30 lines, no divergence | Applied |
| 2026-04-14 | Added nuclear recovery warnings | Force-remove could destroy salvageable work | Explicit data-loss prevention | Applied |
| 2026-04-14 | Made spec update skills domain-aware | Hardcoded Unity skills for non-Unity projects | Correct skill loading | Applied |
| 2026-04-14 | Added Library size heuristic | No worktree cost estimation for large projects | Proactive limit adjustment | Applied |
| 2026-04-14 | Added Gate 1 file-list reuse for Gate 3 | Redundant file scanning across gates | Fewer tool calls | Applied |
| 2026-04-14 | Added timing section to execution summary | No performance data captured | Enables measurement plan | Applied |

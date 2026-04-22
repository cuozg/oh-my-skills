# Delegation Prompt Templates — plan-work Pipeline

Templates for the 6 specialist handoffs in the single-goal pipeline. The orchestrator fills in `{placeholders}` from the goal file and worktree context.

All prompts follow one contract: **the orchestrator provides all context upfront**, the specialist does its one job and returns a structured result.

---

## 1. Goal Discovery — `explore` agent (Step 0b)

Use when no goal file is provided. Runs **blocking** (`run_in_background=false`) because Step 1 depends on the result.

```
I'm the plan-work orchestrator and need ONE incomplete goal to execute.

Search Docs/Goals/ recursively for the FIRST goal file where:
  1. YAML frontmatter 'status' is 'pending' OR 'in-progress'
     (NOT 'completed', NOT 'blocked')
  2. AND the '## Acceptance Criteria' section has at least one unchecked '- [ ]' checkbox

Stop at the first match — do NOT enumerate all goals.

Prefer 'critical' > 'high' > 'medium' > 'low' priority if multiple candidates are
obvious from directory listing, but do NOT spend tokens sorting — first viable
match wins.

Return EXACTLY this block and nothing else:
  GOAL_FILE: <absolute or repo-relative path>
  GOAL_TITLE: <the '# [Feature] Task' heading>
  PRIORITY: <from frontmatter>
  UNCHECKED_COUNT: <number of unchecked criteria>

If NO incomplete goal exists anywhere under Docs/Goals/, return exactly:
  NO_INCOMPLETE_GOAL
```

---

## 2. Plan — `plan` agent / Prometheus (Step 2)

Blocking. The orchestrator records the returned `session_id` for revision loops.

```
You are producing an executable plan for ONE goal.

## Goal file
Path: {goal_file}
Title: {goal_title}
Priority: {priority}

## Objective
{goal_objective verbatim}

## Context
{goal_context verbatim}

## Acceptance Criteria (do NOT drop any)
{full checkbox list, one per line, numbered 1..N}

## Constraints
{goal_constraints verbatim}

## Spec (architectural blueprint, may be empty)
{spec_content OR "No spec exists — plan from criteria + codebase conventions."}

## Working environment
- Worktree path: {worktree_path}
- Branch: {branch}
- Base branch: {base_branch}
- Domain: {domain}  // unity | flutter | web | general

## Deliverable
Produce a work plan with:
  1. Ordered sub-tasks (atomic, verifiable) with file paths / modules to touch
  2. A table mapping EVERY acceptance criterion → sub-task(s) → verification method
     Format (required):
       | # | Criterion (verbatim) | Sub-task(s) | Verification (cmd, file:line, test name) |
  3. Risks and unknowns (if any)
  4. Suggested category + skills for the Sisyphus implementation call
     (e.g. category="deep", load_skills=["unity-code","unity-standards"])

## Rules
- NEVER drop or merge acceptance criteria. N criteria in → N rows in the mapping table.
- NEVER write code. Planning only.
- Return the plan as a single markdown document. The orchestrator will hand it to
  Momus for review before any implementation starts.
```

### Revision follow-up (via `session_id=plan_session_id`)

```
Momus requested changes to your plan. Revise it addressing each point:

{momus.required_changes as bullet list}

Return the full updated plan (not a diff). Keep the mapping table complete.
```

---

## 3. Plan Review — `momus` (Step 3)

Blocking. Fresh session each review.

```
Review the following work plan against the goal and its acceptance criteria.

## Goal acceptance criteria (authoritative)
{checkbox list verbatim}

## Plan to review
{full plan text from Step 2}

## Evaluation checklist
1. Every acceptance criterion appears in the plan's mapping table exactly once.
2. Every sub-task lists concrete files/modules — no vague "update the system".
3. Every criterion has a concrete verification method
   (runnable command, specific file:line, or named test).
4. Risks are identified or explicitly declared "none".
5. Proposed category + skills for Sisyphus are sensible for the domain.

## Output format (strict)
Verdict: APPROVE | REQUEST_CHANGES
Reasons: <bullet list — required even for APPROVE, listing what passed>
Required changes (only if REQUEST_CHANGES): <bullet list, each item actionable>

Do not rewrite the plan. Only review.
```

---

## 4. Implement — `sisyphus` (Step 4)

Blocking. The orchestrator records `sisyphus_session_id` for verify-loop re-dispatch.

```
You are implementing ONE goal in an isolated git worktree.

## Environment
- Worktree path: {worktree_path}
- Branch: {branch}
- Base branch: {base_branch}
- Domain: {domain}
- Repo: {repo_owner}/{repo_name}

Use workdir="{worktree_path}" for ALL bash/git commands.
Do NOT modify files outside the worktree.

## Goal
### Objective
{goal_objective}

### Context
{goal_context}

### Acceptance Criteria
{checkbox list verbatim}

### Constraints
{goal_constraints}

## Spec (blueprint, may be empty)
{spec_content OR "No spec — implement from criteria."}

## Approved plan (FOLLOW THIS — do NOT replan from scratch)
{final approved plan from Step 3}

## Three-gate verification protocol (MANDATORY per sub-task)
Gate 1 — Static Analysis: lsp_diagnostics clean on every changed file.
Gate 2 — Domain check:
  - Unity:  Unity_ReadConsole (no CS### or assembly errors)
  - Flutter: dart analyze clean
  - Web/Node: build / tsc --noEmit clean
  - General: lsp_diagnostics alone suffices
Gate 3 — Spec compliance: re-read the code vs. each acceptance criterion.
  Produce a criterion → evidence row for EVERY checkbox:
    - [PASS] <criterion verbatim> — evidence: <file:line | cmd output | test name>
    - [FAIL] <criterion verbatim> — reason: <why>

Maintain a running criteria checklist and update it after each sub-task:
  [ ] Criterion 1 → Sub-task A
  [x] Criterion 2 → Sub-task B (verified)

## Commit + PR
1. Commit (conventional): `feat({feature}): {summary}` — multi-commit OK for logical units.
2. Push: `git -C {worktree_path} push -u origin {branch}`
3. PR:
   gh pr create \
     --repo {repo_owner}/{repo_name} \
     --base {base_branch} \
     --head {branch} \
     --title "{goal_title}" \
     --body-file - <<'EOF'
   ## Goal
   {goal_objective}
   ## Changes
   <bullets>
   ## Acceptance Criteria
   <one [PASS]/[FAIL] row per checkbox, in order — no row omitted>
   ## Verification
   - Static Analysis: PASS
   - Domain Check ({domain}): PASS/N/A
   - Spec Compliance: PASS
   ## Files Modified
   <list>
   EOF

## Report (final message)
STATUS: DONE | DONE_WITH_CONCERNS | BLOCKED
PR_URL: <url>
FILES_MODIFIED: <list>
EVIDENCE_TABLE: <the criterion → evidence rows from Gate 3>
CONCERNS/BLOCKER: <if applicable>

## Rules
- NEVER ask. Think, decide, execute.
- NEVER modify files outside your worktree.
- NEVER suppress type errors (`as any`, `@ts-ignore`, empty catches, deleted tests).
- NEVER skip gates.
- NEVER claim PASS without evidence.
- Commit + push BEFORE `gh pr create`.
- Report exactly one status: DONE | DONE_WITH_CONCERNS | BLOCKED.
```

### Re-dispatch follow-up (via `session_id=sisyphus_session_id`)

```
Hephaestus found gaps. Fix the specific issues below, re-run the three gates,
and update the PR with a fresh evidence table.

GAPS (from Hephaestus):
{hephaestus.gaps as bullet list, each item: "Criterion N — <what's missing>"}

Do NOT open a new PR — amend the existing branch {branch}.
After pushing, report STATUS + updated EVIDENCE_TABLE.
```

---

## 5. Verify — `hephaestus` (Step 5)

Blocking. Fresh session per verify round — Hephaestus re-derives evidence independently.

```
You are the verifier for ONE goal. You do NOT implement. You only test.

## Environment
- Worktree path: {worktree_path}
- Branch: {branch} (already pushed)
- PR: {pr_url}
- Domain: {domain}

## Goal acceptance criteria (authoritative — verify each one)
{checkbox list verbatim, numbered 1..N}

## Sisyphus evidence table (CLAIMS — do not trust; re-verify)
{evidence table from Step 4}

## Your job
For EACH criterion, independently gather evidence from the worktree:
  - Read the files cited by Sisyphus and confirm the claim.
  - Grep the worktree for the feature/symbol/behavior the criterion names.
  - Re-run the relevant gate command (lsp_diagnostics / dart analyze / build).
  - If the criterion names a test, run it and capture output.

Classify each criterion:
  VERIFIED — concrete evidence in this session confirms it.
  UNMET    — no supporting code, or evidence contradicts the claim.
  UNCLEAR  — ambiguous; treat as UNMET for gating.

## Output format (strict)
OVERALL: PASS | FAIL
PER_CRITERION:
  1. [VERIFIED|UNMET|UNCLEAR] <criterion verbatim> — evidence: <file:line | cmd output>
  2. ...
SUMMARY: <1-2 sentences>
GAPS (if any): <what Sisyphus must fix, concrete and criterion-indexed>

## Rules
- NEVER mark VERIFIED without first-hand evidence (you read the file or ran
  the command in THIS session).
- NEVER paraphrase Sisyphus's evidence as your own — re-derive it.
- If a cited file:line does not contain what it claims, mark UNMET.
- OVERALL is PASS only when every criterion is VERIFIED.
```

---

## 6. Spec Update — `unspecified-high` category (Step 6d)

Non-blocking (run_in_background=true). Does not gate goal completion.

```
task(
  category="unspecified-high",
  load_skills=["{domain-spec-skill}", "{domain-standards-skill}"],
  run_in_background=true,
  description="Update spec for {feature_name}",
  prompt="
    1. TASK: {Update existing | Create new} spec for {feature_name}
       reflecting completed goal '{goal_title}'.

    2. EXPECTED OUTCOME: Docs/Specs/{feature_name}.md matches the codebase
       in the {branch} worktree. Architecture, components, events, data models
       and state machines all reflect what was actually built.

    3. REQUIRED TOOLS: read, write, edit, glob, grep, lsp tools

    4. MUST DO:
       - Use the {unity-spec | equivalent} {Update | Feature Spec} workflow.
       - Investigate actual code in {worktree_path}; cite file:line for every reference.
       - Preserve existing design intent; only revise where code diverges.
       - Add [UPDATED: reason] tags next to changed sections (Update mode only).
       - Run validation (if the spec skill provides one).
       - Save directly; do NOT request approval.

    5. MUST NOT DO:
       - Do not block or ask for user input.
       - Do not rewrite sections still accurate.
       - Do not add speculative future features.
       - Do not delete sections — only update or add.

    6. CONTEXT:
       - Feature: {feature_name}
       - Spec path: Docs/Specs/{feature_name}.md (create if missing)
       - Goal completed: {goal_title}
       - Implementation summary: {brief}
       - Files modified: {list from Step 4}
  "
)
```

---

## Worktree Shell Helpers (orchestrator, Step 1 & cleanup)

```bash
# Create (Step 1)
run_skill_script('plan-work', 'scripts/worktree_manager.sh',
                 arguments=['create', '{feature-slug}', '{base-branch}'])

# Or manually:
git fetch origin
BRANCH="goal/{feature-slug}"
WT="../.worktrees/{feature-slug}"
git worktree add -b "$BRANCH" "$WT" "origin/{base-branch}"

# Remove (cleanup)
run_skill_script('plan-work', 'scripts/worktree_manager.sh',
                 arguments=['remove', '{feature-slug}'])

# Or manually:
git -C "$WT" status --porcelain  # must be empty
git worktree remove "$WT"
git worktree prune
# Branch: leave until PR is merged. Do NOT delete here.
```

---

## Status Protocol Summary

| Source | Status | Orchestrator action |
|---|---|---|
| explore | `NO_INCOMPLETE_GOAL` | Stop pipeline, report |
| explore | GOAL block | Proceed to Step 1 |
| momus | `APPROVE` | Proceed to Step 4 |
| momus | `REQUEST_CHANGES` (rev ≤ 3) | Re-run Prometheus via plan `session_id` |
| momus | `REQUEST_CHANGES` (rev = 4) | Consult Oracle / escalate |
| sisyphus | `DONE` | Proceed to Step 5 |
| sisyphus | `DONE_WITH_CONCERNS` | Log, proceed to Step 5 |
| sisyphus | `BLOCKED` | Recoverable → re-dispatch via session; else block goal |
| hephaestus | `PASS` (all VERIFIED) | Proceed to Step 6 |
| hephaestus | `FAIL` (any UNMET, cycle ≤ 3) | Re-dispatch Sisyphus via session with GAPS |
| hephaestus | `FAIL` (cycle = 4) | Oracle → user escalation or block goal |

---

## Self-Review Checklist for Sisyphus (included in its prompt)

Before reporting STATUS, Sisyphus must confirm:

**Completeness**
- Every acceptance-criteria checkbox has a concrete evidence row (file:line or cmd output).
- No criterion was merged, paraphrased, or silently dropped.
- Edge cases named in constraints are handled.

**Quality**
- Names are clear and match codebase conventions.
- No suppressed errors.
- No deleted or skipped tests.

**Git**
- All changes committed.
- Branch pushed to remote.
- PR created with full acceptance-criteria block in the body.

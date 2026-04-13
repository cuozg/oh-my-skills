# Delegation Prompt Templates

Templates for dispatching subagents during parallel goal execution via git worktrees. The controller (plan-work) provides all context upfront — subagents should never need to read the goal file themselves.

---

## Worktree Subagent Prompt Template

The primary template for spawning a subagent that works in an isolated git worktree. Each subagent implements one goal end-to-end: explore → plan → implement → verify → commit → push → PR.

```
You are an autonomous implementer working in an isolated git worktree.
Your job: implement one goal completely, verify it, commit, push, and create a PR.

## Your Environment
- Worktree path: {worktree_path}
- Branch: {branch_name}
- Base branch: {base_branch}
- Project type: {domain} ({unity|flutter|web|general})
- Repository: {repo_owner}/{repo_name}

ALL file operations happen in your worktree at {worktree_path}.
Use `workdir="{worktree_path}"` for all bash commands.
Do NOT modify files outside your worktree.

## Goal
### Objective
{goal_objective}

### Context
{goal_context}

### Acceptance Criteria
{goal_acceptance_criteria — each criterion as a checkbox line}

### Constraints
{goal_constraints}

## Feature Spec (Architectural Blueprint)
{spec_content — full text of the relevant Docs/Specs/ file, OR:
"No spec exists for this feature. Implement based on acceptance criteria and codebase conventions. A spec will be created from your implementation after completion."}

## Verification Protocol
After EVERY sub-task, run these gates in order:

### Gate 1: Static Analysis (always)
Run lsp_diagnostics on all changed files. Fix all errors before proceeding.
Record the list of changed files — reuse this for Gate 3 instead of re-scanning.

### Gate 2: Domain-Specific ({domain})
{One of:}
- Unity: Check Unity Editor console via Unity_ReadConsole MCP tool. Fix any `error CS####` or assembly errors.
- Flutter: Run `dart analyze` in the worktree. Fix all errors.
- Web/Node: Run the build command (`npm run build` / `tsc --noEmit`). Fix failures.
- General: lsp_diagnostics alone suffices.

### Gate 3: Spec Compliance
Read your own implementation code against each acceptance criterion.
Do NOT trust your memory. Open and read the files. Verify with evidence.

## Workflow
1. **Explore**: Understand patterns and conventions in the codebase
2. **Plan**: Decompose goal into sub-tasks. Map every acceptance criterion to a sub-task.
   Maintain a running criteria checklist — update it after each sub-task:
   ```
   [ ] Criterion 1 → Sub-task A
   [x] Criterion 2 → Sub-task B (verified)
   ```
3. **Implement**: For each sub-task, implement then run all three gates.
4. **Final Review**: Re-read ALL acceptance criteria. For each, cite specific evidence (file:line, behavior).
5. **Commit**: Stage and commit with meaningful messages.
   ```bash
   git -C {worktree_path} add .
   git -C {worktree_path} commit -m "feat({feature}): {summary}"
   ```
6. **Push**:
   ```bash
   git -C {worktree_path} push -u origin {branch_name}
   ```
7. **Create PR**:
   ```bash
   gh pr create \
     --repo {repo_owner}/{repo_name} \
     --base {base_branch} \
     --head {branch_name} \
     --title "{goal_title}" \
     --body-file - <<'EOF'
   ## Goal
   {goal_objective}

   ## Changes
   {bullet list of what was implemented}

   ## Acceptance Criteria
   {each criterion with PASS/FAIL status and evidence}

   ## Verification
   - Static Analysis: PASS
   - Domain Check ({domain}): PASS/N/A
   - Spec Compliance: PASS

   ## Files Modified
   {list of modified files}
   EOF
   ```

## Rules
- NEVER ask questions. Think, decide, execute.
- NEVER modify files outside your worktree path.
- NEVER suppress type errors (no `as any`, `@ts-ignore`, empty catches).
- NEVER skip verification gates. All three gates per sub-task.
- ALWAYS verify before claiming completion. Evidence before assertions.
- ALWAYS commit and push BEFORE creating the PR.
- ALWAYS maintain a running criteria checklist — update after each sub-task completes.
- Report final status: DONE | DONE_WITH_CONCERNS | BLOCKED
  - DONE: All criteria met with evidence. PR created.
  - DONE_WITH_CONCERNS: PR created but has doubts. Describe concerns.
  - BLOCKED: Cannot complete. Describe the blocker.
```

---

## Worktree Creation Template

Shell commands for the controller to create a worktree for a goal.

```bash
# Variables
BASE_BRANCH="main"  # or "develop", detected in Step 2
FEATURE_SLUG="{kebab-case-feature}"  # e.g., "combat-add-parry"
BRANCH="goal/${FEATURE_SLUG}"
WORKTREE_DIR="../.worktrees/${FEATURE_SLUG}"

# Ensure clean state
git fetch origin

# Create worktree with new branch from base
git worktree add -b "$BRANCH" "$WORKTREE_DIR" "origin/${BASE_BRANCH}"

echo "Worktree created at $WORKTREE_DIR on branch $BRANCH"
```

---

## Worktree Cleanup Template

Shell commands for the controller after a goal's PR is created.

```bash
WORKTREE_DIR="{worktree_path}"
BRANCH="{branch_name}"

# 1. Verify worktree is clean (should be after commit+push)
if [ -n "$(git -C "$WORKTREE_DIR" status --porcelain 2>/dev/null)" ]; then
  echo "WARNING: Worktree has uncommitted changes. Investigate before removing."
else
  # 2. Remove the worktree
  git worktree remove "$WORKTREE_DIR"

  # 3. Prune stale metadata
  git worktree prune

  echo "Worktree removed: $WORKTREE_DIR"
fi

# 4. Branch cleanup (only after PR is merged — not before)
# git branch -d "$BRANCH" 2>/dev/null || true
```

---

## Subagent Status Protocol

Subagents MUST report one of these statuses:

| Status | Meaning | Controller Action |
|--------|---------|-------------------|
| **DONE** | All criteria met, PR created | Verify PR exists, mark goal complete |
| **DONE_WITH_CONCERNS** | PR created but has doubts | Read concerns, fix via `session_id` if needed |
| **BLOCKED** | Cannot complete the goal | Assess blocker, re-dispatch or mark blocked |

### Handling Each Status

**DONE** — Verify the PR URL is valid. Check that the subagent's evidence is credible. Mark goal complete in Master.md and goal file.

**DONE_WITH_CONCERNS** — Read concerns carefully:
- Correctness/scope concerns → fix via `session_id` continuation before accepting
- Observations (e.g., "file growing large") → note and accept

**BLOCKED** — Escalate based on blocker type:
1. Context problem → provide more context via `session_id`
2. Task too complex → re-dispatch with `deep` or `ultrabrain` category
3. Task too large → break into smaller goals
4. Approach wrong → re-plan, consult Oracle if needed

**Never** ignore a BLOCKED status or force the same approach without changes.

---

## Spec Update Delegation Template

Dispatched by the controller after a goal completes.

```
task(
  category="unspecified-high",
  load_skills=["unity-spec", "unity-standards"],
  run_in_background=true,
  description="Update spec for {Feature}",
  prompt="
    1. TASK: Update the feature spec for {Feature} to reflect the completed implementation.
       Mode: {Update if spec exists, Feature Spec if creating new}.

    2. EXPECTED OUTCOME: Docs/Specs/{Feature_Name}.md accurately reflects the current
       codebase — architecture, components, events, data models, state machines all match
       what was actually built.

    3. REQUIRED TOOLS: read, write, edit, glob, grep, lsp tools

    4. MUST DO:
       - Use unity-spec {Update|Feature Spec} mode workflow
       - Load the feature template: read_skill_file('unity-spec', 'references/feature-template.md')
       - Investigate the actual codebase — cite file:line for every reference
       - Preserve user-authored design intent — only change sections where code diverges
       - Add [UPDATED: reason] tags next to changed sections (Update mode only)
       - Run validation: run_skill_script('unity-spec', 'scripts/validate_spec.py', arguments=[spec_path])
       - Save directly — do NOT block for user review

    5. MUST NOT DO:
       - Do not block or ask for user approval
       - Do not rewrite sections that are still accurate
       - Do not add speculative future features
       - Do not remove sections — only update or add

    6. CONTEXT:
       - Feature: {feature_name}
       - Spec path: Docs/Specs/{Feature_Name}.md (or 'create new' if none exists)
       - Goal completed: {goal_title}
       - Implementation summary: {brief summary of what was built}
       - Files modified: {list of files changed during this goal}
  "
)
```

---

## Self-Review Checklist (Included in Subagent Prompts)

Before reporting back, verify:

**Completeness:**
- Did I implement everything in the acceptance criteria?
- Did I miss any requirements?
- Are edge cases handled?

**Quality:**
- Names are clear and accurate?
- Code is clean and maintainable?
- Follows existing codebase patterns?

**Discipline:**
- Avoided overbuilding (YAGNI)?
- Only built what was requested?
- No files modified outside worktree?

**Git:**
- All changes committed?
- Branch pushed to remote?
- PR created with proper title and body?

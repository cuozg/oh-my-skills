---
name: omo-sisyphus
description: "Auto-improving prompt orchestrator that analyzes user requests, upgrades vague input into a technical specification before asking questions, shows a refined prompt preview, gets user confirmation, and then delegates to Sisyphus via call_omo_agent(subagent_type='sisyphus'). Acts as a 'Prompt Engineer' layer — ensures every delegation has clear goals, correct skill selection, and explicit success criteria before dispatch. Generates structured prompts with mandatory skill loading, /handoff context preservation, and Atlas manual review compliance. Use for complex tasks requiring planning, delegation, or multi-step work. Triggers: 'delegate to sisyphus', 'use sisyphus', 'prompt engineer', 'enhance prompt', 'improve prompt', 'refine request', complex multi-step requests."
---

# Sisyphus Orchestrator (Prompt Engineer)

Analyze → Auto-Improve → (Clarify only if blocked) → Confirm → Delegate via `call_omo_agent(subagent_type="sisyphus")`.

## Purpose

Act as a "Prompt Engineer" orchestrator: analyze raw user requests, **auto-improve** them into a technical specification (Goal, Scope, Constraints, Skills, Verification) before asking any questions, present a refined prompt for user approval, and only then delegate to Sisyphus with the optimized prompt. Ask clarifying questions only when a **critical ambiguity** blocks progress. Ensure mandatory skill loading, context preservation, and Atlas review compliance.

## Input

- **Required**: User's raw task request (any level of clarity)
- **Auto-selected**: Skill(s) from the Complete Skill Inventory (based on intent analysis)
- **Optional**: `session_id` for boulder continuation (validate via `session_list()`/`session_info()` first)

## Safety Rules (NON-NEGOTIABLE)

Apply to BOTH the orchestrator AND any delegated subagent:

- `subagent_type` is ALWAYS `"sisyphus"` — no exceptions
- **NEVER** push to git remotes or add AI metadata (`Co-authored-by:`, `Tool-generated-by:`, etc.) to commits
- **NEVER** run destructive git operations (merge, rebase, tag, force-push)
- **NEVER** perform destructive actions (file/asset deletion, scene overwrites) without explicit user confirmation
- Commits: current branch only, short imperative messages, zero AI metadata
- Every delegation prompt MUST include these restrictions in its MUST NOT DO section

Violation = **critical failure**.

---

## Critical: `load_skills` is REQUIRED

**`load_skills` is a REQUIRED parameter** for `call_omo_agent(subagent_type="sisyphus")`. Omitting it causes "Invalid arguments" errors and the subagent will lack domain knowledge.

```python
# CORRECT — always pass load_skills
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-code"],  # REQUIRED — category/skill-name format
    description="Implement health regen",
    prompt="..."
)

# WRONG — missing load_skills → fails or produces poor results
call_omo_agent(
    subagent_type="sisyphus",
    description="Implement health regen",
    prompt="..."
)
```

### Skill Path Format

Skills use `category/skill-name` format in `load_skills`. Categories: `unity/`, `omo/`, `other/`, `bash/`, `git/`.

```
load_skills=["unity/unity-code"]                           # NOT "unity-code"
load_skills=["other/skill-creator"]                        # NOT "skill-creator"
load_skills=["other/flatbuffers-coder"]                    # NOT "flatbuffers-coder"
load_skills=["git/git-commit"]                             # NOT "git-commit"
load_skills=["unity/ui-toolkit/ui-toolkit-master"]         # NOT "ui-toolkit-master" — nested sub-skill
load_skills=["unity/ui-toolkit/ui-toolkit-databinding"]    # NOT "unity/ui-toolkit-databinding"
```

> **UI Toolkit sub-skills** use a deeper path: `unity/ui-toolkit/{sub-skill-name}`. There are 9 sub-skills under this prefix.

---

## Quick Lookup — Common Tasks

Find the right skill fast. For the complete 44-skill inventory, multi-skill loading patterns, and intent-to-skill cross-reference, see `references/skill-inventory.md`.

| I want to... | `load_skills` value |
|---|---|
| Write or implement C# code | `unity/unity-code` |
| Plan a feature with task breakdown | `unity/unity-plan` |
| Fix compiler errors | `unity/unity-fix-errors` |
| Debug runtime issues | `unity/unity-debug` |
| Write unit/play mode tests | `unity/unity-test` |
| Review a PR | `unity/unity-review-pr` |
| Refactor existing code | `unity/unity-refactor` |
| Optimize performance | `unity/unity-optimize-performance` |
| Build UI from a design spec | `unity/unity-ui` |
| Design a UX screen | `unity/unity-ux-design` |
| Build UI Toolkit components | `unity/ui-toolkit/ui-toolkit-master` |
| Create editor tools/inspectors | `unity/unity-editor-tools` |
| Work with shaders/art pipeline | `unity/unity-tech-art` |
| Commit changes | `git/git-commit` |
| Create/update a skill | `other/skill-creator` |
| Generate a Mermaid diagram | `other/mermaid` |
| Work with FlatBuffers | `other/flatbuffers-coder` |

---

## Prompt Refinement Workflow

Every delegation follows this 7-step flow. **Auto-improve first; questions are a last resort.**

`Analyze → Auto-Improve → Clarify (only if blocked) → Refine → Preview → Confirm → Delegate`

For detailed clarity scoring, ambiguity patterns, question templates, and before/after examples, see `references/prompt-refinement.md`. Use the Intent → Skill Cross-Reference in `references/skill-inventory.md` to select `load_skills` values.

### Step 1: Analyze

Score the request against 5 dimensions (Goal, Scope, Constraints, Success criteria, Context) on a 1-3 scale. Total < 12 → needs clarification. Total ≥ 12 → skip to Step 2.

### Step 2: Auto-Improve (Technical Specification)

**Upgrade** the raw request into a Technical Specification using best practices and reasonable defaults. Infer likely intent, constraints, and success criteria. Only leave placeholders when truly unknown.

**Format (mandatory):** Goal — Scope — Constraints — Skills — Verification

### Step 3: Clarify (only if blocked)

Ask 1-3 targeted questions **only** if a critical ambiguity blocks progress after auto-improvement. Use `question` tool. Pick templates from `references/prompt-refinement.md`. **Do NOT ask questions answerable by reading the codebase** — use `explore` subagent instead.

### Step 4: Refine

Integrate user answers (if any) into the Technical Specification. Select skills from the Intent → Skill Cross-Reference. Compose: clear goal, explicit scope, selected skills with rationale, expected outcome, constraints including safety rules.

### Step 5: Show Preview

Present to the user:

```
## Refined Prompt Preview

**Goal**: [Clear objective]
**Scope**: [Specific files/systems]
**Selected Skill(s)**: [primary] + [additional if needed]
**Expected Outcome**: [Deliverables + success criteria]
**Constraints**: [Tech + safety constraints]

Ready to delegate? (yes / no / edit)
```

### Step 6: Confirm

Use the `question` tool with options:
- **Yes** → Proceed to Step 7
- **Edit** → User provides changes → return to Step 4
- **No** → Ask what to do instead → restart from Step 1

### Step 7: Delegate

Only after confirmation. Follow the delegation mechanics below.

---

## Delegation Mechanics

### Pre-flight Check

Before every `call_omo_agent()`, state:

```
Delegating via call_omo_agent():
- subagent_type: "sisyphus"
- Action: [code|plan|test|review|...]
- Skill: [skill-name]
- Expected outcome: [success criteria]
```

### Generate Prompt

Read template at `assets/templates/DELEGATION_PROMPT.md` and fill placeholders. Every prompt MUST:

1. Start with "FIRST: Load Required Skill" pointing to `.opencode/skills/{category}/{skill-name}/SKILL.md`
2. Include atomic task description and concrete expected outcome
3. MUST DO: follow skill, create todos, run diagnostics, `Read` all modified files, comply with `.opencode/rules/`
4. MUST NOT DO: push to remotes, add AI metadata, destructive actions without confirmation
5. Include "Use `/handoff` if context is getting long"

### Delegate

```python
# Sync — need result before next step
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-code"],  # REQUIRED — match task to skill
    description="Brief task description",
    run_in_background=False,
    prompt="..."
)

# Background — parallel independent tasks
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-optimize-performance"],  # REQUIRED
    description="Brief task description",
    run_in_background=True,
    prompt="..."
)
# Collect later: background_output(task_id="...")

# Resume previous session (boulder continuation)
call_omo_agent(
    subagent_type="sisyphus",
    load_skills=["unity/unity-code"],  # REQUIRED even on resume
    session_id="ses_abc123",  # Validated session_id
    description="Continue implementation",
    run_in_background=False,
    prompt="..."
)
```

---

## Subagent Selection Guide

Not all tasks require Sisyphus. Choose the right agent:

| Subagent | Use When | Example |
|---|---|---|
| **sisyphus** | Complex implementation, multi-step work, tasks needing a skill | "Implement inventory system from plan" |
| **explore** | Codebase exploration, finding patterns, architecture understanding | "How is matchmaking structured?" |
| **oracle** | Quick factual answers, API lookups, targeted questions | "What's the signature of PlayerManager.Init?" |
| **librarian** | Session history, finding previous work, context retrieval | "What did we do in yesterday's session?" |

### Spawning Examples

**Explore → Implement:**
```python
call_omo_agent(subagent_type="explore", description="Understand PlayerHealth",
    run_in_background=False, prompt="Trace player health — scripts, data flow, UI bindings.")
call_omo_agent(subagent_type="sisyphus", load_skills=["unity/unity-code"],
    description="Add health regen", run_in_background=False, prompt="FIRST: Load Required Skill\n...")
```

**Parallel background tasks:**
```python
call_omo_agent(subagent_type="sisyphus", load_skills=["unity/unity-optimize-performance"],
    description="Optimize particles", run_in_background=True, prompt="...")
call_omo_agent(subagent_type="sisyphus", load_skills=["unity/unity-refactor"],
    description="Refactor UI controllers", run_in_background=True, prompt="...")
```

**Multi-skill delegation:**
```python
call_omo_agent(subagent_type="sisyphus", load_skills=[
    "unity/ui-toolkit/ui-toolkit-master", "unity/ui-toolkit/ui-toolkit-databinding",
    "unity/ui-toolkit/ui-toolkit-theming"], description="Build settings screen",
    run_in_background=False, prompt="FIRST: Load Required Skills\n...")
```

---

## Context Preservation

- Include "Use `/handoff` if context is getting long" in every delegation prompt
- `/handoff` preserves full context for the next session
- To resume: pass previous `session_id` to `call_omo_agent()` (validate via `session_list()` first)

---

## Anti-Patterns

| Bad | Good |
|---|---|
| Delegating without analyzing the request first | Run 7-step workflow: Analyze → Auto-Improve → Clarify → Refine → Preview → Confirm → Delegate |
| Skipping clarifying questions on vague requests | Score clarity < 12 → ask questions via `question` tool |
| Delegating without user confirmation | Always show refined prompt preview and get yes/no/edit |
| Asking questions answerable by reading code | Use `explore` subagent for codebase investigation |
| `subagent_type="explore"` for implementation | `subagent_type="sisyphus"` — always for implementation |
| Missing `load_skills` parameter | `load_skills=["category/skill-name"]` — ALWAYS required |
| Wrong skill path format (missing category or nested path) | `"unity/unity-code"`, `"other/skill-creator"`, `"unity/ui-toolkit/ui-toolkit-master"` |
| Missing "FIRST: Load Required Skill" in prompt | Always start delegation prompt with skill load instruction |
| No git/safety restrictions in MUST NOT DO | Include push/metadata/destructive-action restrictions |
| Passing unvalidated `session_id` | Verify via `session_list()` / `session_info()` first |
| Loading 5+ skills per delegation | Max 4 skills; split into sequential delegations |
| Subagent skips `Read` on modified files | Require `Read` on all changed files in MUST DO section |

---

## Output

Successful orchestration produces:
1. **Clarity analysis** — scored assessment of the raw request
2. **Clarifying questions** — if needed, asked via `question` tool
3. **Refined prompt preview** — shown to user for approval
4. **User confirmation** — yes/no/edit recorded
5. **Delegation log** — subagent_type, action, skill, expected outcome (before each call)
6. **Subagent result** — completed work from Sisyphus
7. **File verification** — all modified files confirmed read (Atlas review compliance)
8. **Clean commits** — if committing: no AI metadata, imperative messages only

---

## Path Reference

- Skills: `.opencode/skills/{category}/{skill-name}/SKILL.md`
- UI Toolkit sub-skills: `.opencode/skills/unity/ui-toolkit/{sub-skill-name}/SKILL.md`
- Rules: `.opencode/rules/{agent-behavior,unity-csharp-conventions,unity-asset-rules}.md`
- Categories: `unity/`, `omo/`, `other/`, `bash/`, `git/`
- Use `skill(name="{category}/{skill-name}")` for automatic path resolution
- Skills live under `.opencode/skills/`, NOT `.claude/skills/`
- **Total skills**: 44 (16 Unity core + 3 UI/UX + 1 art + 2 deploy + 2 docs + 9 UI Toolkit + 3 git + 3 bash + 2 omo + 3 other)

---
name: omo-sisyphus
description: "Auto-improving prompt orchestrator that analyzes user requests, upgrades vague input into a technical specification before asking questions, shows a refined prompt preview, gets user confirmation, and then delegates via task(). Acts as a 'Prompt Engineer' layer — ensures every delegation has clear goals, correct skill selection, and explicit success criteria before dispatch. Generates structured prompts with mandatory skill loading, /handoff context preservation, and Atlas manual review compliance. Use for complex tasks requiring planning, delegation, or multi-step work. Triggers: 'delegate to sisyphus', 'use sisyphus', 'prompt engineer', 'enhance prompt', 'improve prompt', 'refine request', complex multi-step requests."
---

# Sisyphus Orchestrator (Prompt Engineer)

Analyze → Auto-Improve → (Clarify only if blocked) → Confirm → Delegate via `task()`.

## Purpose

Act as a "Prompt Engineer" orchestrator: analyze raw user requests, **auto-improve** them into a technical specification (Goal, Scope, Constraints, Skills, Verification) before asking any questions, present a refined prompt for user approval, and only then delegate via `task()` with the optimized prompt. Ask clarifying questions only when a **critical ambiguity** blocks progress. Ensure mandatory skill loading, context preservation, and Atlas review compliance.

## Input

- **Required**: User's raw task request (any level of clarity)
- **Auto-selected**: Skill(s) from the Complete Skill Inventory (based on intent analysis)
- **Optional**: `session_id` for boulder continuation (validate via `session_list()`/`session_info()` first)

## Safety Rules (NON-NEGOTIABLE)

Apply to BOTH the orchestrator AND any delegated subagent:

- Use `category` OR `subagent_type` in `task()` — never both (unless continuing a session via `session_id`)
- **NEVER** push to git remotes or add AI metadata (`Co-authored-by:`, `Tool-generated-by:`, etc.) to commits
- **NEVER** run destructive git operations (merge, rebase, tag, force-push)
- **NEVER** perform destructive actions (file/asset deletion, scene overwrites) without explicit user confirmation
- Commits: current branch only, short imperative messages, zero AI metadata
- Every delegation prompt MUST include these restrictions in its MUST NOT DO section

Violation = **critical failure**.

---

## Critical: `load_skills` is REQUIRED

**`load_skills` is a REQUIRED parameter** for `task()`. Omitting it causes the subagent to lack domain knowledge.

```python
# CORRECT — always pass load_skills
task(
    category="unspecified-high",
    load_skills=["unity/unity-code"],  # REQUIRED — category/skill-name format
    description="Implement health regen",
    prompt="..."
)

# WRONG — missing load_skills → produces poor results
task(
    category="unspecified-high",
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

## Intent Gate (Phase 0)

Before classifying the request, check these triggers:

| Trigger | Action |
|---|---|
| External library/source mentioned | Fire `librarian` background task |
| 2+ modules involved | Fire `explore` background task |
| Ambiguous or complex request | Consult `metis` before planning |
| Work plan created | Invoke `momus` for review before execution |

### Request Classification

| Type | Signal | Action |
|---|---|---|
| **Trivial** | Single file, known location | Direct tools only (unless trigger applies) |
| **Explicit** | Specific file/line, clear command | Execute directly |
| **Exploratory** | "How does X work?", "Find Y" | Fire explore (1-3) + tools in parallel |
| **Open-ended** | "Improve", "Refactor", "Add feature" | Assess codebase first |
| **Ambiguous** | Unclear scope, multiple interpretations | Ask ONE clarifying question |

---

## Category System

Use `category` in `task()` to select the optimal model for the domain. Use EITHER `category` OR `subagent_type`, never both (unless continuing via `session_id`).

| Category | Best For |
|---|---|
| `visual-engineering` | Frontend, UI/UX, design, styling, animation |
| `ultrabrain` | Hard, logic-heavy tasks (give goals, not steps) |
| `deep` | Autonomous problem-solving requiring deep research |
| `artistry` | Unconventional, creative approaches beyond standard patterns |
| `quick` | Trivial — single file changes, typo fixes |
| `unspecified-low` | Misc tasks, low effort |
| `unspecified-high` | Misc tasks, high effort |
| `writing` | Documentation, prose, technical writing |

```python
# Category-based delegation
task(
    category="deep",
    load_skills=["unity/unity-investigate", "unity/unity-debug"],
    description="Root cause analysis of matchmaking failure",
    prompt="..."
)

# Subagent-based delegation (for specific agent types)
task(
    subagent_type="oracle",
    load_skills=[],
    description="Architecture consultation",
    prompt="..."
)
```

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

Before every `task()` call, state:

```
Delegating via task():
- category: [quick|deep|ultrabrain|...] OR subagent_type: [sisyphus|explore|oracle|...]
- Skills: [load_skills values]
- Action: [code|plan|test|review|...]
- Expected outcome: [success criteria]
```

### Generate Prompt

Read template at `assets/templates/DELEGATION_PROMPT.md` and fill placeholders. Every prompt MUST include these 6 sections:

1. **TASK**: Atomic, specific goal (one action per delegation)
2. **EXPECTED OUTCOME**: Concrete deliverables with success criteria
3. **REQUIRED TOOLS**: Explicit tool whitelist (prevents tool sprawl)
4. **MUST DO**: Exhaustive requirements — follow skill, create todos, run diagnostics, `Read` all modified files, comply with `.opencode/rules/`
5. **MUST NOT DO**: Forbidden actions — push to remotes, add AI metadata, destructive actions without confirmation
6. **CONTEXT**: File paths, existing patterns, constraints

Also include: "FIRST: Load Required Skill" pointing to `.opencode/skills/{category}/{skill-name}/SKILL.md`, and "Use `/handoff` if context is getting long".

### Delegate

```python
# Sync — need result before next step
task(
    category="unspecified-high",
    load_skills=["unity/unity-code"],  # REQUIRED — match task to skill
    description="Brief task description",
    run_in_background=False,
    prompt="..."
)

# Background — parallel independent tasks
task(
    category="unspecified-high",
    load_skills=["unity/unity-optimize-performance"],  # REQUIRED
    description="Brief task description",
    run_in_background=True,
    prompt="..."
)
# Collect later: background_output(task_id="...")

# Resume previous session (session continuity)
task(
    session_id="ses_abc123",  # Validated session_id
    load_skills=["unity/unity-code"],  # REQUIRED even on resume
    description="Continue implementation",
    run_in_background=False,
    prompt="Fix: specific issue from previous attempt"
)
```

---

## Subagent Selection Guide

Not all tasks require category-based delegation. Use `subagent_type` for specialized agents:

| Subagent | Cost | Use When | Example |
|---|---|---|---|
| **explore** | FREE | Codebase exploration, finding patterns, architecture understanding | "How is matchmaking structured?" |
| **librarian** | CHEAP | External docs, OSS examples, library best practices | "How does UniTask handle cancellation?" |
| **oracle** | EXPENSIVE | Read-only high-IQ consultant — architecture, debugging after 2+ failures | "What's the best pattern for cross-system communication?" |
| **metis** | EXPENSIVE | Pre-planning — identifies hidden intentions, ambiguities, failure points | Complex/ambiguous request before planning |
| **momus** | EXPENSIVE | Expert reviewer — evaluates plans for clarity, verifiability, completeness | Review a work plan before execution |

### Explore/Librarian Prompt Structure

These agents are contextual grep tools. Fire liberally, always in background. Structure prompts with:

```
[CONTEXT]: What task I'm working on, which files/modules are involved
[GOAL]: The specific outcome I need — what decision this unblocks
[DOWNSTREAM]: How I will use the results — what I'll build/decide
[REQUEST]: Concrete search instructions — what to find, format, what to SKIP
```

### Spawning Examples

**Explore (background) + Implement:**
```python
task(subagent_type="explore", load_skills=[], description="Understand PlayerHealth",
    run_in_background=True, prompt="[CONTEXT]: Implementing health regen...[REQUEST]: Find health scripts, data flow, UI bindings. Skip tests.")
# Continue working, collect later with background_output(task_id="...")
task(category="unspecified-high", load_skills=["unity/unity-code"],
    description="Add health regen", run_in_background=False, prompt="FIRST: Load Required Skill\n...")
```

**Parallel background tasks:**
```python
task(category="unspecified-high", load_skills=["unity/unity-optimize-performance"],
    description="Optimize particles", run_in_background=True, prompt="...")
task(category="unspecified-high", load_skills=["unity/unity-refactor"],
    description="Refactor UI controllers", run_in_background=True, prompt="...")
```

**Multi-skill delegation:**
```python
task(category="visual-engineering", load_skills=[
    "unity/ui-toolkit/ui-toolkit-master", "unity/ui-toolkit/ui-toolkit-databinding",
    "unity/ui-toolkit/ui-toolkit-theming"], description="Build settings screen",
    run_in_background=False, prompt="FIRST: Load Required Skills\n...")
```

---

## Session Continuity & Context Preservation

Every `task()` output includes a `session_id`. **Reuse it** for follow-ups instead of starting fresh — the subagent retains full conversation context, saving 70%+ tokens.

| Scenario | Action |
|---|---|
| Task failed/incomplete | `session_id="{id}", prompt="Fix: {specific error}"` |
| Follow-up on result | `session_id="{id}", prompt="Also: {question}"` |
| Multi-turn with same agent | Always reuse `session_id` — never start fresh |
| Verification failed | `session_id="{id}", prompt="Failed verification: {error}. Fix."` |

Rules:
- Validate `session_id` via `session_list()` / `session_info()` before reuse
- Include "Use `/handoff` if context is getting long" in every delegation prompt
- `/handoff` preserves full context for the next session

## Post-Delegation Verification

After ANY delegated work returns, ALWAYS verify before reporting success:

1. **Works as expected?** — Does the result match the EXPECTED OUTCOME?
2. **Follows codebase patterns?** — Consistent with existing code style and conventions?
3. **Expected result?** — Deliverables complete, no regressions?
4. **Followed MUST DO / MUST NOT DO?** — Check every requirement was met

If verification fails → resume via `session_id` with specific failure details. Do NOT start a new task.

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
| Starting fresh task instead of reusing session_id | Resume via `session_id` — subagent retains full context |
| Skipping post-delegation verification | ALWAYS verify: works, follows patterns, met MUST DO/MUST NOT DO |

---

## Output

Successful orchestration produces:
1. **Clarity analysis** — scored assessment of the raw request
2. **Clarifying questions** — if needed, asked via `question` tool
3. **Refined prompt preview** — shown to user for approval
4. **User confirmation** — yes/no/edit recorded
5. **Delegation log** — subagent_type, action, skill, expected outcome (before each call)
6. **Subagent result** — completed work from Sisyphus
7. **Post-delegation verification** — works as expected, follows patterns, met all MUST DO / MUST NOT DO
8. **File verification** — all modified files confirmed read (Atlas review compliance)
9. **Clean commits** — if committing: no AI metadata, imperative messages only

---

## Path Reference

- Skills: `.opencode/skills/{category}/{skill-name}/SKILL.md`
- UI Toolkit sub-skills: `.opencode/skills/unity/ui-toolkit/{sub-skill-name}/SKILL.md`
- Rules: `.opencode/rules/{agent-behavior,unity-csharp-conventions,unity-asset-rules}.md`
- Categories: `unity/`, `omo/`, `other/`, `bash/`, `git/`
- Use `skill(name="{category}/{skill-name}")` for automatic path resolution
- Skills live under `.opencode/skills/`, NOT `.claude/skills/`
- **Total skills**: 44 (16 Unity core + 3 UI/UX + 1 art + 2 deploy + 2 docs + 9 UI Toolkit + 3 git + 3 bash + 2 omo + 3 other)

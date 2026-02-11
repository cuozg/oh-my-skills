---
name: omo-sisyphus
description: "Orchestrator that delegates tasks to Sisyphus agent via call_omo_agent(subagent_type='sisyphus'). Generates structured prompts with mandatory skill loading, /handoff context preservation, and Atlas manual review compliance. Supports boulder continuation for Sisyphus sessions (v3.5.0+), category disable control, and improved session_id safety guards (v3.5.2). Use for complex tasks requiring planning, delegation, or multi-step work. Triggers: 'delegate to sisyphus', 'use sisyphus', complex multi-step requests."
---

# Sisyphus Orchestrator

Generate Sisyphus-compatible prompts and delegate via `call_omo_agent(subagent_type="sisyphus")`.

## Purpose

Orchestrate complex, multi-step tasks by generating structured delegation prompts and dispatching them to the Sisyphus agent, ensuring mandatory skill loading, context preservation via `/handoff`, and Atlas manual review compliance.

## Input

- **Required**: Task description with clear intent (e.g., "Implement player health bar UI", "Fix compilation errors in GameManager")
- **Required**: Skill selection — must map intent to one skill from the Skill Selection table
- **Optional**: `session_id` for boulder continuation of a previous Sisyphus session (must be validated)

## Examples

| User Request | Selected Skill | Delegation Mode |
|:---|:---|:---|
| "Implement the inventory system from the plan" | `unity-plan-executor` | Sync (need result) |
| "Write unit tests for PlayerController" | `unity-test` | Sync |
| "Review PR #25141 for performance issues" | `unity-review-pr` | Sync |
| "Optimize the particle system and refactor the UI" | `unity-optimize-performance` + `unity-refactor` | Background (parallel) |
| "Create a FlatBuffers schema for match data" | `flatbuffers-coder` | Sync |

## Hard Constraints

| Rule | Detail |
|------|--------|
| **subagent_type** | Always `"sisyphus"`. No exceptions. |
| **Skill loading** | Every prompt MUST begin with "FIRST: Load Required Skill" section. |
| **Skill Loading Requirement** | When Sisyphus receives a delegated prompt, it MUST execute the "FIRST: Load Required Skill" section before proceeding with any analysis, prompt generation, or task execution. Skill loading is a prerequisite gate—no negotiations, no exceptions. |
| **Context preservation** | Use `/handoff` when context is long. Include in all prompts. |
| **Atlas manual review** | Delegated prompts MUST instruct subagent to use `Read` on all modified files before reporting completion. The orchestrator (Atlas) will verify file reads occurred. Omitting this causes review rejection. |
| **Boulder continuation** | Sisyphus sessions can now participate in boulder continuation (v3.5.0+). Pass valid `session_id` to resume previous Sisyphus sessions. Ensure `session_ids` are validated — invalid IDs cause delegation chain failures. |

---

## RESTRICTIONS (NON-NEGOTIABLE)

> [!CAUTION]
> **The following actions are ABSOLUTELY FORBIDDEN — no exceptions, no overrides.**

- **NEVER** add co-author, committer, or any AI-related metadata to git commits
- **NEVER** include `Co-authored-by:`, `Tool-generated-by:`, or similar attribution lines in commit messages
- **NEVER** run `git push` to any remote
- **NEVER** run destructive git write operations (merge, rebase, tag, etc.)
- **NEVER** instruct the subagent to push to remotes or add AI metadata to commits
- **NEVER** perform destructive actions (file/asset deletion, scene overwrites) without explicit user confirmation _(agent-behavior: Safety First)_
- Commits MUST include only: message, changed files, timestamp — no author, co-author, or tool metadata
- Commits are allowed ONLY to the current branch
- These restrictions apply to BOTH the orchestrator AND any delegated subagent
- Include `"NEVER push to git remotes or add AI metadata to commits"` in every delegation prompt's MUST NOT DO section

Violation of any restriction above is a **critical failure**.

---

## Project Rules Compliance (MANDATORY)

All delegated prompts MUST enforce compliance with `.claude/rules/`. Include these requirements in every delegation:

### From `agent-behavior.md`

- **Safety First**: No destructive actions without explicit user confirmation
- **Proactive**: Suggest next steps after completing tasks
- **Unity Best Practices**: Follow Prefab workflows, ScriptableObjects, Component patterns
- **Tool Mastery**: Use `unityMCP` for Editor tasks over shell commands
- **Communication**: Explain "Why" for architectural decisions, provide evidence-based verification
- **Interaction Pattern**: Discover → Plan → Execute → Collaborate

### From `unity-csharp-conventions.md`

- **Naming**: Classes/Methods=PascalCase, private fields=_camelCase, locals=camelCase, constants=PascalCase
- **Architecture**: Component-Based SRP, ScriptableObjects for config, Object Pooling for frequent instantiation, Assembly Definitions
- **Unity 6**: Prefer `Awaitable` over Coroutines with `if (this == null) return` safety check
- **Performance**: Avoid `Update()` (use events/reactive), cache `GetComponent`/`Camera.main` in `Awake`/`Start`, no string concat in hot paths, avoid boxing
- **Testing**: `Tests/EditMode/` and `Tests/PlayMode/`, naming `[Subject]_[Scenario]_[ExpectedResult]`

### From `unity-asset-rules.md`

- **Project Structure**: Follow `Assets/_Project/` hierarchy (Scripts by feature, Prefabs, Materials, Textures, Scenes)
- **Asset Naming**: Prefabs=PascalCase, Materials=PascalCase_Purpose, Textures=PascalCase_Suffix, Scenes=PascalCase
- **Optimization**: Textures max 2048 mobile/4096 PC (ASTC 6x6, disable Read/Write), models <100k tris/scene mobile with LOD, materials URP/Lit or SimpleLit
- **Prefab Workflow**: Use nested prefabs, variants from base, verify in Prefab Mode before applying

---

## Skill Selection

| User Intent | Skill |
|-------------|-------|
| Write/implement code | `unity-code` |
| Plan/estimate/breakdown | `unity-plan` |
| Write tests | `unity-test` |
| Review PR | `unity-review-pr` |
| Execute task file | `unity-plan-executor` |
| Detail task plan | `unity-plan-detail` |
| Investigate codebase | `unity-investigate` |
| Fix compilation errors | `unity-fix-errors` |
| Debug issues | `unity-debug` |
| Generate flatbuffer | `flatbuffers-coder` |
| Generate diagram | `mermaid` |
| Check bash script | `bash-check` |
| Create/update skill | `skill-creator` |
| Shader/art pipeline work | `unity-tech-art` |
| Editor tools/inspectors | `unity-editor-tools` |
| Performance optimization | `unity-optimize-performance` |
| Refactoring | `unity-refactor` |
| Mobile deployment | `unity-mobile-deploy` |
| WebGL deployment | `unity-web-deploy` |
| UI implementation from design | `unity-ui` |
| Documentation | `unity-write-docs` |
| Technical Design Document | `unity-write-tdd` |
| Generate and commit code changes | `git-commit` |
| `use skill <name> ...` | `<name>` |
| No specific skill | Justify omission |

> **Note (v3.5.0):** Sisyphus can now use `TaskCreate`/`TaskUpdate`/`TaskList` internally for task tracking. No skill routing change needed — this is an executor capability, not a user-facing intent.

---

## v3.5.0 Enhancements

> oh-my-opencode v3.5.0 "Atlas Trusts No One" (2026-02-10)

### Sisyphus Boulder Continuation

Sisyphus sessions can now participate in boulder continuation (previously Atlas-only). To resume a previous Sisyphus session, pass `session_id` to `call_omo_agent()`:

```python
call_omo_agent(
    subagent_type="sisyphus",
    session_id="ses_abc123",  # Resume previous session
    description="Continue implementation",
    run_in_background=False,
    prompt="..."
)
```

- Validate `session_id` before passing — invalid IDs cause delegation chain failures
- Use `session_list()` or `session_info()` to verify session exists
- 500ms session idle dedup window prevents double-firing of continuation hooks

### Sisyphus TaskCreate/Update/List

Sisyphus (the executor) can now use `TaskCreate`, `TaskUpdate`, and `TaskList` tools directly without triggering the delegation tool block. This enables better task tracking within delegated work.

### Skill @path Auto-Resolution

Relative `@scripts/` paths in delegation prompt templates now auto-resolve to absolute paths. No manual path construction needed — use `@scripts/my_script.py` in templates and they resolve correctly.

### Session ID Validation

`session_ids` validation is now enforced in boulder continuation. Invalid or stale session IDs are rejected with clear error messages instead of silently failing. Always verify session validity before resuming.

> **v3.5.2 update:** Optional chaining guard added on `session_ids` in boulder state reads — prevents crashes when session references are null/undefined. The orchestrator no longer needs defensive null checks before accessing session state; the framework handles it internally.

---

## v3.5.2 Enhancements

> oh-my-opencode v3.5.2 (2026-02-11)

### Auto-Update Safety

- Pinned plugin versions are now respected — auto-update skips when a version is explicitly locked in config
- If an update install fails, the config pin reverts to the previous version to prevent mismatch between config and disk
- No orchestrator action needed — this is framework-level safety for plugin management

### Subagent Lifecycle Fixes

- Fixed zombie sessions caused by `permission.question=deny` override in subagent spawning — delegated Sisyphus sessions now terminate cleanly when permissions block execution
- Added optional chaining guard on `session_ids` to prevent crashes in boulder state reads (see [Session ID Validation](#session-id-validation) above)

### MCP Tool Guard

- Tool after-hooks now safely guard `output.output` for MCP tools that return non-standard shapes
- Prevents crashes when MCP tools return unexpected response structures during delegated work
- No orchestrator action needed — the framework handles malformed MCP responses transparently

### Atlas Intelligence

- Boulder verification reminders now include a notepad reading step — Atlas checks its own notes before prompting the orchestrator for continuation
- Results in more context-aware continuation prompts and fewer redundant verification questions

### Category Control

New `disable` field in `CategoryConfigSchema` allows turning off entire delegation categories without removing their config.

Use in delegation prompts when a specific category should be temporarily suppressed:

```python
# Example: disable the "quick" category for a session
# (configured in oh-my-opencode settings, not in call_omo_agent)
# CategoryConfigSchema: { "quick": { "disable": true } }
```

- **What it does**: Prevents tasks from being routed to a disabled category, even if the category config remains in place
- **When to use**: Temporarily suppress a category during debugging, maintenance, or when a category's subagent is misbehaving
- **Delegation impact**: If a category is disabled, tasks that would normally route there will fall through to `unspecified-low` or `unspecified-high` instead
- **In delegation prompts**: Document any disabled categories in the Context section so the subagent understands routing constraints

---

## Git Integration

### Git Commit Capability

omo-sisyphus can now generate commit messages and commit changes to the current branch. All commits are **clean** — no AI metadata, no co-authors, no tool attribution.

#### Commit Rules

- Commits are allowed to the **current branch only** (never push to remotes)
- Commit messages must be **short, meaningful, and imperative**
- Use **bullet points** for multiple changes in the body
- **Zero metadata**: no `Co-authored-by:`, `Tool-generated-by:`, or similar lines

#### Commit Message Format

```
<type>: <subject>

<body (optional, use bullets)>
```

Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `perf`, `style`

#### Examples

**Good**:
```
fix: resolve null reference in PlayerManager initialization
```

```
refactor: decouple UI from data managers

- Extract data access to interfaces
- Implement adapter pattern for data sources
- Update controllers to use adapters
```

**Bad** (NEVER do this):
```
fix: resolve null reference in PlayerManager initialization

Co-authored-by: Claude AI <claude@anthropic.com>
Tool-generated-by: oh-my-opencode
```

#### Delegation with Commits

When delegating tasks that include committing, use the `git-commit` skill for atomic commits with generated messages. Include in the delegation prompt:

```
MUST DO:
- Generate clean commit message (no AI metadata)
- Commit to current branch only

MUST NOT DO:
- NEVER add Co-authored-by or AI attribution
- NEVER push to remote
```

---

## Workflow

### 1. Plan Delegation

Before every `call_omo_agent()`:

```
Delegating via call_omo_agent():
- subagent_type: "sisyphus"
- Action: [code|plan|test|review|...]
- Skill: [skill-name]
- Expected outcome: [success criteria]
```

### 1.5 Mandatory Skill Loading Gate

**This is MANDATORY before step 2.**

When delegated a prompt:
1. Sisyphus immediately loads the required skill using the "FIRST: Load Required Skill" section from the delegated prompt
2. No analysis or prompt generation proceeds until skill is fully loaded
3. Loading is atomic and uninterruptible—if loading fails, stop and report the error
4. Skill context becomes the foundation for all downstream work

### 2. Generate Prompt

Read template at `assets/templates/DELEGATION_PROMPT.md` and fill placeholders. Every prompt MUST:

1. Start with "FIRST: Load Required Skill" section pointing to `.claude/skills/[skill-name]/SKILL.md`
2. Include atomic task description
3. Include concrete expected outcome
4. MUST DO: "Follow skill EXACTLY", create todos, run diagnostics, use `Read` on all modified files, comply with `.claude/rules/`
5. MUST NOT DO: "NEVER push to git remotes or add AI metadata to commits", skip skill, suppress type errors, destructive actions without confirmation
6. Include "Use `/handoff` if context is getting long"
7. Include rule compliance reminder referencing all 3 rule files

### 3. Delegate

```python
# Sync (need result before next step)
call_omo_agent(
    subagent_type="sisyphus",
    description="Brief task description",
    run_in_background=False,
    prompt="..."
)

# Background (parallel tasks)
call_omo_agent(
    subagent_type="sisyphus",
    description="Brief task description",
    run_in_background=True,
    prompt="..."
)
# Collect later: background_output(task_id="...")
```

---

## Anti-Patterns

| Bad | Good |
|-----|------|
| `subagent_type="explore"` | `subagent_type="sisyphus"` |
| Missing skill load section | "FIRST: Load Required Skill" at top |
| No git restrictions in MUST NOT DO | "NEVER push to git remotes or add AI metadata to commits" |
| Instructing subagent to push to remote | Explicitly forbidding push and AI metadata |
| Including co-author or AI metadata in commits | Clean commit messages with no tool/AI information |
| `Co-authored-by: Claude AI` in commit | Simple message: `fix: resolve null reference` |
| Generic prompt without skill ref | Prompt references loaded skill |
| Sisyphus skips skill loading | Sisyphus MUST load skill as first action; failure to load is critical failure |
| Prompt generation before loading skill | Always load skill first, THEN generate prompts based on loaded skill context |
| No rule compliance in delegation | Include `.claude/rules/` compliance in MUST DO |
| Using shell commands for Editor tasks | Use `unityMCP` tools _(agent-behavior: Tool Mastery)_ |
| Destructive actions without confirmation | Require explicit user confirmation _(agent-behavior: Safety First)_ |
| Ignoring C# naming conventions | Enforce PascalCase/_camelCase per `unity-csharp-conventions.md` |
| Skipping Discover phase | Follow Discover → Plan → Execute → Collaborate _(agent-behavior)_ |
| Subagent skips `Read` on modified files | Delegation prompt MUST require `Read` on all changed files _(Atlas review)_ |
| Passing unvalidated `session_id` | Verify session exists via `session_list()`/`session_info()` before resuming |
| Omitting file read verification in prompts | Include "Use `Read` on every modified file before completion" in MUST DO |
| Ignoring disabled categories in delegation context | Document disabled categories in Context section so subagent understands routing constraints |

---

## Output

Successful delegation produces:
1. **Delegation log** — subagent_type, action, skill, and expected outcome stated before each `call_omo_agent()`
2. **Subagent result** — the completed work from Sisyphus (code changes, reports, plans, etc.)
3. **File verification** — all modified files confirmed read by subagent before completion (Atlas review compliance)
4. **Clean commits** — if committing: message contains only type, subject, and optional body (no AI metadata, no co-authors)

The orchestrator does NOT generate separate report files. Results are communicated directly.

---

## Checklist

- [ ] **FIRST: Skill loading executed and confirmed** (mandatory gate before all else)
- [ ] Skill context is available for prompt generation
- [ ] `subagent_type="sisyphus"` specified
- [ ] Correct skill selected for action type
- [ ] Prompt has "FIRST: Load Required Skill" section
- [ ] MUST DO includes "Follow skill EXACTLY as loaded above"
- [ ] MUST DO includes "Use `Read` on every modified file before reporting completion" _(Atlas review)_
- [ ] MUST DO includes "Comply with all `.claude/rules/` (agent-behavior, unity-csharp-conventions, unity-asset-rules)"
- [ ] MUST NOT DO includes "NEVER push to git remotes or add AI metadata to commits"
- [ ] MUST NOT DO includes "NEVER perform destructive actions without explicit user confirmation"
- [ ] `/handoff` mentioned for context preservation
- [ ] Background vs sync mode is intentional
- [ ] Interaction pattern follows Discover → Plan → Execute → Collaborate
- [ ] If resuming session: `session_id` validated via `session_list()`/`session_info()`
- [ ] If categories disabled: documented in delegation prompt Context section _(v3.5.2)_
- [ ] If committing code: verified commit message has no co-author or AI metadata
- [ ] If committing code: message is short, meaningful, uses imperative mood and bullets for multiple changes

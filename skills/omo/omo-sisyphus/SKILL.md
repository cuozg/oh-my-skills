---
name: omo-sisyphus
description: "Orchestrator that delegates tasks to Sisyphus agent via call_omo_agent(subagent_type='sisyphus'). Generates structured prompts with mandatory skill loading, /handoff context preservation, and Atlas manual review compliance. Supports boulder continuation for Sisyphus sessions (v3.5.0+). Use for complex tasks requiring planning, delegation, or multi-step work. Triggers: 'delegate to sisyphus', 'use sisyphus', complex multi-step requests."
---

# Sisyphus Orchestrator

Generate Sisyphus-compatible prompts and delegate via `call_omo_agent(subagent_type="sisyphus")`.

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

- **NEVER** run `git commit` in any form
- **NEVER** run `git push` to any remote
- **NEVER** run destructive git write operations (merge, rebase, tag, etc.)
- **NEVER** instruct the subagent to commit or push
- **NEVER** perform destructive actions (file/asset deletion, scene overwrites) without explicit user confirmation _(agent-behavior: Safety First)_
- These restrictions apply to BOTH the orchestrator AND any delegated subagent
- Include `"NEVER commit or push to git"` in every delegation prompt's MUST NOT DO section

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
| `use skill <name> ...` | `<name>` |
| No specific skill | Justify omission |

> **Note (v3.5.0):** Sisyphus-Junior can now use `TaskCreate`/`TaskUpdate`/`TaskList` internally for task tracking. No skill routing change needed — this is an executor capability, not a user-facing intent.

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

### Sisyphus-Junior TaskCreate/Update/List

Sisyphus-Junior (the executor) can now use `TaskCreate`, `TaskUpdate`, and `TaskList` tools directly without triggering the delegation tool block. This enables better task tracking within delegated work.

### Skill @path Auto-Resolution

Relative `@scripts/` paths in delegation prompt templates now auto-resolve to absolute paths. No manual path construction needed — use `@scripts/my_script.py` in templates and they resolve correctly.

### Session ID Validation

`session_ids` validation is now enforced in boulder continuation. Invalid or stale session IDs are rejected with clear error messages instead of silently failing. Always verify session validity before resuming.

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
5. MUST NOT DO: "NEVER commit or push to git", skip skill, suppress type errors, destructive actions without confirmation
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
| No git restrictions in MUST NOT DO | "NEVER commit or push to git" |
| Instructing subagent to commit | Explicitly forbidding commits |
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
- [ ] MUST NOT DO includes "NEVER commit or push to git"
- [ ] MUST NOT DO includes "NEVER perform destructive actions without explicit user confirmation"
- [ ] `/handoff` mentioned for context preservation
- [ ] Background vs sync mode is intentional
- [ ] Interaction pattern follows Discover → Plan → Execute → Collaborate
- [ ] If resuming session: `session_id` validated via `session_list()`/`session_info()`

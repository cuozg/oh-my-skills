---
name: omo-sisyphus
description: "Orchestrator that delegates tasks to Sisyphus agent via call_omo_agent(subagent_type='sisyphus'). Generates structured prompts with mandatory skill loading, /handoff context preservation, and Atlas manual review compliance. Use for complex tasks requiring planning, delegation, or multi-step work. Triggers: 'delegate to sisyphus', 'use sisyphus', complex multi-step requests."
---

# Sisyphus Orchestrator

Delegate tasks to Sisyphus via `call_omo_agent(subagent_type="sisyphus")`.

## Purpose

Orchestrate complex, multi-step tasks by generating structured delegation prompts, dispatching them to Sisyphus, and ensuring mandatory skill loading, context preservation, and Atlas review compliance.

## Input

- **Required**: Task description with clear intent
- **Required**: Skill selection — map intent to a skill from the Skill Selection table
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

## Skill Selection

| User Intent | Skill |
|---|---|
| Write/implement code | `unity-code` |
| Plan/estimate/breakdown | `unity-plan` |
| Write tests | `unity-test` |
| Review PR | `unity-review-pr` |
| Execute task file | `unity-plan-executor` |
| Detail task plan | `unity-plan-detail` |
| Investigate codebase | `unity-investigate` |
| Fix compilation errors | `unity-fix-errors` |
| Debug issues | `unity-debug` |
| FlatBuffers schema | `flatbuffers-coder` |
| Generate diagram | `mermaid` |
| Check bash script | `bash-check` |
| Create/update skill | `skill-creator` |
| Shader/art pipeline | `unity-tech-art` |
| Editor tools/inspectors | `unity-editor-tools` |
| Performance optimization | `unity-optimize-performance` |
| Refactoring | `unity-refactor` |
| Mobile deployment | `unity-mobile-deploy` |
| WebGL deployment | `unity-web-deploy` |
| UI from design | `unity-ui` |
| UX design | `unity-ux-design` |
| Documentation | `unity-write-docs` |
| Technical Design Doc | `unity-write-tdd` |
| Generate and commit | `git-commit` |
| `use skill <name> ...` | `<name>` |
| No specific skill | Justify omission |

---

## Workflow

### 1. Plan Delegation

Before every `call_omo_agent()`, state:

```
Delegating via call_omo_agent():
- subagent_type: "sisyphus"
- Action: [code|plan|test|review|...]
- Skill: [skill-name]
- Expected outcome: [success criteria]
```

### 2. Generate Prompt

Read template at `assets/templates/DELEGATION_PROMPT.md` and fill placeholders. Every prompt MUST:

1. Start with "FIRST: Load Required Skill" pointing to `.opencode/skills/{category}/{skill-name}/SKILL.md`
2. Include atomic task description and concrete expected outcome
3. MUST DO: follow skill, create todos, run diagnostics, `Read` all modified files, comply with `.opencode/rules/`
4. MUST NOT DO: push to remotes, add AI metadata, destructive actions without confirmation
5. Include "Use `/handoff` if context is getting long"

### 3. Delegate

```python
# Sync — need result before next step
call_omo_agent(
    subagent_type="sisyphus",
    description="Brief task description",
    run_in_background=False,
    prompt="..."
)

# Background — parallel independent tasks
call_omo_agent(
    subagent_type="sisyphus",
    description="Brief task description",
    run_in_background=True,
    prompt="..."
)
# Collect later: background_output(task_id="...")

# Resume previous session (boulder continuation)
call_omo_agent(
    subagent_type="sisyphus",
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

**Example 1: Explore first, then implement**
```python
# Understand the system before implementing
explore_result = call_omo_agent(
    subagent_type="explore",
    description="Understand PlayerHealth system",
    run_in_background=False,
    prompt="Trace how player health is managed — find related scripts, data flow, UI bindings."
)

# Then delegate implementation with loaded skill
call_omo_agent(
    subagent_type="sisyphus",
    description="Add health regeneration feature",
    run_in_background=False,
    prompt="FIRST: Load Required Skill\n..."  # Fill DELEGATION_PROMPT.md template
)
```

**Example 2: Parallel Sisyphus tasks**
```python
# Two independent tasks in parallel
call_omo_agent(
    subagent_type="sisyphus",
    description="Optimize particle system",
    run_in_background=True,
    prompt="..."  # skill: unity-optimize-performance
)
call_omo_agent(
    subagent_type="sisyphus",
    description="Refactor UI controllers",
    run_in_background=True,
    prompt="..."  # skill: unity-refactor
)
# Collect: background_output(task_id="...")
```

**Example 3: Long task with /handoff**
```python
call_omo_agent(
    subagent_type="sisyphus",
    description="Implement full lobby screen",
    run_in_background=False,
    prompt="""FIRST: Load Required Skill
    Load: .opencode/skills/unity/unity-code/SKILL.md

    Task: Implement lobby screen with player stats, matchmaking, and chat.

    MUST DO:
    - Use /handoff if context is getting long — preserves full context
      for continuation in a new session. PREFER /handoff over compaction.
    ..."""
)
```

---

## Context Preservation

**For long-running tasks, always use `/handoff`** instead of letting context compact:
- `/handoff` creates a detailed summary preserving full context for the next session
- Include "Use `/handoff` if context is getting long" in every delegation prompt
- To resume: pass the previous `session_id` to `call_omo_agent()` (boulder continuation)
- Always validate `session_id` via `session_list()`/`session_info()` before resuming

---

## Anti-Patterns

| Bad | Good |
|---|---|
| `subagent_type="explore"` for implementation | `subagent_type="sisyphus"` |
| Missing skill load section in prompt | "FIRST: Load Required Skill" at top |
| No git restrictions in MUST NOT DO | Include push/metadata restrictions |
| Prompt generation before loading skill | Load skill first, then generate |
| Subagent skips `Read` on modified files | Require `Read` on all changed files |
| Passing unvalidated `session_id` | Verify via `session_list()` first |

---

## Output

Successful delegation produces:
1. **Delegation log** — subagent_type, action, skill, expected outcome (before each call)
2. **Subagent result** — completed work from Sisyphus
3. **File verification** — all modified files confirmed read (Atlas review compliance)
4. **Clean commits** — if committing: no AI metadata, imperative messages only

---

## Path Reference

- Skills: `.opencode/skills/{category}/{skill-name}/SKILL.md`
- Rules: `.opencode/rules/{agent-behavior,unity-csharp-conventions,unity-asset-rules}.md`
- Categories: `unity/`, `omo/`, `other/`, `bash/`, `git/`
- Use `skill(name="{category}/{skill-name}")` for automatic path resolution
- Skills live under `.opencode/skills/`, NOT `.claude/skills/`

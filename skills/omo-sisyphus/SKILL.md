---
name: omo-sisyphus
description: "Orchestrator that delegates tasks to Sisyphus agent via call_omo_agent(subagent_type='sisyphus'). Generates structured prompts with mandatory skill loading and /handoff context preservation. Use for complex tasks requiring planning, delegation, or multi-step work. Triggers: 'delegate to sisyphus', 'use sisyphus', complex multi-step requests."
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

---

## RESTRICTIONS (NON-NEGOTIABLE)

> [!CAUTION]
> **The following actions are ABSOLUTELY FORBIDDEN — no exceptions, no overrides.**

- **NEVER** run `git commit` in any form
- **NEVER** run `git push` to any remote
- **NEVER** run destructive git write operations (merge, rebase, tag, etc.)
- **NEVER** instruct the subagent to commit or push
- These restrictions apply to BOTH the orchestrator AND any delegated subagent
- Include `"NEVER commit or push to git"` in every delegation prompt's MUST NOT DO section

Violation of any restriction above is a **critical failure**.

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
| `use skill <name> ...` | `<name>` |
| No specific skill | Justify omission |

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
4. MUST DO: "Follow skill EXACTLY", create todos, run diagnostics
5. MUST NOT DO: "NEVER commit or push to git", skip skill, suppress type errors
6. Include "Use `/handoff` if context is getting long"

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

---

## Checklist

- [ ] **FIRST: Skill loading executed and confirmed** (mandatory gate before all else)
- [ ] Skill context is available for prompt generation
- [ ] `subagent_type="sisyphus"` specified
- [ ] Correct skill selected for action type
- [ ] Prompt has "FIRST: Load Required Skill" section
- [ ] MUST DO includes "Follow skill EXACTLY as loaded above"
- [ ] MUST NOT DO includes "NEVER commit or push to git"
- [ ] `/handoff` mentioned for context preservation
- [ ] Background vs sync mode is intentional

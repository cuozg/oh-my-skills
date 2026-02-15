---
name: omo-prompt-enhancer
description: "Lightweight prompt enhancer that sharpens vague user requests into precise, actionable prompts, then delegates to @sisyphus-junior for execution. Focuses ONLY on prompt improvement — no orchestration, no planning. Rewrites first, asks later. Use when: (1) User prompt is vague or underspecified, (2) Prompt needs structure before delegation, (3) User says 'enhance this', 'improve prompt', 'sharpen this request'. Triggers: 'enhance prompt', 'sharpen prompt', 'improve this prompt', 'make this actionable', 'prompt enhance', 'refine and delegate'."
---

# Prompt Enhancer

Sharpen raw user input into a precise prompt, then delegate to `@sisyphus-junior`.

## Flow

`Receive -> Rewrite -> Confirm -> Delegate`

## Step 1: Rewrite (No Questions)

Transform the raw request. Apply ALL of these:

1. **Extract real intent** — what they want, not what they said
2. **Add specificity** — replace "fix/improve/update" with concrete verbs
3. **Fill gaps** — infer defaults, mark with `[ASSUMED: ...]`
4. **Define done** — add success criteria
5. **Bound scope** — add what's NOT included

Output format:

```
## Enhanced Prompt

**Goal**: [1-2 sentences — what and why]
**Scope**: [files, systems, boundaries]
**Requirements**:
1. [specific, verifiable]
2. ...
**Constraints**: [what NOT to do, style rules]
**Success Criteria**: [checkable outcomes]
**Out of Scope**: [excluded items]
**Assumptions**: [list ASSUMED items for user to verify]
```

## Step 2: Confirm

Show the enhanced prompt. Ask user via `question` tool:
- **Delegate now** — proceed to Step 3
- **Edit** — user provides changes, re-enhance

## Step 3: Delegate

Select appropriate `load_skills` from skill inventory. Compose delegation:

```python
task(
    subagent_type="sisyphus-junior",
    load_skills=["<matched-skill>"],  # REQUIRED
    description="<brief>",
    run_in_background=False,
    prompt="<enhanced prompt with MUST DO / MUST NOT DO sections>"
)
```

**ALWAYS return the `session_id`** from the task result to the user for continuity.

### Delegation prompt MUST include:

- **TASK**: The enhanced goal
- **MUST DO**: Follow loaded skill, create todos for 2+ steps, run `lsp_diagnostics` on changed files
- **MUST NOT DO**: Push to remotes, add AI metadata to commits, delete files without confirmation

## Skill Quick Lookup

| Intent | `load_skills` |
|---|---|
| Write/implement C# | `unity/unity-code` |
| Fix errors | `unity/unity-fix-errors` |
| Debug runtime | `unity/unity-debug` |
| Plan feature | `unity/unity-plan` |
| Refactor | `unity/unity-refactor` |
| Review PR | `unity/unity-review-pr` |
| Optimize perf | `unity/unity-optimize-performance` |
| Write tests | `unity/unity-test` |
| Editor tools | `unity/unity-editor-tools` |
| UI from spec | `unity/unity-ui` |
| Commit | `git/git-commit` |
| Create skill | `other/skill-creator` |

## Rules

- Rewrite FIRST — never ask questions before producing improved version
- Keep enhanced prompts concise — no padding, no filler
- One delegation per task — split multi-part requests
- ALWAYS return `session_id` from delegation result

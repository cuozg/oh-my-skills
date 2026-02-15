---
description: Enhance prompt then delegate to @sisyphus-junior (2-step pipeline)
agent: sisyphus-junior
model: github-copilot/claude-opus-4.6
subtask: true
---

# Delegate Task — Enhance & Execute Pipeline

You are a 2-step pipeline: **enhance** the user's prompt, then **delegate** execution.

## User Request

$ARGUMENTS

---

## Step 1: Load Prompt Enhancer Skill

Load the `omo/omo-prompt-enhancer` skill:

```
skill("omo/omo-prompt-enhancer")
```

Read and follow ALL instructions from the skill.

## Step 2: Enhance the User Prompt

Apply the prompt enhancer to the user request above. Transform it using ALL of these:

1. **Extract real intent** — what they want, not what they said
2. **Add specificity** — replace vague verbs with concrete ones
3. **Fill gaps** — infer defaults, mark with `[ASSUMED: ...]`
4. **Define done** — add success criteria
5. **Bound scope** — add what's NOT included

Output the enhanced prompt in this format:

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

## Step 3: Show Enhanced Prompt & Confirm

Present the enhanced prompt to the user. Ask via `question` tool:
- **Delegate now** — proceed to Step 4
- **Edit** — user provides changes, re-enhance

## Step 4: Delegate Execution

Select appropriate `load_skills` from the skill inventory below. Delegate to a NEW `@sisyphus-junior` agent:

```python
task(
    subagent_type="sisyphus-junior",
    load_skills=["<matched-skill>"],  # REQUIRED — never empty
    description="<concise 5-10 word description>",
    run_in_background=False,
    prompt="""
TASK: <enhanced goal>

MUST DO:
- Follow loaded skill instructions exactly
- Create todos for 2+ steps
- Run lsp_diagnostics on changed files
- Match existing codebase patterns

MUST NOT DO:
- Push to remotes
- Add AI metadata to commits
- Delete files without confirmation
- Leave code in broken state

CONTEXT:
<any relevant context from the original request>
"""
)
```

## Step 5: Return Results

After the delegated task completes, return to the user:
1. **The `session_id`** from the task result (MANDATORY — for continuity)
2. A brief summary of what was accomplished

---

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
| Investigate system | `unity/unity-investigate` |
| Write docs | `unity/unity-write-docs` |
| Write TDD | `unity/unity-write-tdd` |
| Mobile deploy | `unity/unity-mobile-deploy` |
| Web deploy | `unity/unity-web-deploy` |
| Commit | `git/git-commit` |
| Squash commits | `git/git-squash` |
| Create skill | `other/skill-creator` |
| Serialization | `unity/unity-serialization` |
| Event system | `unity/unity-event-system` |
| Object pooling | `unity/unity-object-pooling` |
| Singleton audit | `unity/unity-singleton-auditor` |
| FlatBuffers | `other/flatbuffers-coder` |

## Rules

- **Rewrite FIRST** — never ask questions before producing the enhanced version
- **ALWAYS return `session_id`** from delegation result — non-negotiable
- One delegation per task — split multi-part requests
- Keep enhanced prompts concise — no padding, no filler
- Never use empty `load_skills=[]`

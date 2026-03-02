---
name: unity-plan-quick
description: Inline plan for XS/S tasks with cost, risk, and task_create. Triggers — 'plan this', 'quick plan', 'estimate this', 'small task plan', 'how long will this take'.
---
# unity-plan-quick

Assess a small Unity task inline and register it in the task system immediately.

## When to Use

- Single-file change or isolated bug fix (XS: 0-2h, S: 2-8h)
- Request needs a quick estimate before work begins
- Task has no cross-system dependencies requiring deep investigation

## Workflow

1. **Parse** — Identify what needs to change and where in the codebase
2. **Investigate** — Run `lsp_find_references` or `grep` to confirm scope (≤3 tool calls)
3. **Cost** — Assign size XS/S, hours estimate, risk level (low/medium/high)
4. **Report** — Print inline plan using the output format below
5. **Create** — Call `task_create` for each task node; set `blockedBy` for dependencies

## Rules

- Cap investigation at 3 tool calls — this is a quick plan, not a deep audit
- Never call `task_create` before the report is printed
- One `task_create` per logical unit of work; split if parallelizable
- Risk must be evidence-based (cite a file or dependency)

## Output Format

`▲ {title}` header, single metadata line `{cost} · {hours} · {risk} risk`, one-sentence summary,
then `┌ Tasks` tree with `├─` / `└─` branches per task (subject + `→ skill:{name}`).

## Reference Files

- `references/task-output-format.md` — Full format spec with examples for the ▲ header and task tree

Load references on demand via `read_skill_file("unity-plan-quick", "references/task-output-format.md")`.

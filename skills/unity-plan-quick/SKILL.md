---
name: unity-plan-quick
description: Inline plan for XS/S tasks with cost, risk, and task_create. Triggers — 'plan this', 'quick plan', 'estimate this', 'small task plan', 'how long will this take'.
---
# unity-plan-quick

Assess a small Unity task and report inline. No file output.

## When to Use

- Single-file change or isolated fix (XS: 0-2h, S: 2-8h)
- Quick estimate before work begins
- No cross-system dependencies

## Workflow

1. **Parse** — Identify what and where
2. **Investigate** — Confirm scope (max 3 tool calls)
3. **Report** — Print inline using the format below
4. **Create** — Call `task_create` per task; set `blockedBy`

## Rules

- **No file output** — report directly in chat, never create .md files
- Cap investigation at 3 tool calls
- Print report before calling `task_create`
- Risk must cite a file or dependency as evidence

## Output Format

```
▲ {Feature Name}
{size} ({cost}) · {hours} · {risk} risk

{1-sentence summary with evidence}

┌ Tasks
├─ {subject}
│  {description}
│  → skill:{skill-name}
└─ {subject}
   {description}
   → skill:{skill-name}
```

## Standards

Load `unity-standards` for sizing and risk. Key references:

- `plan/sizing-guide.md` — XS/S/M/L/XL definitions
- `plan/risk-assessment.md` — risk levels
- `plan/task-structure.md` — subject/description format

Load via `read_skill_file("unity-standards", "references/plan/<file>")`.

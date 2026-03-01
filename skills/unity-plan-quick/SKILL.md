---
name: unity-plan-quick
description: "Quick planning for small/fast Unity tasks. Investigate codebase, report assessment directly (no document output), create tasks via task_create. Use when: (1) Estimating effort for a new feature or change, (2) Quick feasibility check, (3) Understanding risk and blast radius, (4) High-level cost before detailed planning. Triggers: 'quick plan', 'small task', 'plan this quickly', 'fast estimate', 'how big is this', 'estimate this', 'quick cost', 'how long will this take', 'is this a big change', 'feasibility check', 'impact assessment', 'effort estimate', 'scope check', 'size this task'."
---
# Quick Task Plan

**Input**: Feature request, task description, or proposed change.

Senior Unity engineer doing fast task planning. Investigate thoroughly, respond concisely. No documents — report directly, then create tasks.

## Workflow

1. **Parse** — Identify what is asked and which systems are involved.
2. **Investigate** — Search codebase for scope. Use `grep`, `read`, `glob`, `lsp_symbols`, `lsp_find_references`, `impact-analyzer`. Read actual code, trace dependencies.
3. **Assess** — Evaluate size, time, risk, downstream impact.
4. **Report** — Use the output template below. Report inline — no document files.
5. **Create Task** — Record via `task_create`. See task-system-output.md (loaded below).

For investigation checklist and size/time references, see investigation-checklist.md (loaded below).
For a worked example, see plan-quick-example.md (loaded below).

## Output Template

Use this exact format. Vercel-inspired tree. No filler, no fluff.

```
▲ {Feature/Task Name}
  {XS|S|M|L|XL} · {X-Y hours} · {Low|Med|High} risk
  {1 sentence — what this involves, anchored in evidence}

  ┌ Tasks
  ├─ {subject}
  │  {description} → skill:{skill-name}
  ├─ {subject}
  │  {description} → skill:{skill-name}
  └─ {subject}
     {description} → skill:{skill-name}
```

**Rules**:
- `▲` header = feature name. Single metadata line: cost · hours · risk.
- Summary: 1 sentence max. Evidence-anchored (file counts, system refs).
- `┌ Tasks` tree: subject + description + `→ skill:{name}` per entry.
- No headings, no bold, no extra markup inside the tree. Clean monospace.

## Task Creation

After reporting, record in the Task System:

1. **Parent task** — subject `▲ {Name}`, description = full assessment tree text.
2. Set `metadata`: `{cost, costHours, risk, skillSource: "unity-plan-quick"}`.
3. **Child tasks** per `┌ Tasks` entry — subject, description, `parentID` → parent, `metadata.skill` = recommended skill.

See task-system-output.md (loaded below) for call patterns and metadata schema.

## Cross-Skill Pipeline

Entry point of the Prometheus planning pipeline. Downstream skills find assessments via `metadata.skillSource: "unity-plan-quick"`.
For the full pipeline guide, see prometheus-pipeline.md (loaded below).

## Rules

- Investigate deep, respond short — read as much code as needed, output stays compact.
- No implementation details — describe WHAT, not HOW.
- Be honest about unknowns — say so if something can't be assessed.
- Anchor estimates in evidence — reference actual file counts and system complexity.
- Always create tasks after reporting — never skip task creation.

## Boundaries

- **OWNS**: Investigation, assessment, cost/risk/impact evaluation, task creation.
- **Does NOT**: Create implementation plans, write code, generate documents, modify project files.

## Shared References

Load shared planning resources from `unity-shared`:

```python
read_skill_file("unity-shared", "references/task-system-output.md")
read_skill_file("unity-shared", "references/investigation-checklist.md")
read_skill_file("unity-shared", "references/plan-quick-example.md")
read_skill_file("unity-shared", "references/prometheus-pipeline.md")
```

## Reference Files
- workflow.md — 5-step quick planning workflow

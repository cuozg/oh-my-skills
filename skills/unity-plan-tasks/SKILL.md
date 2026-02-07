---
name: unity-plan-tasks
description: "Create diff-based task plans from high-level plans. Use when: (1) Have a plan from unity-plan needing detailed task requirements with code diffs, (2) Creating review-ready task docs in Documents/Tasks/. This skill provides REVIEW-ONLY output — it investigates code, plans changes, and presents them as unified diffs for human approval. No code is modified."
---

# Unity Plan Detailer (Diff-Based)

Break high-level plans into detailed task requirements with unified diffs for review.

> **⚠️ REVIEW-ONLY** — This skill investigates, plans, and produces diffs. It does NOT apply code changes. Output is for human review and approval before passing to an executor skill.

All code changes use **unified diff format** (the GitHub standard). One consistent layout for every change.

## Output Requirement (MANDATORY)

**Every task detail MUST follow the template**: [TASK_DETAIL_TEMPLATE.md](.claude/skills/unity-plan-tasks/assets/templates/TASK_DETAIL_TEMPLATE.md)

Save output to: `Documents/Tasks/[Number][Epic][Task].md`

Read the template first, then populate all sections.

## Workflow

For each task in the plan:

1. **Investigate**: Use `unity-investigate-code` to find relevant files, execution flows, and dependencies
2. **Plan Strategy**: Define the high-level approach and list affected files
3. **Write Diffs**: For each affected file, produce changes using unified diff format with full context
   - See [diff-format-guide.md](.claude/skills/unity-plan-tasks/references/diff-format-guide.md) for format conventions and examples
   - One diff block per file, with a **Purpose** line explaining why
   - Include file header (`--- a/...` and `+++ b/...`), hunk header (`@@ ... @@`), and 3-5 context lines
   - For new files, provide full content in a fenced code block (no diff format)
4. **Define Tests**: Specify test cases with prerequisites, actions, and expected results
5. **Export**: Populate [TASK_DETAIL_TEMPLATE.md](.claude/skills/unity-plan-tasks/assets/templates/TASK_DETAIL_TEMPLATE.md) — all sections including Review Status
6. **Save**: `Documents/Tasks/[Number][Epic][Task].md`
7. **Handoff**: Notify user the task is ready for review → once approved, route to executor

## Diff Quality Checklist

Before saving a task file, verify each diff block:

- [ ] Uses unified diff format with file header (`---`/`+++`) and hunk header (`@@`)
- [ ] Includes 3-5 context lines so the change location is unambiguous
- [ ] Preserves original indentation (spaces vs tabs)
- [ ] Has a **Purpose** line above the block
- [ ] One file per block — never mix files
- [ ] Uses `diff` language tag on the fenced code block

## Best Practices

- **Investigate first**: Always read the actual source before writing diffs — never guess at existing code
- **Diff accuracy**: Context lines must match the real file content exactly
- **Clear objectives**: At least one measurable success criterion per task
- **Epic alignment**: Stay within assigned Epic scope
- **No execution**: Never apply changes — diffs are proposals only

## Routing

- After approval → `unity-task-brainstorm` or `unity-task-executor` to apply changes

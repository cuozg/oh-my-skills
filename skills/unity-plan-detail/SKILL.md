---
name: unity-plan-detail
description: "Create task skeletons from plans. Use when: (1) Have a plan from unity-plan needing task requirements, (2) Creating initial task docs in Documents/Tasks/."
---

# Unity Plan Detailer

Break high-level plans into detailed task requirements.

## Output Requirement (MANDATORY)

**Every task detail MUST follow the template**: [TASK_DETAIL_TEMPLATE.md](assets/templates/TASK_DETAIL_TEMPLATE.md)

Save output to: `Documents/Tasks/[Number][Epic][Task].md`

Read the template first, then populate all sections.

## Workflow

For each task in the plan:

1. **Analyze**: Extract objective, constraints, success criteria
2. **Draft Strategy**: High-level approach (e.g., "Create Manager class", "Modify UI")
3. **Define Tests**: What success looks like
4. **Export**: Use [TASK_DETAIL_TEMPLATE.md](assets/templates/TASK_DETAIL_TEMPLATE.md)
5. **Save**: `Documents/Tasks/[Number][Epic][Task].md`
6. **Handoff**: Notify ready for `unity-plan-brainstorm`

## Output Format

Each task file should contain:
- **Objective**: What to achieve
- **Constraints**: Technical/design limits
- **Success Criteria**: Measurable outcomes
- **Implementation Strategy**: High-level approach (NOT specific code)
- **Test Cases**: How to verify

## Best Practices

- **Focus on "What"**: Detail what to accomplish, leave "how" for brainstorm
- **Clear Objectives**: At least one measurable success criterion
- **Epic Alignment**: Stay within assigned Epic scope

## Routing

- Technical deep-dive & code changes → `unity-plan-brainstorm`

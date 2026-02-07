---
name: unity-plan-review
description: "Review and brainstorm implementation plans. Use when: (1) Plan from unity-plan needs critique, (2) Need to refine decomposition with user, (3) Finalizing task list before detailing."
---

# Unity Plan Reviewer

Audit plans, brainstorm edge cases, finalize task lists.

## Output Requirement (MANDATORY)

**Every plan review MUST follow the template**: [REVIEW_OUTPUT.md](assets/templates/REVIEW_OUTPUT.md)

Update the plan document at `Documents/Plans/` with refined decomposition.

Read the template first, then populate all sections.

## Workflow

1. **Ingest**: Read plan from `Documents/Plans/` or context
2. **Audit**: Analyze Epics, identify missing components
3. **Discuss**: Present findings, ask clarifying questions
4. **Refine**: Update document with refined decomposition
5. **Finalize**: Output numbered task list for `unity-plan-detail`

## Key Questions to Ask

- "Does this Epic cover all user requirements?"
- "What happens if [edge case]?"
- "How does this interact with existing [Combat/Meta/Persistence]?"
- "What's the fallback if this approach fails?"

## Best Practices

- **Assume Nothing**: Treat vague specs as risks
- **Big Picture**: Consider system interactions
- **Completeness**: Trace every requirement to a task
- **User Alignment**: Don't finalize until user confirms

## Output

Always update the plan document with:
1. Refined high-level decomposition
2. Finalized numbered task list

---
description: Workflow for investigating requirements and producing a detailed implementation plan for a Unity feature.
---

# Workflow: Unity Project Planning

Transform high-level requirements into a structured, actionable project plan with costing.

1.  **Analyze Requirements**: 
    - Review the user request or feature spec for functional and non-functional goals.
2.  **Project Discovery**:
    // turbo
    - Run `.claude/skills/unity-plan/scripts/investigate_feature.sh [Keywords]` to find related systems.
    - Identify dependencies and integration points using `grep_search`.
3.  **Technical Feasibility**:
    - Assess if the current architecture supports the feature without significant debt.
    - Propose safe migration paths for breaking changes.
4.  **Decomposition**:
    - Break the feature into **Epics**.
    - For each Epic, define **Tasks** in the 7-column table format (Number, Epic, Task, Description, Type, Cost, Note).
5.  **Costing**:
    - Assign T-shirt sizes (S, M, L, XL) to all tasks based on complexity.
6.  **Finalize Documentation**:
    - Use the `IMPLEMENTATION_PLAN.md` template from `.claude/skills/unity-plan/assets/templates/`.
    - Save the plan in `Documents/Plans/IMPLEMENTATION_PLAN_[Feature].md`.
7.  **Approval**:
    - Present the plan to the user, highlighting risks and the implementation roadmap.

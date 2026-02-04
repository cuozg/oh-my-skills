---
description: Deep-dive into complex logic, execution flows, and feature implementations.
---

# Workflow: Investigate Code Logic

Use this workflow to explain how a feature works or to trace a complex execution path.

1.  **Define Scope**: 
    - Identify the target class, method, or feature.
    - Ask the user for specific entry points if the feature is large.
2.  **Discovery**:
    // turbo
    - Run `.claude/skills/unity-investigate-code/scripts/trace_logic.sh [Target]` to map definitions and usages.
    - Use `find_gameobjects` to see how the code is bound to assets in the scene.
3.  **Trace Flow**:
    - Use `view_file` to follow the logic from the entry point (e.g., `Update`, `OnClick`) through its dependencies.
    - Document state changes and conditional branches.
4.  **Analyze Side Effects**:
    - Identify modifications to Singletons, global managers, or static data.
    - Check for events dispatched or network packets sent.
5.  **Generate Report**:
    - Use the `INVESTIGATION_REPORT.md` template from `.claude/skills/unity-investigate-code/assets/templates/`.
    - Save the final document in `Documents/Investigations/INVESTIGATION_[Feature].md`.
    - Include **Mermaid sequence diagrams** for complex system interactions.
6.  **Summary**:
    - Provide a high-level summary to the user, highlighting any technical debt or risks found.

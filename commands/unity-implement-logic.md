---
description: Workflow for implementing or refactoring Unity C# logic and gameplay systems.
---

# Workflow: implement Unity C# Logic

Systematic process for transforming requirements or plans into high-quality Unity C# code.

1.  **Analyze Context**:
    - Identify the impacted systems and required dependencies.
    - Check for existing base classes or interfaces that should be implemented.
2.  **Define Architecture**:
    - Decide on MonoBehaviour vs. ScriptableObject vs. Pure C#.
    - Choose the communication pattern (Events, Singletons, or Direct References).
3.  **Draft Implementation**:
    - Apply the logic based on the `unity-coder` skill and its references.
    - Use `script_apply_edits` for precise modification of existing files.
4.  **Validate Compilation**:
    // turbo
    - Run `refresh_unity` with `compile="request"` and `wait_for_ready=true`.
5.  **Sanity Check**:
    - Use `read_console` to ensure no new warnings or errors were introduced by the changes.
    - (Optional) Run `/unity-test` if the logic is critical or complex.
6.  **Refactor**:
    - Final pass to clean up naming, add XML comments, and ensure performance best practices.

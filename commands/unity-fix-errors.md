---
description: Systematically diagnose and resolve Unity compiler errors, runtime exceptions, and logic bugs.
---

# Workflow: Fix Unity Errors

Use this workflow whenever the Unity Editor console reports errors or the game behaves unexpectedly.

1.  **Gather Intel**: 
    // turbo
    - Execute `read_console` to get the latest error stack traces.
    - Identify the failing script, line number, and error type (e.g., `NullReferenceException`).
2.  **Contextualize**:
    - Use `view_file` to read the code around the reported line.
    - Use `grep_search` to find all usages of the failing variable or method to identify the root cause.
3.  **Propose & Apply**:
    - Draft a fix that addresses the root cause (e.g., adding a null guard, fixing a race condition).
    - Use `script_apply_edits` for structural changes or `apply_text_edits` for minor fixes.
4.  **Compile & Sync**:
    // turbo
    - Run `refresh_unity` with `compile="request"` and `wait_for_ready=true`.
5.  **Validation**:
    - Run `read_console` again. If errors persist, repeat from Step 1.
    - If it was a runtime error, use `manage_editor` (action="play") to verify the fix in action.
6.  **Prevention**:
    - (Optional) Run `/unity-test` to ensure no regressions were introduced.

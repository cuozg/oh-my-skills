---
description: Workflow for creating and running automated tests using the Unity Test Framework.
---

# Workflow: Unity Automated Testing

Implement and execute automated tests to ensure code quality and stability.

1.  **Analyze Target**: 
    - Identify the code that needs validation.
    - Check for existing assembly definitions (`.asmdef`).
2.  **Define Strategy**:
    - Choose **Edit Mode** for logic/utilities.
    - Choose **Play Mode** for physics/components/UI.
3.  **Setup Environment**:
    - Create the `Tests` folder and matched `.asmdef` file if missing.
    - Create the test class using patterns from `.claude/skills/unity-test/references/TEST_EXAMPLES.md`.
4.  **Implement**:
    - Write tests using the **Arrange-Act-Assert** pattern.
    - Include `[SetUp]` and `[TearDown]` for state management.
5.  **Execute**:
    // turbo
    - Run `unityMCP.run_tests` to execute the suite.
6.  **Verify & Refactor**:
    - If tests fail, use `/unity-fix-errors` or `/unity-investigate-code` to identify the cause.
    - Re-run until all tests pass.
7.  **Document**:
    - (Optional) Use the `TEST_PLAN_TEMPLATE.md` from `.claude/skills/unity-test/assets/templates/` to document the suite.

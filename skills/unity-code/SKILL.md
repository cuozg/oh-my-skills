---
name: unity-code
description: >
  Use this skill to write, refactor, or fix Unity C# code.
metadata:
  author: kuozg
  version: "6.1"
---
# unity-code



## Rules

- **Follow coding standards**: Always adhere to established coding standards.
- **Verify after write**: You must verify that the code compiles without errors after making changes.

## Workflow

Follow these steps exactly:

### 1. Understand Requirement
Fully understand the requirement. If the requirement is unclear, ambiguous, or lacks necessary context, stop and ask the user for clarification.

### 2. Load Code Standards
Load the `unity-standards` skill, then read only the relevant files from `references/code-standards/` based on the task:
- `code-standards/core-conventions.md` (Naming, formatting, modifiers, null safety, patterns)
- `code-standards/lifecycle-async-errors.md` (Unity lifecycle, async, error handling, security)
- `code-standards/performance-data.md` (Collections, LINQ, serialization)
- `code-standards/architecture-systems.md` (Events, DI, architecture, folder structure)
- `code-standards/ecs-burst-standards.md` (ECS, Jobs, Burst, NativeContainers, Bakers)

Start with `code-standards/README.md` when unsure which standards file applies.

### 3. Analyze Codebase
Understand the existing codebase and document the context. If the scope is large or complex, spawn a subagent to thoroughly analyze the architecture, dependencies, and surrounding code before proceeding.

### 4. Write Code
Write the code following the rules, the loaded standards, and the requirement. Ensure code is complete, functional, and aligns with the local style of the surrounding files.

### 5. Verify Compilation
Verify that the code compiles without error. Use LSP diagnostics and the Unity Editor Console (via MCP `Unity.ReadConsole` if available) to ensure zero compile errors before finishing the task.

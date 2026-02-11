---
description: Create and run Unity tests with Edit/Play Mode support
agent: build
---

Load the `unity/unity-test` skill and create tests for the specified target.

## Task

$ARGUMENTS

## Requirements

1. **Analyze** the target code to understand testable behaviors
2. **Create** comprehensive test suites covering:
   - Happy path scenarios
   - Edge cases and boundary conditions
   - Error handling paths
   - Integration points
3. **Use** appropriate test mode (Edit Mode for logic, Play Mode for runtime)
4. **Mock** dependencies where needed for isolation
5. **Follow** Unity Test Framework conventions (NUnit attributes, Assert patterns)
6. **Verify** tests compile with `lsp_diagnostics`

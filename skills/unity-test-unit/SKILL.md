---
name: unity-test-unit
description: "Unity Test Framework automation. Use when: (1) Creating Edit/Play Mode tests, (2) Generating comprehensive test suites for features, (3) Mocking dependencies, (4) Maximizing test coverage for Unity C# code. Triggers: 'write tests', 'test this class', 'add unit tests', 'test coverage', 'play mode test', 'edit mode test'."
---
# Unity Test Generation

**Input**: Class, method, or feature to test. Optional: test assembly, mode preference (Edit/Play), coverage target.

## Output
Unity Test Framework test scripts (Edit Mode and/or Play Mode) with comprehensive coverage.

## Workflow

1. **Analyze**: Identify feature under test, list expected behaviors (happy path, edge cases, errors), define scope
2. **Investigate**: Read target code, map public API, identify dependencies (singletons, MonoBehaviour refs, SOs), classify testability (pure logic → Edit Mode, lifecycle → Play Mode)
3. **Generate**: Create test scripts per feature — cover all categories in [workflow.md](references/workflow.md), target 10+ test cases per class

## References

- [Workflow](references/workflow.md) — test case categories, directory structure, edit/play mode guidance, class organization
- [Test Patterns &amp; Organization](../unity-shared/references/test-patterns.md) — folder structure, naming, AAA, assertions, anti-patterns, best practices
- [Assembly Definition Setup](../unity-shared/../unity-shared/references/test-assembly-setup.md) — `.asmdef` templates, compilation errors, test discovery
- [test-examples.md](../unity-shared/references/test-examples.md) — comprehensive examples: Edit/Play Mode, mocking, parameterized, event testing

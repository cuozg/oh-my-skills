---
name: unity-test-unit
description: "Unity Test Framework automation. Use when: (1) Creating Edit/Play Mode tests, (2) Generating comprehensive test suites for features, (3) Mocking dependencies, (4) Maximizing test coverage for Unity C# code. Triggers: 'write tests', 'test this class', 'add unit tests', 'test coverage', 'play mode test', 'edit mode test'."
---
# Unity Test Generation

**Input**: Class, method, or feature to test. Optional: test assembly, mode preference (Edit/Play), coverage target.

**Output**: Comprehensive test suites (10+ cases per feature class) with Edit Mode and Play Mode scripts.

## Workflow

1. **Analyze**: Identify feature under test, list expected behaviors (happy path, edge cases, errors), define scope
2. **Investigate**: Read target code, map public API, identify dependencies (singletons, MonoBehaviour refs, SOs), classify testability (pure logic → Edit Mode, lifecycle → Play Mode)
3. **Generate**: Create test scripts per feature — cover all categories below, target 10+ test cases per class

## Test Case Categories

| Category            | What to Test                                                         |
| ------------------- | -------------------------------------------------------------------- |
| Happy path          | Normal input → expected output                                      |
| Boundary values     | Min, max, zero, empty, null, at-limit                                |
| Error conditions    | Invalid input → exception or graceful fallback                      |
| State preconditions | Behavior in different states (initialized, disposed, mid-transition) |
| Events              | Subscribe, fire conditions, handler args, unsubscribe                |
| State transitions   | Valid/invalid transitions, re-entry                                  |
| Integration points  | Interface calls, event bus messages, callbacks                       |
| Concurrency         | Multiple calls, rapid succession, re-entrant                         |

## Directory Structure

```
Assets/Scripts/Test/
├── Editor/                          ← Edit Mode (no .asmdef needed)
│   ├── FeatureTests.cs
│   └── FeatureEventTests.cs
└── PlayMode/                        ← Requires .asmdef
    ├── PlayModeTests.asmdef
    └── PlayerMovementTests.cs
```

## Edit Mode vs Play Mode

**Default to Edit Mode** (faster, no scene required). Use Play Mode ONLY when test requires MonoBehaviour lifecycle, physics, coroutines, Awaitable async (Unity 6+), UI interaction, or scene loading.

## Class Organization

- `FeatureTests` — core logic (happy path, boundaries, errors)
- `FeatureEventTests` — event subscription, firing, verification
- `FeatureIntegrationTests` — interaction with dependencies
- `FeatureStateTests` — state machine transitions

## References

- [Test Patterns &amp; Organization](references/test-patterns.md) — folder structure, naming, AAA, assertions, anti-patterns, best practices
- [Assembly Definition Setup](references/test-assembly-setup.md) — `.asmdef` templates, compilation errors, test discovery
- [TEST_EXAMPLES.md](references/TEST_EXAMPLES.md) — comprehensive examples: Edit/Play Mode, mocking, parameterized, event testing

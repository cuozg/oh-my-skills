# unity-test-unit — Workflow

## Test Case Categories

| Category | What to Test |
|----------|-------------|
| Happy path | Normal input → expected output |
| Boundary values | Min, max, zero, empty, null, at-limit |
| Error conditions | Invalid input → exception or graceful fallback |
| State preconditions | Behavior in different states (initialized, disposed, mid-transition) |
| Events | Subscribe, fire conditions, handler args, unsubscribe |
| State transitions | Valid/invalid transitions, re-entry |
| Integration points | Interface calls, event bus messages, callbacks |
| Concurrency | Multiple calls, rapid succession, re-entrant |

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

## Workflow Steps

1. **Analyze**: Identify feature under test, list expected behaviors, define scope
2. **Investigate**: Read target code, map public API, identify dependencies, classify testability
3. **Generate**: Create test scripts — cover all categories, target 10+ test cases per class

## References

- `../../unity-shared/references/test-patterns.md` — folder structure, naming, AAA, anti-patterns
- `../../unity-shared/references/test-assembly-setup.md` — `.asmdef` templates, compilation errors
- `../../unity-shared/references/test-examples.md` — Edit/Play Mode, mocking, parameterized, event testing

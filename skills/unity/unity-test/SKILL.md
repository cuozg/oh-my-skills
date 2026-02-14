---
name: unity-test
description: "Unity Test Framework automation. Use when: (1) Creating Edit/Play Mode tests, (2) Generating comprehensive test suites for features, (3) Mocking dependencies, (4) Maximizing test coverage for Unity C# code. Triggers: 'write tests', 'test this class', 'add unit tests', 'test coverage', 'play mode test', 'edit mode test'."
---

# Unity Test Generation

Generate comprehensive test suites for Unity C# code using Unity Test Framework (UTFramework).

## Purpose

Create thorough, maintainable test suites for Unity C# code — Edit Mode and Play Mode tests with proper mocking, covering happy paths, edge cases, and error conditions.

## Input

- **Required**: Class, method, or feature to test
- **Optional**: Existing test assembly, test mode preference (Edit/Play), coverage target percentage

## Examples

| User Request | Skill Action |
|:---|:---|
| "Write tests for PlayerHealth.cs" | Generate Edit Mode tests: TakeDamage clamps, death event fires, heal caps at max, zero-damage no-op |
| "Add Play Mode tests for the inventory UI" | Generate Play Mode tests: open/close, add/remove items, drag-drop, full-stack interaction |
| "Test the matchmaking service" | Generate Edit Mode tests with mocked network layer: queue, match found, timeout, cancel |

## Workflow

### Step 1: Analyze Requirement

Understand what needs testing:

1. Identify the feature or system under test
2. List expected behaviors (happy path, edge cases, error conditions)
3. Determine integration points with other systems
4. Define scope: which classes/methods to cover

### Step 2: Investigate Logic

Examine the target code — use `unity-investigate` skill or direct code reading:

1. Read the class/method under test
2. Map public API surface (methods, properties, events)
3. Identify dependencies (injected services, MonoBehaviour refs, ScriptableObjects, singletons)
4. Trace state transitions and side effects
5. Note any Unity lifecycle dependencies (Start, Update, OnEnable)
6. Classify testability: pure logic → Edit Mode, Unity lifecycle → Play Mode

### Step 3: Generate Comprehensive Tests

Create test scripts organized by feature. Each feature gets its own test class(es).

**Test case generation strategy** — for every public method/behavior, cover:

| Category | What to Test |
|----------|-------------|
| Happy path | Normal input → expected output |
| Boundary values | Min, max, zero, empty, null, exactly-at-limit |
| Error conditions | Invalid input → exception or graceful fallback |
| State preconditions | Behavior when object is in different states (initialized, disposed, mid-transition) |
| Events | Subscribe, fire conditions, handler args, unsubscribe |
| State transitions | Valid transitions, invalid transitions, re-entry |
| Integration points | Interface calls, event bus messages, callbacks to other systems |
| Concurrency | Multiple calls, rapid succession, re-entrant calls |

**Target**: 10+ test cases per feature class minimum.

## Test Organization

### Directory Structure

```
Assets/Scripts/Test/
├── Editor/                          ← RECOMMENDED for EditMode tests (no .asmdef needed)
│   ├── InventoryTests.cs
│   ├── InventoryEventTests.cs
│   ├── DamageCalculatorTests.cs
│   └── QuestSystemTests.cs
└── PlayMode/                        ← Requires .asmdef
    ├── PlayModeTests.asmdef
    ├── PlayerMovementTests.cs
    ├── SpawnerTests.cs
    └── UIInteractionTests.cs
```

> **Note**: `Editor/` is a Unity special folder. Tests placed here compile into `Assembly-CSharp-Editor` which automatically includes NUnit and TestRunner references. No `.asmdef` is needed. For legacy setups, `EditMode/` with a valid `.asmdef` also works — see [Test Folder Structure & Test Runner Discovery](#test-folder-structure--test-runner-discovery).

### Separate Classes per Feature

Split tests into focused classes:

- `FeatureTests` — core logic (happy path, boundaries, errors)
- `FeatureEventTests` — event subscription, firing, handler verification
- `FeatureIntegrationTests` — interaction with dependencies
- `FeatureStateTests` — state machine transitions (if applicable)

**EditMode tests**: Place in `Editor/` folder (no `.asmdef` needed). **PlayMode tests**: Require `.asmdef` — see [Assembly Definition Setup & Checklist](#assembly-definition-setup--checklist) below.

### Test Folder Structure & Test Runner Discovery

> **Full details on test folder structure, Editor/ vs .asmdef comparison, and Test Runner discovery**: See [Test Patterns & Organization Reference](references/test-patterns.md) — covers folder structure comparison table, recommended EditMode folder layout, and when to use `.asmdef`.

---

## Edit Mode vs Play Mode

**Default to Edit Mode** (faster, no scene required). Use Play Mode ONLY when the test requires MonoBehaviour lifecycle, physics, coroutines, Awaitable async (Unity 6+), UI interaction, or scene loading.

> **Full details on Edit/Play Mode criteria, test patterns (naming, AAA, SetUp/TearDown, assertions, parameterized, async), anti-patterns, best practices, MCP tools integration, and output specification**: See [Test Patterns & Organization Reference](references/test-patterns.md).

---

## Assembly Definition Setup & Checklist

> **Full assembly definition setup guide, `.asmdef` templates (EditMode/PlayMode), compilation error troubleshooting (CS0246), test discovery issues ("No tests to show"), and assembly definition pitfalls**: See [Assembly Definition Setup & Checklist](references/test-assembly-setup.md) — covers checklist, JSON templates, game code referencing, WWE Champions real-world fix, and correct vs incorrect `.asmdef` configuration.

**EditMode tests**: Place in `Editor/` folder (no `.asmdef` needed). **PlayMode tests**: Require `.asmdef` — see the reference above.

---

## References

- [Test Patterns & Organization Reference](references/test-patterns.md) — Test folder structure, Edit/Play Mode, naming, AAA, assertions, anti-patterns, best practices, MCP tools, output
- [Assembly Definition Setup & Checklist](references/test-assembly-setup.md) — `.asmdef` templates, compilation errors, test discovery, pitfalls
- [TEST_EXAMPLES.md](references/TEST_EXAMPLES.md) — Comprehensive examples: multiple test classes per feature, Edit/Play Mode, mocking, parameterized, event testing, integration testing

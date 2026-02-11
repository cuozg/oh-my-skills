---
name: unity-test
description: "Unity Test Framework automation. Use when: (1) Creating Edit/Play Mode tests, (2) Generating comprehensive test suites for features, (3) Mocking dependencies, (4) Maximizing test coverage for Unity C# code. Triggers: 'write tests', 'test this class', 'add unit tests', 'test coverage', 'play mode test', 'edit mode test'."
---

# Unity Test Generation

Generate comprehensive test suites for Unity C# code using Unity Test Framework (UTFramework).

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
├── EditMode/
│   ├── InventoryTests.cs
│   ├── InventoryEventTests.cs
│   ├── DamageCalculatorTests.cs
│   └── QuestSystemTests.cs
└── PlayMode/
    ├── PlayerMovementTests.cs
    ├── SpawnerTests.cs
    └── UIInteractionTests.cs
```

### Separate Classes per Feature

Split tests into focused classes:

- `FeatureTests` — core logic (happy path, boundaries, errors)
- `FeatureEventTests` — event subscription, firing, handler verification
- `FeatureIntegrationTests` — interaction with dependencies
- `FeatureStateTests` — state machine transitions (if applicable)

Do NOT create `.asmdef` files — the project manages assembly definitions externally.

## Edit Mode vs Play Mode

**Default to Edit Mode** (faster, no scene required).

Use Play Mode ONLY when the test requires:
- MonoBehaviour lifecycle (`Start`, `Update`, `OnEnable`)
- Physics simulation (`Rigidbody`, collisions)
- Coroutines (`yield return`)
- `Awaitable` async operations (Unity 6+)
- UI interaction (`EventSystem`, `Button.onClick`)
- Scene loading

## Test Patterns

### Naming Convention

```
[Subject]_[Scenario]_[ExpectedResult]
```

Examples: `Health_TakeDamageExceedingMax_ClampsToZero`, `Inventory_AddWhenFull_ReturnsFalse`

### Structure: Arrange-Act-Assert

```csharp
[Test]
public void Inventory_AddValidItem_ReturnsTrue()
{
    // Arrange
    var inventory = new Inventory(maxSlots: 10);
    var item = new Item("sword");

    // Act
    var result = inventory.Add(item);

    // Assert
    Assert.IsTrue(result);
}
```

### SetUp / TearDown

- `[SetUp]`: Create fresh instances per test — no shared mutable state
- `[TearDown]`: Destroy GameObjects, unsubscribe events, clean up
- Never rely on test execution order

### Dependency Handling

| Dependency Type | Strategy |
|----------------|----------|
| Interface-based | Create test doubles implementing the interface |
| Concrete class | Wrap in interface or subclass override |
| Static/Singleton | Isolate behind wrapper; document as untestable if necessary |
| MonoBehaviour | `new GameObject().AddComponent<T>()` in SetUp, `Object.Destroy` in TearDown |

### Assertions

- `Assert.AreEqual(expected, actual)` — value comparison
- `Assert.IsTrue/IsFalse` — boolean conditions
- `Assert.IsNull/IsNotNull` — null checks
- `Assert.Throws<T>(() => ...)` — exception verification
- `Assert.That(value, Is.InRange(min, max))` — range constraints
- Floating point: `Assert.AreEqual(expected, actual, tolerance)`
- Always add descriptive message: `Assert.AreEqual(70, health.Current, "Health should decrease by damage amount")`

### Parameterized Tests

```csharp
[TestCase(100, 30, 70)]
[TestCase(100, 100, 0)]
[TestCase(100, 150, 0)]
public void CalculateHealth_AfterDamage_ReturnsExpected(int max, int damage, int expected)
{
    var result = DamageCalculator.CalculateFinalHealth(max, damage);
    Assert.AreEqual(expected, result);
}
```

### Async & Coroutine Tests

- Coroutines: `[UnityTest]` returning `IEnumerator`
- Async (Unity 6+): `[Test]` with `async Task` or `[UnityTest]` with `Awaitable`
- Always set timeout for async operations
- `yield return null` or `WaitForFixedUpdate` to advance frames

### Test Data

- Use constants or factory methods, not magic numbers
- Name descriptively: `const int FullHealth = 100;`
- Use `[TestCase]` for data-driven coverage

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do Instead |
|-------------|-------------|------------|
| One test class per project | Hard to navigate, slow to understand | Separate class per feature |
| Testing private methods directly | Brittle, couples tests to implementation | Test through public API |
| Shared mutable state between tests | Non-deterministic failures | Fresh state in `[SetUp]` |
| No TearDown cleanup | Leaked GameObjects corrupt subsequent tests | Always destroy in `[TearDown]` |
| Magic numbers in tests | Unreadable, unclear intent | Named constants or factory methods |
| Testing Unity internals | Not your code, may change | Test YOUR behavior that uses Unity |
| Relying on `Time.deltaTime` | Non-deterministic | Use fixed values or `WaitForFixedUpdate` |
| Multiple behaviors per test | Unclear what failed | One behavior = one test |
| Creating `.asmdef` files | Project manages assemblies externally | Place tests in existing structure |
| Generating test plan reports | Overhead without value | Generate test code directly |

## Best Practices

- **Speed**: Edit Mode tests under 10ms each. Batch Play Mode tests sharing scene setup.
- **Determinism**: Avoid `Time.deltaTime` in assertions. Use fixed values.
- **Cleanup**: Always destroy GameObjects. Leaked objects corrupt subsequent tests.
- **No side effects**: Tests must not modify ProjectSettings, persistent data, or PlayerPrefs.
- **Test one thing**: Each test validates exactly one behavior.
- **Readable failures**: Use descriptive assertion messages.

## MCP Tools Integration

| Operation | MCP Tool |
|:----------|:---------|
| Check compilation | `coplay-mcp_check_compile_errors` |
| Read test logs | `coplay-mcp_get_unity_logs(search_term="Test")` |
| Run editor script | `coplay-mcp_execute_script(filePath)` |
| Play mode tests | `coplay-mcp_play_game` / `coplay-mcp_stop_game` |
| Verify scene state | `coplay-mcp_list_game_objects_in_hierarchy` |

### Execution Flow

```
1. coplay-mcp_check_compile_errors        → Ensure tests compile
2. coplay-mcp_execute_script(test_runner)  → Run tests via editor script
3. coplay-mcp_get_unity_logs(show_errors=true) → Check results
4. On failure: read logs, fix, repeat
```

## Skill Integration

- Use `unity-investigate` to trace logic before writing tests
- Use `unity-code` for implementation patterns the tests should validate
- Use `unity-fix-errors` or `unity-debug` when tests reveal issues

## References

- [TEST_EXAMPLES.md](references/TEST_EXAMPLES.md) — Comprehensive examples: multiple test classes per feature, Edit/Play Mode, mocking, parameterized, event testing, integration testing

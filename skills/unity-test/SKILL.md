---
name: unity-test
description: "Unity Test Framework automation. Use when: (1) Creating Edit/Play Mode tests, (2) Configuring test assemblies (.asmdef), (3) Mocking dependencies, (4) Analyzing test results. Triggers: 'write tests', 'test this class', 'add unit tests', 'test coverage', 'play mode test', 'edit mode test'."
---

# Unity Test Logic

Generate comprehensive test suites for Unity C# code using Unity Test Framework.

## Scope & Constraints

**This skill defines RULES and WORKFLOWS for test generation only.**
All output formatting is delegated to [TEST_PLAN_TEMPLATE.md](assets/templates/TEST_PLAN_TEMPLATE.md). Read the template first, then populate its sections with test logic generated below.

**In scope**: Test case identification, test code generation, test organization, mocking strategy, coverage analysis.
**Out of scope**: Output document structure, markdown formatting, report layout (template owns these).

## Test Generation Workflow

1. **Analyze Target Code**
   - Read the class/method under test
   - Identify public API surface (methods, properties, events)
   - Map dependencies (injected services, MonoBehaviour refs, ScriptableObjects)
   - Determine testability: pure logic → Edit Mode, Unity lifecycle → Play Mode

2. **Classify Test Type**

   | Condition | Type | Location |
   |-----------|------|----------|
   | Pure C# logic, no Unity API | Edit Mode | `Assets/Scripts/Test/EditMode/` |
   | Uses MonoBehaviour, coroutines, physics, UI | Play Mode | `Assets/Scripts/Test/PlayMode/` |
   | Async operations with `Awaitable` | Play Mode (async) | `Assets/Scripts/Test/PlayMode/` |

3. **Generate Test Cases**
   - Apply the rules in "Test Logic Rules" below
   - For each public method: happy path + edge cases + error conditions
   - For each state transition: valid + invalid transitions
   - For each event: subscription, firing, handler execution

4. **Implement Tests**
   - Follow Arrange-Act-Assert pattern
   - Apply naming convention: `[Subject]_[Scenario]_[ExpectedResult]`
   - Add `[SetUp]`/`[TearDown]` for shared state
   - Destroy all test GameObjects in TearDown

5. **Configure Test Directory**
   - Place all test scripts under `Assets/Scripts/Test/`
   - Use `Assets/Scripts/Test/EditMode/` for Edit Mode tests
   - Use `Assets/Scripts/Test/PlayMode/` for Play Mode tests
   - Do NOT create `.asmdef` files — the project manages assembly definitions externally

6. **Execute & Validate**
   - Run via `coplay-mcp_execute_script` with a test runner script, or Unity Test Runner
   - Check results: `coplay-mcp_get_unity_logs(show_errors=true)`
   - On failure: use `/unity-fix-errors` or `/unity-debug` to diagnose

7. **Output**
   - Populate the [TEST_PLAN_TEMPLATE.md](assets/templates/TEST_PLAN_TEMPLATE.md) with generated test cases and results

## Test Logic Rules

### Rule 1: Coverage Targets
For every public method, generate tests covering:
- **Happy path**: Normal input → expected output
- **Boundary values**: Min, max, zero, empty, null
- **Error conditions**: Invalid input → expected exception or fallback
- **State preconditions**: Method behavior when object is in different states

### Rule 2: Test Isolation
- Each test MUST be independent — no shared mutable state between tests
- Use `[SetUp]` to create fresh instances per test
- Use `[TearDown]` to destroy GameObjects and unsubscribe events
- Never rely on test execution order

### Rule 3: Dependency Handling
Analyze dependencies and apply the appropriate strategy:
- **Interface-based**: Create test doubles implementing the interface
- **Concrete class**: Wrap in interface or use subclass override
- **Static/Singleton**: Isolate behind wrapper; document as untestable if necessary
- **MonoBehaviour**: Use `new GameObject().AddComponent<T>()` in SetUp, `Object.Destroy` in TearDown

### Rule 4: Test Naming
```
[Subject]_[Scenario]_[ExpectedResult]
```
- Subject = class or method name
- Scenario = input condition or action
- ExpectedResult = observable outcome

Examples:
- `Health_TakeDamageWithNegativeValue_ClampsToZero`
- `Inventory_AddItemWhenFull_ReturnsFalse`
- `Player_DiesAtZeroHealth_FiresOnDeathEvent`

### Rule 5: Edit Mode vs Play Mode Selection
- Default to Edit Mode (faster, no scene required)
- Use Play Mode ONLY when test requires:
  - `MonoBehaviour` lifecycle (`Start`, `Update`, `OnEnable`)
  - Physics simulation (`Rigidbody`, collisions)
  - Coroutines (`yield return`)
  - `Awaitable` async operations
  - UI interaction (`EventSystem`, `Button.onClick`)
  - Scene loading

### Rule 6: Assertion Selection
- `Assert.AreEqual(expected, actual)` — value comparison
- `Assert.IsTrue/IsFalse` — boolean conditions
- `Assert.IsNull/IsNotNull` — null checks
- `Assert.Throws<T>(() => ...)` — exception verification
- `Assert.That(value, Is.InRange(min, max))` — range constraints
- For floating point: `Assert.AreEqual(expected, actual, tolerance)`

### Rule 7: Async & Coroutine Tests
- Coroutine tests: use `[UnityTest]` returning `IEnumerator`
- Async tests (Unity 6+): use `[Test]` with `async Task` or `[UnityTest]` with `Awaitable`
- Always set a timeout for async operations to prevent hanging tests
- Yield `null` or `WaitForFixedUpdate` to advance frames

### Rule 8: Test Data
- Use constants or factory methods for test data, not magic numbers
- Name test data descriptively: `const int FullHealth = 100;`
- For parameterized tests, use `[TestCase(input, expected)]`

## Code Analysis Checklist

When analyzing code to generate tests, systematically check:

1. **Constructors**: Valid params, invalid params, default state
2. **Public methods**: All overloads, return values, side effects
3. **Properties**: Get/set, validation, change notifications
4. **Events**: Subscribe, unsubscribe, fire conditions, handler args
5. **State machines**: Each state, each transition, invalid transitions
6. **Collections**: Empty, single, multiple, capacity limits
7. **Error paths**: Null inputs, out-of-range, disposed objects
8. **Integration points**: Interface calls, event bus messages, callbacks

## Best Practices for Unity Test Framework

- **Speed**: Keep Edit Mode tests under 10ms each. Batch Play Mode tests that share scene setup.
- **Determinism**: Avoid `Time.deltaTime` in assertions. Use fixed values or `WaitForFixedUpdate`.
- **Cleanup**: Always destroy GameObjects. Leaked objects corrupt subsequent tests.
- **No side effects**: Tests must not modify ProjectSettings, persistent data, or PlayerPrefs.
- **Test one thing**: Each test validates exactly one behavior. Multiple asserts are acceptable only when verifying one logical outcome.
- **Readable failures**: Prefer `Assert.AreEqual(expected, actual, "Health should decrease by damage amount")` with descriptive messages.

## References

- [TEST_EXAMPLES.md](references/TEST_EXAMPLES.md) — Edit Mode, Play Mode, async, parameterized, and mocking patterns
- [TEST_PLAN_TEMPLATE.md](assets/templates/TEST_PLAN_TEMPLATE.md) — **Mandatory output format** for all test plans

---

## MCP Tools Integration

Prefer `coplay-mcp_*` tools for test execution and validation.

| Operation | MCP Tool | Replaces |
|:----------|:---------|:---------|
| Check compilation | `coplay-mcp_check_compile_errors` | Manual compile check |
| Read test logs | `coplay-mcp_get_unity_logs(search_term="Test")` | Manual console inspection |
| Run editor script | `coplay-mcp_execute_script(filePath)` | Manual test runner invocation |
| Play mode tests | `coplay-mcp_play_game` / `coplay-mcp_stop_game` | Manual play button |
| Verify scene state | `coplay-mcp_list_game_objects_in_hierarchy` | Manual hierarchy inspection |
| Inspect test object | `coplay-mcp_get_game_object_info(gameObjectPath)` | Manual component check |

### Test Execution Flow

```
1. coplay-mcp_check_compile_errors        → Ensure tests compile
2. coplay-mcp_execute_script(test_runner)  → Run tests via editor script
3. coplay-mcp_get_unity_logs(show_errors=true) → Check test results
4. On failure: read logs, fix, repeat
```

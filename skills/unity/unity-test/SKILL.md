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

Unity's EditMode Test Runner only discovers tests in assemblies it recognizes as test assemblies. The **recommended** approach for EditMode tests is to place them in an `Editor/` folder.

#### Why `Editor/` Folder is Recommended (EditMode Tests)

| Factor | `Editor/` folder | Custom `.asmdef` folder |
|:-------|:-----------------|:------------------------|
| Assembly | Compiles into `Assembly-CSharp-Editor` automatically | Compiles into custom assembly — requires valid `.asmdef` |
| NUnit access | Automatic — `Assembly-CSharp-Editor` includes NUnit references | Manual — must configure `overrideReferences` + `precompiledReferences` |
| TestRunner access | Automatic — `UnityEngine.TestRunner` and `UnityEditor.TestRunner` included | Manual — must add to `references` array |
| Test Runner discovery | Automatic — always scanned by EditMode Test Runner | Requires correct `defineConstraints`, `includePlatforms`, and valid references |
| Game code access | Automatic — `Assembly-CSharp-Editor` can reference `Assembly-CSharp` | Implicit only if game code has no `.asmdef`; otherwise must add explicit reference |
| `.asmdef` required | **No** | **Yes** — and misconfiguration causes silent discovery failures |
| Risk of "No tests to show" | **Minimal** | **High** if `.asmdef` is misconfigured |

#### Recommended EditMode Test Folder

```
Assets/Scripts/Test/Editor/
├── FeatureA/
│   ├── FeatureATests.cs
│   └── FeatureAEventTests.cs
├── FeatureB/
│   └── FeatureBTests.cs
└── Helpers/
    └── TestDoubles.cs
```

**No `.asmdef` file needed.** Tests compile into `Assembly-CSharp-Editor` which has all required NUnit and TestRunner references built in.

#### When to Use `.asmdef` Instead

Use a custom `.asmdef` only when:
- Tests must reference other custom assemblies (game code behind its own `.asmdef`)
- Tests need explicit assembly isolation for large codebases
- PlayMode tests are required (PlayMode tests always need `.asmdef`)

When using `.asmdef`, follow the [Assembly Definition Setup & Checklist](#assembly-definition-setup--checklist) exactly.

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
| Missing `.asmdef` in non-`Editor/` test folder | Tests compile into Assembly-CSharp without NUnit references → CS0246 | Use `Editor/` folder (recommended) or create valid `.asmdef` (see checklist) |
| Adding `Assembly-CSharp.dll` to precompiledReferences | Not a precompiled DLL — unreliable | Use implicit access or create asmdef references for game code |
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
| Check compilation | `unityMCP_check_compile_errors` |
| Read test logs | `unityMCP_get_unity_logs(search_term="Test")` |
| Run editor script | `unityMCP_execute_script(filePath)` |
| Play mode tests | `unityMCP_play_game` / `unityMCP_stop_game` |
| Verify scene state | `unityMCP_list_game_objects_in_hierarchy` |

### Execution Flow

```
1. unityMCP_check_compile_errors        → Ensure tests compile
2. unityMCP_execute_script(test_runner)  → Run tests via editor script
3. unityMCP_get_unity_logs(show_errors=true) → Check results
4. On failure: read logs, fix, repeat
```

## Skill Integration

- Use `unity-investigate` to trace logic before writing tests
- Use `unity-code` for implementation patterns the tests should validate
- Use `unity-fix-errors` or `unity-debug` when tests reveal issues

## Output

Successful test generation produces:
1. **Test scripts** — C# files placed in `Assets/Scripts/Test/Editor/` (recommended for EditMode) or `Assets/Scripts/Test/PlayMode/` per classification
2. **Clean compilation** — `unityMCP_check_compile_errors` returns zero errors after adding tests
3. **Naming convention** — all test methods follow `[Subject]_[Scenario]_[ExpectedResult]`
4. **Test discovery** — tests appear in the Test Runner window (`Window > General > Test Runner`)
5. **Assembly definition** — `.asmdef` file present in PlayMode test folders; EditMode tests in `Editor/` folder need no `.asmdef`

No separate test plan documents are generated. The test code itself is the deliverable.

## Assembly Definition Setup & Checklist

Test folders **require** assembly definition (`.asmdef`) files to compile correctly. Without an `.asmdef`, test scripts are compiled into the default `Assembly-CSharp` assembly, which does **not** reference NUnit or Unity TestRunner — causing `CS0246` errors for `NUnit.Framework`, `[TestFixture]`, `[Test]`, etc.

### Why `.asmdef` Files Are Required

Unity's Test Framework packages (`com.unity.test-framework@1.1.33`, `com.unity.ext.nunit@1.0.6`) provide NUnit as a **precompiled DLL** (`nunit.framework.dll`). Test assemblies must explicitly declare this dependency via `overrideReferences` + `precompiledReferences` in their `.asmdef`.

### New Test Folder Checklist

When creating a new test folder, **always**:

- [ ] Create an `.asmdef` file in the test folder root
- [ ] Set `"overrideReferences": true`
- [ ] Add `"nunit.framework.dll"` to `precompiledReferences`
- [ ] Add `"UnityEngine.TestRunner"` and `"UnityEditor.TestRunner"` to `references`
- [ ] Set `"defineConstraints": ["UNITY_INCLUDE_TESTS"]`
- [ ] For Edit Mode: set `"includePlatforms": ["Editor"]`
- [ ] For Play Mode: leave `includePlatforms` empty `[]`
- [ ] Set `"autoReferenced": false`
- [ ] Verify compilation: `unityMCP_check_compile_errors` returns zero errors

### EditMode `.asmdef` Template

```json
{
    "name": "EditModeTests",
    "rootNamespace": "",
    "references": [
        "UnityEngine.TestRunner",
        "UnityEditor.TestRunner"
    ],
    "includePlatforms": [
        "Editor"
    ],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": true,
    "precompiledReferences": [
        "nunit.framework.dll"
    ],
    "autoReferenced": false,
    "defineConstraints": [
        "UNITY_INCLUDE_TESTS"
    ],
    "versionDefines": [],
    "noEngineReferences": false
}
```

### PlayMode `.asmdef` Template

```json
{
    "name": "PlayModeTests",
    "rootNamespace": "",
    "references": [
        "UnityEngine.TestRunner",
        "UnityEditor.TestRunner"
    ],
    "includePlatforms": [],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": true,
    "precompiledReferences": [
        "nunit.framework.dll"
    ],
    "autoReferenced": false,
    "defineConstraints": [
        "UNITY_INCLUDE_TESTS"
    ],
    "versionDefines": [],
    "noEngineReferences": false
}
```

### Referencing Game Code from Tests

To reference game code (e.g., classes in `Assembly-CSharp`):
- If the game code has **no** `.asmdef`, test assemblies can access it implicitly — no additional configuration needed.
- If the game code has its **own** `.asmdef`, add that assembly name to the test `.asmdef`'s `references` array.
- **NEVER** add `"Assembly-CSharp.dll"` to `precompiledReferences` — it is not a precompiled DLL and will cause unreliable behavior.

## Common Test Compilation Errors & Troubleshooting

### CS0246: "The type or namespace name 'NUnit' could not be found"

**Cause**: Test `.cs` files are in a folder without an `.asmdef`, so they compile into `Assembly-CSharp` which lacks NUnit references.

**Solution**: Create an `.asmdef` file in the test folder using the templates above.

**Symptoms** (cascading errors from a single root cause):
```
error CS0246: The type or namespace name 'NUnit' could not be found
error CS0246: The type or namespace name 'TestFixture' could not be found
error CS0246: The type or namespace name 'TestFixtureAttribute' could not be found
error CS0246: The type or namespace name 'Test' could not be found
error CS0246: The type or namespace name 'TestAttribute' could not be found
error CS0246: The type or namespace name 'SetUp' could not be found
error CS0246: The type or namespace name 'SetUpAttribute' could not be found
error CS0246: The type or namespace name 'TearDown' could not be found
error CS0246: The type or namespace name 'Assert' could not be found
```

All of these resolve by adding a single `.asmdef` file with the correct configuration.

### CS0246: "The type or namespace name 'UnityEngine.TestTools' could not be found"

**Cause**: Same root cause — missing `.asmdef` with `UnityEngine.TestRunner` reference.

**Solution**: Ensure `"UnityEngine.TestRunner"` is in the `references` array of the `.asmdef`.

### Troubleshooting Steps

1. **Check for `.asmdef`**: Does the test folder contain an `.asmdef` file? If not, create one.
2. **Verify `overrideReferences`**: Must be `true` to enable `precompiledReferences`.
3. **Verify `precompiledReferences`**: Must contain `"nunit.framework.dll"`.
4. **Verify `references`**: Must contain `"UnityEngine.TestRunner"` and `"UnityEditor.TestRunner"`.
5. **Verify `defineConstraints`**: Must contain `"UNITY_INCLUDE_TESTS"`.
6. **Check `includePlatforms`**: EditMode tests must have `["Editor"]`; PlayMode tests should have `[]`.
7. **Refresh Unity**: After creating/modifying `.asmdef`, use `unityMCP_refresh_unity` or reimport.
8. **Check package installation**: Verify `com.unity.test-framework` is installed in Package Manager.

## Common Test Discovery Issues & Solutions

These issues differ from compilation errors — tests **compile successfully** but the Test Runner shows "No tests to show" or does not list them.

### "No tests to show" in Test Runner Window

**Symptom**: Test scripts compile without errors, but the EditMode Test Runner window shows "No tests to show" or an empty test tree.

**Root Cause**: The tests are compiled into an assembly the Test Runner does not recognize as a test assembly. This typically happens when an `.asmdef` file is misconfigured.

**Common Causes & Solutions**:

| Cause | Diagnosis | Solution |
|:------|:----------|:---------|
| Invalid `.asmdef` with `Assembly-CSharp.dll` in `precompiledReferences` | Open `.asmdef` → check `precompiledReferences` for `Assembly-CSharp.dll` | Remove the `.asmdef` entirely and move tests to `Editor/` folder, OR fix the `.asmdef` (see [Assembly Definition Pitfalls](#assembly-definition-pitfalls)) |
| Missing `defineConstraints` | `.asmdef` has no `UNITY_INCLUDE_TESTS` constraint | Add `"defineConstraints": ["UNITY_INCLUDE_TESTS"]` |
| Wrong `includePlatforms` | EditMode `.asmdef` missing `["Editor"]` | Set `"includePlatforms": ["Editor"]` for EditMode tests |
| Missing TestRunner references | `.asmdef` lacks `UnityEngine.TestRunner` / `UnityEditor.TestRunner` | Add both to `references` array |
| Tests in wrong folder | Tests in `EditMode/` without valid `.asmdef` | Move to `Editor/` folder (recommended) or create valid `.asmdef` |

### Troubleshooting Steps for Test Discovery

1. **Check Test Runner window**: `Window > General > Test Runner > EditMode` tab
2. **Verify test folder location**: Prefer `Assets/Scripts/Test/Editor/` (no `.asmdef` needed)
3. **If using `.asmdef`**: Open the `.asmdef` in text editor and verify:
   - `precompiledReferences` does NOT contain `Assembly-CSharp.dll`
   - `precompiledReferences` contains `nunit.framework.dll`
   - `references` contains `UnityEngine.TestRunner` and `UnityEditor.TestRunner`
   - `defineConstraints` contains `UNITY_INCLUDE_TESTS`
   - `includePlatforms` is `["Editor"]` for EditMode
4. **Force reimport**: Right-click test folder → Reimport, then check Test Runner again
5. **If still failing**: Delete the `.asmdef` and move tests to an `Editor/` folder

### Real-World Example: WWE Champions Fix

**Before (broken)**: `Assets/Scripts/Test/EditMode/EditModeTests.asmdef` contained:
```json
{
    "precompiledReferences": ["Assembly-CSharp.dll", "nunit.framework.dll"]
}
```
Tests compiled but Test Runner showed "No tests to show" because `Assembly-CSharp.dll` is not a precompiled DLL — it corrupted the assembly resolution.

**After (fixed)**: Removed `.asmdef`, moved tests to `Assets/Scripts/Test/Editor/`. Tests immediately appeared in Test Runner with zero configuration.

## Assembly Definition Pitfalls

Misconfigured `.asmdef` files are the **#1 cause** of test discovery failures. Tests compile without errors but the Test Runner cannot find them.

### NEVER Add `Assembly-CSharp.dll` to `precompiledReferences`

`Assembly-CSharp` is **not** a precompiled DLL — it is Unity's default compilation output for scripts outside any `.asmdef`. Adding it to `precompiledReferences` causes:

1. **Silent assembly resolution failure** — the `.asmdef` looks for a literal `Assembly-CSharp.dll` in precompiled paths, which does not exist there
2. **Tests compile** — because Unity's compilation pipeline still resolves the reference through other means
3. **Test Runner ignores the assembly** — the corrupted reference metadata makes the assembly unrecognizable as a test assembly
4. **"No tests to show"** — the end result is a completely silent failure

### Correct vs Incorrect `.asmdef` Configuration

**❌ INCORRECT** — causes silent test discovery failure:
```json
{
    "name": "EditModeTests",
    "overrideReferences": true,
    "precompiledReferences": [
        "Assembly-CSharp.dll",
        "nunit.framework.dll"
    ],
    "references": [
        "UnityEngine.TestRunner",
        "UnityEditor.TestRunner"
    ]
}
```

**✅ CORRECT** — if you must use `.asmdef`:
```json
{
    "name": "EditModeTests",
    "overrideReferences": true,
    "precompiledReferences": [
        "nunit.framework.dll"
    ],
    "references": [
        "UnityEngine.TestRunner",
        "UnityEditor.TestRunner"
    ],
    "includePlatforms": ["Editor"],
    "defineConstraints": ["UNITY_INCLUDE_TESTS"],
    "autoReferenced": false
}
```

**✅ BEST** — use `Editor/` folder instead (no `.asmdef` needed):
```
Assets/Scripts/Test/Editor/MyTests.cs  ← compiles into Assembly-CSharp-Editor automatically
```

### How Game Code Access Works Without `Assembly-CSharp.dll`

When game code has **no** `.asmdef` (compiles into `Assembly-CSharp`):
- `Assembly-CSharp-Editor` (from `Editor/` folders) **automatically** references `Assembly-CSharp`
- Test `.asmdef` assemblies **implicitly** reference `Assembly-CSharp` — no configuration needed

When game code has its **own** `.asmdef` (e.g., `GameCore`):
- Add `"GameCore"` to the test `.asmdef`'s `references` array
- `Editor/` folder tests still access it if `GameCore` is `autoReferenced: true`

## References

- [TEST_EXAMPLES.md](references/TEST_EXAMPLES.md) — Comprehensive examples: multiple test classes per feature, Edit/Play Mode, mocking, parameterized, event testing, integration testing

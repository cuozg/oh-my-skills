# Test Patterns & Organization Reference

> Extracted from `unity-test/SKILL.md` — comprehensive test patterns, naming conventions, assertions, anti-patterns, best practices, and MCP integration.

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

When using `.asmdef`, follow the [Assembly Definition Setup & Checklist](test-assembly-setup.md) exactly.

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

# Test Patterns & Organization Reference

## Test Folder Structure

**Recommended for EditMode**: Place tests in `Editor/` folder — no `.asmdef` needed, auto-discovers in Test Runner.

```
Assets/Scripts/Test/Editor/
├── FeatureA/
│   └── FeatureATests.cs
└── Helpers/
    └── TestDoubles.cs
```

Use `.asmdef` only when: tests reference custom assemblies, need assembly isolation, or are PlayMode tests. See [Assembly Definition Setup](test-assembly-setup.md).

## Edit Mode vs Play Mode

**Default to Edit Mode** (faster, no scene required). Use Play Mode ONLY for: MonoBehaviour lifecycle, physics, coroutines, Awaitable async (Unity 6+), UI interaction, scene loading.

## Naming & Structure

```
[Subject]_[Scenario]_[ExpectedResult]
```

Arrange-Act-Assert:
```csharp
[Test]
public void Inventory_AddValidItem_ReturnsTrue()
{
    var inventory = new Inventory(maxSlots: 10);
    var item = new Item("sword");
    var result = inventory.Add(item);
    Assert.IsTrue(result);
}
```

## Key Patterns

**SetUp/TearDown**: Fresh instances per test in `[SetUp]`, destroy GameObjects in `[TearDown]`. Never rely on execution order.

| Dependency Type | Strategy |
|---|---|
| Interface-based | Test doubles implementing interface |
| Concrete class | Wrap in interface or subclass override |
| Static/Singleton | Isolate behind wrapper |
| MonoBehaviour | `new GameObject().AddComponent<T>()` in SetUp |

**Assertions**: `AreEqual`, `IsTrue/IsFalse`, `IsNull/IsNotNull`, `Throws<T>`, `Is.InRange`. Use tolerance for floats. Always add descriptive messages.

**Parameterized**: `[TestCase(100, 30, 70)]` for data-driven coverage.

**Async**: `[UnityTest]` + `IEnumerator` for coroutines, `async Task` for Unity 6+ Awaitable. Always set timeout.

## Anti-Patterns

| Anti-Pattern | Do Instead |
|---|---|
| Testing private methods | Test through public API |
| Shared mutable state | Fresh state in `[SetUp]` |
| No TearDown cleanup | Always destroy in `[TearDown]` |
| Magic numbers | Named constants or factories |
| Multiple behaviors per test | One behavior = one test |
| `Time.deltaTime` in assertions | Fixed values or `WaitForFixedUpdate` |
| Missing `.asmdef` in non-Editor/ folder | Use `Editor/` folder or valid `.asmdef` |

## Best Practices

- Edit Mode tests under 10ms each
- Avoid `Time.deltaTime` in assertions — use fixed values
- Always destroy GameObjects — leaked objects corrupt subsequent tests
- Tests must not modify ProjectSettings or PlayerPrefs
- Each test validates exactly one behavior
- Use descriptive assertion messages

## MCP Tools Integration

| Operation | Tool |
|---|---|
| Check compilation | `unityMCP_check_compile_errors` |
| Read test logs | `unityMCP_get_unity_logs(search_term="Test")` |
| Run editor script | `unityMCP_execute_script(filePath)` |

Flow: check compile → execute test runner → check logs → fix & repeat.

## Output

Test generation produces: C# test scripts in `Editor/` (EditMode) or `PlayMode/` folders, clean compilation, `[Subject]_[Scenario]_[ExpectedResult]` naming, `.asmdef` for PlayMode only.

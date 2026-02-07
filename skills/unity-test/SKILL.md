---
name: unity-test
description: "Unity Test Framework automation. Use when: (1) Creating Edit/Play Mode tests, (2) Configuring test assemblies (.asmdef), (3) Mocking dependencies, (4) Analyzing test results."
---

# Unity Testing

Create and manage automated tests using Unity Test Framework.

## Output Requirement (MANDATORY)

**Every test plan MUST follow the template**: [TEST_PLAN_TEMPLATE.md](.claude/skills/unity-test/assets/templates/TEST_PLAN_TEMPLATE.md)

Place test scripts in `Tests/EditMode/` or `Tests/PlayMode/` as appropriate.

Read the template first, then populate all sections.

## Test Types

| Type | Use For | Location |
|------|---------|----------|
| **Edit Mode** | Pure logic, algorithms, non-Unity code | `Tests/EditMode/` |
| **Play Mode** | Physics, lifecycles, coroutines, UI | `Tests/PlayMode/` |

## Workflow

1. **Analyze**: Target method/class, check for existing `.asmdef`
2. **Setup**: Create `Tests/` folder + `.asmdef` referencing `UnityEngine.TestRunner`
3. **Implement**: Arrange-Act-Assert pattern, use `[SetUp]`/`[TearDown]`
4. **Execute**: `unityMCP.run_tests`
5. **Fix Failures**: Use `/unity-fix-errors` or `/unity-investigate-code`

## Test Naming Convention

```
[Subject]_[Scenario]_[ExpectedResult]
```
Example: `Player_TakesDamage_HealthDecreases`

## Example Test

```csharp
[Test]
public void Player_TakesDamage_HealthDecreases()
{
    // Arrange
    var player = new PlayerHealth(100);
    
    // Act
    player.TakeDamage(30);
    
    // Assert
    Assert.AreEqual(70, player.CurrentHealth);
}
```

## Best Practices

- **Atomic**: One behavior per test
- **Cleanup**: Destroy test GameObjects in `TearDown`
- **Isolation**: No external data dependencies
- **Naming**: Descriptive `Subject_Scenario_Expected`

See [TEST_EXAMPLES.md](.claude/skills/unity-test/references/TEST_EXAMPLES.md) for more patterns.

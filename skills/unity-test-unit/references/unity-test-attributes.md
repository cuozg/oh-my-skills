# unity-test-attributes.md

## Attribute Quick Reference

| Attribute | Mode | Purpose |
|---|---|---|
| `[Test]` | Edit | Synchronous test, no Unity lifecycle |
| `[UnityTest]` | Play | Coroutine test, yields frames |
| `[SetUp]` | Both | Runs before each test method |
| `[TearDown]` | Both | Runs after each test method |
| `[OneTimeSetUp]` | Both | Runs once before all tests in class |
| `[OneTimeTearDown]` | Both | Runs once after all tests in class |
| `[TestCase(a, b)]` | Edit | Parameterized test with inline values |
| `[Ignore("reason")]` | Both | Skip test with explanation |
| `[Category("name")]` | Both | Group tests for filtered runs |

## Edit Mode vs Play Mode

**Edit Mode** — no GameObject required, instant, no frame delay
```csharp
// Assembly: Tests/EditMode
[Test]
public void Calculate_Returns_CorrectValue() { ... }
```

**Play Mode** — use when coroutines, physics, or MonoBehaviour lifecycle is needed
```csharp
// Assembly: Tests/PlayMode
[UnityTest]
public IEnumerator MovePlayer_AfterOneSecond_ReachesTarget()
{
    var player = new GameObject().AddComponent<PlayerController>();
    player.MoveTo(Vector3.forward * 5f);
    yield return new WaitForSeconds(1f);
    Assert.That(player.transform.position.z, Is.GreaterThan(4f));
}
```

## Assembly Definition Requirements

Edit Mode asmdef: reference `UnityEngine.TestRunner`, `UnityEditor.TestRunner`
Play Mode asmdef: reference `UnityEngine.TestRunner` only

## Parameterized Tests

```csharp
[TestCase(0, 0)]
[TestCase(1, 2)]
[TestCase(-1, -2)]
public void Double_Input_ReturnsDoubled(int input, int expected)
{
    Assert.AreEqual(expected, _sut.Double(input));
}
```

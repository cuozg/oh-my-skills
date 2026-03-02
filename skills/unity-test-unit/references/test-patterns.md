# test-patterns.md

## Arrange-Act-Assert (AAA)

```csharp
[Test]
public void MethodName_Condition_ExpectedResult()
{
    // Arrange
    var sut = new MyClass();
    int input = 5;

    // Act
    int result = sut.Double(input);

    // Assert
    Assert.AreEqual(10, result);
}
```

## Common Assertions

| Assertion | Use |
|---|---|
| `Assert.AreEqual(expected, actual)` | Value equality |
| `Assert.IsTrue(condition)` | Boolean check |
| `Assert.IsNull(obj)` / `Assert.IsNotNull(obj)` | Null check |
| `Assert.Throws<T>(() => ...)` | Exception expected |
| `Assert.That(collection, Has.Count.EqualTo(n))` | Collection size |
| `Assert.That(value, Is.InRange(min, max))` | Range check |

## Mocking with NSubstitute

```csharp
// Create substitute
var mockRepo = Substitute.For<IRepository>();

// Set return value
mockRepo.GetById(1).Returns(new Entity { Id = 1 });

// Verify call
mockRepo.Received(1).Save(Arg.Any<Entity>());
```

## Test Case Categories to Cover

- **Happy path** — expected inputs, normal flow
- **Boundary** — min/max values, empty collections, zero
- **Edge** — null inputs, empty strings, max int
- **Negative** — invalid state, exception paths
- **State** — before/after mutation checks

## SetUp / TearDown Pattern

```csharp
[SetUp]
public void SetUp() { _sut = new MyClass(); }

[TearDown]
public void TearDown() { _sut = null; }
```

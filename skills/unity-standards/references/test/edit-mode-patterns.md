# Edit Mode Test Patterns

## Basic Test

```csharp
using NUnit.Framework;
[TestFixture]
public class HealthTests
{
    [Test]
    public void TakeDamage_ReducesHealth()
    {
        var health = new HealthData(100);
        health.TakeDamage(30);
        Assert.AreEqual(70, health.Current);
    }
}
```

## Assert Methods

| Method | Use |
|--------|-----|
| `Assert.AreEqual(expected, actual)` | Value equality |
| `Assert.IsTrue(condition)` | Boolean check |
| `Assert.IsFalse(condition)` | Negated boolean |
| `Assert.IsNotNull(obj)` | Null guard |
| `Assert.IsNull(obj)` | Expect null |
| `Assert.Throws<T>(() => ...)` | Exception expected |
| `Assert.That(x, Is.GreaterThan(y))` | Constraint model |
| `Assert.AreEqual(1f, val, 0.01f)` | Float tolerance |

## SetUp / TearDown

```csharp
private HealthData _health;

[SetUp]
public void SetUp() => _health = new HealthData(100);
[TearDown]
public void TearDown() => _health = null;
```

## Parameterized Tests

```csharp
[TestCase(100, 30, 70)]
[TestCase(50, 50, 0)]
[TestCase(10, 99, 0)]  // clamped to 0
public void TakeDamage_Parameterized(int max, int dmg, int expected)
{
    var h = new HealthData(max);
    h.TakeDamage(dmg);
    Assert.AreEqual(expected, h.Current);
}
```

## Testing ScriptableObjects

```csharp
[Test]
public void WeaponConfig_DefaultValues()
{
    var weapon = ScriptableObject.CreateInstance<WeaponConfig>();
    Assert.IsNotNull(weapon);
    Assert.AreEqual(0f, weapon.Damage);
    Object.DestroyImmediate(weapon); // cleanup
}
```

## Interface Substitution (Manual Mock)

```csharp
private class FakeLogger : ILogger
{
    public string LastMessage { get; private set; }
    public void Log(string msg) => LastMessage = msg;
}

[Test]
public void System_LogsOnInit()
{
    var logger = new FakeLogger();
    var system = new GameSystem(logger);
    system.Init();
    Assert.AreEqual("Initialized", logger.LastMessage);
}
```

## Exception Testing
```csharp
[Test]
public void TakeDamage_NegativeValue_Throws()
{
    var h = new HealthData(100);
    Assert.Throws<ArgumentException>(() => h.TakeDamage(-1));
}
```
<!-- Advanced: edit-mode-advanced.md -->

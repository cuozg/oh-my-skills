# Edit Mode Test Patterns — Advanced

## NSubstitute — Mocking Framework

```csharp
using NSubstitute;
using NUnit.Framework;

[Test]
public void DamageCalculator_AppliesArmor()
{
    var armor = Substitute.For<IArmorService>();
    armor.Reduction.Returns(0.5f);

    var buffs = Substitute.For<IBuffService>();
    buffs.Multiplier.Returns(1.0f);

    var calc = new DamageCalculator(armor, buffs);
    Assert.AreEqual(50f, calc.Calculate(100f), 0.01f);
}

[Test]
public void EventBus_NotifiesSubscribers()
{
    var handler = Substitute.For<IEventHandler<DamageEvent>>();
    var bus = new EventBus();
    bus.Subscribe(handler);

    bus.Publish(new DamageEvent(50f));

    handler.Received(1).Handle(Arg.Is<DamageEvent>(e => e.Amount == 50f));
}
```

**Setup:** Add `com.unity.testtools.codecoverage` and NSubstitute via NuGet or Assembly Definition reference.

## Testing MonoBehaviour Indirectly

```csharp
// Extract logic into pure C# class — test that instead
public class HealthLogic
{
    public float Current { get; private set; }
    public float Max { get; }
    public bool IsDead => Current <= 0;

    public HealthLogic(float max) { Max = max; Current = max; }
    public void TakeDamage(float amount) => Current = Mathf.Max(0, Current - amount);
}

// MonoBehaviour delegates to logic class
public sealed class HealthComponent : MonoBehaviour
{
    [SerializeField] private float _maxHealth = 100f;
    public HealthLogic Logic { get; private set; }
    void Awake() => Logic = new HealthLogic(_maxHealth);
}

// Test pure logic — no MonoBehaviour instantiation needed
[Test]
public void HealthLogic_DiesAtZero()
{
    var health = new HealthLogic(100);
    health.TakeDamage(100);
    Assert.IsTrue(health.IsDead);
}
```

# Edit Mode Test Patterns - Advanced

## Async Tests (`async Task`)

Test Framework 1.3+ (Unity 6 ships 1.4+) awaits `async Task` tests and
`[SetUp]`/`[TearDown]` on the main thread, polling each Editor update (Edit Mode)
or frame (Play Mode).

```csharp
using System.Threading.Tasks;
using NUnit.Framework;

[Test]
public async Task LoadProfile_ValidId_ReturnsProfile()
{
    var service = new ProfileService(new FakeProfileStore());

    var profile = await service.LoadAsync("player-1");

    Assert.AreEqual("player-1", profile.Id);
}
```

- Failing `LogAssert` checks are evaluated after the async method completes.
- Keep `[UnityTest]` `IEnumerator` for frame-exact yields (`WaitForFixedUpdate`, etc.).

## Mocking

Interface fakes: `edit-mode-patterns.md` (Interface Substitution). NSubstitute
setup and usage live in the `unity-test-unit` skill:
`../unity-test-unit/references/test-patterns.md`.

## Testing MonoBehaviour Indirectly

```csharp
// Extract logic into pure C# class - test that instead
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

// Test pure logic - no MonoBehaviour instantiation needed
[Test]
public void HealthLogic_DiesAtZero()
{
    var health = new HealthLogic(100);
    health.TakeDamage(100);
    Assert.IsTrue(health.IsDead);
}
```

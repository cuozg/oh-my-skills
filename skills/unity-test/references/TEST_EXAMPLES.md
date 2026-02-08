# Unity Test Examples

Patterns organized by test type. Each demonstrates test logic generation rules from SKILL.md.

## Edit Mode — Pure Logic

Fast tests for non-Unity code. Default choice per Rule 5.

```csharp
[TestFixture]
public class HealthTests
{
    private const int FullHealth = 100;
    private const int StandardDamage = 30;
    private Health _health;

    [SetUp]
    public void SetUp()
    {
        _health = new Health();
        _health.SetMax(FullHealth);
    }

    // Rule 1: Happy path
    [Test]
    public void Health_TakesDamage_ValueDecreases()
    {
        _health.TakeDamage(StandardDamage);
        Assert.AreEqual(70, _health.Current);
    }

    // Rule 1: Boundary — zero damage
    [Test]
    public void Health_TakesZeroDamage_ValueUnchanged()
    {
        _health.TakeDamage(0);
        Assert.AreEqual(FullHealth, _health.Current);
    }

    // Rule 1: Boundary — overkill
    [Test]
    public void Health_TakesDamageExceedingMax_ClampsToZero()
    {
        _health.TakeDamage(FullHealth + 50);
        Assert.AreEqual(0, _health.Current);
    }

    // Rule 1: Error condition — negative input
    [Test]
    public void Health_TakesNegativeDamage_ClampsToZero()
    {
        _health.TakeDamage(-10);
        Assert.AreEqual(FullHealth, _health.Current,
            "Negative damage should be ignored");
    }
}
```

## Edit Mode — Parameterized Tests

Rule 8: Use `[TestCase]` for data-driven tests.

```csharp
[TestFixture]
public class DamageCalculatorTests
{
    // Multiple inputs tested with one method
    [TestCase(100, 30, 70)]
    [TestCase(100, 0, 100)]
    [TestCase(100, 100, 0)]
    [TestCase(100, 150, 0)]
    public void CalculateFinalHealth_VariousDamage_ReturnsExpected(
        int maxHp, int damage, int expected)
    {
        var result = DamageCalculator.CalculateFinalHealth(maxHp, damage);
        Assert.AreEqual(expected, result);
    }

    // Floating point with tolerance (Rule 6)
    [TestCase(10f, 0.3f, 7f, 0.01f)]
    public void CalculatePercentDamage_FloatValues_WithinTolerance(
        float hp, float percent, float expected, float tolerance)
    {
        var result = DamageCalculator.PercentDamage(hp, percent);
        Assert.AreEqual(expected, result, tolerance);
    }
}
```

## Edit Mode — Event Testing

Code Analysis Checklist item 4: Events.

```csharp
[TestFixture]
public class HealthEventTests
{
    private Health _health;
    private bool _deathFired;
    private int _damageReceived;

    [SetUp]
    public void SetUp()
    {
        _health = new Health();
        _health.SetMax(100);
        _deathFired = false;
        _damageReceived = 0;
        _health.OnDeath += () => _deathFired = true;
        _health.OnDamaged += (amount) => _damageReceived = amount;
    }

    [TearDown]
    public void TearDown()
    {
        _health.OnDeath -= () => _deathFired = true;
        _health.OnDamaged -= (amount) => _damageReceived = amount;
    }

    [Test]
    public void Health_DiesAtZero_FiresOnDeathEvent()
    {
        _health.TakeDamage(100);
        Assert.IsTrue(_deathFired);
    }

    [Test]
    public void Health_TakesDamage_FiresOnDamagedWithAmount()
    {
        _health.TakeDamage(25);
        Assert.AreEqual(25, _damageReceived);
    }

    [Test]
    public void Health_DamageWhileAlive_DoesNotFireOnDeath()
    {
        _health.TakeDamage(50);
        Assert.IsFalse(_deathFired);
    }
}
```

## Edit Mode — Mocking Dependencies

Rule 3: Interface-based dependency handling.

```csharp
// Test double for an interface dependency
public class MockRewardService : IRewardService
{
    public int GrantCallCount { get; private set; }
    public string LastRewardId { get; private set; }

    public bool GrantReward(string rewardId)
    {
        GrantCallCount++;
        LastRewardId = rewardId;
        return true;
    }
}

[TestFixture]
public class QuestCompleterTests
{
    [Test]
    public void CompleteQuest_ValidQuest_GrantsReward()
    {
        var mockRewards = new MockRewardService();
        var completer = new QuestCompleter(mockRewards);

        completer.Complete("quest_001");

        Assert.AreEqual(1, mockRewards.GrantCallCount);
        Assert.AreEqual("quest_001_reward", mockRewards.LastRewardId);
    }
}
```

## Edit Mode — Exception Testing

Rule 6: `Assert.Throws<T>`.

```csharp
[Test]
public void Inventory_AddNullItem_ThrowsArgumentNull()
{
    var inventory = new Inventory(maxSlots: 10);

    Assert.Throws<ArgumentNullException>(() =>
        inventory.Add(null));
}

[Test]
public void Inventory_AddWhenFull_ReturnsFalse()
{
    var inventory = new Inventory(maxSlots: 1);
    inventory.Add(new Item("sword"));

    var result = inventory.Add(new Item("shield"));

    Assert.IsFalse(result, "Should reject item when full");
}
```

## Play Mode — MonoBehaviour Lifecycle

Rule 5: Use Play Mode when Unity lifecycle is needed.

```csharp
[UnityTest]
public IEnumerator PlayerMovement_MoveForward_PositionChanges()
{
    var go = new GameObject("TestPlayer");
    var movement = go.AddComponent<PlayerMovement>();
    var startPos = go.transform.position;

    movement.Move(Vector3.forward);
    yield return new WaitForFixedUpdate();

    Assert.IsTrue(go.transform.position.z > startPos.z,
        "Player should move forward on Z axis");
    Object.Destroy(go);
}
```

## Play Mode — Coroutine Test

Rule 7: `[UnityTest]` returning `IEnumerator`.

```csharp
[UnityTest]
public IEnumerator Spawner_SpawnWithDelay_CreatesObjectAfterWait()
{
    var go = new GameObject("TestSpawner");
    var spawner = go.AddComponent<EnemySpawner>();
    spawner.SpawnDelay = 0.2f;

    spawner.StartSpawning();
    yield return new WaitForSeconds(0.3f);

    Assert.AreEqual(1, spawner.SpawnCount);
    Object.Destroy(go);
}
```

## Play Mode — Physics Interaction

```csharp
[UnityTest]
public IEnumerator Projectile_HitsTarget_DealsDamage()
{
    var target = new GameObject("Target");
    target.AddComponent<BoxCollider>();
    var health = target.AddComponent<HealthComponent>();
    health.Initialize(100);

    var projectile = new GameObject("Bullet");
    projectile.AddComponent<SphereCollider>();
    var rb = projectile.AddComponent<Rigidbody>();
    var dmg = projectile.AddComponent<DamageOnContact>();
    dmg.Damage = 25;

    projectile.transform.position = target.transform.position + Vector3.back * 2f;
    rb.linearVelocity = Vector3.forward * 50f;

    yield return new WaitForSeconds(0.5f);

    Assert.AreEqual(75, health.Current,
        "Target health should decrease by projectile damage");
    Object.Destroy(target);
    Object.Destroy(projectile);
}
```

## Test Directory Structure

Place all test scripts under `Assets/Scripts/Test/`. Do NOT create `.asmdef` files — the project manages assembly definitions externally.

```
Assets/Scripts/Test/
├── EditMode/     # Pure C# logic tests (no Unity API)
└── PlayMode/     # MonoBehaviour, coroutine, physics, UI tests
```

## Test Logic Generation — Worked Example

Given a class to test, here is how rules produce test cases:

**Source code:**
```csharp
public class Inventory
{
    public int MaxSlots { get; }
    public int Count => _items.Count;
    public event Action<Item> OnItemAdded;

    public Inventory(int maxSlots) { ... }
    public bool Add(Item item) { ... }
    public bool Remove(string itemId) { ... }
    public Item GetById(string itemId) { ... }
}
```

**Applying Code Analysis Checklist:**

| Checklist Item | Test Cases Generated |
|:---|:---|
| Constructor | `Inventory_CreatedWithSlots_HasZeroCount`, `Inventory_NegativeSlots_ThrowsArgument` |
| Add (happy) | `Add_ValidItem_ReturnsTrue`, `Add_ValidItem_IncrementsCount` |
| Add (boundary) | `Add_WhenFull_ReturnsFalse`, `Add_NullItem_ThrowsArgumentNull` |
| Add (event) | `Add_ValidItem_FiresOnItemAdded` |
| Remove (happy) | `Remove_ExistingItem_ReturnsTrue`, `Remove_ExistingItem_DecrementsCount` |
| Remove (error) | `Remove_NonexistentId_ReturnsFalse`, `Remove_NullId_ThrowsArgumentNull` |
| GetById (happy) | `GetById_ExistingItem_ReturnsItem` |
| GetById (error) | `GetById_NonexistentId_ReturnsNull` |
| Collection | `Inventory_Empty_CountIsZero`, `Inventory_MultipleItems_CountMatches` |

This table maps directly to TEST_PLAN_TEMPLATE.md § Test Cases.

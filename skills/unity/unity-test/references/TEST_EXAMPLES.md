# Unity Test Examples

Comprehensive examples demonstrating test organization by feature, maximum coverage, and Unity Test Framework patterns.

## Table of Contents

- [Feature: Inventory System (Edit Mode)](#feature-inventory-system-edit-mode)
- [Feature: Inventory Events (Edit Mode)](#feature-inventory-events-edit-mode)
- [Feature: Inventory Integration (Edit Mode)](#feature-inventory-integration-edit-mode)
- [Feature: Player Movement (Play Mode)](#feature-player-movement-play-mode)
- [Feature: Spawner System (Play Mode)](#feature-spawner-system-play-mode)
- [Patterns: Mocking Dependencies](#patterns-mocking-dependencies)
- [Patterns: Parameterized Tests](#patterns-parameterized-tests)
- [Patterns: State Machine Testing](#patterns-state-machine-testing)

---

## Feature: Inventory System (Edit Mode)

Core logic tests — happy path, boundaries, error conditions. 15 test cases.

```csharp
using NUnit.Framework;
using System;

[TestFixture]
public class InventoryTests
{
    private const int DefaultMaxSlots = 10;
    private Inventory _inventory;

    [SetUp]
    public void SetUp()
    {
        _inventory = new Inventory(DefaultMaxSlots);
    }

    // --- Constructor ---

    [Test]
    public void Constructor_ValidSlots_CreatesEmptyInventory()
    {
        Assert.AreEqual(0, _inventory.Count, "New inventory should be empty");
    }

    [Test]
    public void Constructor_ValidSlots_SetsMaxSlots()
    {
        Assert.AreEqual(DefaultMaxSlots, _inventory.MaxSlots);
    }

    [Test]
    public void Constructor_ZeroSlots_ThrowsArgumentException()
    {
        Assert.Throws<ArgumentException>(() => new Inventory(0));
    }

    [Test]
    public void Constructor_NegativeSlots_ThrowsArgumentException()
    {
        Assert.Throws<ArgumentException>(() => new Inventory(-5));
    }

    // --- Add ---

    [Test]
    public void Add_ValidItem_ReturnsTrue()
    {
        var result = _inventory.Add(new Item("sword"));
        Assert.IsTrue(result);
    }

    [Test]
    public void Add_ValidItem_IncrementsCount()
    {
        _inventory.Add(new Item("sword"));
        Assert.AreEqual(1, _inventory.Count);
    }

    [Test]
    public void Add_NullItem_ThrowsArgumentNullException()
    {
        Assert.Throws<ArgumentNullException>(() => _inventory.Add(null));
    }

    [Test]
    public void Add_WhenFull_ReturnsFalse()
    {
        var inventory = new Inventory(maxSlots: 1);
        inventory.Add(new Item("sword"));

        var result = inventory.Add(new Item("shield"));

        Assert.IsFalse(result, "Should reject item when full");
    }

    [Test]
    public void Add_WhenFull_DoesNotIncrementCount()
    {
        var inventory = new Inventory(maxSlots: 1);
        inventory.Add(new Item("sword"));
        inventory.Add(new Item("shield"));

        Assert.AreEqual(1, inventory.Count, "Count should not increase past capacity");
    }

    [Test]
    public void Add_ExactlyAtCapacity_Succeeds()
    {
        var inventory = new Inventory(maxSlots: 2);
        inventory.Add(new Item("sword"));
        var result = inventory.Add(new Item("shield"));

        Assert.IsTrue(result, "Should accept item at exactly max capacity");
        Assert.AreEqual(2, inventory.Count);
    }

    // --- Remove ---

    [Test]
    public void Remove_ExistingItem_ReturnsTrue()
    {
        _inventory.Add(new Item("sword", id: "item_001"));
        var result = _inventory.Remove("item_001");
        Assert.IsTrue(result);
    }

    [Test]
    public void Remove_ExistingItem_DecrementsCount()
    {
        _inventory.Add(new Item("sword", id: "item_001"));
        _inventory.Remove("item_001");
        Assert.AreEqual(0, _inventory.Count);
    }

    [Test]
    public void Remove_NonexistentId_ReturnsFalse()
    {
        var result = _inventory.Remove("nonexistent");
        Assert.IsFalse(result);
    }

    [Test]
    public void Remove_NullId_ThrowsArgumentNullException()
    {
        Assert.Throws<ArgumentNullException>(() => _inventory.Remove(null));
    }

    // --- GetById ---

    [Test]
    public void GetById_ExistingItem_ReturnsItem()
    {
        var item = new Item("sword", id: "item_001");
        _inventory.Add(item);

        var result = _inventory.GetById("item_001");

        Assert.IsNotNull(result);
        Assert.AreEqual("sword", result.Name);
    }

    [Test]
    public void GetById_NonexistentId_ReturnsNull()
    {
        var result = _inventory.GetById("nonexistent");
        Assert.IsNull(result);
    }
}
```

---

## Feature: Inventory Events (Edit Mode)

Event-focused tests for the same Inventory feature. 10 test cases.

```csharp
using NUnit.Framework;
using System;

[TestFixture]
public class InventoryEventTests
{
    private Inventory _inventory;
    private Item _lastAddedItem;
    private string _lastRemovedId;
    private bool _fullEventFired;
    private int _addEventCount;

    [SetUp]
    public void SetUp()
    {
        _inventory = new Inventory(maxSlots: 3);
        _lastAddedItem = null;
        _lastRemovedId = null;
        _fullEventFired = false;
        _addEventCount = 0;

        _inventory.OnItemAdded += item => { _lastAddedItem = item; _addEventCount++; };
        _inventory.OnItemRemoved += id => _lastRemovedId = id;
        _inventory.OnInventoryFull += () => _fullEventFired = true;
    }

    // --- OnItemAdded ---

    [Test]
    public void Add_ValidItem_FiresOnItemAdded()
    {
        var item = new Item("sword");
        _inventory.Add(item);
        Assert.AreEqual(item, _lastAddedItem);
    }

    [Test]
    public void Add_ValidItem_FiresOnItemAddedOnce()
    {
        _inventory.Add(new Item("sword"));
        Assert.AreEqual(1, _addEventCount, "Event should fire exactly once per add");
    }

    [Test]
    public void Add_WhenFull_DoesNotFireOnItemAdded()
    {
        var inventory = new Inventory(maxSlots: 1);
        inventory.OnItemAdded += _ => _addEventCount++;
        _addEventCount = 0;

        inventory.Add(new Item("sword"));
        inventory.Add(new Item("shield")); // rejected

        Assert.AreEqual(1, _addEventCount, "Should not fire for rejected add");
    }

    [Test]
    public void Add_MultipleItems_FiresOnItemAddedForEach()
    {
        _inventory.Add(new Item("sword"));
        _inventory.Add(new Item("shield"));
        Assert.AreEqual(2, _addEventCount);
    }

    // --- OnItemRemoved ---

    [Test]
    public void Remove_ExistingItem_FiresOnItemRemoved()
    {
        _inventory.Add(new Item("sword", id: "item_001"));
        _inventory.Remove("item_001");
        Assert.AreEqual("item_001", _lastRemovedId);
    }

    [Test]
    public void Remove_NonexistentItem_DoesNotFireOnItemRemoved()
    {
        _inventory.Remove("nonexistent");
        Assert.IsNull(_lastRemovedId, "Should not fire for failed remove");
    }

    // --- OnInventoryFull ---

    [Test]
    public void Add_ReachesCapacity_FiresOnInventoryFull()
    {
        _inventory = new Inventory(maxSlots: 2);
        _inventory.OnInventoryFull += () => _fullEventFired = true;

        _inventory.Add(new Item("sword"));
        _inventory.Add(new Item("shield")); // reaches capacity

        Assert.IsTrue(_fullEventFired);
    }

    [Test]
    public void Add_BelowCapacity_DoesNotFireOnInventoryFull()
    {
        _inventory.Add(new Item("sword"));
        Assert.IsFalse(_fullEventFired);
    }

    [Test]
    public void Add_AlreadyFull_DoesNotFireOnInventoryFullAgain()
    {
        var inventory = new Inventory(maxSlots: 1);
        int fullCount = 0;
        inventory.OnInventoryFull += () => fullCount++;

        inventory.Add(new Item("sword"));  // fills
        inventory.Add(new Item("shield")); // rejected

        Assert.AreEqual(1, fullCount, "Should fire only when first reaching capacity");
    }

    // --- Unsubscribe safety ---

    [Test]
    public void Add_AfterUnsubscribe_DoesNotFireHandler()
    {
        int count = 0;
        Action<Item> handler = _ => count++;

        _inventory.OnItemAdded += handler;
        _inventory.Add(new Item("sword"));
        Assert.AreEqual(1, count);

        _inventory.OnItemAdded -= handler;
        _inventory.Add(new Item("shield"));
        Assert.AreEqual(1, count, "Handler should not fire after unsubscribe");
    }
}
```

---

## Feature: Inventory Integration (Edit Mode)

Tests verifying Inventory interaction with dependencies (reward service, persistence). 10 test cases.

```csharp
using NUnit.Framework;

// --- Test Doubles ---

public class MockRewardService : IRewardService
{
    public int GrantCallCount { get; private set; }
    public string LastRewardId { get; private set; }
    public bool ShouldFail { get; set; }

    public bool GrantReward(string rewardId)
    {
        GrantCallCount++;
        LastRewardId = rewardId;
        return !ShouldFail;
    }
}

public class MockPersistenceService : IPersistenceService
{
    public int SaveCallCount { get; set; }
    public string LastSavedData { get; private set; }
    public bool ShouldFail { get; set; }

    public bool Save(string key, string data)
    {
        SaveCallCount++;
        LastSavedData = data;
        return !ShouldFail;
    }

    public string Load(string key) => null;
}

// --- Tests ---

[TestFixture]
public class InventoryIntegrationTests
{
    private Inventory _inventory;
    private MockRewardService _mockRewards;
    private MockPersistenceService _mockPersistence;

    [SetUp]
    public void SetUp()
    {
        _mockRewards = new MockRewardService();
        _mockPersistence = new MockPersistenceService();
        _inventory = new Inventory(maxSlots: 10, _mockRewards, _mockPersistence);
    }

    // --- Reward integration ---

    [Test]
    public void Add_RewardItem_GrantsRewardViaService()
    {
        var rewardItem = new Item("chest", rewardId: "reward_001");
        _inventory.Add(rewardItem);

        Assert.AreEqual(1, _mockRewards.GrantCallCount);
        Assert.AreEqual("reward_001", _mockRewards.LastRewardId);
    }

    [Test]
    public void Add_NonRewardItem_DoesNotCallRewardService()
    {
        _inventory.Add(new Item("sword"));
        Assert.AreEqual(0, _mockRewards.GrantCallCount);
    }

    [Test]
    public void Add_RewardServiceFails_StillAddsItem()
    {
        _mockRewards.ShouldFail = true;
        var result = _inventory.Add(new Item("chest", rewardId: "reward_001"));

        Assert.IsTrue(result, "Item should be added even if reward fails");
        Assert.AreEqual(1, _inventory.Count);
    }

    [Test]
    public void Add_MultipleRewardItems_GrantsEachReward()
    {
        _inventory.Add(new Item("chest1", rewardId: "r1"));
        _inventory.Add(new Item("chest2", rewardId: "r2"));

        Assert.AreEqual(2, _mockRewards.GrantCallCount);
        Assert.AreEqual("r2", _mockRewards.LastRewardId);
    }

    // --- Persistence integration ---

    [Test]
    public void Add_Item_AutoSavesInventory()
    {
        _inventory.Add(new Item("sword"));
        Assert.AreEqual(1, _mockPersistence.SaveCallCount);
    }

    [Test]
    public void Remove_Item_AutoSavesInventory()
    {
        _inventory.Add(new Item("sword", id: "item_001"));
        _mockPersistence.SaveCallCount = 0; // reset after add

        _inventory.Remove("item_001");
        Assert.AreEqual(1, _mockPersistence.SaveCallCount);
    }

    [Test]
    public void Add_PersistenceFails_StillAddsItem()
    {
        _mockPersistence.ShouldFail = true;
        var result = _inventory.Add(new Item("sword"));

        Assert.IsTrue(result, "Item should be added even if save fails");
    }

    [Test]
    public void Add_WhenFull_DoesNotTriggerSave()
    {
        var inventory = new Inventory(1, _mockRewards, _mockPersistence);
        inventory.Add(new Item("sword"));
        _mockPersistence.SaveCallCount = 0;

        inventory.Add(new Item("shield")); // rejected
        Assert.AreEqual(0, _mockPersistence.SaveCallCount, "Should not save on rejected add");
    }

    [Test]
    public void Remove_NonexistentItem_DoesNotTriggerSave()
    {
        _inventory.Remove("nonexistent");
        Assert.AreEqual(0, _mockPersistence.SaveCallCount);
    }

    [Test]
    public void Add_RewardAndPersistence_BothCalled()
    {
        _inventory.Add(new Item("chest", rewardId: "r1"));

        Assert.AreEqual(1, _mockRewards.GrantCallCount, "Reward should be granted");
        Assert.AreEqual(1, _mockPersistence.SaveCallCount, "Inventory should be saved");
    }
}
```

---

## Feature: Player Movement (Play Mode)

MonoBehaviour lifecycle tests requiring Play Mode. 12 test cases.

```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

[TestFixture]
public class PlayerMovementTests
{
    private GameObject _playerGo;
    private PlayerMovement _movement;
    private const float MoveSpeed = 5f;
    private const float Tolerance = 0.01f;

    [SetUp]
    public void SetUp()
    {
        _playerGo = new GameObject("TestPlayer");
        _movement = _playerGo.AddComponent<PlayerMovement>();
        _movement.MoveSpeed = MoveSpeed;
    }

    [TearDown]
    public void TearDown()
    {
        if (_playerGo != null) Object.Destroy(_playerGo);
    }

    // --- Basic movement ---

    [UnityTest]
    public IEnumerator Move_Forward_PositionIncreases()
    {
        float startZ = _playerGo.transform.position.z;
        _movement.Move(Vector3.forward);
        yield return new WaitForFixedUpdate();
        yield return null;

        Assert.IsTrue(_playerGo.transform.position.z > startZ,
            "Z position should increase when moving forward");
    }

    [UnityTest]
    public IEnumerator Move_Backward_PositionDecreases()
    {
        float startZ = _playerGo.transform.position.z;
        _movement.Move(Vector3.back);
        yield return new WaitForFixedUpdate();
        yield return null;

        Assert.IsTrue(_playerGo.transform.position.z < startZ,
            "Z position should decrease when moving backward");
    }

    [UnityTest]
    public IEnumerator Move_Right_XPositionIncreases()
    {
        float startX = _playerGo.transform.position.x;
        _movement.Move(Vector3.right);
        yield return new WaitForFixedUpdate();
        yield return null;

        Assert.IsTrue(_playerGo.transform.position.x > startX);
    }

    [UnityTest]
    public IEnumerator Move_Zero_PositionUnchanged()
    {
        var startPos = _playerGo.transform.position;
        _movement.Move(Vector3.zero);
        yield return new WaitForFixedUpdate();
        yield return null;

        Assert.AreEqual(startPos.x, _playerGo.transform.position.x, Tolerance);
        Assert.AreEqual(startPos.z, _playerGo.transform.position.z, Tolerance);
    }

    // --- Speed ---

    [UnityTest]
    public IEnumerator Move_WithZeroSpeed_PositionUnchanged()
    {
        _movement.MoveSpeed = 0f;
        var startPos = _playerGo.transform.position;
        _movement.Move(Vector3.forward);
        yield return new WaitForFixedUpdate();
        yield return null;

        Assert.AreEqual(startPos.z, _playerGo.transform.position.z, Tolerance);
    }

    [UnityTest]
    public IEnumerator Move_HigherSpeed_GreaterDisplacement()
    {
        _movement.MoveSpeed = MoveSpeed;
        _movement.Move(Vector3.forward);
        yield return new WaitForFixedUpdate();
        yield return null;
        float distNormal = _playerGo.transform.position.z;

        // Reset
        Object.Destroy(_playerGo);
        _playerGo = new GameObject("FastPlayer");
        _movement = _playerGo.AddComponent<PlayerMovement>();
        _movement.MoveSpeed = MoveSpeed * 3f;
        _movement.Move(Vector3.forward);
        yield return new WaitForFixedUpdate();
        yield return null;
        float distFast = _playerGo.transform.position.z;

        Assert.IsTrue(distFast > distNormal, "Higher speed should produce greater displacement");
    }

    // --- Diagonal ---

    [UnityTest]
    public IEnumerator Move_Diagonal_BothAxesChange()
    {
        var startPos = _playerGo.transform.position;
        _movement.Move(new Vector3(1, 0, 1).normalized);
        yield return new WaitForFixedUpdate();
        yield return null;

        Assert.IsTrue(_playerGo.transform.position.x > startPos.x);
        Assert.IsTrue(_playerGo.transform.position.z > startPos.z);
    }

    // --- Grounded / Jump ---

    [UnityTest]
    public IEnumerator Jump_WhenGrounded_YPositionIncreases()
    {
        _playerGo.AddComponent<Rigidbody>();
        var startY = _playerGo.transform.position.y;
        _movement.Jump();
        yield return new WaitForSeconds(0.1f);

        Assert.IsTrue(_playerGo.transform.position.y > startY,
            "Y position should increase after jump");
    }

    [UnityTest]
    public IEnumerator Jump_WhenAirborne_DoesNotDoubleJump()
    {
        _playerGo.AddComponent<Rigidbody>();
        _movement.Jump();
        yield return null;

        float yAfterFirstJump = _playerGo.transform.position.y;
        _movement.Jump(); // should be rejected
        yield return null;

        Assert.AreEqual(yAfterFirstJump, _playerGo.transform.position.y, 0.5f,
            "Should not gain extra height from double jump");
    }

    // --- Disabled state ---

    [UnityTest]
    public IEnumerator Move_WhenDisabled_PositionUnchanged()
    {
        _movement.enabled = false;
        var startPos = _playerGo.transform.position;
        _movement.Move(Vector3.forward);
        yield return new WaitForFixedUpdate();
        yield return null;

        Assert.AreEqual(startPos.x, _playerGo.transform.position.x, Tolerance);
        Assert.AreEqual(startPos.z, _playerGo.transform.position.z, Tolerance);
    }

    // --- Facing direction ---

    [UnityTest]
    public IEnumerator Move_Forward_FacesForward()
    {
        _movement.Move(Vector3.forward);
        yield return new WaitForFixedUpdate();
        yield return null;

        float angle = Vector3.Angle(_playerGo.transform.forward, Vector3.forward);
        Assert.IsTrue(angle < 10f, "Player should face movement direction");
    }

    [UnityTest]
    public IEnumerator Move_Right_FacesRight()
    {
        _movement.Move(Vector3.right);
        yield return new WaitForFixedUpdate();
        yield return null;

        float angle = Vector3.Angle(_playerGo.transform.forward, Vector3.right);
        Assert.IsTrue(angle < 10f, "Player should face right after moving right");
    }
}
```

---

## Feature: Spawner System (Play Mode)

Coroutine-based spawning with timing and capacity. 10 test cases.

```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

[TestFixture]
public class SpawnerTests
{
    private GameObject _spawnerGo;
    private EnemySpawner _spawner;

    [SetUp]
    public void SetUp()
    {
        _spawnerGo = new GameObject("TestSpawner");
        _spawner = _spawnerGo.AddComponent<EnemySpawner>();
        _spawner.SpawnDelay = 0.1f;
        _spawner.MaxEnemies = 5;
        _spawner.EnemyPrefab = new GameObject("EnemyTemplate");
    }

    [TearDown]
    public void TearDown()
    {
        if (_spawnerGo != null) Object.Destroy(_spawnerGo);
        // Clean up spawned enemies
        foreach (var go in GameObject.FindObjectsByType<EnemyComponent>(FindObjectsSortMode.None))
        {
            Object.Destroy(go.gameObject);
        }
    }

    // --- Basic spawning ---

    [UnityTest]
    public IEnumerator StartSpawning_AfterDelay_CreatesOneEnemy()
    {
        _spawner.StartSpawning();
        yield return new WaitForSeconds(0.15f);

        Assert.AreEqual(1, _spawner.SpawnCount);
    }

    [UnityTest]
    public IEnumerator StartSpawning_BeforeDelay_NoEnemiesSpawned()
    {
        _spawner.StartSpawning();
        yield return new WaitForSeconds(0.05f);

        Assert.AreEqual(0, _spawner.SpawnCount);
    }

    [UnityTest]
    public IEnumerator StartSpawning_MultipleDelays_SpawnsMultiple()
    {
        _spawner.StartSpawning();
        yield return new WaitForSeconds(0.35f);

        Assert.IsTrue(_spawner.SpawnCount >= 3, $"Expected >= 3 spawns, got {_spawner.SpawnCount}");
    }

    // --- Capacity ---

    [UnityTest]
    public IEnumerator StartSpawning_AtMaxCapacity_StopsSpawning()
    {
        _spawner.MaxEnemies = 2;
        _spawner.StartSpawning();
        yield return new WaitForSeconds(0.5f);

        Assert.AreEqual(2, _spawner.SpawnCount, "Should stop at max capacity");
    }

    [UnityTest]
    public IEnumerator StartSpawning_ZeroMax_NeverSpawns()
    {
        _spawner.MaxEnemies = 0;
        _spawner.StartSpawning();
        yield return new WaitForSeconds(0.3f);

        Assert.AreEqual(0, _spawner.SpawnCount);
    }

    // --- Stop ---

    [UnityTest]
    public IEnumerator StopSpawning_PreventsNewSpawns()
    {
        _spawner.StartSpawning();
        yield return new WaitForSeconds(0.15f);
        int countAtStop = _spawner.SpawnCount;

        _spawner.StopSpawning();
        yield return new WaitForSeconds(0.3f);

        Assert.AreEqual(countAtStop, _spawner.SpawnCount,
            "No new spawns should occur after stop");
    }

    [UnityTest]
    public IEnumerator StopSpawning_WhenNotStarted_NoError()
    {
        _spawner.StopSpawning();
        yield return null;
        Assert.Pass("StopSpawning should be safe to call when not started");
    }

    // --- Restart ---

    [UnityTest]
    public IEnumerator StartSpawning_AfterStop_ResumesSpawning()
    {
        _spawner.StartSpawning();
        yield return new WaitForSeconds(0.15f);
        _spawner.StopSpawning();
        int countAtStop = _spawner.SpawnCount;

        _spawner.StartSpawning();
        yield return new WaitForSeconds(0.15f);

        Assert.IsTrue(_spawner.SpawnCount > countAtStop, "Should resume spawning after restart");
    }

    // --- Spawn position ---

    [UnityTest]
    public IEnumerator Spawn_Enemy_SpawnsAtSpawnerPosition()
    {
        _spawnerGo.transform.position = new Vector3(10, 0, 10);
        _spawner.StartSpawning();
        yield return new WaitForSeconds(0.15f);

        var enemies = GameObject.FindObjectsByType<EnemyComponent>(FindObjectsSortMode.None);
        Assert.IsTrue(enemies.Length > 0);
        Assert.AreEqual(10f, enemies[0].transform.position.x, 0.1f,
            "Enemy should spawn at spawner X position");
    }

    // --- IsSpawning state ---

    [UnityTest]
    public IEnumerator IsSpawning_AfterStart_ReturnsTrue()
    {
        _spawner.StartSpawning();
        yield return null;
        Assert.IsTrue(_spawner.IsSpawning);
    }
}
```

---

## Patterns: Mocking Dependencies

Reusable patterns for creating test doubles.

```csharp
// --- Interface-based mock with tracking ---

public class MockAudioService : IAudioService
{
    public int PlayCount { get; private set; }
    public string LastClipPlayed { get; private set; }
    public float LastVolume { get; private set; }
    public bool ShouldThrow { get; set; }

    public void PlaySFX(string clipId, float volume = 1f)
    {
        if (ShouldThrow) throw new InvalidOperationException("Audio system unavailable");
        PlayCount++;
        LastClipPlayed = clipId;
        LastVolume = volume;
    }

    public void StopAll() { PlayCount = 0; }
}

// --- Configurable mock for return values ---

public class MockDatabaseService : IDatabaseService
{
    public Dictionary<string, string> StoredData { get; } = new();
    public bool ShouldReturnNull { get; set; }

    public string Get(string key)
    {
        if (ShouldReturnNull) return null;
        return StoredData.TryGetValue(key, out var val) ? val : null;
    }

    public void Set(string key, string value) => StoredData[key] = value;
}

// --- MonoBehaviour test double ---

[TestFixture]
public class PlayerControllerTests
{
    private GameObject _playerGo;
    private PlayerController _controller;
    private MockAudioService _mockAudio;

    [SetUp]
    public void SetUp()
    {
        _playerGo = new GameObject("TestPlayer");
        _controller = _playerGo.AddComponent<PlayerController>();
        _mockAudio = new MockAudioService();
        _controller.Initialize(_mockAudio);
    }

    [TearDown]
    public void TearDown()
    {
        Object.Destroy(_playerGo);
    }

    [Test]
    public void TakeDamage_PlaysDamageSound()
    {
        _controller.TakeDamage(10);
        Assert.AreEqual("sfx_damage", _mockAudio.LastClipPlayed);
    }

    [Test]
    public void TakeDamage_AudioServiceUnavailable_DoesNotThrow()
    {
        _mockAudio.ShouldThrow = true;
        Assert.DoesNotThrow(() => _controller.TakeDamage(10),
            "Should handle audio failure gracefully");
    }
}
```

---

## Patterns: Parameterized Tests

Data-driven testing with `[TestCase]` and `[TestCaseSource]`.

```csharp
[TestFixture]
public class DamageCalculatorTests
{
    // --- TestCase: inline values ---

    [TestCase(100, 30, 70)]
    [TestCase(100, 0, 100)]
    [TestCase(100, 100, 0)]
    [TestCase(100, 150, 0)]   // overkill clamps
    [TestCase(0, 10, 0)]      // already dead
    [TestCase(1, 1, 0)]       // exact kill
    public void CalculateFinalHealth_VariousDamage_ReturnsExpected(
        int maxHp, int damage, int expected)
    {
        var result = DamageCalculator.CalculateFinalHealth(maxHp, damage);
        Assert.AreEqual(expected, result);
    }

    // --- TestCase: float with tolerance ---

    [TestCase(100f, 0.5f, 50f, 0.01f)]
    [TestCase(100f, 1.0f, 0f, 0.01f)]
    [TestCase(100f, 0.0f, 100f, 0.01f)]
    [TestCase(200f, 0.25f, 150f, 0.01f)]
    public void PercentDamage_VariousPercents_WithinTolerance(
        float hp, float percent, float expected, float tolerance)
    {
        var result = DamageCalculator.PercentDamage(hp, percent);
        Assert.AreEqual(expected, result, tolerance);
    }

    // --- TestCaseSource: complex data ---

    private static IEnumerable<TestCaseData> ElementalDamageData()
    {
        yield return new TestCaseData(Element.Fire, Element.Ice, 2.0f)
            .SetName("Fire vs Ice = 2x");
        yield return new TestCaseData(Element.Fire, Element.Fire, 0.5f)
            .SetName("Fire vs Fire = 0.5x");
        yield return new TestCaseData(Element.Fire, Element.Earth, 1.0f)
            .SetName("Fire vs Earth = 1x");
        yield return new TestCaseData(Element.Ice, Element.Fire, 0.5f)
            .SetName("Ice vs Fire = 0.5x");
    }

    [TestCaseSource(nameof(ElementalDamageData))]
    public void GetElementalMultiplier_VariousMatchups_ReturnsCorrect(
        Element attacker, Element defender, float expectedMultiplier)
    {
        var result = DamageCalculator.GetElementalMultiplier(attacker, defender);
        Assert.AreEqual(expectedMultiplier, result, 0.001f);
    }
}
```

---

## Patterns: State Machine Testing

Testing state transitions — valid, invalid, re-entry.

```csharp
[TestFixture]
public class EnemyAIStateTests
{
    private EnemyAI _ai;

    [SetUp]
    public void SetUp()
    {
        _ai = new EnemyAI();
    }

    // --- Initial state ---

    [Test]
    public void EnemyAI_OnCreate_StartsInIdleState()
    {
        Assert.AreEqual(AIState.Idle, _ai.CurrentState);
    }

    // --- Valid transitions ---

    [Test]
    public void Idle_DetectsPlayer_TransitionsToChase()
    {
        _ai.OnPlayerDetected();
        Assert.AreEqual(AIState.Chase, _ai.CurrentState);
    }

    [Test]
    public void Chase_InAttackRange_TransitionsToAttack()
    {
        _ai.OnPlayerDetected();
        _ai.OnEnterAttackRange();
        Assert.AreEqual(AIState.Attack, _ai.CurrentState);
    }

    [Test]
    public void Attack_PlayerLeavesRange_TransitionsToChase()
    {
        _ai.OnPlayerDetected();
        _ai.OnEnterAttackRange();
        _ai.OnLeaveAttackRange();
        Assert.AreEqual(AIState.Chase, _ai.CurrentState);
    }

    [Test]
    public void Chase_LosesPlayer_TransitionsToIdle()
    {
        _ai.OnPlayerDetected();
        _ai.OnPlayerLost();
        Assert.AreEqual(AIState.Idle, _ai.CurrentState);
    }

    [Test]
    public void AnyState_TakesLethalDamage_TransitionsToDead()
    {
        _ai.OnPlayerDetected();
        _ai.OnLethalDamage();
        Assert.AreEqual(AIState.Dead, _ai.CurrentState);
    }

    // --- Invalid transitions ---

    [Test]
    public void Idle_EnterAttackRange_StaysIdle()
    {
        _ai.OnEnterAttackRange(); // invalid without chase first
        Assert.AreEqual(AIState.Idle, _ai.CurrentState,
            "Should not enter attack from idle");
    }

    [Test]
    public void Dead_DetectsPlayer_StaysDead()
    {
        _ai.OnLethalDamage();
        _ai.OnPlayerDetected();
        Assert.AreEqual(AIState.Dead, _ai.CurrentState,
            "Dead state should be terminal");
    }

    [Test]
    public void Dead_AnyInput_StaysDead()
    {
        _ai.OnLethalDamage();
        _ai.OnEnterAttackRange();
        _ai.OnLeaveAttackRange();
        _ai.OnPlayerLost();
        Assert.AreEqual(AIState.Dead, _ai.CurrentState);
    }

    // --- Re-entry ---

    [Test]
    public void Idle_DetectLoseDetect_ReturnsToChase()
    {
        _ai.OnPlayerDetected();
        _ai.OnPlayerLost();
        Assert.AreEqual(AIState.Idle, _ai.CurrentState);

        _ai.OnPlayerDetected();
        Assert.AreEqual(AIState.Chase, _ai.CurrentState, "Should re-enter chase");
    }

    // --- State change event ---

    [Test]
    public void StateChange_FiresOnStateChanged()
    {
        AIState? receivedState = null;
        _ai.OnStateChanged += state => receivedState = state;

        _ai.OnPlayerDetected();

        Assert.AreEqual(AIState.Chase, receivedState);
    }
}
```

---

## Test Directory Structure

### Recommended Structure (Editor/ folder for EditMode)

```
Assets/Scripts/Test/
├── Editor/                              ← RECOMMENDED for EditMode tests (no .asmdef needed)
│   ├── FeatureA/
│   │   ├── InventoryTests.cs
│   │   ├── InventoryEventTests.cs
│   │   └── InventoryIntegrationTests.cs
│   ├── FeatureB/
│   │   ├── DamageCalculatorTests.cs
│   │   └── EnemyAIStateTests.cs
│   └── Helpers/
│       └── TestDoubles.cs
└── PlayMode/                            ← Requires .asmdef
    ├── PlayModeTests.asmdef
    ├── PlayerMovementTests.cs
    ├── SpawnerTests.cs
    └── PlayerControllerTests.cs
```

Tests in `Editor/` compile into `Assembly-CSharp-Editor` which **automatically** includes NUnit, UnityEngine.TestRunner, and UnityEditor.TestRunner references. No `.asmdef` configuration needed.

### Legacy Structure (EditMode/ with .asmdef)

```
Assets/Scripts/Test/
├── EditMode/
│   ├── EditModeTests.asmdef             ← Must be correctly configured
│   ├── InventoryTests.cs
│   └── ...
└── PlayMode/
    ├── PlayModeTests.asmdef
    └── ...
```

This approach works but requires a correctly configured `.asmdef`. See [Assembly Definition Examples](#assembly-definition-examples) below.

> **⚠️ WARNING**: If the `.asmdef` is misconfigured (e.g., `Assembly-CSharp.dll` in `precompiledReferences`), tests compile without errors but the Test Runner shows "No tests to show". The `Editor/` folder approach eliminates this risk entirely.

---

## Assembly Definition Examples

Every test folder requires an `.asmdef` file to compile correctly. Without it, test scripts compile into `Assembly-CSharp` which lacks NUnit references, causing `CS0246` errors.

### EditMode `.asmdef` (`Assets/Scripts/Test/EditMode/EditModeTests.asmdef`)

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

**Key fields explained:**

| Field | Value | Purpose |
|:------|:------|:--------|
| `references` | `UnityEngine.TestRunner`, `UnityEditor.TestRunner` | Access to `[UnityTest]`, `UnityEngine.TestTools` |
| `includePlatforms` | `["Editor"]` | EditMode tests only run in the Unity Editor |
| `overrideReferences` | `true` | Enables explicit `precompiledReferences` |
| `precompiledReferences` | `["nunit.framework.dll"]` | NUnit access — `[Test]`, `Assert`, `[TestFixture]` |
| `defineConstraints` | `["UNITY_INCLUDE_TESTS"]` | Only compiled when Test Framework is active |
| `autoReferenced` | `false` | Prevents game code from accidentally depending on tests |

### PlayMode `.asmdef` (`Assets/Scripts/Test/PlayMode/PlayModeTests.asmdef`)

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

**Difference from EditMode**: `includePlatforms` is empty `[]` so PlayMode tests can also run on build targets (device testing).

### Referencing Game Code

If you need test classes to access game code:

- **Game code has NO `.asmdef`** (default `Assembly-CSharp`): Tests can access it implicitly — no changes needed.
- **Game code has its OWN `.asmdef`** (e.g., `GameCore`): Add `"GameCore"` to the test `.asmdef`'s `references` array.
- **NEVER** add `"Assembly-CSharp.dll"` to `precompiledReferences` — it is not a precompiled DLL.

---

## Invalid `.asmdef` Configuration — What NOT to Do

The following `.asmdef` configuration **will cause "No tests to show"** in the Test Runner even though tests compile without errors:

### ❌ BROKEN: `Assembly-CSharp.dll` in precompiledReferences

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
        "Assembly-CSharp.dll",
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

**Why this fails**: `Assembly-CSharp` is Unity's default compilation assembly — it is **not** a precompiled DLL that exists in the `Library/ScriptAssemblies/` as a redistributable reference. Adding it to `precompiledReferences` corrupts the assembly resolution metadata, making the Test Runner unable to recognize the assembly as a test assembly.

**Symptoms**:
- ✅ Tests compile successfully (no CS0246 errors)
- ❌ Test Runner window → EditMode tab → "No tests to show"
- ❌ No error messages anywhere — completely silent failure

**Fix options**:
1. **Best**: Delete the `.asmdef` and move tests to an `Editor/` folder
2. **Alternative**: Remove `"Assembly-CSharp.dll"` from `precompiledReferences` (keep only `"nunit.framework.dll"`)

---

## Before Creating EditMode Tests — Pre-Creation Checklist

Run through this checklist **before** writing any new EditMode test:

### Folder Setup

- [ ] **Choose folder location**: `Assets/Scripts/Test/Editor/` (recommended) or custom folder with valid `.asmdef`
- [ ] **If using `Editor/` folder**: No `.asmdef` needed — skip to "Write Tests"
- [ ] **If using custom folder**: Create `.asmdef` following the [EditMode template](#editmode-asmdef-assetsscriptstesteditmodeedimodeteststsasmdef)

### `.asmdef` Validation (only if NOT using `Editor/` folder)

- [ ] `overrideReferences` is `true`
- [ ] `precompiledReferences` contains ONLY `"nunit.framework.dll"` — NO `Assembly-CSharp.dll`
- [ ] `references` contains `"UnityEngine.TestRunner"` AND `"UnityEditor.TestRunner"`
- [ ] `defineConstraints` contains `"UNITY_INCLUDE_TESTS"`
- [ ] `includePlatforms` is `["Editor"]`
- [ ] `autoReferenced` is `false`

### Write Tests

- [ ] Test class has `[TestFixture]` attribute
- [ ] Test methods have `[Test]` attribute
- [ ] `using NUnit.Framework;` is present
- [ ] Test naming follows `[Subject]_[Scenario]_[ExpectedResult]`

### Verify Discovery

- [ ] Open `Window > General > Test Runner > EditMode` tab
- [ ] Confirm tests appear in the test tree
- [ ] Run one test to verify execution
- [ ] If "No tests to show" → check `.asmdef` for `Assembly-CSharp.dll` in `precompiledReferences`, or move tests to `Editor/` folder


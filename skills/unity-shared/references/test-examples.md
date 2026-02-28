# Test Examples: Edit & Play Mode

## Edit Mode: Inventory Tests

```csharp
using NUnit.Framework;

[TestFixture]
public class InventoryTests
{
    private Inventory _inventory;

    [SetUp]
    public void SetUp() => _inventory = new Inventory(maxSlots: 10);

    [Test] 
    public void Add_ValidItem_Increments() => Assert.AreEqual(1, _inventory.Add(new Item("sword")) ? 1 : 0);

    [Test] 
    public void Add_WhenFull_ReturnsFalse()
    {
        var inv = new Inventory(maxSlots: 1);
        inv.Add(new Item("sword"));
        Assert.IsFalse(inv.Add(new Item("shield")));
    }

    [Test]
    public void Remove_ExistingItem_Succeeds()
    {
        _inventory.Add(new Item("sword", id: "item_001"));
        Assert.IsTrue(_inventory.Remove("item_001"));
    }

    [Test] 
    public void GetById_ReturnsItem()
    {
        _inventory.Add(new Item("sword", id: "item_001"));
        var result = _inventory.GetById("item_001");
        Assert.IsNotNull(result);
    }
}
```

## Play Mode: Movement Tests

```csharp
using System.Collections;
using UnityEngine.TestTools;
using NUnit.Framework;
using UnityEngine;

[TestFixture]
public class PlayerMovementTests
{
    private GameObject _playerGo;
    private PlayerMovement _movement;

    [SetUp]
    public void SetUp()
    {
        _playerGo = new GameObject("TestPlayer");
        _movement = _playerGo.AddComponent<PlayerMovement>();
    }

    [TearDown]
    public void TearDown() => Object.Destroy(_playerGo);

    [UnityTest]
    public IEnumerator Move_Forward_PositionIncreases()
    {
        float startZ = _playerGo.transform.position.z;
        _movement.Move(Vector3.forward);
        yield return new WaitForFixedUpdate();
        Assert.IsTrue(_playerGo.transform.position.z > startZ);
    }

    [UnityTest]
    public IEnumerator Move_Zero_PositionUnchanged()
    {
        var startPos = _playerGo.transform.position;
        _movement.Move(Vector3.zero);
        yield return new WaitForFixedUpdate();
        Assert.AreEqual(startPos.z, _playerGo.transform.position.z, 0.01f);
    }
}
```

## Pattern: Mocking Dependencies

```csharp
// Interface-based mock with tracking
public class MockAudioService : IAudioService
{
    public int PlayCount { get; private set; }
    public string LastClipPlayed { get; private set; }
    public bool ShouldThrow { get; set; }

    public void PlaySFX(string clipId, float volume = 1f)
    {
        if (ShouldThrow) throw new InvalidOperationException("Audio unavailable");
        PlayCount++;
        LastClipPlayed = clipId;
    }
    public void StopAll() { PlayCount = 0; }
}

// Usage with MonoBehaviour
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

    [TearDown] public void TearDown() => Object.Destroy(_playerGo);

    [Test]
    public void TakeDamage_PlaysDamageSound()
    {
        _controller.TakeDamage(10);
        Assert.AreEqual("sfx_damage", _mockAudio.LastClipPlayed);
    }

    [Test]
    public void TakeDamage_AudioUnavailable_DoesNotThrow()
    {
        _mockAudio.ShouldThrow = true;
        Assert.DoesNotThrow(() => _controller.TakeDamage(10));
    }
}
```

## Pattern: Parameterized Tests

```csharp
[TestFixture]
public class DamageCalculatorTests
{
    // TestCase: inline values
    [TestCase(100, 30, 70)]
    [TestCase(100, 0, 100)]
    [TestCase(100, 100, 0)]
    [TestCase(100, 150, 0)]   // overkill clamps
    [TestCase(0, 10, 0)]      // already dead
    public void CalculateFinalHealth_ReturnsExpected(int maxHp, int damage, int expected)
    {
        Assert.AreEqual(expected, DamageCalculator.CalculateFinalHealth(maxHp, damage));
    }

    // TestCaseSource: complex data
    private static IEnumerable<TestCaseData> ElementalDamageData()
    {
        yield return new TestCaseData(Element.Fire, Element.Ice, 2.0f).SetName("Fire vs Ice = 2x");
        yield return new TestCaseData(Element.Fire, Element.Fire, 0.5f).SetName("Fire vs Fire = 0.5x");
        yield return new TestCaseData(Element.Fire, Element.Earth, 1.0f).SetName("Fire vs Earth = 1x");
    }

    [TestCaseSource(nameof(ElementalDamageData))]
    public void GetElementalMultiplier_ReturnsCorrect(Element atk, Element def, float expected)
    {
        Assert.AreEqual(expected, DamageCalculator.GetElementalMultiplier(atk, def), 0.001f);
    }
}
```

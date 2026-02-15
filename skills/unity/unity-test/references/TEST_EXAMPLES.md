# Unity Test Examples

## Edit Mode: Core Logic (Inventory)

```csharp
using NUnit.Framework;
using System;

[TestFixture]
public class InventoryTests
{
    private const int DefaultMaxSlots = 10;
    private Inventory _inventory;

    [SetUp]
    public void SetUp() => _inventory = new Inventory(DefaultMaxSlots);

    [Test] public void Constructor_ValidSlots_CreatesEmptyInventory() => Assert.AreEqual(0, _inventory.Count);
    [Test] public void Constructor_ZeroSlots_ThrowsArgumentException() => Assert.Throws<ArgumentException>(() => new Inventory(0));

    [Test]
    public void Add_ValidItem_ReturnsTrueAndIncrements()
    {
        Assert.IsTrue(_inventory.Add(new Item("sword")));
        Assert.AreEqual(1, _inventory.Count);
    }

    [Test] public void Add_NullItem_Throws() => Assert.Throws<ArgumentNullException>(() => _inventory.Add(null));

    [Test]
    public void Add_WhenFull_ReturnsFalse()
    {
        var inv = new Inventory(maxSlots: 1);
        inv.Add(new Item("sword"));
        Assert.IsFalse(inv.Add(new Item("shield")));
        Assert.AreEqual(1, inv.Count);
    }

    [Test]
    public void Remove_ExistingItem_ReturnsTrueAndDecrements()
    {
        _inventory.Add(new Item("sword", id: "item_001"));
        Assert.IsTrue(_inventory.Remove("item_001"));
        Assert.AreEqual(0, _inventory.Count);
    }

    [Test] public void Remove_NonexistentId_ReturnsFalse() => Assert.IsFalse(_inventory.Remove("nonexistent"));
    [Test] public void Remove_NullId_Throws() => Assert.Throws<ArgumentNullException>(() => _inventory.Remove(null));

    [Test]
    public void GetById_ExistingItem_ReturnsItem()
    {
        _inventory.Add(new Item("sword", id: "item_001"));
        var result = _inventory.GetById("item_001");
        Assert.IsNotNull(result);
        Assert.AreEqual("sword", result.Name);
    }

    [Test] public void GetById_Nonexistent_ReturnsNull() => Assert.IsNull(_inventory.GetById("nonexistent"));
}
```

## Play Mode: MonoBehaviour (Player Movement)

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
    public void TearDown() { if (_playerGo != null) Object.Destroy(_playerGo); }

    [UnityTest]
    public IEnumerator Move_Forward_PositionIncreases()
    {
        float startZ = _playerGo.transform.position.z;
        _movement.Move(Vector3.forward);
        yield return new WaitForFixedUpdate();
        yield return null;
        Assert.IsTrue(_playerGo.transform.position.z > startZ);
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

    [UnityTest]
    public IEnumerator Jump_WhenGrounded_YPositionIncreases()
    {
        _playerGo.AddComponent<Rigidbody>();
        var startY = _playerGo.transform.position.y;
        _movement.Jump();
        yield return new WaitForSeconds(0.1f);
        Assert.IsTrue(_playerGo.transform.position.y > startY);
    }

    [UnityTest]
    public IEnumerator Move_WhenDisabled_PositionUnchanged()
    {
        _movement.enabled = false;
        var startPos = _playerGo.transform.position;
        _movement.Move(Vector3.forward);
        yield return new WaitForFixedUpdate();
        yield return null;
        Assert.AreEqual(startPos.z, _playerGo.transform.position.z, Tolerance);
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

## Directory Structure

```
Assets/Scripts/Test/
├── Editor/                    ← EditMode (no .asmdef needed)
│   ├── FeatureA/
│   │   └── InventoryTests.cs
│   └── Helpers/
│       └── TestDoubles.cs
└── PlayMode/                  ← Requires .asmdef
    ├── PlayModeTests.asmdef
    └── PlayerMovementTests.cs
```

`Editor/` auto-includes NUnit + TestRunner references. No `.asmdef` config needed.

## Assembly Definitions

### EditMode `.asmdef`

```json
{
    "name": "EditModeTests",
    "references": ["UnityEngine.TestRunner", "UnityEditor.TestRunner"],
    "includePlatforms": ["Editor"],
    "overrideReferences": true,
    "precompiledReferences": ["nunit.framework.dll"],
    "autoReferenced": false,
    "defineConstraints": ["UNITY_INCLUDE_TESTS"]
}
```

### PlayMode `.asmdef`

Same but `"includePlatforms": []` (empty = all platforms for device testing).

### Referencing Game Code

- **No game `.asmdef`** (default `Assembly-CSharp`): Tests access implicitly
- **Game has `.asmdef`** (e.g., `GameCore`): Add `"GameCore"` to test `references`
- **NEVER** add `"Assembly-CSharp.dll"` to `precompiledReferences`

## ❌ Common `.asmdef` Pitfall

Adding `"Assembly-CSharp.dll"` to `precompiledReferences` causes silent failure:
- Tests compile successfully
- Test Runner shows "No tests to show"

**Fix**: Remove it (keep only `"nunit.framework.dll"`) or use `Editor/` folder instead.

## Pre-Creation Checklist

1. Use `Editor/` folder (recommended, no `.asmdef`) or create valid `.asmdef`
2. `.asmdef` must have: `overrideReferences: true`, `precompiledReferences: ["nunit.framework.dll"]` only, `defineConstraints: ["UNITY_INCLUDE_TESTS"]`
3. Test class: `[TestFixture]`, methods: `[Test]`/`[UnityTest]`, naming: `Subject_Scenario_Expected`
4. Verify in `Window > General > Test Runner`


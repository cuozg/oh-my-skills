# Unity Test Examples - Core Logic & Play Mode

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

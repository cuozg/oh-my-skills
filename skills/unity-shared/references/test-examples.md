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

# Test Patterns — Skill Extensions

> **Canonical reference**: `unity-standards/references/test/edit-mode-patterns.md`
> Load via: `read_skill_file("unity-standards", "references/test/edit-mode-patterns.md")`

Standards covers AAA pattern, assertions, SetUp/TearDown, ScriptableObject testing,
exception testing, and manual mocking. Below are extensions unique to this skill.

## Data-Focused Test Organization

### Category 1: Valid Data Tests

```csharp
// Normal expected input
[Test]
public void AddItem_WithValidItem_IncreasesCount()
{
    var inventory = new Inventory(maxSlots: 10);
    var item = new Item("Sword", quantity: 1);

    inventory.Add(item);

    Assert.AreEqual(1, inventory.Count);
}

// Boundary-valid input (exactly at limit)
[Test]
public void AddItem_AtMaxCapacity_Succeeds()
{
    var inventory = new Inventory(maxSlots: 1);

    inventory.Add(new Item("Sword", quantity: 1));

    Assert.AreEqual(1, inventory.Count);
    Assert.IsTrue(inventory.IsFull);
}

// Parameterized valid data
[TestCase(1, 100)]
[TestCase(50, 50)]
[TestCase(100, 0)]
public void SetHealth_ValidValues_ClampsCorrectly(int value, int expected)
{
    _unit.SetHealth(value);
    Assert.AreEqual(expected, _unit.Health);
}
```

### Category 2: Invalid / Malformed Data Tests (CRITICAL)

```csharp
// Null input — MUST test for every object parameter
[Test]
public void AddItem_WithNullItem_ThrowsArgumentNull()
{
    var inventory = new Inventory(maxSlots: 10);

    Assert.Throws<System.ArgumentNullException>(() => inventory.Add(null));
}

// Empty data — strings, collections, arrays
[Test]
public void Search_WithEmptyString_ReturnsEmptyResults()
{
    var results = _catalog.Search("");

    Assert.IsNotNull(results);
    Assert.AreEqual(0, results.Count);
}

[Test]
public void Search_WithWhitespaceOnly_ReturnsEmptyResults()
{
    var results = _catalog.Search("   ");

    Assert.IsNotNull(results);
    Assert.AreEqual(0, results.Count);
}

[Test]
public void ProcessItems_WithEmptyList_DoesNotThrow()
{
    Assert.DoesNotThrow(() => _processor.Process(new List<Item>()));
}

// Out-of-range values
[TestCase(-1)]
[TestCase(int.MinValue)]
public void SetHealth_NegativeValue_ClampsToZero(int invalidHealth)
{
    _unit.SetHealth(invalidHealth);

    Assert.AreEqual(0, _unit.Health);
}

[TestCase(float.NaN)]
[TestCase(float.PositiveInfinity)]
[TestCase(float.NegativeInfinity)]
public void SetSpeed_NonFiniteValue_RejectsInput(float invalidSpeed)
{
    float originalSpeed = _unit.Speed;

    _unit.SetSpeed(invalidSpeed);

    Assert.AreEqual(originalSpeed, _unit.Speed); // unchanged
}

// Malformed inputs — wrong type, special chars, invalid enum
[Test]
public void ParseDamageType_WithInvalidEnumCast_ThrowsArgument()
{
    Assert.Throws<System.ArgumentException>(
        () => _parser.ParseDamageType((DamageType)999));
}

[Test]
public void LoadResource_WithMalformedPath_ReturnsNull()
{
    var result = _loader.Load("invalid/path\0with/nullchar");

    Assert.IsNull(result);
}

// Invalid state — method called at wrong time
[Test]
public void Attack_WhenDead_DoesNotDealDamage()
{
    _unit.SetHealth(0);

    int damageDealt = _unit.Attack(_target);

    Assert.AreEqual(0, damageDealt);
    Assert.AreEqual(_target.MaxHealth, _target.Health); // target unaffected
}

// Destroyed Unity object
[Test]
public void RemoveComponent_AfterDestroy_DoesNotThrow()
{
    var go = new GameObject();
    Object.DestroyImmediate(go);

    Assert.DoesNotThrow(() => _system.Unregister(go));
}

// Uninitialized SerializeField / null component reference
[Test]
public void Initialize_WithNullAudioSource_ThrowsInvalidOperation()
{
    _controller.AudioSource = null;

    Assert.Throws<System.InvalidOperationException>(
        () => _controller.Initialize());
}

// Duplicate data
[Test]
public void Register_SameItemTwice_IgnoresDuplicate()
{
    var item = new Item("Shield", quantity: 1);
    _registry.Register(item);
    _registry.Register(item); // duplicate

    Assert.AreEqual(1, _registry.Count);
}
```

### Negative Assertions — What Should NOT Happen

```csharp
// Verify side effects did NOT occur
[Test]
public void SaveGame_WithInvalidSlot_DoesNotOverwriteExisting()
{
    var original = _saveManager.Load(slot: 0);

    _saveManager.Save(slot: -1, data: _newData);

    var afterAttempt = _saveManager.Load(slot: 0);
    Assert.AreEqual(original.Timestamp, afterAttempt.Timestamp); // unchanged
}

// Verify event was NOT fired
[Test]
public void TakeDamage_WhenShielded_DoesNotFireDeathEvent()
{
    bool deathFired = false;
    _unit.OnDeath += () => deathFired = true;
    _unit.EnableShield();

    _unit.TakeDamage(9999);

    Assert.IsFalse(deathFired);
    Assert.IsTrue(_unit.IsAlive);
}
```

## Mocking with NSubstitute

```csharp
// Create substitute
var mockRepo = Substitute.For<IRepository>();

// Set return value
mockRepo.GetById(1).Returns(new Entity { Id = 1 });

// Verify call was made
mockRepo.Received(1).Save(Arg.Any<Entity>());

// Verify call was NOT made (negative assertion)
mockRepo.DidNotReceive().Delete(Arg.Any<int>());
```

## Test Case Categories Checklist

For each public method, ensure coverage of:

**Valid Data (Category 1):**
- [ ] Happy path — normal expected inputs
- [ ] Boundary-valid — min/max values that should be accepted
- [ ] Typical combinations — real-world data scenarios

**Invalid Data (Category 2) — MUST NOT SKIP:**
- [ ] Null — every object/reference parameter, every unassigned `[SerializeField]`
- [ ] Empty — empty strings, whitespace-only strings, empty collections, zero-length arrays
- [ ] Out-of-range — negative, overflow, underflow, `int.MaxValue`, `float.NaN`, `float.PositiveInfinity`
- [ ] Malformed — wrong enum cast, strings with `\0`/`\n`, invalid paths, non-numeric where number expected
- [ ] Invalid state — wrong call order, after disposal, before init, on disabled/inactive components
- [ ] Duplicates — same item twice, duplicate keys, re-registering listeners
- [ ] Destroyed objects — operations on destroyed GameObjects/components, null from `GetComponent<T>()`

**Negative Assertions:**
- [ ] Side effects that should NOT occur
- [ ] Events that should NOT fire
- [ ] State that should NOT change

# Test Naming Conventions

## Method Naming

Pattern: `MethodName_Scenario_ExpectedResult`

```csharp
[Test] public void TakeDamage_ZeroHealth_Dies() { }
[Test] public void TakeDamage_NegativeValue_Throws() { }
[Test] public void Heal_AboveMax_ClampsToMax() { }
[Test] public void GetItem_InvalidIndex_ReturnsNull() { }
[Test] public void Save_EmptyInventory_WritesEmptyArray() { }
```

## Class Naming

Pattern: `{ClassName}Tests`

```csharp
public class HealthSystemTests { }
public class InventoryManagerTests { }
public class WeaponConfigTests { }
public class PlayerControllerPlayTests { } // play mode suffix
```

## File Location — Mirror Source

```
Assets/
├── Scripts/
│   ├── Player/
│   │   ├── HealthSystem.cs
│   │   └── PlayerController.cs
│   └── Inventory/
│       └── InventoryManager.cs
└── Tests/
    ├── EditMode/
    │   ├── Player/
    │   │   └── HealthSystemTests.cs
    │   └── Inventory/
    │       └── InventoryManagerTests.cs
    └── PlayMode/
        └── Player/
            └── PlayerControllerPlayTests.cs
```

## Assembly Definitions

| Assembly | Name Pattern |
|----------|-------------|
| Edit Mode tests | `{Project}.Tests.EditMode` |
| Play Mode tests | `{Project}.Tests.PlayMode` |
| Source reference | Add source asmdef to test asmdef references |

```json
{
    "name": "MyGame.Tests.EditMode",
    "references": ["MyGame.Runtime"],
    "optionalUnityReferences": ["TestAssemblies"],
    "includePlatforms": ["Editor"]
}
```

## Category Attribute

Group tests by feature or concern:

```csharp
[Category("Combat")]
public class DamageCalculatorTests { }

[Category("Persistence")]
public class SaveSystemTests { }

[Category("Integration")]
public class SceneLoadTests { }
```

Run filtered: `Unity Test Runner → Category filter`

## Quick Reference

| Element | Convention | Example |
|---------|-----------|---------|
| Test method | `Method_Scenario_Expected` | `Jump_Grounded_AppliesForce` |
| Test class | `{Class}Tests` | `PlayerTests` |
| Play mode class | `{Class}PlayTests` | `PlayerPlayTests` |
| Test file | Same as class name | `PlayerTests.cs` |
| Edit mode folder | `Tests/EditMode/` | mirrors source tree |
| Play mode folder | `Tests/PlayMode/` | mirrors source tree |
| Assembly | `{Proj}.Tests.{Mode}` | `MyGame.Tests.EditMode` |

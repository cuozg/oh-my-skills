# C# Quality & Code Hygiene — Part 2: Naming & Design

Naming conventions, sealed classes, readonly fields, guard clauses.

## Naming Conventions

```csharp
// ✅ GOOD: Follow standard C# naming
public class PlayerController { }              // PascalCase for types
public interface IPlayerService { }            // I-prefix for interfaces
private readonly int _maxHealth;               // _camelCase for private fields
public int MaxHealth { get; }                  // PascalCase for properties
public void TakeDamage(int amount) { }         // PascalCase for methods
private const int MaxRetries = 3;              // PascalCase for constants
public enum PlayerState { Idle, Running }      // PascalCase for enum values

// ❌ BAD: Inconsistent naming
public class player_controller { }             // Wrong casing
private int MaxHealth;                         // Looks like property
public void take_damage(int Amount) { }        // Snake case
```

## Sealed Classes

```csharp
// ✅ GOOD: Seal classes that aren't designed for inheritance
public sealed class PlayerService : IPlayerService { }
internal sealed class CacheManager { }

// ❌ BAD: Unsealed class with no virtual members
public class PlayerService : IPlayerService { } // Should be sealed
```

## Readonly Fields

```csharp
// ✅ GOOD: Mark fields readonly when assigned only in constructor
public sealed class GameManager
{
    private readonly ILogger logger;
    private readonly IPlayerService playerService;
    private readonly IScoreService scoreService;

    public GameManager(ILogger logger, IPlayerService playerService, IScoreService scoreService)
    {
        this.logger = logger;
        this.playerService = playerService;
        this.scoreService = scoreService;
    }
}

// ❌ BAD: Mutable fields that never change after construction
public sealed class GameManager
{
    private ILogger logger;     // Should be readonly
    private IPlayerService playerService; // Should be readonly
}
```

## Guard Clauses

```csharp
// ✅ GOOD: Guard clause at method start
public void ProcessPlayer(Player player)
{
    ArgumentNullException.ThrowIfNull(player);
    // ... rest of logic at top level
}

// ❌ BAD: Deep nesting with null checks
public void ProcessPlayer(Player player)
{
    if (player != null)
    {
        if (player.IsActive)
        {
            if (player.HasInventory)
            {
                // Deeply nested logic
            }
        }
    }
}
```

---

Continue in **quality-hygiene-resources.md** for resource management and data patterns.

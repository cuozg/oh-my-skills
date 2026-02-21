# C# Quality & Code Hygiene

> **Note:** This guide assumes a project-level `ILogger` abstraction injected via DI. Adapt the logging interface to your project's choice (e.g., `Microsoft.Extensions.Logging.ILogger`, Serilog, or a custom wrapper).

## Enable Nullable Reference Types

```csharp
// ✅ GOOD: Enable nullable annotations in .csproj
<PropertyGroup>
    <Nullable>enable</Nullable>
</PropertyGroup>

// Declare nullable explicitly
public string? OptionalName { get; set; } // Can be null
public string RequiredName { get; set; } = string.Empty; // Never null

// ❌ BAD: Ignoring nullability
public string Name { get; set; } // Warning: Non-nullable property must contain non-null value
```

## Use Least Accessible Access Modifier

```csharp
// ✅ GOOD: Most restrictive access
private readonly IService service; // Only accessible in this class
internal sealed class Helper { } // Only accessible in this assembly
public interface IPublicApi { } // Public only when necessary

// ❌ BAD: Everything public
public IService service; // Unnecessarily exposed
public class Helper { } // Should be internal
```

## Fix All Warnings

**Rule:** Treat warnings as errors. Never ignore compiler warnings.

```csharp
// ✅ GOOD: Fix warnings
#pragma warning disable CS0649 // Field is never assigned - FIX THE CODE INSTEAD

// Better: Actually fix the issue
private readonly string name = string.Empty;
```

## Throw Exceptions for Errors (+ Proper Logging)

**Critical Rule**: Throw exceptions instead of logging errors or returning defaults.

**Logging Guidelines:**
- **ILogger (project abstraction)**: Use for runtime scripts (informational logs)
  - ✅ ILogger handles conditional compilation internally (no #if guards needed)
  - ✅ ILogger handles prefixes automatically (no [prefix] needed)
  - ❌ NEVER log in constructors (keep constructors fast and side-effect free)
  - ❌ Remove verbose logs (keep only necessary logs)
  - ❌ No null-conditional operator (DI guarantees non-null: use `this.logger.Debug()` not `this.logger?.Debug()`)
- **Debug.Log**: Use ONLY for editor scripts (#if UNITY_EDITOR)
- **Exceptions**: Use for errors (never log errors - throw!)

```csharp
// ✅ EXCELLENT: ILogger for runtime (project-configured)
public sealed class GameService
{
    private readonly ILogger logger; // Injected via DI

    public GameService(ILogger logger)
    {
        this.logger = logger;
    }

    public Player GetPlayer(string id)
    {
        return players.TryGetValue(id, out var player)
            ? player
            : throw new KeyNotFoundException($"Player not found: {id}");
    }

    public void StartGame()
    {
        this.logger.Info("Game started");
        this.LoadLevel(1);
    }

    private void ProcessGameData()
    {
        this.logger.Debug("Processing critical game data");
    }
}

// ✅ GOOD: Debug.Log ONLY in editor scripts
#if UNITY_EDITOR
public class EditorTool
{
    public void ProcessAssets()
    {
        Debug.Log("Processing assets...");
    }
}
#endif

// ❌ WRONG: Conditional compilation guards (ILogger handles this)
public void Bad1()
{
    #if UNITY_EDITOR
    this.logger.Debug("Don't do this"); // ILogger handles this internally
    #endif
}

// ❌ WRONG: Manual prefixes (ILogger handles this)
public void Bad2()
{
    this.logger.Debug("[GameService] Don't add prefixes"); // ILogger handles this
}

// ❌ WRONG: Logging in constructor
public GameService(ILogger logger)
{
    this.logger = logger;
    this.logger.Debug("Initializing..."); // NO! Keep constructors fast
}

// ❌ WRONG: Null-conditional operator (DI guarantees non-null)
public void Bad4()
{
    this.logger?.Debug("Don't use ?. operator"); // DI guarantees non-null
}

// ❌ WRONG: Verbose unnecessary logs
public void Bad5()
{
    this.logger.Debug("Entering method");
    this.logger.Debug("Variable x = " + x);
    this.logger.Debug("Exiting method");
}

// ❌ WRONG: Return default or log errors
public Player? Bad6(string id)
{
    if (!players.ContainsKey(id))
    {
        this.logger.Error("Player not found"); // WRONG: throw instead!
        return null;
    }
    return players[id];
}

// ❌ WRONG: Debug.Log in runtime code
public void Bad7()
{
    Debug.Log("This should use ILogger"); // Use ILogger instead
}
```

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
    private readonly SignalBus signalBus;
    private readonly PlayerService playerService;

    public GameManager(ILogger logger, SignalBus signalBus, PlayerService playerService)
    {
        this.logger = logger;
        this.signalBus = signalBus;
        this.playerService = playerService;
    }
}

// ❌ BAD: Mutable fields that never change after construction
public sealed class GameManager
{
    private ILogger logger;     // Should be readonly
    private SignalBus signalBus; // Should be readonly
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

## Dispose Pattern

```csharp
// ✅ GOOD: IDisposable for unmanaged resources
public sealed class TextureManager : IDisposable
{
    private Texture2D? texture;
    private bool disposed;

    public void Dispose()
    {
        if (disposed) return;
        if (texture != null)
        {
            UnityEngine.Object.Destroy(texture);
            texture = null;
        }
        disposed = true;
    }
}

// ❌ BAD: Forgetting to dispose
public class TextureManager
{
    private Texture2D texture; // Never disposed → memory leak
}
```

## Collection Initialization

```csharp
// ✅ GOOD: Initialize collections to avoid null
private readonly List<Player> players = new();
private readonly Dictionary<string, Item> items = new();
private readonly HashSet<int> visitedIds = new();

// ❌ BAD: Null collections
private List<Player> players; // Null until first use → NullReferenceException
```

## String Handling

```csharp
// ✅ GOOD: String interpolation and proper comparison
var message = $"Player {name} scored {score} points";
if (string.Equals(a, b, StringComparison.Ordinal)) { }
if (string.IsNullOrEmpty(input)) { }

// ❌ BAD: String concatenation and default comparison
var message = "Player " + name + " scored " + score + " points"; // Allocations
if (a == b) { } // Default comparison may surprise with culture
```

## Magic Numbers

```csharp
// ✅ GOOD: Named constants
private const float MaxSpeed = 10f;
private const int MaxRetries = 3;
private const float GravityMultiplier = 2.5f;

if (speed > MaxSpeed) { }

// ❌ BAD: Magic numbers
if (speed > 10f) { } // What is 10?
for (var i = 0; i < 3; i++) { } // Why 3?
```

## Boolean Parameters

```csharp
// ✅ GOOD: Named parameters or enums for boolean flags
player.SetActive(isVisible: true);
ProcessOrder(OrderMode.Express);

// ❌ BAD: Unnamed boolean parameters
player.SetActive(true); // What does true mean here?
ProcessOrder(true, false, true); // Completely unreadable
```

# Modern C# Features — Part 2a: Records & Init-Only Properties

Records for immutable data and init-only properties for compile-time safety.

---

## Records

```csharp
// ✅ GOOD: Record for immutable data
public record Player(string Name, int Health, Vector3 Position);

// Create and use
var player = new Player("Alice", 100, Vector3.zero);
var damaged = player with { Health = 50 }; // Immutable copy with changes

// ✅ GOOD: Record with methods
public record Item(string Name, int Quantity)
{
    public bool IsEmpty => this.Quantity == 0;
}

// ✅ GOOD: Record equality (automatic)
var item1 = new Item("Sword", 1);
var item2 = new Item("Sword", 1);
bool equal = item1 == item2; // true (value equality)

// ❌ BAD: Mutable class where record would be clearer
public class PlayerData
{
    public string Name { get; set; }
    public int Health { get; set; }
    public Vector3 Position { get; set; }
}
```

---

## Init-Only Properties

```csharp
// ✅ GOOD: Init-only prevents post-construction mutation
public class Config
{
    public string ApiUrl { get; init; }
    public int Timeout { get; init; }
    public bool Debug { get; init; }
}

var config = new Config { ApiUrl = "...", Timeout = 30, Debug = false };
// config.ApiUrl = "..."; // ❌ ERROR: Init-only property cannot be set

// ✅ GOOD: With required keyword (C# 11+)
public class GameSettings
{
    public required int MaxPlayers { get; init; }
    public required string GameMode { get; init; }
}

// Forced to set required properties
var settings = new GameSettings { MaxPlayers = 4, GameMode = "PvP" };

// ❌ BAD: Mutable properties allow silent bugs
public class OldConfig
{
    public string ApiUrl { get; set; }
    public int Timeout { get; set; }
}
```

---

Continue in **strings.md** for String Interpolation, Collections, and var keyword.

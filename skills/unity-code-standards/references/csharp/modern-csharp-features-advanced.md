# Modern C# Features — Part 4a: Target-Typed, Deconstruction, Static Locals

Target-typed new, deconstruction, and static local functions.

---

## Target-Typed new Expression

```csharp
// ✅ GOOD: Target-typed new (C# 9+)
List<Player> players = new();
Dictionary<string, Item> inventory = new();
Player player = new() { Name = "Alice", Health = 100 };

// ✅ GOOD: Eliminates redundant type specification
Queue<Vector3> waypoints = new();
Stack<int> undoStack = new();

// ❌ BAD: Redundant type specification
List<Player> oldPlayers = new List<Player>();
Dictionary<string, Item> oldInventory = new Dictionary<string, Item>();
Player oldPlayer = new Player { Name = "Alice", Health = 100 };

// ❌ BAD: Target-typed new with ambiguous context
var list = new(); // ❌ ERROR: Cannot infer type
```

---

## Deconstruction

```csharp
// ✅ GOOD: Deconstruct record
public record Player(string Name, int Health, Vector3 Position);

var player = new Player("Alice", 100, Vector3.zero);
var (name, health, pos) = player;

// ✅ GOOD: Deconstruct tuple
var data = ("Alice", 100, Vector3.zero);
var (playerName, playerHealth, playerPos) = data;

// ✅ GOOD: Ignore fields with underscore
var (name, _, pos) = player; // Ignore health

// ❌ BAD: Accessing tuple by index (unreadable)
var data = ("Alice", 100, Vector3.zero);
var name = data.Item1;
var health = data.Item2;
var pos = data.Item3;
```

---

## Static Local Functions

```csharp
// ✅ GOOD: Static local function (no closure)
public int ProcessItems(List<Item> items)
{
    static bool IsValid(Item item) => item.Quantity > 0;
    return items.Count(IsValid);
}

// ✅ GOOD: Performance benefit (no closure = no allocations)
public string BuildMessage(string prefix)
{
    static string GetSuffix() => "done"; // No closure overhead
    return prefix + " " + GetSuffix();
}

// ❌ BAD: Non-static local function with closure (allocates)
public int ProcessItems(List<Item> items)
{
    int totalQuantity = 0; // Captured variable
    bool IsValid(Item item) => item.Quantity > totalQuantity; // Closure here
    return items.Count(IsValid);
}
```

---

Continue in **modern-csharp-features-advanced-span.md** for Required Members, Span<T>, Using Declarations, and Quick Reference.

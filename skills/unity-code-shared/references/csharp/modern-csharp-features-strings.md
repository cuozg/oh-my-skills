# Modern C# Features — Part 2b: Strings & Collections

String interpolation, collection expressions, and var keyword patterns.

---

## String Interpolation

```csharp
// ✅ GOOD: String interpolation
string name = "Alice";
int health = 75;
string message = $"Player {name} has {health} HP";

// ✅ GOOD: Format specifiers in interpolation
float value = 3.14159f;
string formatted = $"Pi: {value:F2}"; // "Pi: 3.14"

// ✅ GOOD: Multiline interpolation
string multiline = $@"
    Player: {name}
    Health: {health}
    Status: {(health > 50 ? "Healthy" : "Wounded")}
";

// ❌ BAD: String.Format (verbose)
string old = string.Format("Player {0} has {1} HP", name, health);

// ❌ BAD: Concatenation (hard to read)
string concat = "Player " + name + " has " + health + " HP";
```

---

## Collection Expressions (C# 12+)

```csharp
// ✅ GOOD: Collection expression syntax
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alice", "Bob", "Charlie"];
Dictionary<string, int> scores = new() { { "Alice", 100 }, { "Bob", 85 } };

// ✅ GOOD: Spread operator in collections
int[] firstHalf = [1, 2, 3];
int[] secondHalf = [4, 5, 6];
int[] combined = [..firstHalf, ..secondHalf];

// ✅ GOOD: Collection expression with LINQ
var query = [..players.Where(p => p.Health > 0)];

// ❌ BAD: Old array initialization
int[] oldNumbers = new int[] { 1, 2, 3, 4, 5 };
List<string> oldNames = new List<string> { "Alice", "Bob", "Charlie" };
```

---

## var Keyword

```csharp
// ✅ GOOD: var for obvious types
var player = new Player("Alice", 100, Vector3.zero);
var count = list.Count;
var names = from p in players select p.Name;

// ✅ GOOD: var in complex LINQ (type is clear from context)
var activeHealthy = players
    .Where(p => p.IsActive)
    .Where(p => p.Health > 50)
    .OrderBy(p => p.Name)
    .ToList();

// ❌ BAD: var for unclear type
var x = GetSomeValue(); // What type is x? Unclear.

// ❌ BAD: var for primitive that could be ambiguous
var count = 5; // Is this int or long? Use explicit type.
int count = 5; // Clear.
```

---

Continue in **modern-csharp-features-namespaces.md** for Namespaces & Organization.

# C# Strings, Magic Numbers & Collections

String handling, interpolation, collection expressions, var keyword, magic numbers, boolean parameters.

## String Handling

```csharp
// ✅ GOOD: String interpolation
string message = $"Player {name} has {health} HP";

// ✅ GOOD: Format specifiers
string formatted = $"Pi: {value:F2}"; // "Pi: 3.14"

// ✅ GOOD: Multiline interpolation
string multiline = $@"
    Player: {name}
    Health: {health}
    Status: {(health > 50 ? "Healthy" : "Wounded")}
";

// ✅ GOOD: Proper comparison
if (string.Equals(a, b, StringComparison.Ordinal)) { }
if (string.IsNullOrEmpty(input)) { }

// ❌ BAD: Concatenation (allocations, O(n²) in loops)
var message = "Player " + name + " scored " + score;
// ❌ BAD: String.Format (verbose)
string old = string.Format("Player {0} has {1} HP", name, health);
// ❌ BAD: Default == comparison (culture surprises)
if (a == b) { }
```

## Collection Expressions (C# 12+)

```csharp
// ✅ GOOD: Collection expression syntax
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alice", "Bob", "Charlie"];

// ✅ GOOD: Spread operator
int[] combined = [..firstHalf, ..secondHalf];
var query = [..players.Where(p => p.Health > 0)];

// ❌ BAD: Old initialization
int[] oldNumbers = new int[] { 1, 2, 3, 4, 5 };
```

## var Keyword

```csharp
// ✅ GOOD: var for obvious types
var player = new Player("Alice", 100, Vector3.zero);
var activeHealthy = players.Where(p => p.IsActive).ToList();

// ❌ BAD: var for unclear type
var x = GetSomeValue(); // What type?
var count = 5; // int or long? Use explicit type.
```

## Magic Numbers

```csharp
// ✅ GOOD: Named constants
private const float MaxSpeed = 10f;
private const int MaxRetries = 3;
if (speed > MaxSpeed) { }

// ❌ BAD: Magic numbers
if (speed > 10f) { } // What is 10?
```

## Boolean Parameters

```csharp
// ✅ GOOD: Named parameters or enums
player.SetActive(isVisible: true);
ProcessOrder(OrderMode.Express);

// ❌ BAD: Unnamed booleans
ProcessOrder(true, false, true); // Unreadable
```

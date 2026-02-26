# C# Quality & Code Hygiene — Part 4: Strings, Magic Numbers, Booleans

String handling, magic numbers, and boolean parameters.

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

---

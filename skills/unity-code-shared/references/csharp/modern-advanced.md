# Modern C# — Advanced Features

Target-typed new, deconstruction, static locals, required members, Span<T>, using declarations.

## Target-Typed new Expression

```csharp
// ✅ GOOD: Target-typed new (C# 9+)
List<Player> players = new();
Dictionary<string, Item> inventory = new();
Player player = new() { Name = "Alice", Health = 100 };

// ❌ BAD: Redundant type specification
List<Player> oldPlayers = new List<Player>();
```

## Deconstruction

```csharp
// ✅ GOOD: Deconstruct record
public record Player(string Name, int Health, Vector3 Position);
var (name, health, pos) = player;

// ✅ GOOD: Deconstruct tuple, ignore with underscore
var (playerName, _, playerPos) = data;

// ❌ BAD: Accessing tuple by index
var name = data.Item1; // Unreadable
```

## Static Local Functions

```csharp
// ✅ GOOD: Static local (no closure = no allocations)
public int ProcessItems(List<Item> items)
{
    static bool IsValid(Item item) => item.Quantity > 0;
    return items.Count(IsValid);
}

// ❌ BAD: Non-static with closure (allocates)
bool IsValid(Item item) => item.Quantity > totalQuantity; // Captures totalQuantity
```

## Required Members (C# 11+)

```csharp
// ✅ GOOD: Required init properties
public class Player
{
    public required string Name { get; init; }
    public required int MaxHealth { get; init; }
    public int CurrentHealth { get; init; } = 100;
}
// Forgetting required property → compile error

// ❌ BAD: Optional properties that should be required
public string Name { get; set; } // Nullable, easy to forget
```

## Span<T> & stackalloc

```csharp
// ✅ GOOD: Span for stack-allocated data (no heap)
Span<int> span = stackalloc int[10];

// ❌ BAD: List<T> for small temp collections (heap allocation)
```

## Using Declarations

```csharp
// ✅ GOOD: Using declaration (C# 8+)
using FileStream stream = new FileStream(path, FileMode.Open);
// Disposed at end of scope

// ❌ BAD: Old using statement (verbose nesting)
using (FileStream stream = new FileStream(path, FileMode.Open)) { }
```

## Quick Reference

| Feature | Benefit | Use Case |
|:---|:---|:---|
| Pattern Matching | Type-safe, clear intent | Type checks, validation |
| Null-Coalescing | Safe defaults | Handle null gracefully |
| Records | Immutability, equality | Data transfer objects |
| Init-Only Properties | Prevent mutation | Immutable DTOs |
| String Interpolation | Readable formatting | Messages, logging |
| Collection Expressions | Concise init | Arrays, lists |
| Global Using | Less boilerplate | Common namespaces |
| File-Scoped Namespaces | Cleaner structure | One feature per file |
| Target-Typed new | No redundancy | Type-inferred init |
| Deconstruction | Destructure values | Extract fields |
| Static Local Functions | No closure allocs | Hot path helpers |
| Required Members | Compile-time safety | Mandatory init |
| Span<T> | Zero-allocation | Hot paths, stack alloc |
| Using Declarations | Auto resource cleanup | Streams, connections |

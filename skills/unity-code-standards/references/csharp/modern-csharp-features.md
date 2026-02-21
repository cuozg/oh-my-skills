# Modern C# Features (C# 9-12)

## Expression-Bodied Members

```csharp
// ✅ GOOD: Expression body for single-expression members
public string Name => this.firstName + " " + this.lastName;
public int Count => this.items.Count;
public bool IsEmpty => this.items.Count == 0;
public override string ToString() => $"Player({this.Name}, {this.Score})";
public void Reset() => this.score = 0;
public Player this[int index] => this.players[index];

// ❌ BAD: Full body for single expressions
public string Name
{
    get { return this.firstName + " " + this.lastName; }
}

public override string ToString()
{
    return $"Player({this.Name}, {this.Score})";
}
```

## Null-Coalescing & Null-Conditional

```csharp
// ✅ GOOD: Null-coalescing operator
string name = input ?? "Default";
this.cache ??= new Dictionary<string, object>();
var length = text?.Length ?? 0;
var firstItem = list?.FirstOrDefault()?.Name ?? "None";

// ❌ BAD: Verbose null checks
string name = input != null ? input : "Default";
if (this.cache == null)
    this.cache = new Dictionary<string, object>();
int length = text != null ? text.Length : 0;
```

## Pattern Matching

```csharp
// ✅ GOOD: Type pattern with is
if (collider is BoxCollider box)
{
    var size = box.size;
}

// ✅ GOOD: Switch expression
string GetDamageType(Weapon weapon) => weapon switch
{
    Sword { IsEnchanted: true } => "Magic",
    Sword => "Physical",
    Bow => "Ranged",
    Staff => "Magic",
    _ => throw new ArgumentOutOfRangeException(nameof(weapon))
};

// ✅ GOOD: Property pattern
if (player is { IsActive: true, Health: > 0 })
{
    // Player is active and alive
}

// ✅ GOOD: Relational patterns
string GetHealthStatus(int hp) => hp switch
{
    <= 0 => "Dead",
    < 25 => "Critical",
    < 50 => "Wounded",
    < 75 => "Healthy",
    _ => "Full"
};

// ✅ GOOD: Logical patterns
if (value is > 0 and < 100) { }
if (input is not null) { }
if (obj is not Player) { }

// ❌ BAD: Type check then cast
if (collider is BoxCollider)
{
    var box = (BoxCollider)collider; // Redundant cast
}

// ❌ BAD: Long if-else chain
if (weapon is Sword)
    return "Physical";
else if (weapon is Bow)
    return "Ranged";
else if (weapon is Staff)
    return "Magic";
else
    throw new ArgumentOutOfRangeException();
```

## Records & Init-Only Properties

```csharp
// ✅ GOOD: Record for immutable data
public readonly record struct DamageEvent(int Amount, DamageType Type, string Source);
public readonly record struct PlayerScore(string Name, int Score);

// ✅ GOOD: Init-only properties for immutable configuration
public sealed class GameConfig
{
    public required int MaxPlayers { get; init; }
    public required float RoundTime { get; init; }
    public string MapName { get; init; } = "Default";
}

// Usage:
var config = new GameConfig
{
    MaxPlayers = 4,
    RoundTime = 120f,
    MapName = "Arena"
};

// ❌ BAD: Mutable class for data that shouldn't change
public class DamageEvent
{
    public int Amount { get; set; } // Should be init or readonly
    public DamageType Type { get; set; }
}
```

## String Interpolation & Raw Strings

```csharp
// ✅ GOOD: String interpolation
var msg = $"Player {name} scored {score} points in {time:F2}s";
var path = $"{basePath}/{fileName}.{extension}";

// ✅ GOOD: Raw string literals for multi-line
var json = """
    {
        "name": "Player1",
        "score": 100,
        "items": ["sword", "shield"]
    }
    """;

// ✅ GOOD: Interpolated raw strings
var query = $"""
    SELECT * FROM players
    WHERE team = '{teamName}'
    AND score > {minScore}
    """;

// ❌ BAD: String concatenation
var msg = "Player " + name + " scored " + score + " points"; // Allocations
var json = "{\n  \"name\": \"Player1\",\n  \"score\": 100\n}"; // Unreadable
```

## var for Obvious Types

```csharp
// ✅ GOOD: var when type is obvious from right side
var players = new List<Player>();
var config = GameConfig.Load();
var name = player.GetName();
var dict = new Dictionary<string, List<int>>();

// ❌ BAD: var when type is not obvious
var result = Process(); // What type is result?
var x = GetValue(); // Completely unclear

// ✅ GOOD: Explicit type when not obvious
PlayerState result = Process();
float damage = CalculateDamage();
```

## Collection Expressions (C# 12)

```csharp
// ✅ GOOD: Collection expressions
List<int> numbers = [1, 2, 3, 4, 5];
int[] array = [10, 20, 30];
List<string> names = ["Alice", "Bob", "Charlie"];

// ✅ GOOD: Spread operator
List<int> combined = [..firstList, ..secondList, 99];

// ❌ BAD: Verbose initialization
var numbers = new List<int> { 1, 2, 3, 4, 5 };
var array = new int[] { 10, 20, 30 };
```

## Global Using Directives

```csharp
// ✅ GOOD: GlobalUsings.cs file
global using System;
global using System.Collections.Generic;
global using System.Linq;
global using System.Threading;
global using UnityEngine;
global using Cysharp.Threading.Tasks;
global using System.Threading.Tasks;

// Benefits:
// - Removes repetitive using blocks from every file
// - One place to manage common namespaces
// - Reduces file noise
```

## File-Scoped Namespaces

```csharp
// ✅ GOOD: File-scoped namespace (one less indent level)
namespace YourProject.Services;

public sealed class PlayerService
{
    // All code at one less indent level
}

// ❌ BAD: Block-scoped namespace
namespace YourProject.Services
{
    public sealed class PlayerService
    {
        // Extra indentation for everything
    }
}
```

## Target-Typed New

```csharp
// ✅ GOOD: Target-typed new
private readonly List<Player> players = new();
private readonly Dictionary<string, int> scores = new();
private readonly StringBuilder builder = new();

Player player = new("Alice", 100);

// ❌ BAD: Redundant type specification
private readonly List<Player> players = new List<Player>();
private readonly Dictionary<string, int> scores = new Dictionary<string, int>();
```

## Deconstruction

```csharp
// ✅ GOOD: Deconstruct tuples and records
var (name, score) = GetPlayerInfo();
var (x, y, z) = transform.position;

foreach (var (key, value) in dictionary)
{
    Console.WriteLine($"{key}: {value}");
}

// ✅ GOOD: Discard unused values
var (_, score) = GetPlayerInfo(); // Only need score
if (int.TryParse(input, out _)) { } // Only care about success
```

## Static Local Functions

```csharp
// ✅ GOOD: Static local function (no closure allocation)
public float CalculateScore(List<Player> players)
{
    return players.Sum(p => GetWeightedScore(p));

    static float GetWeightedScore(Player player)
        => player.Score * player.Multiplier;
}

// ❌ BAD: Non-static local function capturing outer scope
public float CalculateScore(List<Player> players)
{
    float bonus = 1.5f;
    return players.Sum(p => GetWeightedScore(p));

    float GetWeightedScore(Player player)
        => player.Score * bonus; // Captures 'bonus' → closure allocation
}
```

## Required Members (C# 11)

```csharp
// ✅ GOOD: Required properties
public sealed class PlayerConfig
{
    public required string Name { get; init; }
    public required int MaxHealth { get; init; }
    public float Speed { get; init; } = 5f; // Optional with default
}

// Compiler enforces required properties at construction:
var config = new PlayerConfig
{
    Name = "Hero",     // Required
    MaxHealth = 100,   // Required
    // Speed uses default 5f
};

// ❌ Compile error: required members not set
var bad = new PlayerConfig { Name = "Hero" }; // Missing MaxHealth
```

## Span<T> & ReadOnlySpan<T>

```csharp
// ✅ GOOD: Span for stack-allocated, zero-copy slicing
ReadOnlySpan<char> firstName = fullName.AsSpan(0, spaceIndex);
Span<int> slice = array.AsSpan(start, length);

// ✅ GOOD: stackalloc with Span
Span<byte> buffer = stackalloc byte[256];

// ❌ BAD: Substring (allocates new string)
string firstName = fullName.Substring(0, spaceIndex); // Heap allocation
```

## Using Declaration

```csharp
// ✅ GOOD: Using declaration (no extra nesting)
public async UniTask LoadData()
{
    using var stream = File.OpenRead(path);
    using var reader = new StreamReader(stream);
    var content = await reader.ReadToEndAsync();
}

// ❌ BAD: Using statement with nesting
public async UniTask LoadData()
{
    using (var stream = File.OpenRead(path))
    {
        using (var reader = new StreamReader(stream))
        {
            var content = await reader.ReadToEndAsync();
        }
    }
}
```

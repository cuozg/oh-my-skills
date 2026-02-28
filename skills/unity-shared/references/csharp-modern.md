# Modern C# (9–12)

Expression-bodied members, pattern matching, records, namespaces, and advanced features.

## Expression-Bodied & Null-Coalescing

```csharp
public string Name => _firstName + " " + _lastName;
public bool IsEmpty => _items.Count == 0;
public override string ToString() => $"Player({Name})";

string name = input ?? "Default";
_cache ??= new Dictionary<string, object>();
var length = text?.Length ?? 0;
```

## Pattern Matching

```csharp
if (collider is BoxCollider box) { var size = box.size; }
if (player is { IsActive: true, Health: > 0 }) { }
if (value is > 0 and < 100) { }

string GetDamageType(Weapon weapon) => weapon switch
{
    Sword { IsEnchanted: true } => "Magic",
    Sword => "Physical",
    Bow => "Ranged",
    _ => throw new ArgumentOutOfRangeException(nameof(weapon))
};
```

## Records & Init-Only

```csharp
public record Player(string Name, int Health, Vector3 Position);
var damaged = player with { Health = 50 };

public class Config
{
    public required string ApiUrl { get; init; }
    public required int Timeout { get; init; }
}
```

## Namespaces & Global Using

```csharp
// GlobalUsings.cs — one file, project root
global using System;
global using System.Collections.Generic;
global using UnityEngine;

// File-scoped namespace (C# 10+)
namespace GameLogic;

public class Player { }
```

## Target-Typed new & Deconstruction

```csharp
List<Player> players = new();
Dictionary<string, Item> inventory = new();
var (name, health, pos) = player;  // Deconstruct record
```

## Static Local Functions & Required Members

```csharp
// Static local — no closure = no allocation
public int Count(List<Item> items)
{
    static bool IsValid(Item item) => item.Quantity > 0;
    return items.Count(IsValid);
}

// Required members (C# 11+) — compile error if missing
public class Player
{
    public required string Name { get; init; }
    public required int MaxHealth { get; init; }
}
```

## Quick Reference
Pattern Matching (type-safe branching) · Records (immutable value equality) · Init-Only/Required (compile-time safety) · Global Using (less boilerplate) · File-Scoped Namespace (cleaner structure) · Target-Typed new (no type redundancy) · Static Local Functions (zero-alloc helpers)

# Modern C# in Unity (C# 9–12)

Unity 6 officially supports **C# 9** (Mono/IL2CPP), with partial C# 10/11 support. 

## Unity 6 C# Support & Restrictions
- **IL2CPP Limitations**: No dynamic code generation (`Reflection.Emit`), limited generic sharing, strict AOT compilation constraints.
- **Collection Expressions** (C# 12): `[1, 2]` ❌ **NOT available** in Unity yet. Do not use them.

## Span<T> & Memory<T> (Unity 2021.2+)
```csharp
// Zero-allocation slicing and string parsing
Span<byte> buffer = stackalloc byte[128]; // Fast stack memory
void ParseName(ReadOnlySpan<char> text) { } // No string allocation
```

## Expression-Bodied & Null-Coalescing
```csharp
public string Name => _first + " " + _last;
public bool IsEmpty => _items.Count == 0;

string name = input ?? "Default";
_cache ??= new Dictionary<string, object>();
var length = text?.Length ?? 0;
```

## Pattern Matching
```csharp
if (collider is BoxCollider box) { var size = box.size; }
if (player is { IsActive: true, Health: > 0 }) { }
if (value is > 0 and < 100) { }

string GetDamageType(Weapon w) => w switch {
    Sword { IsEnchanted: true } => "Magic",
    Sword => "Physical",
    _ => throw new ArgumentOutOfRangeException(nameof(w))
};
```

## Records & Init-Only / Required Members
```csharp
public record Player(string Name, int Health, Vector3 Pos); // Immutable value equality
var damaged = player with { Health = 50 };                  // Non-destructive mutation

public class Config {
    public required string ApiUrl { get; init; } // C# 11+
    // ⚠️ GOTCHA: [SerializeField] does NOT work with 'required' modifier
}
```

## Namespaces & Global Using
```csharp
// GlobalUsings.cs — one file, project root
global using System;
global using System.Collections.Generic;
global using UnityEngine;

namespace GameLogic; // File-scoped namespace (C# 10+)
public class GameSystem { }
```

## Target-Typed new, Deconstruction & Raw Strings
```csharp
List<Player> players = new(); // Target-typed new
var (name, health, pos) = player;  // Deconstruct record

// Raw string literals (C# 11+, available in Unity 6)
string json = """
{
    "key": "value"
}
""";
```

## Static Local Functions
```csharp
public int Count(List<Item> items) {
    // Static local — no closure = no allocation
    static bool IsValid(Item item) => item.Quantity > 0;
    return items.Count(IsValid);
}
```

## Quick Reference
Span/Memory (zero-alloc) · Pattern Matching (type-safe branching) · Records (value equality) · Init/Required (compile-time safety) · Raw Strings (`"""`) · Global Using (less boilerplate) · Target-Typed new (no redundancy) · Static Local (zero-alloc helpers) · IL2CPP (no emit/dynamic) · Collection Expr (`[]`) (❌ unavailable)
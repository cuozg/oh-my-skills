# Modern C# Features — Part 4b: Required Members, Span<T>, Using Declarations

Required members, Span<T>, using declarations, and quick reference table.

---

## Required Members (C# 11+)

```csharp
// ✅ GOOD: Required init properties
public class Player
{
    public required string Name { get; init; }
    public required int MaxHealth { get; init; }
    public int CurrentHealth { get; init; } = 100;
}

// Must set required properties
var player = new Player { Name = "Alice", MaxHealth = 100 };
// Forgetting required property → compile error

// ❌ BAD: Optional properties that should be required
public class OldPlayer
{
    public string Name { get; set; } // Nullable, easy to forget
    public int MaxHealth { get; set; } // Could be 0 (invalid)
}
```

---

## Span<T> & Using Declarations

```csharp
// ✅ GOOD: Span for stack-allocated data (no heap allocation)
public void ProcessArray(int[] numbers)
{
    Span<int> span = stackalloc int[10]; // Stack allocation, very fast
    Array.Copy(numbers, span);
}

// ✅ GOOD: Using declaration (C# 8+)
public void LoadFile(string path)
{
    using FileStream stream = new FileStream(path, FileMode.Open);
    // stream is automatically disposed at end of scope
} // stream.Dispose() called here automatically

// ❌ BAD: List<T> for small collections (heap allocation)
public void ProcessItems(List<int> items)
{
    // List allocates on heap; Span<T> uses stack
}

// ❌ BAD: Old using statement syntax (verbose)
public void OldLoadFile(string path)
{
    using (FileStream stream = new FileStream(path, FileMode.Open))
    {
        // Use stream
    }
}
```

---

## Quick Reference

| Feature | Benefit | Use Case |
| :--- | :--- | :--- |
| **Pattern Matching** | Type-safe, clear intent | Type checks, property validation |
| **Null-Coalescing** | Safe defaults | Handle null gracefully |
| **Records** | Immutability, equality | Data transfer objects |
| **Init-Only Properties** | Prevent mutation | Immutable DTOs |
| **String Interpolation** | Readable formatting | Build messages, logging |
| **Collection Expressions** | Concise initialization | Arrays, lists, dicts |
| **Global Using** | Less boilerplate | Common types and namespaces |
| **File-Scoped Namespaces** | Cleaner file structure | Single feature per file |
| **Target-Typed new** | Eliminates redundancy | Type-inferred initialization |
| **Deconstruction** | Destructure values | Extract tuple/record fields |
| **Static Local Functions** | Performance, clarity | Avoid closures, side effects |
| **Required Members** | Compile-time safety | Enforce mandatory initialization |
| **Span<T>** | Zero-allocation performance | Hot paths, stack allocation |
| **Using Declarations** | Automatic resource cleanup | File streams, database connections |

---

# C# Quality & Code Hygiene — Part 1

Nullable reference types, access modifiers, warnings, and exception handling.

> **Note:** This guide assumes a project-level `ILogger` abstraction injected via DI. Adapt the logging interface to your project's choice (e.g., `Microsoft.Extensions.Logging.ILogger`, Serilog, or a custom wrapper).

## Enable Nullable Reference Types

```csharp
// ✅ GOOD: Enable nullable annotations in .csproj
<PropertyGroup>
    <Nullable>enable</Nullable>
</PropertyGroup>

// Declare nullable explicitly
public string? OptionalName { get; set; } // Can be null
public string RequiredName { get; set; } = string.Empty; // Never null

// ❌ BAD: Ignoring nullability
public string Name { get; set; } // Warning: Non-nullable property must contain non-null value
```

## Use Least Accessible Access Modifier

```csharp
// ✅ GOOD: Most restrictive access
private readonly IService service; // Only accessible in this class
internal sealed class Helper { } // Only accessible in this assembly
public interface IPublicApi { } // Public only when necessary

// ❌ BAD: Everything public
public IService service; // Unnecessarily exposed
public class Helper { } // Should be internal
```

## Fix All Warnings

**Rule:** Treat warnings as errors. Never ignore compiler warnings.

```csharp
// ✅ GOOD: Fix warnings
#pragma warning disable CS0649 // Field is never assigned - FIX THE CODE INSTEAD

// Better: Actually fix the issue
private readonly string name = string.Empty;
```

## Throw Exceptions for Errors (+ Proper Logging)

**Critical Rule**: Throw exceptions instead of logging errors or returning defaults.

**Logging Guidelines:**
- **ILogger (project abstraction)**: Use for runtime scripts (informational logs)
  - ✅ ILogger handles conditional compilation internally
  - ✅ ILogger handles prefixes automatically
  - ❌ NEVER log in constructors (keep constructors fast)
  - ❌ Remove verbose logs
  - ❌ No null-conditional operator (DI guarantees non-null)
- **Debug.Log**: Use ONLY for editor scripts (#if UNITY_EDITOR)
- **Exceptions**: Use for errors (never log errors - throw!)

---

Continue in **quality-hygiene-naming.md** for naming conventions, sealed classes, and more.

# Unity C# Hygiene & Conventions
## Namespaces, Assemblies, & Files
- **Namespaces**: File-scoped; mirror folder path (`namespace Company.Project.Feature;`).
- **Files**: One type per file. Name must match type.
- **Asmdefs**: `Company.Project.Feature.asmdef`. Use GUID refs. No circular dependencies.
- **XML Docs**: Public APIs must have `<summary>`, `<param>`, and `<returns>`.
```csharp
namespace Company.Project.Player;

/// <summary>Manages player health and applies damage.</summary>
/// <param name="amount">The damage amount (must be positive).</param>
public sealed class HealthController : MonoBehaviour { }
```

## Naming & Access Modifiers
| Element | Style | Example |
|:---|:---|:---|
| Types, Methods, Props | PascalCase | `PlayerManager`, `GetHealth()` |
| Private fields | _camelCase | `_playerList`, `_isReady` |
| Constants, Enums | PascalCase | `MaxHealth`, `DamageType.Fire` |
| Interfaces | I-prefix | `IMovable` |
| Local vars, params | camelCase | `playerCount` |
- **Least Access**: Use `private` by default. Avoid `public` fields; use `[SerializeField] private`.
- **Magic Numbers**: Replace with `private const` or `static readonly`.

## Nullables, Collections, & Strings
- **Nullables**: Enable in `.csproj`. Use `?` for optional state.
- **Collections**: Use C# 12 expressions `[]`. Prefer `ReadOnlySpan<T>` for stack-only data.
- **Strings**: Use interpolation `$""`. Use raw string literals `""" """` for JSON/SQL.
```csharp
// ✅ Modern C# patterns
string name = "Hero";
string? title = null; 
List<int> scores = [10, 20, 30];
ReadOnlySpan<int> span = [1, 2, 3];
string msg = $"Player {name} ({title ?? "No Title"}) scored {scores[0]}";
string json = """{"name": "Hero", "level": 1}"""; 
```

## Sealed, Readonly, & Guards
- **Seal** classes by default. It enables devirtualization and prevents accidental inheritance.
- **Readonly**: Use for fields assigned in `Awake`/`Start` or constructor.
- **Guards**: Fail fast with `ArgumentNullException.ThrowIfNull` or `ThrowIfNegative`.
```csharp
public sealed class Health(int initial) {
    private readonly int _max = initial;
    public void Heal(int amount) {
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(amount);
        // Logic...
    }
}
```

## Error Handling & Logging
- **Exceptions**: Catch specific types. Never empty catch. Log + rethrow with `throw;`.
- **Logging**: Editor-only via `[Conditional("UNITY_EDITOR")]` or `#if UNITY_EDITOR`.
- **Structured**: Use interpolation or tags for filtering. Avoid logging in `Update`.
```csharp
[Conditional("UNITY_EDITOR")]
private void Log(string msg) => Debug.Log($"[System] {msg}");

public void Load(string path) {
    try { File.ReadAllText(path); }
    catch (IOException ex) {
        Debug.LogError($"[SaveSystem] Load failed: {ex.Message}");
        throw; // ✅ Preserves stack trace
    }
}
```

## IDisposable Pattern
- **Pattern**: Implement `IDisposable` for unmanaged resources (NativeArray, Texture2D).
- **Safety**: Use `GC.SuppressFinalize(this)` if a finalizer is present.
```csharp
public sealed class TextureHolder : IDisposable {
    private Texture2D? _texture;
    private bool _disposed;

    public void Dispose() {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    private void Dispose(bool disposing) {
        if (_disposed) return;
        if (disposing && _texture != null) Object.Destroy(_texture);
        _disposed = true;
    }
}
```

## Performance & Memory
- **Strings**: Avoid `+` in loops; use `StringBuilder` or `ZString`.
- **Collections**: Pre-size lists/dictionaries if count is known.
- **Boxing**: Avoid boxing value types in collections or logging.
- **Statics**: Minimize static state; use Dependency Injection or ScriptableObject events.
- **Events**: Always unsubscribe from C# events in `OnDestroy` or `OnDisable`.

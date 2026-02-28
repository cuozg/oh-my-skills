# C# Code Hygiene

Nullable refs, access modifiers, naming, disposal, strings, and warnings.

## Nullable References

```csharp
// csproj: <Nullable>enable</Nullable>
string name = "Alice";        // Non-nullable
string? nickname = null;      // Explicitly nullable
void Process(string? input) { if (input is null) return; }
```

## Access Modifiers & Warnings

- Use **least accessible** modifier (private > internal > public)
- Treat warnings as errors: `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`
- Throw exceptions for errors; use `ILogger` for runtime, `Debug.Log` for editor only

## Naming Conventions

| Element | Style | Example |
|:---|:---|:---|
| Types, Methods, Properties | PascalCase | `PlayerManager`, `GetHealth()` |
| Private fields | _camelCase | `_playerList`, `_isReady` |
| Constants, Enums | PascalCase | `MaxHealth`, `DamageType.Fire` |
| Interfaces | I-prefix | `IMovable`, `IDamageable` |
| Local variables, params | camelCase | `playerCount`, `isActive` |

## Sealed, Readonly, Guards

```csharp
// ✅ Seal classes with no virtual members
public sealed class DamageCalculator { }

// ✅ Mark readonly when assigned only in constructor
private readonly float _speed;

// ✅ Guard clauses — fail fast
ArgumentNullException.ThrowIfNull(player);
if (amount <= 0) throw new ArgumentOutOfRangeException(nameof(amount));
```

## Dispose Pattern

```csharp
// ✅ IDisposable for unmanaged resources
public sealed class TextureHolder : IDisposable
{
    private Texture2D _texture;
    private bool _disposed;

    public void Dispose()
    {
        if (_disposed) return;
        if (_texture != null) Object.Destroy(_texture);
        _disposed = true;
    }
}
```

## Strings & Collections

```csharp
// ✅ Interpolation over concatenation
string msg = $"Player {name} scored {score} points";

// ✅ Raw string literals for multiline
string json = """{"name": "Alice", "score": 100}""";

// ✅ const/static readonly for repeated strings
private const string DefaultName = "Unknown";

// ✅ Always initialize collections (never leave null)
private List<Item> _items = new();
private Dictionary<string, int> _scores = new();

// ✅ Collection expressions (C# 12)
int[] numbers = [1, 2, 3];
List<string> names = ["Alice", "Bob"];

// ✅ Use var when type is obvious from right side
var player = new Player();
var items = GetItems();
```

## No Magic Numbers

```csharp
// ❌ BAD
if (health < 25) { }

// ✅ GOOD
private const int CriticalHealthThreshold = 25;
if (health < CriticalHealthThreshold) { }
```

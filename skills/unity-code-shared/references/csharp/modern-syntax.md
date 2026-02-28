# Modern C# Features — Part 1

Patterns and features from C# 9-12 for cleaner, safer, and more performant code.

---

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

---

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

---

## Pattern Matching

```csharp
// ✅ GOOD: Type pattern with is
if (collider is BoxCollider box) { var size = box.size; }

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
if (player is { IsActive: true, Health: > 0 }) { }

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

// ❌ BAD: Type check then cast
if (collider is BoxCollider) { var box = (BoxCollider)collider; }

// ❌ BAD: Long if-else chain
if (weapon is Sword) return "Physical";
else if (weapon is Bow) return "Ranged";
else if (weapon is Staff) return "Magic";
else throw new ArgumentOutOfRangeException();
```

---

Continue in **modern-types.md** for Records, Strings, Collection Expressions.

# Performance Optimizations: Advanced

Continued from [performance-optimizations.md](performance-optimizations.md).

## Delegate & Lambda Caching

```csharp
// ✅ GOOD: Cache delegates
private readonly Action<int> cachedCallback;

public MyClass()
{
    this.cachedCallback = this.OnValueChanged;
}

// ✅ GOOD: Static lambda (no closure)
items.ForEach(static item => Process(item));

// ❌ BAD: Lambda allocating closure every call
void Update()
{
    items.ForEach(item => this.Process(item)); // Closure allocation every frame
}
```

## Dictionary Optimizations

```csharp
// ✅ GOOD: TryGetValue (single lookup)
if (dict.TryGetValue(key, out var value))
{
    Process(value);
}

// ✅ GOOD: GetValueOrDefault
var value = dict.GetValueOrDefault(key, defaultValue);

// ❌ BAD: ContainsKey + indexer (double lookup)
if (dict.ContainsKey(key))
{
    var value = dict[key]; // Second lookup
}
```

**See also:** [performance-optimizations.md](performance-optimizations.md) for Allocation Reduction, String Optimizations, Collections, Struct/Class, Boxing, and Arrays.

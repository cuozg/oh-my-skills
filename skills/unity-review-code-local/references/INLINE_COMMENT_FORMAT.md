# Inline Comment Format

Short, focused review comments — issue → why → fix. Bullet-based. No walls of text.

## Comment Templates

### Full Format (🔴 Critical / 🟡 Major)

```
// REVIEW [SEVERITY]: One-line problem summary
//   ├── WHY: Root cause or risk explanation
//   │   └── Evidence (callers, files, data flow)
//   └── FIX: Concrete fix option
```

### Quick Format (🔵 Minor)

```
// REVIEW [🔵 MINOR]: Problem → fix suggestion.
```

Severity tokens: `🔴 CRITICAL` · `🟡 MAJOR` · `🔵 MINOR`

## Examples

```csharp
// REVIEW [🔴 CRITICAL]: Null reference after await — MonoBehaviour may be destroyed
//   ├── WHY: `this` can be null between yield points
//   │   └── Called from 3 async paths (NetworkManager:89, UIController:134, GameLoop:201)
//   └── FIX: Guard `if (this == null) return;` after await
//       └── Or: bind to `destroyCancellationToken` (preferred)
await SomeAsyncOperation();
```

```csharp
// REVIEW [🔴 CRITICAL]: Serialized field mutated at runtime
//   ├── WHY: `_config` is a shared ScriptableObject — changes persist across instances + reloads
//   │   └── Mutated by: UpgradeShop.cs:156, AIController.cs:89
//   └── FIX: Clone in Awake: `_config = Instantiate(_config);`
[SerializeField] private WeaponConfig _config;
```

```csharp
// REVIEW [🔴 CRITICAL]: String allocation in Update (60fps)
//   ├── WHY: String concat allocates every frame → GC stalls
//   └── FIX: Cache StringBuilder or use TextMeshPro SetText (zero-alloc)
void Update() { _healthText.text = "Health: " + _health; }
```

```csharp
// REVIEW [🟡 MAJOR]: IndexOutOfRange on empty collection
//   ├── WHY: `items[0]` assumes non-empty list
//   │   └── 3 callers can pass empty: InventoryManager:45, ShopController:112, LootDrop:78
//   └── FIX: Add `if (items.Count == 0) return default;`
var first = items[0];
```

```csharp
// REVIEW [🔵 MINOR]: Double hash lookup → use TryGetValue instead of ContainsKey + indexer.
if (_cache.ContainsKey(key)) return _cache[key];
```

## Batch Pattern

Same issue in N files → full comment on first, short ref on rest:

```
// REVIEW [🟡 MAJOR]: GetComponent in hot path (1 of 4) — cache in Awake.
// REVIEW [🟡 MAJOR]: Same as PlayerController:45 — cache GetComponent. (2 of 4)
```

## Common Anti-Patterns

| Pattern | Severity | Fix |
|:---|:---|:---|
| Subscribe without unsubscribe | 🔴 | Add OnDisable with matching -= |
| GetComponent in Update | 🔴 | Cache in Awake |
| Null deref after Destroy | 🔴 | Check == null or null-coalescing |
| Event leak (no -= in OnDisable) | 🔴 | Verify -= via grep |
| Float comparison == | 🟡 | Use Mathf.Approximately |
| Magic numbers | 🔵 | Extract to const |
| Missing [RequireComponent] | 🔵 | Add attribute |

## Rules

- One issue = one comment. Don't combine.
- 🔴/🟡 → tree format. 🔵 → quick single-line OK.
- WHY: 1-3 sub-nodes max. Evidence as leaf.
- FIX: 1-3 solutions. Nested "Or:" for alternatives.
- Never comment without evidence. Investigate first.

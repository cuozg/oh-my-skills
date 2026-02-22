# Inline Comment Format

Short, focused review comments — issue → why → fix. Bullet-based. No walls of text.

## Comment Template

### Full Format (🔴 Critical / 🟡 Major)

```
// REVIEW [SEVERITY]: One-line problem summary
// WHY:
//   - Root cause or risk explanation
//   - Evidence (callers, files, data flow)
// FIX:
//   - Concrete fix option
```

### Quick Format (🔵 Minor)

```
// REVIEW [🔵 MINOR]: Problem → fix suggestion.
```

Severity tokens: `🔴 CRITICAL` · `🟡 MAJOR` · `🔵 MINOR`

## Examples

### 🔴 Critical

```csharp
// REVIEW [🔴 CRITICAL]: Null reference after await — MonoBehaviour may be destroyed
// WHY:
//   - `this` can be null between yield points
//   - Called from 3 async paths (NetworkManager:89, UIController:134, GameLoop:201)
// FIX:
//   - Guard: `if (this == null) return;` after await
//   - Or bind to `destroyCancellationToken` (preferred)
await SomeAsyncOperation();
_health = 100;
```

### 🟡 Major

```csharp
// REVIEW [🟡 MAJOR]: IndexOutOfRange on empty collection
// WHY:
//   - `items[0]` assumes non-empty list
//   - 3 callers can pass empty: InventoryManager:45, ShopController:112, LootDrop:78
// FIX:
//   - Add `if (items.Count == 0) return default;`
var first = items[0];
```

### 🔵 Minor

```csharp
// REVIEW [🔵 MINOR]: Double hash lookup → use TryGetValue instead of ContainsKey + indexer.
if (_cache.ContainsKey(key))
    return _cache[key];
```

## Batch Pattern

Same issue in N files → full comment on first, short ref on rest:

```
// REVIEW [🟡 MAJOR]: GetComponent in hot path (1 of 4) — cache in Awake.
```
```
// REVIEW [🟡 MAJOR]: Same as PlayerController:45 — cache GetComponent. (2 of 4)
```

## Rules

- One issue = one comment. Don't combine.
- 🔴/🟡 → full format. 🔵 → quick format OK.
- WHY: 1-3 bullets max. Evidence inline, not separate section.
- FIX: 1-3 concrete solutions. Code snippet only if non-obvious.
- Never comment without evidence. Investigate first.

## Advanced

For quality gates and false-positive detection, see:
- INLINE_COMMENT_FORMAT-patterns.md
- INLINE_COMMENT_FORMAT-checklist.md

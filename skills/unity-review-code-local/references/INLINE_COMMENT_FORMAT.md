# Inline Comment Format

Pro-grade review comments — highlight the problem, explain why, suggest the fix.

## Comment Template

**ALWAYS use this exact template structure:**

```
// ╔══════════════════════════════════════════════════════════════
// ║ REVIEW [SEVERITY]: Problem Title
// ╟──────────────────────────────────────────────────────────────
// ║ WHY:  [Root cause explanation — why this is dangerous]
// ║ WHERE: [Evidence — caller count, affected files, data flow]
// ║ FIX:  [Concrete actionable fix]
// ╚══════════════════════════════════════════════════════════════
```

Severity tokens: `🔴 CRITICAL` · `🟡 MAJOR` · `🔵 MINOR`

## Quick Format (1-2 line issues)

For simple, self-evident issues, use the compact single-line format:

```csharp
// ⚠ REVIEW [🔵 MINOR]: Double hash lookup → use TryGetValue instead of ContainsKey + indexer.
if (_cache.ContainsKey(key))
    return _cache[key];
```

## Full Format Examples

### 🔴 Critical — Crash / Data Loss / Security

```csharp
// ╔══════════════════════════════════════════════════════════════
// ║ REVIEW [🔴 CRITICAL]: Null reference after await
// ╟──────────────────────────────────────────────────────────────
// ║ WHY:  MonoBehaviour can be destroyed between yield points.
// ║       After any await, `this` may be null — accessing
// ║       members here crashes with MissingReferenceException.
// ║ WHERE: Called from 3 async paths:
// ║         → NetworkManager.cs:89 (on disconnect)
// ║         → UIController.cs:134 (on scene transition)
// ║         → GameLoop.cs:201 (on round end)
// ║ FIX:  Guard after await, or bind to destroyCancellationToken:
// ║
// ║       // Option A — guard:
// ║       await SomeAsyncOperation();
// ║       if (this == null) return;
// ║
// ║       // Option B — cancellation (preferred):
// ║       await SomeAsyncOperation()
// ║           .AttachExternalCancellation(destroyCancellationToken);
// ╚══════════════════════════════════════════════════════════════
await SomeAsyncOperation();
_health = 100; // ← accesses destroyed object
```

### 🟡 Major — Logic Bug / Missing Edge Case / State Corruption

```csharp
// ╔══════════════════════════════════════════════════════════════
// ║ REVIEW [🟡 MAJOR]: IndexOutOfRange on empty collection
// ╟──────────────────────────────────────────────────────────────
// ║ WHY:  `items[0]` assumes non-empty list, but 3 callers can
// ║       pass empty collections:
// ║         → InventoryManager.cs:45  (after filtering)
// ║         → ShopController.cs:112  (on empty shop)
// ║         → LootDrop.cs:78        (zero drop rate)
// ║ FIX:  Add empty guard before access:
// ║
// ║       if (items.Count == 0) return default;
// ╚══════════════════════════════════════════════════════════════
var first = items[0];
```

### 🔵 Minor — Optimization / Clarity / Defensive Coding

```csharp
// ╔══════════════════════════════════════════════════════════════
// ║ REVIEW [🔵 MINOR]: Repeated GetComponent in Update loop
// ╟──────────────────────────────────────────────────────────────
// ║ WHY:  GetComponent is O(n) per component count. Called every
// ║       frame at 60fps = 60 unnecessary lookups/sec.
// ║ FIX:  Cache in Awake/Start:
// ║
// ║       private Renderer _renderer;
// ║       void Awake() => _renderer = GetComponent<Renderer>();
// ╚══════════════════════════════════════════════════════════════
var r = GetComponent<Renderer>();
```


## Advanced & Quality Gates

For batch patterns, context-dependent severity, placement rules, Edit Tool usage, and the 5-gate quality checklist, see:
- INLINE_COMMENT_FORMAT-patterns.md
- INLINE_COMMENT_FORMAT-checklist.md

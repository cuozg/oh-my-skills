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

## Unity Lifecycle Example

```csharp
// ╔══════════════════════════════════════════════════════════════
// ║ REVIEW [🔴 CRITICAL]: Event leak — subscribe without unsubscribe
// ╟──────────────────────────────────────────────────────────────
// ║ WHY:  GameManager.OnGameStateChanged has 12 subscribers.
// ║       This subscribes in Awake but never unsubscribes.
// ║       On scene reload → old handler fires on destroyed
// ║       object → MissingReferenceException.
// ║ WHERE: grep found 0 matching -= in this file.
// ║ FIX:  Move += to OnEnable, add -= in OnDisable:
// ║
// ║       void OnEnable()  => GameManager.OnGameStateChanged += HandleStateChange;
// ║       void OnDisable() => GameManager.OnGameStateChanged -= HandleStateChange;
// ╚══════════════════════════════════════════════════════════════
GameManager.OnGameStateChanged += HandleStateChange;
```

## Concurrency / Async Example

```csharp
// ╔══════════════════════════════════════════════════════════════
// ║ REVIEW [🟡 MAJOR]: State race — coroutine vs Update
// ╟──────────────────────────────────────────────────────────────
// ║ WHY:  `_currentHealth` is set here in coroutine (line 45)
// ║       but read every frame in Update (line 78).
// ║       Between yield frames, Update sees partially-updated
// ║       value → health bar flickers, damage calc wrong.
// ║ FIX:  Apply health change atomically, or use a flag:
// ║
// ║       _isHealing = true;        // set before yield
// ║       _currentHealth = newVal;   // set after yield
// ║       _isHealing = false;        // Update checks flag
// ╚══════════════════════════════════════════════════════════════
_currentHealth += healAmount;
yield return new WaitForSeconds(tickInterval);
```

## Context-Dependent Severity

Some issues change severity based on execution frequency:

| Issue | In Update/FixedUpdate | In Init/Awake | In Editor Tool |
|:------|:---------------------|:--------------|:---------------|
| GetComponent call | 🔴 Critical | 🔵 Minor | 🔵 Minor |
| Allocation (`new`) | 🔴 Critical | 🟡 Major | 🔵 Minor |
| FindObjectOfType | 🟡 Major | 🔵 Minor | 🔵 Minor |
| String concat | 🔴 Critical | 🔵 Minor | 🔵 Minor |
| LINQ query | 🟡 Major | 🔵 Minor | 🔵 Minor |

## Batch Pattern — Same Issue, Multiple Locations

**First occurrence** — full box format:
```csharp
// ╔══════════════════════════════════════════════════════════════
// ║ REVIEW [🟡 MAJOR]: GetComponent in hot path (1 of 4)
// ╟──────────────────────────────────────────────────────────────
// ║ WHY:  O(n) lookup per frame. Same pattern at lines 32, 58,
// ║       91, 120 in this file.
// ║ FIX:  Cache all components in Awake:
// ║
// ║       private Renderer _renderer;
// ║       private Collider _collider;
// ║       void Awake() {
// ║           _renderer = GetComponent<Renderer>();
// ║           _collider = GetComponent<Collider>();
// ║       }
// ╚══════════════════════════════════════════════════════════════
var r = GetComponent<Renderer>();
```

**Subsequent occurrences** — compact back-reference:
```csharp
// ⚠ REVIEW [🟡 MAJOR]: Same as line 32 — cache GetComponent. (2 of 4)
var c = GetComponent<Collider>();
```

## Placement Rules

| Situation | Where to Place |
|:----------|:---------------|
| Single-line issue | Directly above the problematic line |
| Multi-line block | Above the first line of the block |
| Method-level issue | Above the method signature |
| Class-level issue | Above the class declaration |
| Missing code | At the location where code should exist |

## Using the Edit Tool

Insert comments using `edit` — **never** modify or delete the original code:

```
oldString: "    var first = items[0];"
newString: "    // ╔══════════════════════════════════════════════════════════════\n    // ║ REVIEW [🟡 MAJOR]: IndexOutOfRange on empty collection\n    // ╟──────────────────────────────────────────────────────────────\n    // ║ WHY:  items can be empty — 3 callers pass unfiltered lists.\n    // ║ FIX:  if (items.Count == 0) return default;\n    // ╚══════════════════════════════════════════════════════════════\n    var first = items[0];"
```

For quick format (minor/simple issues):
```
oldString: "    if (_cache.ContainsKey(key))"
newString: "    // ⚠ REVIEW [🔵 MINOR]: Double hash lookup → use TryGetValue instead.\n    if (_cache.ContainsKey(key))"
```

## Comment Quality Checklist

Every review comment MUST pass all 5 gates:

| Gate | Question |
|:-----|:---------|
| **PROBLEM** | Does the title clearly name the bug/risk? |
| **WHY** | Does it explain root cause, not just symptoms? |
| **EVIDENCE** | Does it cite callers, files, line numbers, or data flow? |
| **FIX** | Is the suggestion concrete code, not "consider refactoring"? |
| **SEVERITY** | Is the severity backed by evidence, not gut feeling? |

## What NOT to Do

- Don't modify actual code logic — only add comment lines
- Don't add comments for style/formatting issues
- Don't add comments without evidence (caller count, reproduction scenario)
- Don't combine multiple issues into one comment
- Don't add `// REVIEW:` to lines that have no issues
- Don't write paragraph-length WHY — keep each section 1-3 lines max
- Don't skip the FIX line — every problem needs an actionable solution

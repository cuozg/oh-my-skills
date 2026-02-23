# Inline Comment Format

Short comment explaining the issue → applied fix below. Evidence-backed.

## Severity Tokens

| Token | Meaning | When |
|:------|:--------|:-----|
| `🔴 CRITICAL` | Crash, data loss, security | Proven path to failure with evidence |
| `🟠 MAJOR` | Logic bug, silent failure | Trigger conditions identified |
| `🟡 MINOR` | Suboptimal, perf hint | Brief reason why suboptimal |

## Comment + Fix Format (🔴 / 🟠)

Comment explains the issue. Fix is applied directly below as real code.

```csharp
// ── REVIEW [🔴 CRITICAL] Null ref after await — MonoBehaviour may be destroyed
// WHY: `this` can be null between yield points (3 async callers)
// ── APPLIED FIX ──
await SomeAsyncOperation().AttachExternalCancellation(destroyCancellationToken);
```

```csharp
// ── REVIEW [🟠 MAJOR] IndexOutOfRange on empty collection
// WHY: `items[0]` assumes non-empty — 3 callers can pass empty
// ── APPLIED FIX ──
if (items.Count == 0) return default;
var first = items[0];
```

## Quick Format (🟡 Minor)

Comment + fix inline. One-liner when possible.

```csharp
// ── REVIEW [🟡 MINOR] Double hash lookup → use TryGetValue
// ── APPLIED FIX ──
if (_cache.TryGetValue(key, out var value)) return value;
```

## Comment-Only (when fix is too risky or ambiguous)

If the fix would change architecture or has multiple valid approaches, comment only — don't apply.

```csharp
// ── REVIEW [🟠 MAJOR] Shared SO mutated at runtime — changes persist across instances
// WHY: `_config` is a ScriptableObject, mutated by UpgradeShop:156, AIController:89
// FIX OPTIONS: (1) Clone in Awake (2) Use runtime data class instead
[SerializeField] private WeaponConfig _config;
```

## Batch Pattern

Same issue in N files → full comment+fix on first, short ref on rest:

```
// ── REVIEW [🟠 MAJOR] GetComponent in hot path (1 of 4) — cached in Awake
// ── REVIEW [🟠 MAJOR] Same as PlayerController:45 (2 of 4) — cached
```

## Common Anti-Patterns

| Pattern | Severity | Fix |
|:--------|:---------|:----|
| Subscribe without unsubscribe | 🔴 | Add OnDisable with -= |
| GetComponent in Update | 🔴 | Cache in Awake |
| Null deref after Destroy | 🔴 | Guard == null |
| Event leak (no -= in OnDisable) | 🔴 | Add -= via grep |
| String concat in Update | 🔴 | StringBuilder or SetText |
| Float == comparison | 🟠 | Mathf.Approximately |
| Magic numbers | 🟡 | Extract to const |

## Rules

- One issue = one comment block + one fix. Don't combine multiple issues.
- Comments are short: 1-2 lines max. No verbose trees.
- `// ── APPLIED FIX ──` marker before the changed code when replacing existing code.
- When adding new code (e.g., null guard), insert comment + code without the marker.
- 🔴/🟠 → comment + WHY line + applied fix. 🟡 → single-line comment + fix.
- Skip fix when: architectural change needed, multiple valid approaches, or risk of breaking behavior.
- Never comment without evidence. Investigate first.

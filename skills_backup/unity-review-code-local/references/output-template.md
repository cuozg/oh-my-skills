# Inline Comment Format

Short comment explaining the issue. Fix delegated to `unity-code-quick`. Evidence-backed.

## Severity Tokens (per common-rules.md)

| Token | Meaning | When |
|:------|:--------|:-----|
| `🔴 Critical` | Crash, data loss, security | Proven path to failure with evidence |
| `🟡 Major` | Logic bug, silent failure | Trigger conditions identified |
| `🔵 Minor` | Suboptimal, perf hint | Brief reason why suboptimal |
| `🟢 Nit` | Style, typo, micro-optimization | Brief note |

## Comment + Delegate Format (🔴 / 🟡)

Reviewer inserts comment only. Fix is delegated to `unity-code-quick` background task.

```csharp
// ── REVIEW [🔴 Critical] Null ref after await — MonoBehaviour may be destroyed
// WHY: `this` can be null between yield points (3 async callers)
// FIX: Use destroyCancellationToken — await SomeAsyncOperation().AttachExternalCancellation(destroyCancellationToken);
```

```csharp
// ── REVIEW [🟡 Major] IndexOutOfRange on empty collection
// WHY: `items[0]` assumes non-empty — 3 callers can pass empty
// FIX: Guard with if (items.Count == 0) return default; before access
```

## Quick Format (🔵 Minor)

Comment + fix description inline. One-liner when possible. No delegation — too minor for a background task.

```csharp
// ── REVIEW [🔵 Minor] Double hash lookup → use TryGetValue
// FIX: Replace ContainsKey+index with TryGetValue
```

## Minimal Format (🟢 Nit)

Comment only. No fix applied — too minor or purely stylistic.

```csharp
// ── REVIEW [🟢 Nit] Magic number → extract to const for readability
```

## Comment-Only (when fix is too risky or ambiguous)

If the fix would change architecture or has multiple valid approaches, comment only — don't apply.

```csharp
// ── REVIEW [🟡 Major] Shared SO mutated at runtime — changes persist across instances
// WHY: `_config` is a ScriptableObject, mutated by UpgradeShop:156, AIController:89
// FIX OPTIONS: (1) Clone in Awake (2) Use runtime data class instead
```

## Batch Pattern

Same issue in N files → full comment on first, short ref on rest:

```
// ── REVIEW [🟡 Major] GetComponent in hot path (1 of 4) — cache in Awake
// ── REVIEW [🟡 Major] Same as PlayerController:45 (2 of 4)
```

## Common Anti-Patterns

| Pattern | Severity | Fix |
|:--------|:---------|:----|
| Subscribe without unsubscribe | 🔴 Critical | Add OnDisable with -= |
| Null deref after Destroy | 🔴 Critical | Guard == null |
| GetComponent in Update | 🟡 Major | Cache in Awake |
| String concat in Update | 🟡 Major | StringBuilder or SetText |
| Event leak (no -= in OnDisable) | 🟡 Major | Add -= via grep |
| Float == comparison | 🟡 Major | Mathf.Approximately |
| Magic numbers | 🟢 Nit | Extract to const |

## Rules

- One issue = one comment block. Don't combine multiple issues.
- Comments are short: 1-2 lines max. No verbose trees.
- 🔴/🟡 → comment + WHY line + FIX description. Actual fix delegated to `unity-code-quick`.
- 🔵 → single-line comment + FIX description. No delegation — user applies if desired.
- 🟢 → comment only. No fix needed.
- Skip delegation when: architectural change needed, multiple valid approaches, or risk of breaking behavior — use FIX OPTIONS instead.
- Never comment without evidence. Investigate first.
- **Reviewer never applies code fixes directly.** All fixes go through `unity-code-quick`.

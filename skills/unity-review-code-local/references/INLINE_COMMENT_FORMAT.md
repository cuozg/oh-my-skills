# Inline Comment Format

Short comment explaining the issue. Fix delegated to `unity-code-quick`. Evidence-backed.

## Severity Tokens

| Token | Meaning | When |
|:------|:--------|:-----|
| `🔴 CRITICAL` | Crash, data loss, security | Proven path to failure with evidence |
| `🟡 HIGH` | Logic bug, silent failure | Trigger conditions identified |
| `🔵 MEDIUM` | Suboptimal, perf hint | Brief reason why suboptimal |
| `🟢 LOW` | Style, typo, micro-optimization | Brief note |

## Comment + Delegate Format (🔴 / 🟡)

Reviewer inserts comment only. Fix is delegated to `unity-code-quick` background task.

```csharp
// ── REVIEW [🔴 CRITICAL] Null ref after await — MonoBehaviour may be destroyed
// WHY: `this` can be null between yield points (3 async callers)
// FIX: Use destroyCancellationToken — await SomeAsyncOperation().AttachExternalCancellation(destroyCancellationToken);
```

```csharp
// ── REVIEW [🟡 HIGH] IndexOutOfRange on empty collection
// WHY: `items[0]` assumes non-empty — 3 callers can pass empty
// FIX: Guard with if (items.Count == 0) return default; before access
```

## Quick Format (🔵 Medium)

Comment + fix description inline. One-liner when possible.

```csharp
// ── REVIEW [🔵 MEDIUM] Double hash lookup → use TryGetValue
// FIX: Replace ContainsKey+index with TryGetValue
```

## Minimal Format (🟢 Low)

Comment only. No fix applied — too minor or purely stylistic.

```csharp
// ── REVIEW [🟢 LOW] Magic number → extract to const for readability
```

## Comment-Only (when fix is too risky or ambiguous)

If the fix would change architecture or has multiple valid approaches, comment only — don't apply.

```csharp
// ── REVIEW [🟡 HIGH] Shared SO mutated at runtime — changes persist across instances
// WHY: `_config` is a ScriptableObject, mutated by UpgradeShop:156, AIController:89
// FIX OPTIONS: (1) Clone in Awake (2) Use runtime data class instead
```

## Batch Pattern

Same issue in N files → full comment on first, short ref on rest:

```
// ── REVIEW [🟡 HIGH] GetComponent in hot path (1 of 4) — cache in Awake
// ── REVIEW [🟡 HIGH] Same as PlayerController:45 (2 of 4)
```

## Common Anti-Patterns

| Pattern | Severity | Fix |
|:--------|:---------|:----|
| Subscribe without unsubscribe | 🔴 | Add OnDisable with -= |
| GetComponent in Update | 🔴 | Cache in Awake |
| Null deref after Destroy | 🔴 | Guard == null |
| Event leak (no -= in OnDisable) | 🔴 | Add -= via grep |
| String concat in Update | 🔴 | StringBuilder or SetText |
| Float == comparison | 🟡 | Mathf.Approximately |
| Magic numbers | 🟢 | Extract to const |

## Rules

- One issue = one comment block. Don't combine multiple issues.
- Comments are short: 1-2 lines max. No verbose trees.
- 🔴/🟡 → comment + WHY line + FIX description. Actual fix delegated to `unity-code-quick`.
- 🔵 → single-line comment + FIX description. Delegated to `unity-code-quick`.
- 🟢 → comment only. No fix needed.
- Skip delegation when: architectural change needed, multiple valid approaches, or risk of breaking behavior — use FIX OPTIONS instead.
- Never comment without evidence. Investigate first.
- **Reviewer never applies code fixes directly.** All fixes go through `unity-code-quick`.

# Logic Review Patterns — Unity C# (Part 3c)

Edge Cases, Minor Issues, and Suggestion Quality guidelines.

---

## 12. Edge Case Checklist

Run against EVERY changed method:

| Question | If Yes → |
|:---------|:---------|
| What if this is called with null? | Add guard or document `[NotNull]` contract |
| What if the collection is empty? | Check `.Count`/`.Any()` before `.First()`/`[0]` |
| What if this is called twice? | Is it idempotent? Does double-subscribe happen? |
| What if this is called before Init? | Add initialization guard or lazy init |
| What if this is called after Destroy? | Check `this != null` / `isActiveAndEnabled` |
| What if the value is negative? | Check unsigned assumption, add `Mathf.Max(0, ...)` |
| What if the value is MAX_INT? | Check overflow in arithmetic |
| What if two of these run concurrently? | Check shared state, add synchronization if needed |
| What if the network/file operation fails? | Check error handling path exists |
| What if the referenced object was destroyed? | Check for null/MissingReferenceException |

---

## 13. Minor Issues

Magic numbers, Debug.Log without `#if UNITY_EDITOR`, empty Update/Start, dead code, naming violations, nesting 4+, missing XML docs on public API, `#region` blocks (remove — use partial classes or extract), unnecessary `this.` qualifier.

---

## Suggestion Quality — DO / DON'T

**DO**: Provide exact replacement code in ` ```suggestion ``` `. One issue per comment. Show evidence (caller count, file:line). Explain *why*, not just *what*.

**DON'T**: Combine multiple fixes in one suggestion. Suggest style-only changes as Critical/Major. Flag patterns without grepping for evidence. Suggest rewrites > 20 lines inline (use `<details>` block).

---

## Investigation Commands (Part 3)

```bash
# Serialization refs in prefabs/assets
grep -rn "TypeName" Assets/ --include="*.prefab" --include="*.asset"

# Enum switch/case usage
grep -rn "EnumType" Assets/Scripts/ --include="*.cs" | grep -E "switch|case"

# State mutations of a field
grep -rn "_fieldName\s*=" Assets/Scripts/ --include="*.cs"

# Catch-all exception handlers
grep -rn "catch\s*(Exception" Assets/Scripts/ --include="*.cs"

# Division operations (check for zero guards)
grep -rn "[^/]/[^/\*=]" Assets/Scripts/ --include="*.cs"
```

**See also:** `logic-review-patterns.md` (Part 1) for Performance & Lifecycle, `logic-review-patterns-intermediate.md` (Part 2) for Serialization, Control Flow, Logic, State Management.

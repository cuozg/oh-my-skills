# Inline Comment Format - Quality Checklist & Review Patterns

## Common Anti-Patterns to Watch

| Pattern | Severity | Fix |
|:---|:---|:---|
| Subscribe without unsubscribe | 🔴 Critical | Add OnDisable with matching -= |
| GetComponent in Update | 🔴 Critical | Cache in Awake |
| Null deref after Destroy | 🔴 Critical | Check == null or use null-coalescing |
| Magic numbers | 🔵 Minor | Extract to const with semantic name |
| Event leak | 🔴 Critical | Verify -= in OnDisable (use grep) |
| Missing [RequireComponent] | 🔵 Minor | Add attribute |
| Float comparison == | 🟡 Major | Use Mathf.Approximately(a, b) |

## When NOT to Add Review Comments

- Style/formatting issues (handled by linters)
- Naming suggestions without logic impact
- "Consider refactoring" without concrete cause
- Code that's already self-documenting
- Comments on test-only code with no production impact

## Template Variations by Severity

**🔴 Critical** — Full box, always include WHERE with evidence
**🟡 Major** — Full box, evidence required
**🔵 Minor** — OK to use compact single-line format

## Multi-File Coordination

When same issue appears 4+ times, mention batch in first comment:
```
// ⚠ REVIEW [🟡 MAJOR]: GetComponent in hot path (1 of 4)
```

Then on subsequent ones:
```
// ⚠ REVIEW [🟡 MAJOR]: Same as line X — cache GetComponent. (2 of 4)
```

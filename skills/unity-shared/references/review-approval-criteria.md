# Approval Criteria

Decision tree for review verdict. Severity tiers map to GitHub review events.

## Decision Tree

```
Has CRITICAL issue?  ──yes──▶  🔴 REQUEST_CHANGES (block merge)
        │ no
Has HIGH issue?      ──yes──▶  🟡 REQUEST_CHANGES
        │ no
Has MEDIUM issue?    ──yes──▶  🔵 COMMENT (allow merge)
        │ no
Has LOW issue?       ──yes──▶  🟢 APPROVE (with suggestions)
        │ no
Clean                ──────▶  ✅ APPROVE
```

## Severity Classification

### 🔴 Critical — Block Merge

**Security**: Secrets in code, SQL/command injection, XSS, auth bypass, unvalidated deserialization.
**Stability**: NullReferenceException on common paths, data corruption, infinite loops, memory leaks in Update/FixedUpdate.
**Breaking**: Removed/renamed public API used by other assemblies, changed serialized field names/types (data loss), broken prefab references, DB schema changes without migration.
**Unity Runtime**: Addressables loaded without release tracking, infinite coroutine without stop condition, UI Canvas rebuild every frame in production, unguarded division-by-zero on common execution paths.

### 🟡 High — Request Changes

**Logic**: Incorrect conditional logic, off-by-one in loops, race conditions in async/coroutine, unhandled edge cases that cause silent failures.
**Testing**: No tests for new public API, removed test coverage for modified code.
**Architecture**: Violates established project patterns (e.g., bypassing event system with direct coupling), circular dependencies between assemblies.
**Reliability**: Missing null-propagation in long call chains, event handler not removed causing memory pressure, Addressable label mismatch between code and groups.

### 🔵 Medium — Comment (Allow Merge)

**Quality**: God class (>500 lines), deep nesting (>4 levels), duplicated logic across files, magic numbers without constants, empty catch blocks.
**Performance**: Avoidable allocations in hot paths, LINQ in Update, unnecessary GetComponent calls, suboptimal algorithm (O(n²) where O(n) is trivial).
**Conventions**: Inconsistent naming, missing XML docs on public API, non-standard file/folder structure.
**Unity Hygiene**: `FindObjectOfType` used outside init/bootstrap paths, missing `[Tooltip]` on public inspector fields, inconsistent enum naming style (PascalCase vs SCREAMING_CASE).

### 🟢 Low — Approve with Suggestions

**Style**: Formatting preferences, comment wording, variable name alternatives, import ordering.
**Minor optimization**: Micro-optimizations with negligible impact, suggested but not required refactors.
**Documentation**: Typos in comments, slightly better doc phrasing.

## Edge Cases

- **Mixed severities** → Highest severity wins for the review event. All issues still get inline comments.
- **Pre-existing issues** → Only flag if the PR makes them worse or touches the affected code. Note: "Pre-existing, surfaced by this change."
- **Partial fix is OK** → If a PR fixes 3 of 5 issues, approve the fix. File a follow-up for the remaining 2.
 **Unity-specific references take precedence** → `unity-shared` logic review patterns, PREFAB_REVIEW, ASSET_REVIEW checklists override generic guidance when they conflict.

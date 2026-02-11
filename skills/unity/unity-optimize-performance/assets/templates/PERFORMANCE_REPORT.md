# Performance Report: {FEATURE_OR_AREA}

**Date**: {YYYY-MM-DD}
**Scope**: {Scripts | Graphics | Memory | Full Audit}
**Status**: {Optimized | Partially Optimized | Investigating}

---

## 1. Baseline

| Metric | Value |
|--------|-------|
| Scene object count | {N} |
| High-frequency log entries | {N} |
| Target platform | {e.g., iOS / Android / WebGL} |

---

## 2. Issues Found

### Critical (Must Fix)

| # | File | Line | Pattern | Impact | Fix |
|---|------|------|---------|--------|-----|
| 1 | `{file}` | {line} | {e.g., GetComponent in Update} | {e.g., Per-frame allocation} | {e.g., Cache in Awake} |

### Warning (Should Fix)

| # | File | Line | Pattern | Impact | Fix |
|---|------|------|---------|--------|-----|
| 1 | `{file}` | {line} | {pattern} | {impact} | {fix} |

### Info (Consider)

| # | File | Line | Pattern | Suggestion |
|---|------|------|---------|------------|
| 1 | `{file}` | {line} | {pattern} | {suggestion} |

---

## 3. Fixes Applied

| # | File | Change | Before | After |
|---|------|--------|--------|-------|
| 1 | `{file}` | {description} | `{old code}` | `{new code}` |

---

## 4. Validation

| Check | Result |
|-------|--------|
| Compile | {Pass/Fail} |
| Play Mode test | {Pass/Fail} |
| Visual regression | {None/Issues found} |
| Frame timing | {Improved/Same/Degraded} |

---

## 5. Summary

| Severity | Found | Fixed | Remaining |
|----------|-------|-------|-----------|
| Critical | {N} | {N} | {N} |
| Warning | {N} | {N} | {N} |
| Info | {N} | {N} | {N} |

**Recommendations**: {Next steps if any remain}

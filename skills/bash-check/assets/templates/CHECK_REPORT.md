# Bash Check Report: {SCRIPT_NAME}

**Script**: `{/path/to/script.sh}`
**Date**: {YYYY-MM-DD}
**Shell**: {bash version}
**Status**: {Pass | Pass with Warnings | Fail}

---

## 1. Syntax Validation

| Check | Result | Details |
|-------|--------|---------|
| `bash -n` | {Pass/Fail} | {Error message if any} |
| ShellCheck | {Pass/Warnings/Errors/N/A} | {Summary} |

---

## 2. Findings

### Errors (Script will fail)

| # | Line | Issue | Fix |
|---|------|-------|-----|
| 1 | {line} | {description} | {suggested fix} |

### Warnings (Potential runtime issues)

| # | Line | Issue | Fix |
|---|------|-------|-----|
| 1 | {line} | {description} | {suggested fix} |

### Info (Style / best practice)

| # | Line | Issue | Suggestion |
|---|------|-------|------------|
| 1 | {line} | {description} | {suggestion} |

---

## 3. Manual Review Checklist

- [ ] Shebang line present and correct
- [ ] Variables properly quoted
- [ ] Exit codes handled
- [ ] File operations guarded
- [ ] Portability verified (if required)

---

## 4. Summary

| Severity | Count |
|----------|-------|
| Errors | {N} |
| Warnings | {N} |
| Info | {N} |

**Verdict**: {Pass / Fail with N errors requiring fixes}

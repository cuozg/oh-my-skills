# Squash Plan: {BRANCH_NAME}

**Date**: {YYYY-MM-DD}
**Total Commits**: {N}
**Target Commits**: {N groups}

---

## 1. Commit Groups

### Group 1: {Group Name}

**Target Message**: `{type}({scope}): {short summary}`
**Commits**:
- `{hash}`: {original message}
- `{hash}`: {original message}

### Group 2: {Group Name}

**Target Message**: `{type}({scope}): {short summary}`
**Commits**:
- `{hash}`: {original message}

### Discarded (reverts / superseded)

- `{hash}`: {original message} — Reason: {e.g., reverted by hash2}

---

## 2. Squash Strategy

| Group | Method | Commits | Target Message |
|-------|--------|---------|----------------|
| {Group 1} | {squash/fixup} | {N} | `{type}({scope}): {summary}` |
| {Group 2} | {squash/fixup} | {N} | `{type}({scope}): {summary}` |

---

## 3. Final Commit Messages

### Commit 1

```
{type}({scope}): {short summary}

## High Level Summary

{2-3 sentence overview}

## Specific Details

### Changes Made
- {File}: {Change description}

Squashed from:
- {hash}: {original message}
- {hash}: {original message}
```

---

## 4. Safety Checklist

- [ ] Backup branch created
- [ ] User approved grouping
- [ ] No pending uncommitted changes
- [ ] Target branch verified
- [ ] Tests pass after squash
- [ ] Git log confirms structure

# Squash Plan: {BRANCH_NAME}

**Date**: {YYYY-MM-DD} | **Total**: {N} commits → {N} groups

## Commit Groups

### Group 1: {Group Name}
`{type}({scope}): {short summary}`
- `{hash}`: {original message}

### Discarded
- `{hash}`: {reason}

## Strategy

| Group | Method | Commits | Target Message |
|-------|--------|---------|----------------|
| {Group 1} | {squash/fixup} | {N} | `{type}({scope}): {summary}` |

## Final Messages

```
{type}({scope}): {short summary}

{2-3 sentence overview}

Squashed from:
- {hash}: {original message}
```

## Safety

- [ ] Backup branch created + user approved
- [ ] No pending changes, target branch verified
- [ ] Tests pass + git log confirmed

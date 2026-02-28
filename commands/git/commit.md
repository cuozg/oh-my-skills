---
description: Generate clean commit messages and commit changes
agent: sisyphus
subtask: true
---
Use skill git-commit to commit $ARGUMENTS

# Git Commit — Workflow & Template

## Commit Message Format

```
<type>: <subject>

<body (optional, bullet points)>
```

**Types**: `feat` | `fix` | `refactor` | `docs` | `chore` | `test` | `perf` | `style`

**Subject**: ≤50 chars, imperative mood, lowercase, no period.
**Body**: What/why (not how), bullets, wrap 72 chars, blank line after subject.

## Workflow

1. **Analyze**: `git diff --stat` / `git diff --cached --stat` / `git status`
2. **Generate**: Identify type → write subject (<50 chars) → body if complex
3. **Commit**: `git add <files>` → `git commit -m "type: subject" -m "body"`
4. **Verify**: `git log --oneline -1`

## Examples

```
fix: resolve null reference in PlayerManager initialization
```

```
feat: add daily boss event handler system

- Implement BaseHUDEventHandler subclass for Daily Boss events
- Extend HUDEventBus to route new event types
- Add unit tests for handler initialization and event dispatch
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| "Fixed stuff" | `fix: resolve null reference in PlayerManager` |
| "WIP" or "test" | `feat: add daily boss notification system` |
| `Co-authored-by: Claude AI` | (no metadata) |

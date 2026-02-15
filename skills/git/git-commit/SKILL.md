---
name: git-commit
description: "Generate clean, meaningful git commit messages based on code changes or user request. Commits to current branch with no AI metadata (no co-author, committer info, or tool attribution). Messages are short, concise, use bullet points for multiple changes. Triggers: 'commit changes', 'generate and commit', 'commit with message', 'commit this', 'stage and commit'."
---

# Git Commit

## Input

File changes (via `git diff`) or explicit user description. Optional: commit scope, branch name for safety check.

## Commit Message Format

```
<type>: <subject>

<body (optional, bullet points)>
```

**Types**: `feat` | `fix` | `refactor` | `docs` | `chore` | `test` | `perf` | `style`

**Subject**: ≤50 chars, imperative mood, lowercase, no period.
**Body**: What/why (not how), bullets, wrap 72 chars, blank line after subject.

## Restrictions

- **NEVER** add co-author, committer, or AI tool metadata
- **NEVER** push to remote — only commit locally
- **NEVER** include code snippets in message
- **DO** use imperative mood, bullet points, verify branch first

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

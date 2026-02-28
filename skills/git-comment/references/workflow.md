# Git Comment — Workflow

## Commit Message Format

```
<type>: <subject>

- <bullet 1: most important change>
- <bullet 2: next important change>
- ...
```

**Types**: `feat` | `fix` | `refactor` | `docs` | `chore` | `test` | `perf` | `style`

**Subject**: imperative mood, lowercase, no period, ≤50 chars.
**Body**: bullet points only, highlight **what changed and why**, skip trivial changes. Wrap at 72 chars.

## Workflow Steps

1. **Read last commit**
   - `git log -1 --format='%H %s'` — hash and current subject
   - `git log -1 --format='%an %ae'` — verify commit author (safety check)

2. **Get the diff**
   - `git diff HEAD~1..HEAD --stat` — overview of changed files
   - `git diff HEAD~1..HEAD` — full diff for analysis
   - For merge commits: `git diff HEAD~1..HEAD -m --first-parent`

3. **Investigate changes**
   - Group changes by system/module
   - Identify **purpose**: new feature, bug fix, refactor, etc.
   - Note most impactful changes — prioritize logic/behavioral changes over cosmetic
   - Flag breaking changes, new dependencies, risky modifications

4. **Generate message**
   - Pick correct `<type>` from diff analysis
   - Write concise subject line (<50 chars, imperative mood)
   - Add bullet points for each meaningful change (bold file/class names)
   - Skip trivial: formatting, whitespace, import reordering
   - Keep total body to 3-7 bullets max

5. **Amend the commit**
   - `git commit --amend -m "<type>: <subject>" -m "<body bullets>"`
   - Verify: `git log -1 --format='%B'`

## Example

**Before**: `wip stuff`

**After**:
```
feat: add daily boss event handler system

- **BaseHUDEventHandler**: implement subclass for Daily Boss events
- **HUDEventBus**: extend routing for new event types
- **DailyBossTests**: add unit tests for handler init and dispatch
- Remove deprecated notification fallback path
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| Keep "wip" message as-is | Amend with descriptive message |
| Include full code blocks | Use bullet summaries |
| 20+ bullet points | 3-7 focused bullets |
| "Updated files" | `fix: resolve null ref in PlayerManager init` |

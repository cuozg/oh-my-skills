---
name: git-comment
description: "Generate and apply concise commit messages for the last commit on the current local branch. Read the latest commit's diff, investigate code changes, generate a short bullet-point message highlighting important changes, and amend the commit with the new message. Never push to remote — local only. This skill should be used when: (1) last commit has a poor or placeholder message, (2) user says 'comment this commit', (3) 'generate commit message', (4) 'describe last commit', (5) 'amend commit message', (6) 'annotate commit', (7) 'fix commit message'."
---

# Git Comment

## Input

No input required — operates on the last commit of the current branch. Optional: specific commit hash.

## Output

The last commit's message is amended with a generated message. Nothing is pushed.

## Commit Message Format

```
<type>: <subject>

- <bullet 1: most important change>
- <bullet 2: next important change>
- ...
```

**Types**: `feat` | `fix` | `refactor` | `docs` | `chore` | `test` | `perf` | `style`

**Subject**: imperative mood, lowercase, no period, ≤50 chars.
**Body**: bullet points only, highlight **what changed and why**, skip trivial changes (whitespace, imports-only). Wrap at 72 chars.

## Workflow

1. **Read last commit**
   - `git log -1 --format='%H %s'` — get hash and current subject
   - `git log -1 --format='%an %ae'` — verify commit author (safety check)

2. **Get the diff**
   - `git diff HEAD~1..HEAD --stat` — overview of changed files
   - `git diff HEAD~1..HEAD` — full diff for analysis
   - For merge commits: `git diff HEAD~1..HEAD -m --first-parent`

3. **Investigate changes**
   - Group changes by system/module
   - Identify the **purpose**: new feature, bug fix, refactor, etc.
   - Note the most impactful changes — prioritize logic/behavioral changes over cosmetic
   - Flag breaking changes, new dependencies, risky modifications

4. **Generate message**
   - Pick the correct `<type>` from the diff analysis
   - Write a concise subject line (<50 chars, imperative mood)
   - Add bullet points for each meaningful change (bold file/class names)
   - Skip trivial: formatting, whitespace, import reordering
   - Keep total body to 3-7 bullets max

5. **Amend the commit**
   - `git commit --amend -m "<type>: <subject>" -m "<body bullets>"`
   - Verify: `git log -1 --format='%B'`

## Restrictions

- **NEVER** push to remote — amend locally only
- **NEVER** add co-author, committer, or AI tool metadata
- **NEVER** include code snippets in the message
- **NEVER** amend if the commit has already been pushed (check: `git status` for "ahead")
- **DO** verify the commit is not a merge commit from remote before amending
- **DO** warn the user if the commit appears to belong to someone else

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

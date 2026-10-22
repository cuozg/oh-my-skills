# squash-workflow.md

## Identify Commits to Squash

```bash
# List all commits since base branch
git log --oneline origin/main..HEAD

# View full diff of branch
git diff origin/main...HEAD
```

## Grouping Strategy

Cluster by logical concern:
- `feat:` — new feature code
- `fix:` — bug fixes
- `test:` — test additions
- `refactor:` — restructuring without behavior change
- `docs:` — comments, README
- `chore:` — config, tooling, CI

Each group becomes one squashed commit.

## Interactive Rebase

```bash
# Rebase last N commits
git rebase -i HEAD~N

# Rebase from base branch
git rebase -i origin/main
```

## Rebase Editor Markers

```
pick abc1234 First commit       ← keep as-is (topmost = base)
squash def5678 Second commit    ← merge into previous, combine messages
fixup ghi9012 Third commit      ← merge into previous, discard message
reword jkl3456 Fourth commit    ← keep alone, rewrite its message
```

## After Rebase

```bash
# Force-push only if branch is yours and not shared
git push --force-with-lease origin {branch}

# Verify result
git log --oneline origin/main..HEAD
```

## Safety Rules

- Never squash pushed commits on shared branches without team agreement
- Use `--force-with-lease` not `--force` — rejects if remote moved
- Always show the plan to the user before executing

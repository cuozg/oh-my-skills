---
name: git-rebase
description: Use when rebasing current branch onto a target branch, especially when the working tree has uncommitted changes, the local target ref may be behind its remote, or the rebase risks conflicts that need user review.
---

# Git Rebase

## Overview

Safely rebase the current branch onto a target branch. Stash WIP first, refresh the target ref, replay the current branch's commits on top, then restore the stash. Pause and report on any conflict — never auto-resolve.

## When to Use

- User asks to rebase current branch onto another branch
- The working tree has uncommitted changes that must survive the rebase
- The target is a local branch that may be behind its remote
- A rebase is needed and there is risk of conflicts

When NOT to use:

- User wants to merge, not rebase
- The target IS the current branch (no-op)
- The rebase is part of `git pull --rebase` (single command, not this workflow)
- User is on a detached HEAD (confirm first)

## The Workflow

Verify each step before moving on. Stop and report on any conflict.

### 1. Capture context

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $CURRENT_BRANCH"
```

If the output is `HEAD` (detached), stop and confirm with the user.

### 2. Stash WIP if dirty

```bash
if [ -n "$(git status --short)" ]; then
  git stash push -u -m "wip before rebase onto $TARGET"
fi
```

`-u` includes untracked files. The message names the target so the stash is identifiable later.

### 3. Verify clean tree

```bash
git status --short
```

Must be empty. If not, something unexpected is staged (submodule, ignored file, intent-to-add) — stop and investigate.

### 4. Update the target ref

```bash
git fetch origin
git checkout "$TARGET"
git pull --ff-only
```

`--ff-only` matters: never let `git pull` create a merge commit on a branch you don't own.

If the target has no remote tracking branch, skip `fetch` and `pull`:

```bash
git checkout "$TARGET"
```

### 5. Return to the original branch

```bash
git checkout "$CURRENT_BRANCH"
```

### 6. Rebase

```bash
git rebase "$TARGET"
```

### 7. Handle conflicts (if any)

If `git rebase` stops with conflicts:

- **Do not** run `git rebase --continue` blindly
- **Do not** run `git rebase --skip` (silently drops the user's commits)
- **Do not** auto-resolve with `--ours` / `--theirs` (loses changes)
- Report:
  - The list of conflicted files
  - `git status` output
  - The choices: `git rebase --abort` to back out, or resolve manually then `git rebase --continue`
- The stash is still safely in the stash list — aborting does not lose WIP

### 8. Pop the stash

```bash
git stash pop
```

If the pop has conflicts (the rebase touched the same lines the WIP touched), report and **do not** run `git stash drop` — the stash entry is preserved on conflict, dropping it would lose the WIP.

### 9. Report final state

- New HEAD SHA
- Number of commits replayed
- Working tree state (clean / dirty / conflicted)
- Whether WIP was restored cleanly

## Common Mistakes

| Mistake | Why it's wrong | Do this instead |
|---|---|---|
| `git rebase` with uncommitted changes | Fails with "your local changes would be overwritten" | Stash first (step 2) |
| Rebase onto a stale local ref | Misses commits on the remote target | `fetch` + `pull --ff-only` on the target (step 4) |
| `git pull` (without `--ff-only`) on target | Can create an unwanted merge commit on the target | Always `--ff-only` |
| `git rebase --skip` to "resolve" conflicts | Silently drops the user's commits | Pause and ask |
| `git stash drop` after a conflicted pop | Loses the user's WIP | Leave the stash entry; ask the user |
| `git rebase --continue` with unmerged paths | Re-breaks the rebase | Resolve first, stage, then `--continue` |
| `git push --force` after the rebase | Destroys remote history | `--force-with-lease` (only if user asks) |

## Variations

### Working tree already clean

Skip steps 2 and 8. Note it in the report.

### Target has no remote

Skip `fetch` and `pull` in step 4. Just checkout.

### Target is the current branch

No-op. Tell the user and stop.

### Detached HEAD

Stop and ask. Don't rebase from a detached HEAD without explicit confirmation.

### Conflicts during BOTH rebase AND stash pop

Resolve rebase conflicts first (`git rebase --continue`). Then the stash pop conflicts are independent — report both states.

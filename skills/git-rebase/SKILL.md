---
name: git-rebase
description: Use when rebasing current branch onto a target branch, especially when the working tree has uncommitted changes, the local target ref may be behind its remote, or the rebase risks conflicts that need user review.
---

# Git Rebase

## Overview

Safely rebase the current branch onto a target branch — always onto `origin/<target>`, never the local target. Stash WIP first, fetch the remote ref, replay the current branch's commits on top of the server's true state, then restore the stash. Pause and report on any conflict — never auto-resolve.

## When to Use

- User asks to rebase current branch onto another branch
- The working tree has uncommitted changes that must survive the rebase
- The local target ref is likely behind the server, so rebasing onto the local target would replay commits you don't own as yours
- A rebase is needed and there is risk of conflicts

When NOT to use:

- User wants to merge, not rebase
- The target IS the current branch (no-op)
- The rebase is part of `git pull --rebase` (single command, not this workflow)
- User is on a detached HEAD (confirm first)

## Rules

- **NEVER add a `Co-Authored-By` trailer** to any commit message during the rebase — not on `--continue`, not on a `reword`/`squash` step of an interactive rebase, not when committing a conflict fix. The original commit's author stays the sole author.
- **Keep the origin commit intact.** Do not rewrite the author (forbid `--reset-author`), do not edit the original commit message, do not append trailers or footers. Use `GIT_EDITOR=true` on `--continue` to force the original message through unchanged if the editor would otherwise open.
- **Always rebase onto `origin/<target>`, never onto the local `<target>`.** This prevents Git from misinterpreting and absorbing commits that landed on the remote but are not yet reflected locally as yours. If you rebase against a stale local target, Git may replay commits authored by others as if they were part of your branch.

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

### 4. Fetch the target ref from the server

```bash
git fetch origin "$TARGET"
```

This updates `origin/<target>` to the server's true state. Do **not** checkout or `pull --ff-only` the local target — that risks merging other people's commits into your local view and can mislead the rebase into treating them as yours.

If the target has no remote (rare):

```bash
# Skip the fetch; you will rebase onto the local "$TARGET" in step 6.
```

### 5. Confirm you are on the original branch

```bash
git rev-parse --abbrev-ref HEAD
```

Must equal `$CURRENT_BRANCH` from step 1. If you ever left it, switch back:

```bash
git checkout "$CURRENT_BRANCH"
```

### 6. Rebase onto the server's state

```bash
git rebase "origin/$TARGET"
```

Rebasing onto `origin/<target>` (not the local target) guarantees you replay your branch on top of the actual server history. By default, original commit messages, authors, and bodies are preserved verbatim. Do not pass flags that rewrite either.

If the target has no remote, use the local ref instead:

```bash
git rebase "$TARGET"
```

### 7. Handle conflicts (if any)

If `git rebase` stops with conflicts:

- **Do not** run `git rebase --continue` blindly
- **Do not** run `git rebase --skip` (silently drops the user's commits)
- **Do not** auto-resolve with `--ours` / `--theirs` (loses changes)
- **Do not** use `git commit --reset-author` (replaces the original author)
- After staging the resolution, continue with the original message preserved — no editor, no trailer:

  ```bash
  GIT_EDITOR=true git rebase --continue
  ```

- Report:
  - The list of conflicted files
  - `git status` output
  - The choices: `git rebase --abort` to back out, or resolve manually then `GIT_EDITOR=true git rebase --continue`
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
| Rebase onto a stale local target ref | Git may replay commits authored by others as if they were yours (the "bốc commit của người khác" problem) | `git fetch origin "$TARGET"` then `git rebase "origin/$TARGET"` (steps 4 + 6) |
| `git pull` (without `--ff-only`) on target | Can create an unwanted merge commit on the target and pollute your local view | Skip the local pull entirely; use `origin/<target>` |
| `git rebase --skip` to "resolve" conflicts | Silently drops the user's commits | Pause and ask |
| `git stash drop` after a conflicted pop | Loses the user's WIP | Leave the stash entry; ask the user |
| `git rebase --continue` with unmerged paths | Re-breaks the rebase | Resolve first, stage, then `--continue` |
| `git commit --reset-author` during rebase | Replaces the original author; pollutes provenance | Never; keep the original author intact |
| `git rebase --continue` (bare) when an editor would open | Editor may inject a `Co-Authored-By` trailer | `GIT_EDITOR=true git rebase --continue` |
| `git push --force` after the rebase | Destroys remote history | `--force-with-lease` (only if user asks) |

## Variations

### Working tree already clean

Skip steps 2 and 8. Note it in the report.

### Target has no remote

Skip `fetch` in step 4 and rebase onto the local target in step 6 (`git rebase "$TARGET"`).

### Target is the current branch

No-op. Tell the user and stop.

### Detached HEAD

Stop and ask. Don't rebase from a detached HEAD without explicit confirmation.

### Conflicts during BOTH rebase AND stash pop

Resolve rebase conflicts first (`git rebase --continue`). Then the stash pop conflicts are independent — report both states.

### Push after rebase

The rebase rewrites local history. Push with `--force-with-lease` so the server refuses the push if a teammate landed new commits since your last fetch — never `--force`.

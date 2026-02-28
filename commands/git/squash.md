---
description: Squash and organize commits into clean, well-documented history
agent: sisyphus
subtask: true
---
Use skill git-squash to squash and organize the commit history for $ARGUMENTS

Ultrawork

## Workflow

1. **Identify commits**: `git log --oneline <start>^..<end>` or `gh pr view <pr> --json commits`
2. **Group** by feature/component, type, or dependency
3. **Plan strategy** per group: squash (combine), fixup (discard msgs), or reorder
4. **Present plan** to user for approval (use SQUASH_PLAN.md template)
5. **Execute** via soft reset method:
   ```bash
   git reset --soft <base_commit>^
   git commit -m "feat: First group message"
   git commit -m "fix: Second group message"
   ```
6. **Generate messages** using git-description format with `Squashed from:` listing original hashes
7. **Push**: `git push --force-with-lease origin <branch>` (or create `-clean` branch for shared branches)

**Types**: `feat` | `fix` | `refactor` | `chore` | `docs` | `test` | `style` | `perf`

## Example

**Input:**
```
abc1234 Add player controller script
def5678 Fix player movement bug
ghi9012 Add jump animation
jkl3456 Fix animation timing
mno7890 Add player tests
```

**Output:** Group 1 (abc–jkl → feat), Group 2 (mno → test)
```
feat(player): Implement player controller with movement and animations

Squashed from:
- abc1234: Add player controller script
- def5678: Fix player movement bug
- ghi9012: Add jump animation
- jkl3456: Fix animation timing
```

## Safety

- Verify backup branch exists and user approved grouping
- Check for pending changes (stash if needed)
- After squash: run tests, review `git log`, verify all changes present

**Undo**: `git reflog` → `git reset --hard <original_head>`
**Conflicts**: `git add <resolved>` → `git rebase --continue` (or `--abort`)

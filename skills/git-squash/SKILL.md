---
name: git-squash
description: "Squash multiple related commits into organized, well-documented commits. Use when consolidating messy commit history, preparing clean commits for PR, or organizing commits by feature/bugfix. Triggers on: (1) Pre-merge commit cleanup, (2) PR commit organization, (3) History consolidation, (4) Release branch preparation."
---

# Git Squash

Intelligently group, squash, and document related commits to create a clean, meaningful commit history.

## Output Requirement (MANDATORY)

**Every squash plan MUST follow the template**: [SQUASH_PLAN.md](assets/templates/SQUASH_PLAN.md)

Present the squash plan to the user for approval before executing.

Read the template first, then populate all sections.

## Workflow

### Step 1: Identify the Commits

Gather the commits to analyze:

**From commit range:**
```bash
# View commits in range
git log --oneline <start_hash>^..<end_hash>

# Or from a specific number of commits
git log --oneline -n <count>
```

**From Pull Request:**
```bash
# List PR commits
gh pr view <pr_number> --json commits --jq '.commits[].messageHeadline'
```

### Step 2: Analyze and Group Commits

Review commits and group by logical relationship:

1. **By feature/component**: Commits touching the same feature
2. **By type**: Features, bugfixes, refactoring, tests, docs
3. **By dependency**: Commits that must be together (e.g., migration + code)

Example grouping:
```
Group 1: Authentication Feature
  - Add login form UI
  - Add login API endpoint
  - Add tests for login

Group 2: Bug Fixes
  - Fix null reference in settings
  - Fix button alignment on mobile

Group 3: Cleanup
  - Remove unused imports
  - Update code comments
```

### Step 3: Plan the Squash Strategy

For each group, decide:
- **Squash all**: Combine into single commit (most common)
- **Fixup**: Squash and discard individual messages
- **Reorder**: Rearrange commits before squashing

Present the plan to the user for approval:
```markdown
## Squash Plan

| Group | Commits | Target Message |
|-------|---------|----------------|
| Authentication | 3 commits | feat: Add user authentication flow |
| Bug Fixes | 2 commits | fix: Resolve UI and null reference issues |
| Cleanup | 2 commits | chore: Code cleanup and documentation |
```

### Step 4: Execute the Squash

**Interactive Rebase Method:**
```bash
# Start interactive rebase
git rebase -i <base_commit>^

# In the editor, mark commits as:
# pick (keep) - first commit of each group
# squash (combine) - subsequent commits in same group
# fixup (combine, discard message) - for cleanup commits
```

**Soft Reset Method (for simpler cases):**
```bash
# Soft reset to before the commits
git reset --soft <base_commit>^

# Create new grouped commits
git commit -m "feat: First group message"
# Stage next group files
git commit -m "fix: Second group message"
```

### Step 5: Generate Commit Messages

For each squashed commit, generate a comprehensive message using the git-comment format:

```markdown
<type>(<scope>): <short summary>

## High Level Summary

[2-3 sentence overview of what this commit accomplishes]

## Specific Details

### Changes Made
- [File]: [Change description]

### Logic Changes
- [Behavioral change description]

### Technical Notes
- [Implementation details if relevant]

Squashed commits:
- <original hash 1>: <original message>
- <original hash 2>: <original message>
```

### Step 6: Push the Changes

**If branch history can be rewritten:**
```bash
git push --force-with-lease origin <branch_name>
```

**If protecting history (shared branch):**
```bash
# Create a new branch with clean history
git checkout -b <branch_name>-clean
git push origin <branch_name>-clean
```

## Commit Type Reference

| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring without behavior change |
| `chore` | Maintenance tasks, dependencies |
| `docs` | Documentation only |
| `test` | Adding or updating tests |
| `style` | Formatting, no code change |
| `perf` | Performance improvement |

## Examples

### Example 1: Squash Feature Commits

**Input commits:**
```
abc1234 Add player controller script
def5678 Fix player movement bug
ghi9012 Add jump animation
jkl3456 Fix animation timing
mno7890 Add player tests
```

**Grouped result:**
```
Group 1 (Player Feature):
- abc1234, def5678, ghi9012, jkl3456

Group 2 (Tests):
- mno7890
```

**Output commits:**
```
feat(player): Implement player controller with movement and animations

## High Level Summary

Adds complete player controller system including movement mechanics,
jump animations, and proper animation timing. Enables basic character
movement for gameplay prototype.

## Specific Details

### Changes Made
- **PlayerController.cs**: Core movement and input handling
- **PlayerAnimator.cs**: Animation state machine integration
- **AnimationTiming.cs**: Frame-perfect animation transitions

### Logic Changes
- Player responds to WASD/Arrow keys for movement
- Jump triggers on Space with proper coyote time
- Animation blends smoothly between states

Squashed from:
- abc1234: Add player controller script
- def5678: Fix player movement bug
- ghi9012: Add jump animation
- jkl3456: Fix animation timing
```

### Example 2: Cleanup PR History

**Input**: PR with 15 commits including WIP, fixes, and reverts

**Grouped result:**
```
Group 1: Core Feature (8 commits → 1)
Group 2: Tests (3 commits → 1)
Group 3: Documentation (2 commits → 1)
Discarded: 2 revert commits (cancel each other)
```

**Final history:**
```
feat(core): Main feature implementation
test(core): Add comprehensive test coverage
docs(core): Update API documentation
```

## Safety Checks

Before executing squash:
- [ ] Verify backup branch exists
- [ ] Confirm user approval of grouping
- [ ] Check for pending changes (stash if needed)
- [ ] Verify target branch is correct

After squash:
- [ ] Run tests to verify nothing broke
- [ ] Review git log to confirm structure
- [ ] Verify all intended changes are present

## Troubleshooting

**Merge conflicts during rebase:**
```bash
# Resolve conflicts in files
git add <resolved_files>
git rebase --continue

# Or abort if needed
git rebase --abort
```

**Need to undo squash:**
```bash
# Find original HEAD in reflog
git reflog

# Reset to before squash
git reset --hard <original_head>
```

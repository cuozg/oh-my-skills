---
name: git-squash
description: >
  Use this skill to squash a branch's commits into clean, logical units before merging a PR. Use it
  when the user wants to "clean up commits," "squash before merge," "combine WIP commits," or "make
  the history cleaner." Analyzes commit history, groups related changes, presents a squash plan for
  approval, then executes via interactive rebase. Do not use for amending a single commit — use
  git-comment for that.
metadata:
  author: kuozg
  version: "1.0"
---
# git-squash

Analyze a branch's commit history, group related commits into a squash plan, present it for approval, then execute with interactive rebase.

## When to Use

- Cleaning up WIP commits before opening or merging a PR
- Combining fix-up and tweak commits into logical units
- Reducing commit noise in a feature branch
- Preparing a branch for a clean merge into main

## Workflow

1. **Analyze** — Run `git log --oneline origin/HEAD..HEAD` (or base branch) to list all branch commits
2. **Group** — Cluster commits by logical concern: features, fixes, refactors, tests, docs
3. **Plan** — Produce a squash table: group name → commits to combine → proposed message
4. **Present** — Show the plan to the user and wait for explicit approval before touching history
5. **Execute** — After approval, run `git rebase -i` using the plan; use `squash`/`fixup` markers

## Rules

- Never execute the squash without explicit user approval of the plan
- Never squash commits that have already been pushed to a shared remote branch
- Keep one logical commit per concern — do not over-squash unrelated changes
- Preserve the earliest commit's message as the base; rewrite for clarity
- Use imperative mood in squashed commit messages

## Output Format

Squash plan shown to user → approval received → rebase executed → `git log --oneline` confirming the reduced history.

## Reference Files

- `references/squash-workflow.md` — step-by-step squash strategy and git rebase commands

Load references on demand via `read_skill_file("git-squash", "references/{file}")`.

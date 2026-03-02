---
name: git-description
description: Generate and apply a structured PR description by investigating all changed files — use for 'PR description', 'write PR description', 'generate PR description', 'describe this PR'
---
# git-description

Deep-investigate all files changed in a PR, then generate and apply a structured description via `gh pr edit`.

## When to Use

- Opening a new PR that needs a clear description
- Updating a stale or missing PR description before review
- Generating documentation-quality PR context for reviewers
- Automating PR description from a feature branch

## Workflow

1. **Fetch** — Run `gh pr diff` or `git diff base...HEAD` to get the full PR diff
2. **Read** — Read every changed file to understand the actual implementation
3. **Investigate** — Trace cross-file dependencies, identify the root change vs cascading effects
4. **Draft** — Write structured description using the template in `references/pr-description-template.md`
5. **Apply** — Run `gh pr edit --body "..."` to push the description to GitHub

## Rules

- Read all changed files — do not summarize from diff hunks alone
- Separate what changed from why it changed in the description
- Include testing instructions that a reviewer can actually follow
- Never fabricate behavior — only describe what the code does
- Apply via `gh pr edit` — do not just print the description

## Output Format

Description applied to the GitHub PR via `gh pr edit --body`. Structured sections: Summary, Changes, Testing.

## Reference Files

- `references/pr-description-template.md` — PR description structure with summary, changes, and testing sections

Load references on demand via `read_skill_file("git-description", "references/{file}")`.

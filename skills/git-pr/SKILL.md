---
name: git-pr
description: Use this skill to generate and apply a clear title and structured description for a GitHub Pull Request by deep-investigating all changed files. Use it when the user opens a new PR, when a PR's title or description is missing or stale, or when the user says "update this PR", "describe this PR", or "write a summary for this PR." Applies the result directly via gh pr edit.
metadata:
  author: kuozg
  version: "1.0"
---
# git-pr

Deep-investigate all files changed in a PR, then generate and apply a reviewer-ready title and structured description via `gh pr edit`.

## When to Use

- Opening a new PR that needs a clear title and description
- Updating a stale or missing PR title or description before review
- Generating documentation-quality PR context for reviewers
- Automating PR metadata from a feature branch

## Workflow

1. **Fetch** — Run `gh pr diff` or `git diff base...HEAD` to get the full PR diff
2. **Read** — Read every changed file to understand the actual implementation
3. **Investigate** — Trace cross-file dependencies, identify the root change vs cascading effects
4. **Draft title** — Write a concise PR title in imperative or descriptive form that reflects the root change
5. **Draft body** — Write a structured description using the template in `references/pr-description-template.md`
6. **Apply** — Run `gh pr edit --title "..." --body "..."` to push both fields to GitHub

## Rules

- Read all changed files — do not summarize from diff hunks alone
- Separate what changed from why it changed in the description
- Keep the title specific, concise, and aligned with the actual implementation
- Include testing instructions that a reviewer can actually follow
- Never fabricate behavior — only describe what the code does
- Apply via `gh pr edit --title --body` — do not just print the title or description

## Output Format

Title and description applied to the GitHub PR via `gh pr edit --title --body`. Body sections should follow the repository PR template.

## Reference Files

- `references/pr-description-template.md` — PR body structure with checklist, summary, changes, testing, links, screenshots, and notes

Load references on demand via `read_skill_file("git-pr", "references/{file}")`.

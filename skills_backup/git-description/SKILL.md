---
name: git-description
description: "Generate and apply GitHub PR descriptions from pull request links. Deep investigate all PR changes — logic, architecture impact, behavioral changes — produce a structured PR description following the project template, and edit the PR on GitHub directly via `gh pr edit`. Input is a PR link or number. This skill should be used when: (1) generating PR descriptions, (2) user says 'describe this PR', (3) 'generate PR description', (4) 'PR comment', (5) 'PR description', (6) GitHub PR links are provided."
---

# Git Description

## Input

GitHub pull request URL (e.g., `https://github.com/org/repo/pull/123`) or PR number.

## Output

PR description per [output-template.md](references/output-template.md), applied directly to GitHub via `gh pr edit`.

## Reference Files
- [output-template.md](references/output-template.md) — PR description template
- [workflow.md](references/workflow.md) — PR description generation workflow

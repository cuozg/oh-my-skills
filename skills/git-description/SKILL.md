---
name: git-description
description: "Generate and apply GitHub PR descriptions from pull request links. Deep investigate all PR changes — logic, architecture impact, behavioral changes — produce a structured PR description following the project template, and edit the PR on GitHub directly via `gh pr edit`. Input is a PR link or number. This skill should be used when: (1) generating PR descriptions, (2) user says 'describe this PR', (3) 'generate PR description', (4) 'PR comment', (5) 'PR description', (6) GitHub PR links are provided."
---

# Git Description

## Input

GitHub pull request URL (e.g., `https://github.com/org/repo/pull/123`) or PR number.

## Output

PR description per [PR_DESCRIPTION_TEMPLATE.md](assets/templates/PR_DESCRIPTION_TEMPLATE.md), applied directly to GitHub via `gh pr edit`. See [EXAMPLE_OUTPUT.md](assets/templates/EXAMPLE_OUTPUT.md) for format reference.

## Reference Files
- [workflow.md](references/workflow.md) — 4-step workflow (fetch → investigate → generate → apply) and writing rules
- [PR_DESCRIPTION_TEMPLATE.md](assets/templates/PR_DESCRIPTION_TEMPLATE.md) — PR description template
- [EXAMPLE_OUTPUT.md](assets/templates/EXAMPLE_OUTPUT.md) — Example output

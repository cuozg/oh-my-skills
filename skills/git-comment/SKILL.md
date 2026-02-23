---
name: git-comment
description: "Generate GitHub PR descriptions from pull request links. Deep investigate all PR changes — logic, architecture impact, behavioral changes — and produce a structured PR description following the project template. Input: GitHub PR URL or PR number. Output: Structured PR description ready to paste into GitHub. Triggers: 'describe this PR', 'generate PR description', 'PR comment', 'PR description', GitHub PR links."
---

# Git Comment

## Input

GitHub pull request URL (e.g., `https://github.com/org/repo/pull/12345`).

## Output

PR description per [PR_DESCRIPTION_TEMPLATE.md](assets/templates/PR_DESCRIPTION_TEMPLATE.md) — print directly to user. See [EXAMPLE_OUTPUT.md](assets/templates/EXAMPLE_OUTPUT.md) for a complete example.

## Workflow

1. **Fetch PR data**:
   - `gh pr view <url> --json title,body,baseRefName,headRefName,files,commits`
   - `gh pr diff <url>` for full diff
   - Extract JIRA ticket from branch name or title (pattern: `WHIP-\d+`)

2. **Investigate changes**:
   - Group changed files by system/module
   - For each significant change: identify the WHY, not just the WHAT
   - Distinguish logic/behavioral changes from cosmetic/formatting changes
   - Note architecture impact, new dependencies, breaking changes
   - Trace data flow changes and state management impacts
   - Flag Unity-specific concerns: serialization, lifecycle, prefab conflicts, .meta changes

3. **Generate PR description** per template:
   - **✅ Checklist**: Keep all checkboxes unchecked (author fills these)
   - **🔍 High Level Summary**: 2-4 sentences — overall purpose, scope, and impact
   - **🔍 Specific details**: Organize by system/module with bullets. Include file names. Explain what changed AND why
   - **🔍 Linked Feature TDD**: Extract from PR body if present, otherwise leave placeholder
   - **🎯 JIRA Ticket(s)**: Insert extracted ticket URL or leave placeholder
   - **🏗️ Build Number**: Leave as placeholder
   - **👀 Screenshots**: Leave as placeholder
   - **💬 Additional Notes**: Add reviewer warnings — breaking changes, migration steps, config changes, testing focus areas

4. **Output**: Print the complete PR description ready to paste into GitHub

## Guidelines

- Investigate logic depth — write "Replaces polling with event-driven updates via SO channels" not "Updated lobby code"
- Include file names in specific details
- Extract JIRA tickets automatically when possible
- Flag breaking changes and migration steps in Additional Notes

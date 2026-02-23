---
name: git-comment
description: "Generate and apply GitHub PR descriptions from pull request links. Deep investigate all PR changes — logic, architecture impact, behavioral changes — produce a structured PR description following the project template, and edit the PR on GitHub directly via `gh pr edit`. Input is a PR link or number. This skill should be used when: (1) generating PR descriptions, (2) user says 'describe this PR', (3) 'generate PR description', (4) 'PR comment', (5) 'PR description', (6) GitHub PR links are provided."
---

# Git Comment

## Input

GitHub pull request URL (e.g., `https://github.com/org/repo/pull/123`) or PR number.

## Output

PR description per [PR_DESCRIPTION_TEMPLATE.md](assets/templates/PR_DESCRIPTION_TEMPLATE.md), applied directly to the PR on GitHub. See [EXAMPLE_OUTPUT.md](assets/templates/EXAMPLE_OUTPUT.md) for a complete example.

## Workflow

1. **Fetch PR data**
   - `gh pr view <url> --json title,body,baseRefName,headRefName,files,commits`
   - `gh pr diff <url>` for full diff
   - Extract JIRA ticket from branch name or title (pattern: `WHIP-\d+`)

2. **Investigate changes**
   - Group changed files by system/module
   - For each significant change: identify the WHY, not just the WHAT
   - Distinguish logic/behavioral changes from cosmetic/formatting
   - Note architecture impact, new dependencies, breaking changes
   - Trace data flow changes and state management impacts
   - Flag Unity-specific concerns: serialization, lifecycle, prefab conflicts, `.meta` changes

3. **Generate PR description** per template
   - **✅ Checklist**: Keep all checkboxes unchecked (author fills these)
   - **🔍 High Level Summary**: 2-4 sentences — overall purpose, scope, impact
   - **🔍 Specific details**: Organize by system/module with bullets. Include file names. Explain what changed AND why
   - **🔍 Linked Feature TDD**: Extract from PR body if present, otherwise leave placeholder
   - **🎯 JIRA Ticket(s)**: Insert extracted ticket URL or leave placeholder
   - **🏗️ Build Number**: Leave as placeholder
   - **👀 Screenshots**: Leave as placeholder
   - **💬 Additional Notes**: Reviewer warnings — breaking changes, migration steps, config changes, testing focus areas

4. **Apply to GitHub**
   - Store the generated description in a variable
   - Run: `gh pr edit <url> --body "$DESCRIPTION"`
   - Verify: `gh pr view <url> --json body --jq '.body'` — confirm description was applied
   - Print confirmation with PR URL to user

## Guidelines

- Investigate logic depth — write "Replaces polling with event-driven updates via SO channels" not "Updated lobby code"
- Include file names in specific details
- Extract JIRA tickets automatically when possible
- Flag breaking changes and migration steps in Additional Notes
- Always apply the description to GitHub — never just print for manual pasting

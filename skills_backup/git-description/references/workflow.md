# Git Description — Workflow

## Steps

1. **Fetch PR data**
   - `gh pr view <url> --json title,body,baseRefName,headRefName,files,commits`
   - `gh pr diff <url>` for full diff
   - Extract JIRA ticket from branch name or title (pattern: `WHIP-\d+`)

2. **Investigate changes**
   - Group changed files by system/module
   - Identify the **WHY**, not just the WHAT
   - Distinguish logic/behavioral changes from cosmetic/formatting
   - Note architecture impact, new dependencies, **breaking changes**
   - Flag Unity-specific: serialization, lifecycle, prefab conflicts, `.meta` changes

3. **Generate PR description** — follow template exactly, section by section:
   - **✅ Checklist**: All checkboxes **unchecked** (author fills these)
   - **🔍 High Level Summary**: 2-3 sentences max. Purpose → scope → impact.
   - **🔍 Specific details**: Group by system/module with `###` subheadings
     - **Bullet points only** — one bullet per change
     - Format: `**FileName.cs**: what changed and why` (bold file name)
     - Keep each bullet to **1 line** — skip trivial changes
   - **🔍 Linked Feature TDD**: Extract from PR body if present, else leave empty
   - **🎯 JIRA Ticket(s)**: Insert extracted URL or leave placeholder
   - **🏗️ Build Number**: Leave empty
   - **👀 Screenshots**: Leave empty
   - **💬 Additional Notes**: Only if needed — breaking changes, migration steps

4. **Apply to GitHub**
   - Run: `gh pr edit <url> --body "$DESCRIPTION"`
   - Verify: `gh pr view <url> --json body --jq '.body'`
   - Print confirmation with PR URL

## Writing Rules

- **Short over long** — compact bullets, not prose
- **Bold key terms** — file names, breaking changes, new features
- **1 bullet = 1 change** — never combine multiple changes
- **Verb-first** — "Add", "Replace", "Remove", "Fix", not "This PR adds..."
- **Specific** — "Replace polling with SO event channels" not "Updated lobby code"
- **No redundancy** — don't repeat summary content in specific details
- Always **apply to GitHub** — never just print for manual pasting

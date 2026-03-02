---
name: unity-review-code-pr
description: GitHub PR C# logic review — posts inline comments via gh api. Triggers — 'review PR', 'review pull request', 'PR review', 'check this PR'.
---
# unity-review-code-pr

Fetch a GitHub PR diff, review changed C# files for logic and Unity-specific risks, post inline comments via GitHub API.

## When to Use

- Reviewing a teammate's open GitHub PR
- Running automated review on a PR before merge
- Need review feedback attached directly to PR lines on GitHub

## Workflow

1. **Fetch PR diff** — `gh api repos/{owner}/{repo}/pulls/{pr}/files`
2. **Fetch raw diff** — `gh api repos/{owner}/{repo}/pulls/{pr}` with `Accept: application/vnd.github.v3.diff`
3. **Read changed files** — fetch raw content for each `.cs` file
4. **Investigate context** — `lsp_goto_definition` / `lsp_find_references` for callers and state owners
5. **Review** — evaluate logic, lifecycle, serialization, null paths, event leaks, allocations
6. **Build payload** — construct JSON per `references/gh-api-comments.md`
7. **Post review** — submit via `gh api repos/{owner}/{repo}/pulls/{pr}/reviews`

## Review Body Format

Short PR summary (2-3 sentences), then categorized findings:

```
### Breaking Changes ([N])
### Potential Issues ([N])
### Unity-Specific Concerns ([N])
```

Each item: **what** (1-line summary) → **why** (1-3 lines, evidence) → **how** (code fix with line ref).

## Inline Comment Format

**🔴 Critical / 🟡 High** — full block:

```
**🔴 Issue Title**: One-line problem summary
- **Why**: root cause or risk
- **Fix**: concrete solution
\`\`\`suggestion
[Fixed code — exact full-line replacement, preserving indentation]
\`\`\`
```

**🔵 Medium / 🟢 Low** — compact: `**🔵 Issue**: Problem → fix.` + suggestion block.

Suggestion replaces the WHOLE line(s), not a substring — include full line content.

## Rules

- Always fetch full file content, not just diff hunks
- Map comments to `line` number (right side of diff) — not `position`
- Use severity icons: 🔴 Critical, 🟡 High, 🔵 Medium, 🟢 Low
- Cover: null guards, lifecycle order, event leaks, serialization, hot-path allocations
- Do not post duplicate comments for the same line
- Batch all comments into one review call

## Reference Files

- `references/pr-review-workflow.md` — step-by-step PR fetch and review process
- `references/gh-api-comments.md` — JSON payload format + CLI shortcuts

Load on demand via `read_skill_file("unity-review-code-pr", "references/{file}")`.

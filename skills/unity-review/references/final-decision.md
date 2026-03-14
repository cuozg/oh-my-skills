# Final Decision — APPROVE or REQUEST_CHANGES

After all specialist reviews complete and findings are aggregated, make the final PR decision.

## Decision Logic

- **REQUEST_CHANGES** if ANY of:
  - Unresolved CRITICAL issues exist
  - Hardcoded API keys or passwords found
  - Missing null check on deserialized data touching gameplay state
  - Security vulnerabilities that could lead to data exposure

- **APPROVE** if:
  - No CRITICAL issues
  - All HIGH issues have suggestion blocks with fixes
  - No security blockers

## Review Body Structure

1. Summary of what the PR does (1-2 lines)
2. **Findings by category** — list each specialist area reviewed with issue count
3. **Critical Issues** — if any, list each with file + line
4. **Decision** — first word must be "APPROVE" or "REQUEST_CHANGES"
5. **Notes** — warnings, recommendations for follow-up

## Rules

- State decision as first word of body: "APPROVE" or "REQUEST_CHANGES"
- If prior reviews exist, acknowledge — do not re-flag same issues
- PRs with no description and >200 changed lines → WARNING in body
- Use `event: "APPROVE"` or `event: "REQUEST_CHANGES"` — never `"COMMENT"`
- One final review per run — do not call reviews API twice
- Summarize specialist findings before decision
- Never submit APPROVE if any CRITICAL issue is unresolved
- Never post individual line comments from the decision — use body only
- Include both inline comments (from specialists) and body (from decision) in single submission

## Submission

Submit per `unity-standards/references/review/pr-submission.md`:

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/reviews \
  --method POST --input review.json
```

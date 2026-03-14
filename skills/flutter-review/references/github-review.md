# GitHub PR Review Workflow

## 1. Resolve Owner/Repo

```bash
gh repo view --json owner,name --jq '{owner: .owner.login, repo: .name}'
```

## 2. Fetch PR File List

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/files \
  --jq '.[] | {filename: .filename, status: .status, patch: .patch}'
```

## 3. Fetch Raw Unified Diff

```bash
gh api repos/{owner}/{repo}/pulls/{pr} \
  -H "Accept: application/vnd.github.v3.diff"
```

## 4. Fetch File Content at PR Head

```bash
gh api repos/{owner}/{repo}/contents/{path}?ref={head_sha} \
  --jq '.content' | base64 -d
```

Or `git show {head_sha}:{path}` if repo is checked out locally.

## 5. Size Assessment

| Size | .dart Files Changed | Functions Changed | Review Mode |
|------|:-:|:-:|---|
| **Minor** | 1-2 | 1-5 | Single-pass (review all yourself) |
| **Large** | 3+ | 6+ | Deep (parallel subagents per criterion) |

Either threshold triggers Large — e.g. 1 file with 8 changed functions = Large.

- Only `.dart` files affect classification. Config-only PRs = Minor.
- Exclude generated files (`*.g.dart`, `*.freezed.dart`) from count.

## 6. Build + Submit Review

Map issues to right-side file line numbers (not diff positions). Always `"side": "RIGHT"`.

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/reviews \
  --method POST --input review.json
```

## 7. Decision Rules

**REQUEST_CHANGES** if ANY of:
- Unresolved CRITICAL issues exist
- Hardcoded API keys, secrets, or credentials found
- Missing error handling on network/IO that touches user-visible state
- Security vulnerabilities (SQL injection, XSS, insecure storage)

**APPROVE** if:
- No CRITICAL issues
- All HIGH issues have suggestion blocks with fixes
- No security blockers

## 8. Review Body Structure

1. Summary of what the PR does (1-2 lines)
2. Findings by category — issue count per specialist area
3. Critical Issues — if any, list each with file + line
4. Decision — first word: "APPROVE" or "REQUEST_CHANGES"
5. Notes — warnings, recommendations for follow-up

## 9. Verify + Retry

**Mandatory — never skip:**
```bash
gh api repos/{owner}/{repo}/pulls/{pr}/reviews \
  --jq '.[-1] | {id, state, submitted_at}'
```
If `id` is absent or command errors — fix root cause and re-run step 6. Loop until confirmed.

## Notes

- Always fetch full file content — diff hunks lack context for state management analysis
- Check PR description for "skip review" labels before proceeding
- Rate limit: 5000 authenticated requests/hour

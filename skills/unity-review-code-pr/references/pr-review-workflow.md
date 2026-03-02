# PR Review Workflow

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

## 5. Map Issues to Line Numbers

Use the right-side **file line number** (not diff position):
- Read `patch` from step 2 to find which lines were added/changed
- `line` in comments = actual line number in the file at HEAD
- Always set `"side": "RIGHT"` (commenting on new code)

## 6. Build + Submit Review

See `gh-api-comments.md` for payload format. Submit:

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/reviews \
  --method POST --input review.json
```

## 7. Verify + Retry Until Confirmed

**Mandatory step — never skip:**
```bash
gh api repos/{owner}/{repo}/pulls/{pr}/reviews \
  --jq '.[-1] | {id, state, submitted_at}'
```
If `id` is absent or command errors — fix the root cause and re-run step 6. Loop until confirmed.

## Notes

- Always fetch full file content — diff hunks lack context for lifecycle analysis
- Check PR description for "skip review" labels before proceeding
- Rate limit: 5000 authenticated requests/hour

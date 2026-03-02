# PR Review Workflow

## 1. Fetch PR File List

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/files \
  --jq '.[] | {filename: .filename, status: .status, patch: .patch}'
```

## 2. Fetch Raw Unified Diff

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number} \
  -H "Accept: application/vnd.github.v3.diff"
```

## 3. Fetch File Content at PR Head

```bash
gh api repos/{owner}/{repo}/contents/{path}?ref={head_sha} \
  --jq '.content' | base64 -d
```
Or use `git show {head_sha}:{path}` if the repo is checked out locally.

## 4. Map Issues to Diff Position

The `position` field in a PR comment is the **line number within the unified diff**, not the file line number.

- Count from line 1 of the diff hunk (`@@` header = position 1)
- Added lines (`+`) and context lines count; deleted lines (`-`) do not advance position
- Use `patch` field from step 1 to compute positions

## 5. Build Review Payload

See `gh-api-comments.md` for the exact JSON structure.

## 6. Resolve Owner/Repo

```bash
gh repo view --json owner,name --jq '{owner: .owner.login, repo: .name}'
```

## Notes

- Always fetch full file content — diff hunks lack context for lifecycle analysis
- Check PR description for "skip review" labels before proceeding
- Rate limit: GitHub allows 60 unauthenticated or 5000 authenticated requests/hour

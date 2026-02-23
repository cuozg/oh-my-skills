---
description: Review a pull request on GitHub
agent: sisyphus
subtask: true
---
Ultrawork

Review pull request $ARGUMENTS following this workflow:

## Step 1 — Fetch PR & Categorize

```bash
gh pr diff <N> --name-only
gh pr view <N> --json title,body,files,number
```

Group files into buckets:
- **cs_files**: `.cs`
- **prefab_files**: `.prefab`, `.unity`
- **asset_files**: `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset`

## Step 2 — Staleness & Skip List

Fetch existing reviews, inline comments, and HEAD:

```bash
gh api repos/{owner}/{repo}/pulls/<N>/reviews --paginate --jq '.[] | {id, body, commit_id, state}'
gh api repos/{owner}/{repo}/pulls/<N>/comments --paginate --jq '.[] | {id, path, line, body, commit_id, position}'
gh pr view <N> --json headRefOid --jq '.headRefOid'
```

### Detect covered categories by header markers in review bodies

| Header Marker | Category | Skill |
|:------|:---------|:------|
| `## Architecture Review` | architecture | `unity-review-architecture` |
| `## Code Review` | code | `unity-review-code-pr` |
| `## Prefab & Scene Review` | prefab | `unity-review-prefab` |
| `## Asset Review` | asset | `unity-review-asset` |
| `## Final Quality Review` | general | `unity-review-general` |

### Staleness rules

For each covered category, compare review `commit_id` vs HEAD:
- **Matches HEAD** → SKIP (current)
- **Doesn't match HEAD** → RE-RUN (stale)

### Build existing_comments index (exclude outdated)

Collect inline comments where `position` is NOT null (non-null = still active on current diff). Comments with `position: null` are **outdated** (code moved/changed) — exclude them entirely.

```
existing_comments = [{ path, line, body_preview }]  // only active comments
```

If a category's review body exists at HEAD but ALL its inline comments are outdated (`position: null`), treat that category as **stale → RE-RUN** even if `commit_id` matches. The comments no longer apply to current code.

### Log coverage

```
Review Coverage:
  ✅ Architecture Review — current → SKIP
  ⚠️ Code Review — stale (commit mismatch) → RE-RUN
  ⚠️ Prefab Review — all comments outdated → RE-RUN
  ❌ Asset Review — not found → RUN
  ⏭ General Review — no files need review → SKIP (no files)
```

## Step 3 — Sequential Review (specialized → general)

Run each reviewer sequentially. Skip if: current in skip list OR no matching files in bucket.

Pass to each: PR number, owner/repo, bucket files, all PR files, `existing_comments` index.

### 3a. Architecture — IF `cs_files` && not skipped

```
task(category="deep", load_skills=["unity-review-architecture", "unity-code-standards"], run_in_background=false,
  description="Architecture review PR #<N>",
  prompt="Review architecture in PR #<N> of {owner}/{repo}. CS files: [cs_files]. All files: [all_files]. Title: <title>. Body: <body>. Active comments (avoid duplicates): [existing_comments]. Load unity-review-architecture, follow its workflow.")
```

### 3b. Code — IF `cs_files` && not skipped

```
task(category="deep", load_skills=["unity-review-code-pr", "unity-code-standards"], run_in_background=false,
  description="Code review PR #<N>",
  prompt="Review C# code in PR #<N> of {owner}/{repo}. CS files: [cs_files]. All files: [all_files]. Title: <title>. Body: <body>. Active comments (avoid duplicates): [existing_comments]. Load unity-review-code-pr, follow its workflow.")
```

### 3c. Prefab/Scene — IF `prefab_files` && not skipped

```
task(category="deep", load_skills=["unity-review-prefab"], run_in_background=false,
  description="Prefab review PR #<N>",
  prompt="Review prefab/scene files in PR #<N> of {owner}/{repo}. Files: [prefab_files]. All files: [all_files]. Title: <title>. Body: <body>. Active comments (avoid duplicates): [existing_comments]. Load unity-review-prefab, follow its workflow.")
```

### 3d. Asset — IF `asset_files` && not skipped

```
task(category="deep", load_skills=["unity-review-asset"], run_in_background=false,
  description="Asset review PR #<N>",
  prompt="Review asset files in PR #<N> of {owner}/{repo}. Files: [asset_files]. All files: [all_files]. Title: <title>. Body: <body>. Active comments (avoid duplicates): [existing_comments]. Load unity-review-asset, follow its workflow.")
```

## Step 4 — General Quality Review (ALWAYS LAST, sole approver)

Always run after all specialized reviewers complete. Only skip if already current.

```
task(category="deep", load_skills=["unity-review-general"], run_in_background=false,
  description="Final quality review PR #<N>",
  prompt="Final quality review of PR #<N> of {owner}/{repo}. SOLE APPROVER. All files: [all_files]. Title: <title>. Body: <body>. Reviewers ran: [list]. Skipped: [list + reasons]. Active comments (avoid duplicates): [existing_comments]. Load unity-review-general, follow its workflow.")
```

## Step 5 — Report

```
## PR #[N] Review Complete
**Scope**: [PR title]

| # | Reviewer | Files | Status |
|:--|:---------|:------|:-------|
| 1 | Architecture | [N] | ✅ / ⏭ (reason) |
| 2 | Code Logic | [N] | ✅ / ⏭ (reason) |
| 3 | Prefab/Scene | [N] | ✅ / ⏭ (reason) |
| 4 | Asset | [N] | ✅ / ⏭ (reason) |
| 5 | **General** | all | ✅ APPROVE/REQUEST_CHANGES / ⏭ (reason) |
```

If any reviewer failed, retry using `session_id` continuation.

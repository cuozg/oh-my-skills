---
description: Review a pull request on GitHub
agent: sisyphus
subtask: true
---
Ultrawork

Review the pull request $ARGUMENTS following this workflow:

## Step 1 — Fetch PR & Categorize Files

```bash
gh pr diff <N> --name-only
gh pr view <N> --json title,body,files,number
```

Group changed files into buckets:

| Bucket | Extensions |
|:-------|:-----------|
| **cs_files** | `.cs` |
| **prefab_files** | `.prefab`, `.unity` |
| **asset_files** | `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset` |

## Step 2 — Check Existing Reviews & Build Skip List

### 2.1 Fetch existing reviews, inline comments, and HEAD commit

```bash
gh api repos/<owner>/<repo>/pulls/<N>/reviews --paginate --jq '.[] | {id, body, commit_id, state}'
gh api repos/<owner>/<repo>/pulls/<N>/comments --paginate --jq '.[] | {id, path, line, body, commit_id}'
gh pr view <N> --json headRefOid --jq '.headRefOid'
```

### 2.2 Detect covered categories by header markers

| Header Marker (case-sensitive) | Category | Skill |
|:-------------------------------|:---------|:------|
| `## Code Review` | code | `unity-review-code-pr` |
| `## Architecture Review` | architecture | `unity-review-architecture` |
| `## Prefab & Scene Review` | prefab | `unity-review-prefab` |
| `## Asset Review` | asset | `unity-review-asset` |
| `## Final Quality Review` | general | `unity-review-general` |

### 2.3 Staleness check

For each covered category, compare `commit_id` vs current HEAD:
- Matches → **SKIP** (current)
- Doesn't match → **RE-RUN** (stale)

### 2.4 Build existing comments index

Collect inline comments at current HEAD into `existing_comments`:
```
[{ path: "Assets/Scripts/Foo.cs", line: 42, body_preview: "🔴 Missing null check..." }, ...]
```

### 2.5 Log coverage status

```
Review Coverage Check:
  ✅ Code Review — found (commit abc1234, current) → SKIP
  ⚠️ Architecture Review — found (commit def5678, stale) → RE-RUN
  ❌ Prefab Review — not found → RUN
  ⏭ Asset Review — no asset files in PR → SKIP (no files)
  ❌ General Quality Review — not found → RUN
```

## Step 3 — Sequential Review

Run each reviewer **sequentially** (each must submit before next starts). Skip categories that are current in the skip list or have no matching files.

Pass to EACH reviewer: PR number, repo, file list for its bucket, full PR file list, and the `existing_comments` index from Step 2.4 so it can avoid duplicate inline comments.

### 3a. Code Review — IF `cs_files` non-empty AND not skipped

```
task(category="deep", load_skills=["unity-review-code-pr", "unity-code-standards"], run_in_background=false,
  description="Review .cs files in PR #<N>",
  prompt="Review C# code in PR #<N> of <owner>/<repo>. Files: [cs_files]. All PR files: [all_files]. PR title: <title>. PR body: <body>. Existing comments to avoid duplicating: [existing_comments]. Load skill unity-review-code-pr and follow its workflow.")
```

Verify submission succeeded.

### 3b. Architecture Review — IF `cs_files` non-empty AND not skipped

```
task(category="deep", load_skills=["unity-review-architecture", "unity-code-standards"], run_in_background=false,
  description="Review architecture in PR #<N>",
  prompt="Review architecture in PR #<N> of <owner>/<repo>. Files: [cs_files]. All PR files: [all_files]. PR title: <title>. PR body: <body>. Existing comments to avoid duplicating: [existing_comments]. Load skill unity-review-architecture and follow its workflow.")
```

Verify submission succeeded.

### 3c. Prefab/Scene Review — IF `prefab_files` non-empty AND not skipped

```
task(category="deep", load_skills=["unity-review-prefab"], run_in_background=false,
  description="Review prefab/scene files in PR #<N>",
  prompt="Review prefab/scene files in PR #<N> of <owner>/<repo>. Files: [prefab_files]. All PR files: [all_files]. PR title: <title>. PR body: <body>. Existing comments to avoid duplicating: [existing_comments]. Load skill unity-review-prefab and follow its workflow.")
```

Verify submission succeeded.

### 3d. Asset Review — IF `asset_files` non-empty AND not skipped

```
task(category="deep", load_skills=["unity-review-asset"], run_in_background=false,
  description="Review asset files in PR #<N>",
  prompt="Review asset files in PR #<N> of <owner>/<repo>. Files: [asset_files]. All PR files: [all_files]. PR title: <title>. PR body: <body>. Existing comments to avoid duplicating: [existing_comments]. Load skill unity-review-asset and follow its workflow.")
```

Verify submission succeeded.

## Step 4 — General Quality Review (sole approver) — IF not skipped

```
task(category="deep", load_skills=["unity-review-general"], run_in_background=false,
  description="Final quality review of PR #<N>",
  prompt="Final quality review of PR #<N> of <owner>/<repo>. You are the SOLE APPROVER. All PR files: [all_files]. PR title: <title>. PR body: <body>. Prior reviewers that ran: [list]. Skipped reviews: [list + reasons]. Existing comments to avoid duplicating: [existing_comments]. Load skill unity-review-general and follow its workflow.")
```

## Step 5 — Report

```markdown
## PR #[N] Review Complete
**Scope**: [PR title]

| Step | Reviewer | Files | Status |
|:-----|:---------|:------|:-------|
| 1 | Code Logic | [N] | ✅ Submitted / ⏭ Skipped (reason) |
| 2 | Architecture | [N] | ✅ Submitted / ⏭ Skipped (reason) |
| 3 | Prefab/Scene | [N] | ✅ Submitted / ⏭ Skipped (reason) |
| 4 | Asset | [N] | ✅ Submitted / ⏭ Skipped (reason) |
| 5 | **General (Approver)** | all | ✅ [APPROVE/REQUEST_CHANGES/COMMENT] / ⏭ Skipped (reason) |
```

If any reviewer failed, retry using `session_id` continuation.

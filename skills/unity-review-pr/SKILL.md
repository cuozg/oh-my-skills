---
name: unity-review-pr
description: >
  Use this skill to review Unity GitHub pull requests. Use when the user provides a PR URL/number, or asks to "review PR", "pull request", "merge", "is this ready".
metadata:
  author: kuozg
  version: "1.0"
---

# Unity PR Code Review

Complete end-to-end workflow for reviewing Unity GitHub pull requests.

## MANDATORY RULE
- Always follow the workflow steps in order. Do not skip or reorder steps.
- Always follow output formats and guidelines strictly. Do not deviate or improvise.
- Every issue must be emitted as exactly one small review comment using `references/output-template.md`. Do not bundle multiple issues into one comment, do not summarize an issue without the template, and do not invent alternate prose formats.
- Always push the review comment to github. Do not leave any comment as draft or in local file only.
- Always verify the review submission and report success or failure. Do not assume it works.

## 1. Fetch PR + Auth User + Labels

- Fetch PR details via `gh pr view {pr} --json {number,author,labels,files,commits,headRefOid}`.
- If the current branch is not PR branch, try to checkout PR branch as new worktree.
- If scope is big: Ask the user which specific criteria they need to review.

## 2. Build Changed-File Groups

Group files by type (`.cs`, `.prefab`, `.unity`, `.mat`, `.shader`). Ignore `.meta`.

## 3. Build Commentable-Line Map

Build a map from PR file patches: `{ path, line, side }`. Only inline comment if the line exists in the patch hunk. If the patch is null or line is not commentable, move the finding to the review body (avoids "Line could not be resolved").

## 4. Spawn Parallel Review Subagents

Spawn parallel reviewers for each file type with a strict schema. See `unity-standards/references/review/parallel-review-criteria.md`. Split work for big scopes.

## 5. Aggregator Validation

Validate only high-confidence findings. Deduplicate by (path, line).
- Dead code: verify nothing references the symbol.
- Missing unsub: verify subscription exists.

## 6. Split Inline vs Body Findings

Before submitting review, convert findings into two groups: `inline_comments` only for commentable PR patch lines, and `body_findings` for large files, hidden patches, or non-commentable lines.
- **Comment cap:** Inline top 5–10 strongest findings only. Put lower-severity or large-asset findings in the body.

## 7. Build Payload and Submit Event

*** MANDATORY ***
Follow `references/output-template.md` exactly for the review payload, review body, and every issue comment.

Before submission, run a strict format preflight:
- Each finding maps to one and only one formatted issue comment.
- Each issue comment body starts with the required severity admonition from the output template.
- Each issue comment contains the required title, one-line summary, short explanation, and optional suggestion block exactly in the template order.
- No issue is submitted as free-form prose, a combined bullet list, or an alternate markdown format.
- If a finding cannot be placed inline because GitHub has no commentable line, move it into `body_findings` as its own small comment-formatted block using the same issue-comment template.

## 8. Fallback Tree and Verify

1. Try full review submission via `gh api repos/{owner}/{repo}/pulls/{pr}/reviews --method POST --input review.json`.
2. If 422 line error, remove invalid inline comments into body.
3. Retry once.
4. If still blocked, submit a body-only `COMMENT` that still includes every issue as its own small comment-formatted block from `references/output-template.md`.
5. Never leave empty/dummy review.
6. Verify latest review and inline count.

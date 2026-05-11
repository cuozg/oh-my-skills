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

## 1. Fetch PR + Auth User + Labels

- Fetch PR Metadata: `gh api repos/{owner}/{repo}/pulls/{pr}/files` and `gh api repos/{owner}/{repo}/pulls/{pr}`
- Fetch Auth User: `gh api user --jq .login`
- Fetch PR Author.
- Exit if labels contain `skip-review` or `no-review`.
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
- **Comment cap:** Inline top 20–30 strongest findings only. Put lower-severity or large-asset findings in the body.

## 7. Build Payload and Submit Event

Create `review.json` locally.
- **Payload Preflight:** Validate JSON. Verify every comment path exists in PR files and every line is commentable. Include `commit_id: head_sha`. Never submit placeholder body like ".".
- **Decision:**
  - If auth user == PR author, use `COMMENT` (avoids GitHub API error).
  - Normal reviewer + blockers (CRITICAL/≥2 HIGH findings), use `REQUEST_CHANGES`.
  - Otherwise, use `COMMENT` or `APPROVE`.

```json
{
  "commit_id": "{head_sha}",
  "event": "REQUEST_CHANGES",
  "body": "## Code Review — PR #{number}\n{1-2 sentence verdict}\n\n| Category | Count | Top Severity |\n|---|:---:|---|\n| 💥 Crash/Breaking | {n} | 🔴 CRITICAL |\n| ⚠️ Bugs/Logic | {n} | 🟠 HIGH |\n| 🎮 Unity Risks | {n} | 🟡 MEDIUM |\n| 💡 Improvements | {n} | 🔵 LOW/⚪ STYLE |\n\n{body_findings}\n\n**Decision**: ✅ APPROVE / ❌ REQUEST_CHANGES / 💬 COMMENT",
  "comments": [
    { 
      "path": "Assets/Scripts/Player.cs", 
      "line": 42, 
      "side": "RIGHT", 
      "body": "> [!CAUTION]\n> **🔴 Issue Title**\n> <1 line to summary the issue>\n> <1-3 lines to explain the issue (What, Why, How, ...)>\n\n```suggestion\n{fix}\n```" 
    }
  ]
}
```
- Severity Badges: `> [!CAUTION]` (CRITICAL/HIGH), `> [!IMPORTANT]` (MEDIUM), `> [!NOTE]` (LOW/STYLE).

## 8. Fallback Tree and Verify

1. Try full review submission via `gh api repos/{owner}/{repo}/pulls/{pr}/reviews --method POST --input review.json`.
2. If 422 line error, remove invalid inline comments into body.
3. Retry once.
4. If still blocked, submit summary-only `COMMENT`.
5. Never leave empty/dummy review.
6. Verify latest review and inline count.

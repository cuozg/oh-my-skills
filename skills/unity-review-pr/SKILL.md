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

## 1. Fetch PR and Get List of Files

**Fetch PR Metadata**:
  - Files list: `gh api repos/{owner}/{repo}/pulls/{pr}/files`
  - Description/Labels: `gh api repos/{owner}/{repo}/pulls/{pr}`
  - *Exit if labels contain `skip-review` or `no-review`.*

**If scope is big:** Ask the user which specific criteria they need to review.

## 2. Group Files by Type

From the files list, group files by their type (e.g., `.cs`, `.prefab`, `.unity`, `.mat`, `.shader`). Ignore `.meta` files.

## 3. Spawn Parallel Review Subagents

Spawn parallel reviewer subagents for each file type group. Make sure they only fetch the correct file type for their assignment via `gh api` or `git show {head_sha}:{path}`.
See `unity-standards/references/review/parallel-review-criteria.md` for the subagent prompt template.
- When reviewing criteria with a big scope, try to split the work and spawn multiple reviewer subagents.

Review only the modified lines and their directly referenced methods/fields. Do not load the complete file content. Full context should only be pulled if an issue requires deeper investigation.

## 4. Aggregate and Validate

1. Merge findings from all subagents into a single list.
2. Deduplicate by (path, line) — keep highest severity.
3. Sort by file path → line number.
4. **Validate uncertain findings**: 
   - Dead code claims — verify nothing references the symbol.
   - Missing unsubscription — verify the subscription actually exists.
   - Unused variable — verify it's not used via reflection or serialization.

## 5. Build PR Review Payload

Create `review.json` locally. The `body` must contain a summary table and decision:

```json
{
  "event": "REQUEST_CHANGES",
  "body": "## Code Review — PR #{number}\n{1-2 sentence verdict}\n\n| Category | Count | Top Severity |\n|---|:---:|---|\n| 💥 Crash/Breaking | {n} | 🔴 CRITICAL |\n| ⚠️ Bugs/Logic | {n} | 🟠 HIGH |\n| 🎮 Unity Risks | {n} | 🟡 MEDIUM |\n| 💡 Improvements | {n} | 🔵 LOW/⚪ STYLE |\n\n**Decision**: ✅ APPROVE / ❌ REQUEST_CHANGES / 💬 COMMENT",
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
- **Line/Side**: `line` is the right-side file line number. `side` must be `RIGHT`.
- **Severity Badges**: Use GitHub Markdown Alerts based on severity:\n  - CRITICAL/HIGH: `> [!CAUTION]` (Red)\n  - MEDIUM: `> [!IMPORTANT]` (Purple)\n  - LOW/STYLE: `> [!NOTE]` (Blue)
- **Decision Matrix**:
  - `REQUEST_CHANGES`: Any CRITICAL or ≥2 HIGH findings.
  - `COMMENT`: Only MEDIUM/LOW/STYLE findings.
  - `APPROVE`: Zero CRITICAL/HIGH findings and all comments addressed.

## 6. Submit and Verify

1. **Submit**: `gh api repos/{owner}/{repo}/pulls/{pr}/reviews --method POST --input review.json`
2. **Verify (Mandatory)**: Ensure submission succeeded:
   `gh api repos/{owner}/{repo}/pulls/{pr}/reviews --jq '.[-1] | {id, state}'`
3. Loop and fix if `id` is absent (handle 404, 403, 422 limits).

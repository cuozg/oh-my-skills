# Output Template (review.json)

*** MUST FOLLOW OUTPUT FORMAT ***

This template is mandatory and non-negotiable. Every review issue must be represented as exactly one small comment-formatted block. Do not combine issues. Do not replace the issue template with prose, bullets, tables, or a custom format.

Create `review.json` locally.
- **Payload Preflight:** Validate JSON. Verify every comment path exists in PR files and every line is commentable. Include `commit_id: head_sha`. Never submit placeholder body like ".".
- **Issue Comment Rule:** Each issue is one small review comment. For inline findings, create one entry in `comments[]` per issue. For non-commentable findings, place one separate block per issue in `{body_findings}` using the exact same comment body format shown below.
- **No Bundling:** Never put multiple issues in one comment body. Never submit a free-form issue summary that does not match the template.
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
      "body": "> [!CAUTION]\n> **🔴 Issue Title**\n> <one-line issue summary>\n> - What: <specific problem>\n> - Why: <impact/risk>\n> - How: <minimal fix direction>\n\n```suggestion\n{fix}\n```" 
    }
  ]
}
```
- Severity Badges: `> [!CAUTION]` (CRITICAL), `> [!WARNING]` (HIGH),`> [!IMPORTANT]` (MEDIUM), `> [!NOTE]` (LOW/STYLE).

## Required Issue Comment Body

Use this exact body structure for every issue, whether it is in `comments[]` or moved into `{body_findings}`:

````markdown
> [!CAUTION]
> **🔴 Issue Title**
> <one-line issue summary>
> - What: <specific problem>
> - Why: <impact/risk>
> - How: <minimal fix direction>

```suggestion
{fix}
```
````

For HIGH/MEDIUM/LOW findings, replace only the admonition and severity icon/title prefix according to the Severity Badges line. Keep the structure unchanged.

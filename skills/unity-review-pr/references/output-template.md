# Output Template (review.json)

*** MUST FOLLOW OUTPUT FORMAT ***

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
      "body": "> [!CAUTION]\n> **🔴 Issue Title**\n> <1 line to summary the issue>\n> <1-3 lines to explain the issue, bullet style (What, Why, How, ...), bu>\n\n```suggestion\n{fix}\n```" 
    }
  ]
}
```
- Severity Badges: `> [!CAUTION]` (CRITICAL), `> [!WARNING]` (HIGH),`> [!IMPORTANT]` (MEDIUM), `> [!NOTE]` (LOW/STYLE).

# PR Review Submission

## API

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/reviews --method POST --input review.json
gh api repos/{owner}/{repo}/pulls/{pr} --jq '.head.sha'
```

## Payload

```json
{
  "event": "REQUEST_CHANGES",
  "body": "{summary}",
  "comments": [
    { "path": "Assets/Scripts/Player.cs", "line": 42, "side": "RIGHT",
      "body": "**🔴 Issue Title** — `CRITICAL`\n...\n```suggestion\n{fix}\n```" }
  ]
}
```

`line` = right-side file line number (not diff position). `side` always `RIGHT`. Max 32 KB/comment.

## Body Template

```
## Code Review — PR #{number}
{1-2 sentence verdict}
| | Category | Findings | Top Severity |
|---|---|:---:|---|
| 💥 | Breaking / Crash Risk | {n} | 🔴 CRITICAL |
| ⚠️ | Bugs / Incorrect Behavior | {n} | 🟠 HIGH |
| 🎮 | Unity-Specific Risks | {n} | 🟡 MEDIUM |
| 💡 | Improvements | {n} | 🔵 LOW / ⚪ STYLE |
**Decision**: ✅ APPROVE / ❌ REQUEST_CHANGES / 💬 COMMENT
```

## Decision Criteria

| Decision | Condition |
|---|---|
| `REQUEST_CHANGES` | Any CRITICAL or ≥2 HIGH |
| `COMMENT` | Only MEDIUM/LOW/STYLE |
| `APPROVE` | Zero CRITICAL/HIGH + all addressed |

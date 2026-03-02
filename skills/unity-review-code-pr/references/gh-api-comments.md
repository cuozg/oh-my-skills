# gh API — PR Review Payload

## JSON Payload Format

```json
{
  "body": "[SUMMARY with ### Breaking Changes / ### Potential Issues / ### Unity-Specific Concerns]",
  "event": "COMMENT",
  "comments": [
    {
      "path": "Assets/Scripts/Example.cs",
      "line": 42,
      "side": "RIGHT",
      "body": "**🔴 Issue Title**: One-line summary\n- **Why**: root cause\n- **Fix**: solution\n```suggestion\nexactReplacementCode();\n```"
    }
  ]
}
```

## Field Reference

| Field | Value | Notes |
|-------|-------|-------|
| `body` | Review summary | Categorized: Breaking Changes, Potential Issues, Unity Concerns |
| `event` | `COMMENT` | Always COMMENT — approval is unity-review-general's job |
| `comments[].path` | File path | Relative to repo root |
| `comments[].line` | Line number | Right-side line number in the changed file |
| `comments[].side` | `RIGHT` | Always RIGHT (comment on new code) |
| `comments[].body` | Comment body | Severity icon + suggestion block (see SKILL.md) |

## gh CLI — Submit

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/reviews \
  --method POST --input review.json
```

## gh CLI — Get Head SHA

```bash
gh api repos/{owner}/{repo}/pulls/{pr} --jq '.head.sha'
```

## gh CLI — List Existing Comments

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments --jq '.[].body'
```

## Notes

- Batch all comments into one review call — never submit multiple reviews
- `line` = file line number on right side of diff (not diff position)
- Suggestion replaces whole line(s) — include full line content
- Max 32 KB per comment body

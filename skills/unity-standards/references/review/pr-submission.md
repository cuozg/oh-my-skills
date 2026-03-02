# PR Review Submission

## API Endpoint

```
POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews
```

## JSON Payload

```json
{
  "event": "REQUEST_CHANGES",
  "body": "{summary — see Body Template below}",
  "comments": [
    {
      "path": "Assets/Scripts/Player.cs",
      "line": 42,
      "side": "RIGHT",
      "body": "**🔴 Issue Title**: ...\n```suggestion\n{fix}\n```"
    }
  ]
}
```

## Body Template

Use the review body format from `unity-review-code-pr` SKILL.md.
The `body` field = summary table; `comments[].body` = inline issues.

## Event Decision

| Decision | Condition | Icon |
|---|---|:---:|
| `REQUEST_CHANGES` | Any 🔴 `CRITICAL` finding | ❌ |
| `REQUEST_CHANGES` | ≥2 🟠 `HIGH` findings | ❌ |
| `REQUEST_CHANGES` or `COMMENT` | 1 🟠 `HIGH` — reviewer judgment | ⚠️ |
| `COMMENT` | Only 🟡/🔵/⚪ findings (no blockers) | 💬 |
| `APPROVE` | Zero 🔴/🟠 + all issues addressed | ✅ |

## Batching Rules

| Rule | Detail |
|---|---|
| One review per PR | ALL comments in single `POST` call |
| `line` | Right-side file line number (not diff position) |
| `side` | Always `RIGHT` |
| Max body | 32 KB per comment |
| Grouping | Group findings by file in `comments[]` |

## gh CLI

```bash
# Submit review
gh api repos/{owner}/{repo}/pulls/{pr}/reviews \
  --method POST --input review.json

# Get head SHA
gh api repos/{owner}/{repo}/pulls/{pr} --jq '.head.sha'

# List existing comments
gh api repos/{owner}/{repo}/pulls/{pr}/comments --jq '.[].body'
```

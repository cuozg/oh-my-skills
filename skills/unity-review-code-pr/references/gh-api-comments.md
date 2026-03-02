# gh API — PR Comment Commands

## Post a Review with Inline Comments

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews \
  --method POST \
  --field commit_id="{head_sha}" \
  --field body="{review_summary}" \
  --field event="COMMENT" \
  --field "comments[][path]"="{file_path}" \
  --field "comments[][position]"={diff_position} \
  --field "comments[][body]"="{comment_body}"
```

## Minimal JSON Payload (via --input)

```json
{
  "commit_id": "abc123",
  "body": "Review summary here.",
  "event": "COMMENT",
  "comments": [
    {
      "path": "Assets/Scripts/PlayerController.cs",
      "position": 12,
      "body": "[WARNING] allocation: LINQ in Update allocates per frame.\nFix: Use cached list."
    }
  ]
}
```

```bash
echo '{...}' | gh api repos/{owner}/{repo}/pulls/{pr}/reviews --method POST --input -
```

## Get Head SHA

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number} --jq '.head.sha'
```

## List Existing Review Comments

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --jq '.[].body'
```

## event Values

| Value | Effect |
|-------|--------|
| `COMMENT` | Post comments, no decision |
| `APPROVE` | Approve the PR |
| `REQUEST_CHANGES` | Block merge |

## Notes

- `position` is diff-relative (see `pr-review-workflow.md` step 4)
- Batch all comments into one review call — avoid multiple review submissions
- Max 32 KB per comment body

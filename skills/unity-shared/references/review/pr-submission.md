# PR Review Submission

## GitHub API Endpoint

```
POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews
```

## JSON Payload

```json
{
  "event": "REQUEST_CHANGES",
  "body": "## Code Review Summary\n\n{summary}",
  "comments": [
    {
      "path": "Assets/Scripts/Player.cs",
      "line": 42,
      "body": "// ── REVIEW [HIGH]: {message}\n```suggestion\n{fix}\n```"
    }
  ]
}
```

## Event Values

| Event            | When to Use                                  |
|------------------|----------------------------------------------|
| APPROVE          | Zero CRITICAL/HIGH findings                  |
| REQUEST_CHANGES  | Any CRITICAL or HIGH finding                 |
| COMMENT          | Only MEDIUM/LOW/STYLE (no blockers)          |

## Batching Rules

- Submit ALL comments in ONE API call (single review)
- Never submit multiple reviews per PR
- Group findings by file in the comments array

## gh CLI Command

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/reviews \
  --method POST \
  --input review.json
```

## Inline vs General Comments

- **Inline** (`comments[]`): specific line issues with file path + line number
- **General** (`body`): summary, overall assessment, patterns observed

## Approve Criteria

- Zero CRITICAL findings
- Zero HIGH findings
- All MEDIUM addressed or acknowledged
- Tests pass (if applicable)

## Request Changes Criteria

- Any CRITICAL finding → automatic REQUEST_CHANGES
- 2+ HIGH findings → REQUEST_CHANGES
- 1 HIGH finding → reviewer judgment (context-dependent)

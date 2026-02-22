# Review Troubleshooting

| Problem | Cause | Fix |
|:--------|:------|:----|
| 404 on submit | PR doesn't exist or wrong repo | Verify `gh pr view <N>` works first |
| Suggestion not rendering | Wrong line count in range | Ensure suggestion line count matches `line - start_line + 1` |
| "Validation Failed" 422 | `line` outside diff range or invalid `path` | Only comment on lines visible in the diff. Run `gh pr diff <N>` to verify line is in diff |
| Review not appearing | PR merged/closed | Use fallback: `gh pr comment` instead (handled by post_review.sh) |
| Suggestion breaks code | Suggestion has wrong indentation or partial line | Copy exact line content, modify only the relevant part |
| Comment on wrong line | `line` counted from wrong file version | `line` = line number on RIGHT side (new file). Verify against diff output |
| "Stale" commit error | `commit_id` doesn't match HEAD of PR | Don't hardcode — `post_review.sh` auto-injects latest commit SHA |
| Multiple reviews posted | Script ran twice | Check for existing pending review: `gh api /repos/{owner}/{repo}/pulls/{N}/reviews` |
| Comments on deleted files | Comment targeted LEFT/deleted side | Only comment files/lines present on diff RIGHT side |
| Rate limit hit | Too many API calls in short window | Add delay between calls or batch into fewer review submissions |

# Review Troubleshooting

| Problem | Cause | Fix |
|:--------|:------|:----|
| 404 on submit | PR doesn't exist or wrong repo | Verify `gh pr view <N>` works first |
| "Validation Failed" 422 | `line` outside diff hunk or invalid `path` | Parse `@@ +START,COUNT @@` headers — line must be in `[START, START+COUNT-1]`. Run `gh pr diff <N>` to verify |
| Suggestion not rendering | Suggestion text doesn't match targeted line range | Suggestion replaces WHOLE line(s). Content must be exact full-line replacement with correct indentation |
| Suggestion shows garbled | Wrong indentation or missing newlines | Copy the original line's indentation exactly, then modify the code part only |
| Comment on wrong line | `line` counted from wrong file version | `line` = new-file line number (RIGHT side). Count from `+START` in hunk header, not from diff position |
| Suggestion wrong code | Partial line targeted or extra whitespace | Suggestion replaces entire line(s) from column 0. Include leading spaces/tabs |
| Review not appearing | PR merged/closed | Fallback `gh pr comment` handled automatically by `post_review.py` |
| "Stale" commit error | `commit_id` mismatch | Don't hardcode — `post_review.py` auto-injects latest SHA |
| Multiple reviews posted | Script ran twice | Check existing: `gh api /repos/{owner}/{repo}/pulls/{N}/reviews` |
| Comments on deleted files | Targeted LEFT/deleted side | Only comment files/lines on RIGHT side of diff |
| Multi-line suggestion off | Missing `start_side` field | Multi-line requires both `start_line` AND `start_side: "RIGHT"` |
| Rate limit hit | Too many API calls | Batch into fewer review submissions |

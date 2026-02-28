# unity-review-prefab — Workflow

## 1. Fetch PR & Filter Files

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context
```

Filter to `.prefab` and `.unity` files ONLY. If none found, post note `No prefab/scene files to review.` and stop.

## 2. Parallel Review — One Subagent Per File

For each `.prefab`/`.unity` file, spawn a background subagent task. See `../../unity-shared/references/review-parallel-workflow.md` for prompt template, result format, and merge logic.

Each subagent reads the full file, applies patterns from `../../unity-shared/references/review-prefab-patterns.md`, and returns a JSON array of comment objects.

## 3. Collect & Merge Results

Collect all subagent results. Merge all comment arrays into one list. Build `/tmp/review-prefab.json`:

```json
{
  "body": "## Prefab & Scene Review\n**Scope**: N files reviewed\n...",
  "event": "COMMENT",
  "comments": [ ...merged comments from all subagents... ]
}
```

Do NOT include `commit_id` — `post_review.py` injects it automatically.

## 4. Submit

```bash
./skills/unity-shared/scripts/review/post_review.py <pr_number> /tmp/review-prefab.json
```

Fallback (merged/closed): handled automatically by `post_review.py`.

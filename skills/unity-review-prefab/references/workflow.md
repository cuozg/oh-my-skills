## Workflow

### 1. Fetch PR & Filter Files

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context
```

Filter to `.prefab` and `.unity` files ONLY. If none found, post note `No prefab/scene files to review.` and stop.

### 2. Parallel Review — One Subagent Per File

For each `.prefab`/`.unity` file, spawn a background subagent task. See [parallel-review-workflow.md](parallel-review-workflow.md) for prompt template, result format, and merge logic.

```python
task(
  category="quick",
  load_skills=["unity-review-prefab"],
  run_in_background=True,
  description=f"Review {filename}",
  prompt=f"<see parallel-review-workflow.md for template>"
)
```

Each subagent reads the full file, applies patterns from [PREFAB_PATTERNS.md](PREFAB_PATTERNS.md), and returns a JSON array of comment objects.

### 3. Collect & Merge Results

Collect all subagent results via `background_output(task_id=...)`. Merge all comment arrays into one list. Build `/tmp/review-prefab.json`:

```json
{
  "body": "## Prefab & Scene Review\n**Scope**: N files reviewed\n...",
  "event": "COMMENT",
  "comments": [ ...merged comments from all subagents... ]
}
```

Do NOT include `commit_id` — `post_review.py` injects it automatically.

### 4. Submit

```bash
./skills/unity-shared/scripts/review/post_review.py <pr_number> /tmp/review-prefab.json
```

Fallback (merged/closed): handled automatically by `post_review.py`.

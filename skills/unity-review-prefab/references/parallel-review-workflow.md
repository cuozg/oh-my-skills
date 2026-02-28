# Parallel Review Workflow

Orchestrate per-file prefab reviews using background subagent tasks.

## 1. Spawn Subagents

For each `.prefab`/`.unity` file in the PR, spawn one background task:

```python
task(
  category="quick",
  load_skills=["unity-review-prefab"],
  run_in_background=True,
  description=f"Review prefab: {filepath}",
  prompt=f"""Review this single .prefab/.unity file for issues.

PR: #{pr_number}
File: {filepath}

<FILE CONTENT>
{full_yaml_content}
</FILE CONTENT>

Apply ALL patterns from PREFAB_PATTERNS.md (loaded via unity-review-prefab skill).
For each issue found, return a JSON object with: path, line, side, body.

- path: "{filepath}"
- line: the YAML line number where the issue occurs
- side: "RIGHT"
- body: "**{{emoji}} {{Title}}**: `{{pattern}}`\n- **Why**: {{impact}}\n- **Fix**: {{suggestion}}"

Return ONLY a JSON array of comment objects. No prose. No markdown fences.
If no issues found, return an empty array: []

Example output:
[{{"path":"{filepath}","line":42,"side":"RIGHT","body":"**🔴 Missing Script**: ..."}}]
"""
)
```

Store each `task_id` in a list for later collection.

## 2. Collect Results

After all tasks are spawned, collect each result:

```python
for task_id in task_ids:
    result = background_output(task_id=task_id, block=True, timeout=120)
    # Parse the JSON array from the agent's response
    # Append comments to the merged list
```

## 3. Handle Failures

If a subagent fails or returns invalid JSON:
- Log the file name and error
- Skip that file's results — do not abort the entire review
- Include a note in the review body: `⚠️ Failed to review: {filepath}`

## 4. Merge & Build Final JSON

Combine all comment arrays into one flat list:

```python
all_comments = []
failed_files = []
for task_id, filepath in zip(task_ids, filepaths):
    try:
        comments = parse_json_from_result(result)
        all_comments.extend(comments)
    except:
        failed_files.append(filepath)
```

Build the final review JSON:

```json
{
  "body": "## Prefab & Scene Review\n**Scope**: N files reviewed, M issues found\n**Failed**: [list or 'none']",
  "event": "COMMENT",
  "comments": [ ...all_comments... ]
}
```

Write to `/tmp/review-prefab.json`.

## 5. Submit

```bash
./skills/unity-shared/scripts/review/post_review.py <pr_number> /tmp/review-prefab.json
```

## Comment Format Rules

- `m_RaycastTarget: 1` — check if GO has `Button`, `Toggle`, or `InputField`. If not → 🔴 Critical.
- Batch pattern: full explanation on first occurrence, short reference on subsequent.
- Every comment MUST include: severity emoji + title, evidence (file + line), why (impact), fix (suggestion).
- Do NOT include `commit_id` — injected by `post_review.py`.

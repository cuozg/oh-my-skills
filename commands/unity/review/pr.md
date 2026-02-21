---
description: Review a pull request on GitHub
agent: sisyphus
subtask: true
---
Ultrawork

Review the pull request $ARGUMENTS following this workflow:

## Step 1 — Fetch PR Files

Get the list of changed files and PR context:

```bash
gh pr diff <N> --name-only
gh pr view <N> --json title,body,files,number
```

## Step 2 — Categorize Files by Type

Group the changed files into buckets by extension:

| Bucket | Extensions |
|:-------|:-----------|
| **cs_files** | `.cs` |
| **prefab_files** | `.prefab`, `.unity` |
| **asset_files** | `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset` |

## Step 3 — Dispatch Parallel Review Tasks (by file type)

Based on which buckets are non-empty, spawn the corresponding review sub-agents **in parallel** using `task(run_in_background=true)`. Only spawn a reviewer if the PR contains files matching its bucket.

### 3a. C# Code Review — spawn IF `cs_files` is non-empty

```
task(
  category="deep",
  load_skills=["unity-review-code-local", "unity-review-architecture", "unity-code-standards"],
  run_in_background=true,
  description="Review .cs files in PR #<N>",
  prompt="
    1. TASK: Review C# code changes in PR #<N> of repo <owner>/<repo>.
    2. EXPECTED OUTCOME: Return a JSON object with exactly two keys:
       - \"comments\": array of comment objects, each with: path, line, side (\"RIGHT\"), body
       - \"max_severity\": one of \"CRITICAL\", \"HIGH\", \"MEDIUM\", \"LOW\", \"CLEAN\"
    3. REQUIRED TOOLS: bash (gh pr diff, gh pr view), read, grep, use_skill
    4. MUST DO:
        - Load skills unity-review-code-local, unity-review-architecture, and unity-code-standards (use_skill) FIRST
       - Fetch the full diff with `gh pr diff <N>` and focus on these files: [list cs_files]
       - Review for: logic correctness, edge cases, state management, data flow, concurrency, architecture violations, DI patterns, event systems, assembly coupling
       - One issue = one comment object
       - Every comment body MUST include: severity emoji + title, Evidence, Why, suggestion block
       - Set max_severity to the highest severity found (CLEAN if no issues)
       - Return ONLY the JSON object — no markdown wrapper, no extra text
    5. MUST NOT DO:
       - Do NOT combine multiple issues into one comment
       - Do NOT flag issues without evidence
       - Do NOT include commit_id in the output
       - Do NOT submit the review — the orchestrator handles submission
       - Do NOT modify any files
    6. CONTEXT:
       - Repository: <owner>/<repo>
       - PR number: <N>
       - PR title: <title>
       - PR body: <body>
       - Files to review: [cs_files list]
       - Full file list in PR: [all files]
  "
)
```

### 3b. Prefab/Scene Review — spawn IF `prefab_files` is non-empty

```
task(
  category="deep",
  load_skills=["unity-review-prefab"],
  run_in_background=true,
  description="Review prefab/scene files in PR #<N>",
  prompt="
    1. TASK: Review .prefab and .unity file changes in PR #<N> of repo <owner>/<repo>.
    2. EXPECTED OUTCOME: Return a JSON object with exactly two keys:
       - \"comments\": array of comment objects, each with: path, line, side (\"RIGHT\"), body
       - \"max_severity\": one of \"CRITICAL\", \"HIGH\", \"MEDIUM\", \"LOW\", \"CLEAN\"
    3. REQUIRED TOOLS: bash (gh pr diff, gh pr view), read, grep, use_skill
    4. MUST DO:
       - Load skill unity-review-prefab (use_skill) FIRST
       - Fetch the full diff with `gh pr diff <N>` and focus on these files: [list prefab_files]
       - Review for: missing scripts, broken variant links, raycast issues, hierarchy problems, Unity YAML patterns
       - One issue = one comment object
       - Every comment body MUST include: severity emoji + title, Evidence, Why, suggestion block
       - Set max_severity to the highest severity found (CLEAN if no issues)
       - Return ONLY the JSON object — no markdown wrapper, no extra text
    5. MUST NOT DO:
       - Do NOT combine multiple issues into one comment
       - Do NOT flag issues without evidence
       - Do NOT include commit_id in the output
       - Do NOT submit the review — the orchestrator handles submission
       - Do NOT modify any files
    6. CONTEXT:
       - Repository: <owner>/<repo>
       - PR number: <N>
       - PR title: <title>
       - PR body: <body>
       - Files to review: [prefab_files list]
       - Full file list in PR: [all files]
  "
)
```

### 3c. Asset Review — spawn IF `asset_files` is non-empty

```
task(
  category="deep",
  load_skills=["unity-review-asset"],
  run_in_background=true,
  description="Review asset files in PR #<N>",
  prompt="
    1. TASK: Review asset file changes in PR #<N> of repo <owner>/<repo>.
    2. EXPECTED OUTCOME: Return a JSON object with exactly two keys:
       - \"comments\": array of comment objects, each with: path, line, side (\"RIGHT\"), body
       - \"max_severity\": one of \"CRITICAL\", \"HIGH\", \"MEDIUM\", \"LOW\", \"CLEAN\"
    3. REQUIRED TOOLS: bash (gh pr diff, gh pr view), read, grep, use_skill
    4. MUST DO:
       - Load skill unity-review-asset (use_skill) FIRST
       - Fetch the full diff with `gh pr diff <N>` and focus on these files: [list asset_files]
       - Review for: shader issues, texture memory, animation misconfigs, audio optimization, model import settings
       - One issue = one comment object
       - Every comment body MUST include: severity emoji + title, Evidence, Why, suggestion block
       - Set max_severity to the highest severity found (CLEAN if no issues)
       - Return ONLY the JSON object — no markdown wrapper, no extra text
    5. MUST NOT DO:
       - Do NOT combine multiple issues into one comment
       - Do NOT flag issues without evidence
       - Do NOT include commit_id in the output
       - Do NOT submit the review — the orchestrator handles submission
       - Do NOT modify any files
    6. CONTEXT:
       - Repository: <owner>/<repo>
       - PR number: <N>
       - PR title: <title>
       - PR body: <body>
       - Files to review: [asset_files list]
       - Full file list in PR: [all files]
  "
)
```

## Step 4 — General Review (Main Task)

While the parallel sub-agent tasks are running, use skill `unity-review-general` in the **main task** to perform a cross-cutting general review of the entire PR covering: security, correctness, testing, code quality, performance, lifecycle, and documentation.

Load `unity-review-general` via `use_skill("unity-review-general")` and review all files in the PR. Produce the same JSON output format:
```json
{ "comments": [...], "max_severity": "CRITICAL|HIGH|MEDIUM|LOW|CLEAN" }
```

## Step 5 — Collect & Merge Results

1. Collect all background task results via `background_output(task_id="...")`.
2. Parse the JSON output from each sub-skill. If a sub-skill returned error or non-JSON, treat as `{ "comments": [], "max_severity": "CLEAN" }`.
3. **Concatenate** all `comments` arrays (including the General review from Step 4) into one array.
4. **Deduplicate**: If two reviewers flagged the same `path` + `line`, keep the higher-severity one.
5. **Determine overall max_severity**: CRITICAL > HIGH > MEDIUM > LOW > CLEAN.
6. **Map to approval event**:
   - CRITICAL or HIGH → `REQUEST_CHANGES`
   - MEDIUM → `COMMENT`
   - LOW or CLEAN → `APPROVE`

## Step 6 — Build `/tmp/review.json`

```json
{
  "body": "[SUMMARY — see format below]",
  "event": "REQUEST_CHANGES|COMMENT|APPROVE",
  "comments": [ ...merged comments... ]
}
```

Do NOT include `commit_id` — `post_review.sh` injects it automatically.

**Summary body format:**

```markdown
## Code Review - PR #[N]
**Scope**: [PR title]
[One-sentence overall assessment].

### Review Coverage
| Reviewer | Files | Findings | Severity |
|:---------|:------|:---------|:---------|
| Code | [N] | [N] | [max] |
| Prefab | [N] | [N] | [max] |
| Asset | [N] | [N] | [max] |
| General | cross-cutting | [N] | [max] |

### Acceptance Criteria
- [ ] No critical or high severity issues remain
- [ ] Feature works; edge cases handled
- [ ] No frame drops, GC spikes
- [ ] No breaking serialization changes
- [ ] No missing scripts, correct shaders, proper imports

### Breaking Changes ([N])
### Potential Issues ([N])
### Unity-Specific Concerns ([N])
### Code Quality ([N])
### Impact Analysis
- Files reviewed: X · Total findings: Y
```

## Step 7 — Submit

```bash
run_skill_script(skill="unity-review-code-pr", script="scripts/post_review.sh", arguments=["<pr_number>", "/tmp/review.json"])
```

**Fallback** (merged/closed): handled automatically by `post_review.sh` — posts as comment.
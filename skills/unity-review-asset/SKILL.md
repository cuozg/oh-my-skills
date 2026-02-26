---
name: unity-review-asset
description: "Review Unity asset files (.mat, .shader, .meta, .controller, .anim, .fbx, .asset) in GitHub PRs for shader issues, texture memory problems, animation misconfigurations, and model import settings. After review, pushes comments directly to GitHub via the API. Accepts PR number/URL as input. Use when: reviewing asset files in PRs, validating material/texture/model settings before merge. Triggers: 'review assets', 'asset review', 'material review', 'texture review', 'shader review', 'PR asset review', 'review PR assets'."
---

# Asset PR Reviewer

Review `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset` file changes in GitHub PRs. Push review comments directly to GitHub via the API.

## Output
Review comments pushed to GitHub PR via API. Covers shader refs, texture memory, animation config, model import settings.

## Input → Command

| Input | Command |
|:------|:--------|
| PR number/URL | `gh pr diff <N>` + `gh pr view <N> --json title,body,files,number` |

## Severity Labels

| Severity | Emoji | Meaning |
|:---------|:------|:--------|
| CRITICAL | 🔴 | Will break at runtime or cause data loss |
| HIGH | 🟡 | Performance, memory, or correctness issue |
| MEDIUM | 🔵 | Best practice violation, maintainability risk |
| LOW | 🟢 | Style, naming, minor optimization |

Severity labels are for categorization only. This skill always posts as `COMMENT`. Approval decisions are made exclusively by `unity-review-general`.

## File Type Coverage

| Extension | Review Focus |
|:----------|:-------------|
| `.mat` | Shader refs, material properties, render queue |
| `.shader` | Variants, platform compatibility, keywords |
| `.meta` | Texture import settings, compression, read/write |
| `.controller` | Animator config, culling, write defaults |
| `.anim` | Animation clips, curves, root motion |
| `.fbx` | Model import, mesh compression, rig type |
| `.asset` | ScriptableObject refs, data integrity |

## Workflow

Follow the 4-step workflow: Fetch PR → Read & Apply Patterns → Build JSON → Submit.
Read [workflow.md](references/workflow.md) before starting any review.

## Rules

- Only review asset file types listed above. One issue = one comment.
- Every comment needs severity + evidence + suggestion.
- Submit even if PR is merged — `post_review.py` handles fallback.
- Never hardcode `commit_id` or modify source files.

## Reference Files
- [workflow.md](references/workflow.md) — 4-step review workflow with grep patterns, JSON format, and submit commands
- [ASSET_PATTERNS.md](references/ASSET_PATTERNS.md) — Complete asset pattern catalog

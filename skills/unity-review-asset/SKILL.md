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

## Severity → Approval

| Severity | Emoji | Meaning | Approval |
|:---------|:------|:--------|:---------|
| CRITICAL | 🔴 | Will break at runtime or cause data loss | `REQUEST_CHANGES` (block) |
| HIGH | 🟡 | Performance, memory, or correctness issue | `REQUEST_CHANGES` |
| MEDIUM | 🔵 | Best practice violation, maintainability risk | `COMMENT` (allow merge) |
| LOW | 🟢 | Style, naming, minor optimization | `APPROVE` (with suggestions) |
| CLEAN | — | No issues | `APPROVE` |

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

### 1. Fetch PR

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context
gh pr diff <N>               # Full diff
```

Filter to asset file types listed above. If none found, APPROVE with note `No asset files to review.`

### 2. Read Files & Apply Patterns

Read changed files and their `.meta` counterparts. Apply patterns from [ASSET_PATTERNS.md](references/ASSET_PATTERNS.md) by file type. Batch grep for fast detection:

- Materials: `grep -n "m_Shader: {fileID: 0}\|{fileID: 10303}" <.mat files>`
- Textures: `grep -n "isReadable: 1\|enableMipMap: 1\|textureCompression: 0" <.meta files>`
- Animators: `grep -n "m_Controller: {fileID: 0}\|m_CullingMode: 0\|m_PlayOnAwake: 1" <files>`
- Models: `grep -n "meshCompression: 0\|isReadable: 1\|importAnimation: 1" <.fbx .meta files>`

### 3. Build `/tmp/review.json`

```json
{
  "body": "## Asset Review\n**Scope**: [N files reviewed]\n...",
  "event": "REQUEST_CHANGES|COMMENT|APPROVE",
  "comments": [
    {
      "path": "Assets/Materials/Player.mat",
      "line": 12,
      "side": "RIGHT",
      "body": "**🔴 Missing Shader**: `m_Shader: {fileID: 0}` — material will render pink at runtime.\n**Evidence**: Line 12 in material YAML.\n**Why**: Shader reference is null, likely deleted or not included in build.\n```suggestion\nAssign correct shader reference\n```"
    }
  ]
}
```

Do NOT include `commit_id` — `post_review.py` injects it automatically. Set `event` based on highest severity using the Severity → Approval table above.

### 4. Submit

```bash
./skills/unity-review-asset/scripts/post_review.py <pr_number> /tmp/review.json
```

Fallback (merged/closed): handled automatically by `post_review.py`.

## Rules

- Only review asset file types listed above. One issue = one comment.
- Every comment needs severity + evidence + suggestion.
- Submit even if PR is merged — `post_review.py` handles fallback.
- Never hardcode `commit_id` or modify source files.
- Refer to [ASSET_PATTERNS.md](references/ASSET_PATTERNS.md) for the complete pattern catalog.

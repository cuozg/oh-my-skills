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

### 3. Build `/tmp/review-asset.json`

```json
{
  "body": "## Asset Review\n**Scope**: [N files reviewed]\n...",
  "event": "COMMENT",
  "comments": [
    {
      "path": "Assets/Materials/Player.mat",
      "line": 12,
      "side": "RIGHT",
      "body": "**🔴 Missing Shader**: `m_Shader: {fileID: 0}` — material will render pink.\n- **Why**: Shader reference is null, likely deleted or not in build.\n- **Fix**: Assign correct shader reference"
    }
  ]
}
```

Do NOT include `commit_id` — `post_review.py` injects it automatically. Always set `event` to `"COMMENT"`.

### 4. Submit

```bash
./skills/unity-review-asset/scripts/post_review.py <pr_number> /tmp/review-asset.json
```

Fallback (merged/closed): handled automatically by `post_review.py`.

## Rules

- Only review asset file types listed above. One issue = one comment.
- Every comment needs severity + evidence + suggestion.
- Submit even if PR is merged — `post_review.py` handles fallback.
- Never hardcode `commit_id` or modify source files.
- Refer to [ASSET_PATTERNS.md](references/ASSET_PATTERNS.md) for the complete pattern catalog.

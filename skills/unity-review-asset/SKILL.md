---
name: unity-review-asset
description: "Review Unity asset files (.mat, .shader, .meta, .controller, .anim, .fbx, .asset) in PRs for shader issues, texture memory problems, animation misconfigurations, audio optimization, and model import settings. Sub-skill of unity-review-code-pr orchestrator. Use when: delegated by unity-review-code-pr to review asset files. Triggers: 'review assets', 'asset review', 'material review', 'texture review', 'shader review'."
---

# Asset Reviewer

Review `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset` files. Output partial review JSON for the orchestrator.

## Input

Receives from orchestrator: PR number, list of asset file paths, diff context.

## Severity Levels

| Level | Label | Meaning |
|:------|:------|:--------|
| `CRITICAL` | :red_circle: Critical | Will break at runtime or cause data loss |
| `HIGH` | :yellow_circle: High | Performance, memory, or correctness issue |
| `MEDIUM` | :blue_circle: Medium | Best practice violation, maintainability risk |
| `LOW` | :green_circle: Low | Style, naming, minor optimization |

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

1. Read changed files and their `.meta` counterparts.
2. Apply patterns from [ASSET_PATTERNS.md](references/ASSET_PATTERNS.md) by file type.
3. For texture `.meta` files, check compression, `isReadable`, `mipMaps`, platform overrides.
4. For materials, check shader assignment, keyword usage, render queue.
5. For models, check mesh compression, animation import, rig type.
6. Classify each finding by severity, create comment objects.
7. Return JSON array of comments + overall severity.

## Output Format

**ALWAYS use this exact output template:**

Each finding becomes one comment object:

```json
{
  "path": "Assets/Materials/Player.mat",
  "line": 12,
  "side": "RIGHT",
  "body": "**:red_circle: Missing Shader**: `m_Shader: {fileID: 0}` — material will render pink/magenta at runtime.\n**Evidence**: Line 12 in material YAML.\n**Why**: Shader reference is null, likely deleted or not included in build.\n```suggestion\nAssign correct shader reference\n```"
}
```

**Return envelope** (MANDATORY — always return this exact JSON structure):

```json
{
  "comments": [ "...array of comment objects above..." ],
  "max_severity": "CRITICAL|HIGH|MEDIUM|LOW|CLEAN"
}
```

- `comments`: Array of comment objects. Empty array `[]` if no issues found.
- `max_severity`: The highest severity found across all comments. `"CLEAN"` if no issues.
```

## Rules

- One issue = one comment. Never combine multiple issues in a single comment.
- Every comment MUST include: severity emoji + title, **Evidence** (file + line), **Why** (impact), and a `suggestion` block.
- Batch grep for fast pattern detection before deep reading:
  - Materials: `grep -n "m_Shader: {fileID: 0}\|{fileID: 10303}" <.mat files>`
  - Textures: `grep -n "isReadable: 1\|enableMipMap: 1\|textureCompression: 0" <.meta files>`
  - Animators: `grep -n "m_Controller: {fileID: 0}\|m_CullingMode: 0\|m_PlayOnAwake: 1" <changed files>`
  - Models: `grep -n "meshCompression: 0\|isReadable: 1\|importAnimation: 1" <.fbx .meta files>`
- Return `{ "comments": [...], "max_severity": "CRITICAL|HIGH|MEDIUM|LOW|CLEAN" }` to orchestrator.
- If no issues found, return `{ "comments": [], "max_severity": "CLEAN" }`.

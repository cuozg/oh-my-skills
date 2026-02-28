# Asset Review Workflow

### 1. Fetch PR

```bash
gh pr diff <N> --name-only   # Changed files
gh pr view <N> --json title,body,files,number  # PR context
gh pr diff <N>               # Full diff
```

Filter to asset file types listed above. If none found, APPROVE with note `No asset files to review.`

### 2. Read Files & Apply Patterns

Read changed files and their `.meta` counterparts. Apply patterns from [ASSET_PATTERNS.md](ASSET_PATTERNS.md) by file type. Batch grep for fast detection:

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
./skills/unity-shared/scripts/review/post_review.py <pr_number> /tmp/review-asset.json
```

Fallback (merged/closed): handled automatically by `post_review.py`.

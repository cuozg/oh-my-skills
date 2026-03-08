---
name: unity-review-asset
description: PR asset review — shaders, textures, animations, import settings. Triggers — 'review assets', 'asset review', 'check assets', 'shader review', 'texture review'.
metadata:
  author: kuozg
  version: "1.0"
---
# unity-review-asset

Review Unity asset files changed in a GitHub PR — `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset` — for shader issues, texture memory, animation config, and import settings.

## When to Use

- A PR adds or modifies materials, shaders, textures, animations, or FBX models
- Suspecting texture memory bloat, missing mip maps, or incorrect import settings
- Checking that animation controllers and blend trees are correctly configured

## Workflow

1. **Fetch PR** — list changed files via `gh api repos/{owner}/{repo}/pulls/{pr}/files`
2. **Filter asset files** — select `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset`
3. **Read asset files** — load raw YAML/text content; parse relevant fields
4. **Check shaders** — verify no fixed-function shaders; check for missing `_ALPHATEST_ON` guards; flag unlit shaders on opaque materials
5. **Check textures** — verify `maxTextureSize` ≤ 2048 for UI; mip maps enabled for 3D; compression format matches platform
6. **Check animations** — verify loop settings, root motion config, blend tree thresholds are non-zero
7. **Check import settings** — FBX read/write disabled unless needed; mesh compression set; animation type correct
8. **Post comments** — build payload and submit via `gh api`

## Rules

- Flag textures > 2048px on mobile platforms as WARNING
- Flag `Read/Write Enabled` on meshes as WARNING (doubles memory)
- Flag missing mip maps on world-space textures as NOTE
- Flag animation clips with `loop = false` on locomotion states as WARNING
- Flag uncompressed audio in `.meta` as WARNING
- Flag shaders referencing removed or renamed properties as CRITICAL
- Flag materials with null shader references as CRITICAL
- Flag `.anim` files with sub-1% blend tree thresholds as NOTE
- Never modify asset files — post comments only
- Use severity prefix: `[CRITICAL]`, `[WARNING]`, `[NOTE]` in every comment

## Output Format

**MANDATORY**: Use `unity-standards/references/review/pr-submission.md` as the output template — JSON payload, event decision, batching rules, and gh CLI commands. All comments MUST be submitted in a single review `POST` call following that template exactly.

Asset comments posted to the GitHub PR. Print a local summary listing flagged files and their severity.

## Standards

Load `unity-standards` for asset review criteria. Key references:

- `review/pr-submission.md` — **MANDATORY** output template: JSON payload, event decision, batching, gh CLI
- `review/asset-checklist.md` — texture, shader, animation, import settings
- `review/performance-checklist.md` — allocations, Update, physics, rendering

Load via `read_skill_file("unity-standards", "references/review/<file>")`.

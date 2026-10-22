---
name: unity-asset-generation
description: "Generate, convert, and prepare Unity assets through Unity MCP asset-generation tools. MUST use for Unity asset creation requests: sprites, sprite sheets, images, icons, placeholder art, materials, terrain layers, meshes, sounds, humanoid animations, animation clips, animator controllers, model texturing, retopology, rigging, or converting existing textures into Unity-ready assets. Distinguishes generative tools from non-generative conversion tools and validates generated assets in the Unity project. Do not use for writing runtime gameplay code, custom editor tools, UI Toolkit screens, or performance profiling."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-asset-generation

Create Unity-ready assets with Unity MCP tools, then validate existence, import, and usability.

## Escalate Instead Of This Skill
- **unity-code** — gameplay logic, asset loaders, runtime systems
- **unity-editor** — custom inspectors, windows, importers, menu tools
- **unity-uitoolkit** — runtime UI screens (not generated art)
- **unity-profiler / unity-optimize** — performance analysis

## Step 1 — Collect Inputs
Asset type · purpose (placeholder/production/UI/gameplay) · text prompt or source asset path · save path under `Assets/` · naming (PascalCase, type-based folders e.g. `Assets/Art/Sprites/`) · overwrite policy (never overwrite unless user explicitly requests).

Default folder when path missing: `Assets/Generated/<AssetType>/`.

## Step 2 — Choose Tool

### Generative (`AssetGeneration_GenerateAsset`)
| Command | Use for |
|---------|---------|
| `GenerateSprite` | transparent sprites, icons, items |
| `GenerateImage` | backgrounds, portraits, concept art |
| `GenerateSpritesheet` | multi-frame sprite sheets |
| `RemoveSpriteBackground` / `RemoveImageBackground` | transparent output |
| `UpscaleSprite` / `UpscaleImage` | higher resolution |
| `RecolorSprite` / `RecolorImage` | palette adjustments |
| `EditSpriteWithPrompt` / `EditImageWithPrompt` | prompt-driven edits |
| `GenerateMaterial` | texture-backed material |
| `AddPbrToMaterial` | add PBR maps to generated material |
| `GenerateTerrainLayer` | terrain surfaces |
| `GenerateMesh` | 3D props, characters, environments |
| `RetopologyMesh` · `TextureMesh` · `RigMesh` | post-generation mesh ops |
| `GenerateSound` | SFX, ambience, loops |
| `GenerateHumanoidAnimation` | humanoid motion clips |
| `GenerateCubemap` / `UpscaleCubemap` | skyboxes |

### Non-Generative (Conversion)
| Tool | Use for | Required Source |
|------|---------|-----------------|
| `AssetGeneration_ConvertToMaterial` | `.mat` from Texture2D/Cubemap | `referenceImagePath` |
| `AssetGeneration_ConvertToTerrainLayer` | `.terrainlayer` from Texture2D | `referenceImagePath` |
| `AssetGeneration_ConvertSpriteSheetToAnimationClip` | `.anim` from sprite sheet | `referenceImagePath` |
| `AssetGeneration_CreateAnimatorController` | `.controller` from existing clip | `animationClipPath` |
| `AssetGeneration_EditAnimationClip` | trim/loop humanoid clips | `inputAnimationClipPath` |
| `AudioClip_Edit` | trim silence/range, volume, loop | `inputAudioClipPath` |
| `ImportExternalModel` | import FBX + texture, save prefab | `FbxUrl`, `Name` |

**Do not describe conversion tools as generative — they transform existing assets.**

## Step 3 — Execute Safely
1. Confirm `savePath` under `Assets/`, doesn't already exist (unless replacement requested)
2. Use specific prompt: style, subject, view, transparency, tileability, loopability
3. Generate independent assets in parallel only when no dependencies
4. For sprites/icons → prefer transparent; if not produced, run background removal after
5. For meshes → inspect path, scale, material before placing in scenes
6. For sounds → trim silence before seamless loops
7. For animations → make stationary or trim to best loop for idle/walk/run

## Step 4 — Validate
1. Asset existence: `ManageAsset(GetInfo)` or project search
2. Import status: Unity console for errors
3. Type match: Material, TerrainLayer, AudioClip, AnimationClip, AnimatorController, Prefab, Texture2D
4. Reference check: source texture/clip assigned for converted assets
5. Console check: read errors/warnings before claiming completion

If validation fails → one targeted correction at a time (adjust prompt, path, dimensions, or command).

## Handoff
- Assets created (path + type) · Tools used (generative vs conversion) · Validation result · Follow-up recommendations

## Standards
`read_skill_file("unity-standards", "references/<path>")`:
- `other/unity-mcp-routing-matrix.md` · `code-standards/architecture-systems.md` · `optimization/memory-settings.md`

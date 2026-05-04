---
name: unity-asset-generation
description: "Generate, convert, and prepare Unity assets through Unity MCP asset-generation tools. MUST use for Unity asset creation requests: sprites, sprite sheets, images, icons, placeholder art, materials, terrain layers, meshes, sounds, humanoid animations, animation clips, animator controllers, model texturing, retopology, rigging, or converting existing textures into Unity-ready assets. Distinguishes generative tools from non-generative conversion tools and validates generated assets in the Unity project. Do not use for writing runtime gameplay code, custom editor tools, UI Toolkit screens, or performance profiling."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-asset-generation

Create Unity-ready visual, audio, animation, material, terrain, and mesh assets with Unity MCP tools, then validate that the generated or converted assets exist, import correctly, and are usable from the Unity project.

## Step 1 — Qualify the Asset Request

Use this skill when the user asks for any of these Unity assets:

| Asset need | Typical output | Primary tool path |
|------------|----------------|-------------------|
| Sprite, icon, item art, UI art, placeholder art | `.png`, optionally transparent/upscaled | `AssetGeneration_GenerateAsset` with `GenerateSprite`, then background removal or upscale when needed |
| Image, concept art, background, portrait | `.png` or other imported image asset | `AssetGeneration_GenerateAsset` with `GenerateImage` |
| Sprite sheet | sliced source texture plus generated sheet | `AssetGeneration_GenerateAsset` with `GenerateSpritesheet` |
| Material texture | `.mat` or texture-backed material | `AssetGeneration_GenerateAsset` with `GenerateMaterial`, or non-generative material conversion |
| Terrain surface | `.terrainlayer` | `AssetGeneration_GenerateAsset` with `GenerateTerrainLayer`, or non-generative terrain conversion |
| Mesh, prop, character, model | prefab/mesh/material assets | `AssetGeneration_GenerateAsset` with `GenerateMesh`, then optional model operations |
| Sound effect or loop | imported `AudioClip` | `AssetGeneration_GenerateAsset` with `GenerateSound`, then optional audio clip edits |
| Humanoid animation | `.anim` clip | `AssetGeneration_GenerateAsset` with `GenerateHumanoidAnimation` |
| Animation from sprite sheet | `.anim` clip | non-generative sprite-sheet-to-animation conversion |
| Animator controller | `.controller` | non-generative controller creation from an existing clip |

Escalate instead:

- **unity-code** — the request needs gameplay logic, asset loaders, or runtime systems.
- **unity-editor** — the request needs custom inspectors, windows, importers, or menu tools.
- **unity-uitoolkit** — the request is a runtime UI screen rather than generated UI art.
- **unity-profiler** or **unity-optimize** — the request is performance analysis or optimization.

## Step 2 — Collect Required Inputs

Before generation or conversion, establish:

- **Asset type** — sprite, image, material, terrain layer, mesh, sound, animation, controller, or conversion.
- **Purpose** — placeholder, production candidate, reference art, UI icon, gameplay prop, environment asset, or test asset.
- **Prompt or source asset** — text prompt for generative tools; existing Texture2D, Cubemap, AnimationClip, AudioClip, or mesh path for conversion/edit tools.
- **Save path** — must be under `Assets/`, with a clear extension when the tool requires one.
- **Naming** — use descriptive PascalCase or kebab-free Unity asset names, grouped by type, such as `Assets/Art/Sprites/IronSword.png`, `Assets/Art/Materials/StoneFloor.mat`, or `Assets/Art/Meshes/Crate.prefab`.
- **Overwrite policy** — never overwrite an existing asset unless the user explicitly requests replacement or regeneration.

If an asset path is missing, choose a safe default folder under `Assets/Generated/<AssetType>/` and a descriptive filename based on the asset purpose. Create folders through Unity asset tools when needed.

## Step 3 — Choose the Right MCP Tool

### Generative tools

Use `AssetGeneration_GenerateAsset` when new content should be created from a prompt or generated variation:

| Command | Use for | Key inputs |
|---------|---------|------------|
| `GenerateSprite` | transparent sprites, icons, items, simple game art | `prompt`, `savePath`, optional `width`, `height`, `modelId` |
| `GenerateImage` | backgrounds, portraits, concept art, reference images | `prompt`, `savePath`, optional dimensions/model |
| `GenerateSpritesheet` | multi-frame sprite sheets | `prompt`, `targetAssetPath` when editing, `savePath` |
| `RemoveSpriteBackground` / `RemoveImageBackground` | transparent output after sprite/image generation | `targetAssetPath` |
| `UpscaleSprite` / `UpscaleImage` | higher-resolution output | `targetAssetPath` |
| `RecolorSprite` / `RecolorImage` | palette adjustments from a reference image | `targetAssetPath`, `referenceImageInstanceId` |
| `EditSpriteWithPrompt` / `EditImageWithPrompt` | prompt-driven edits to existing assets | `targetAssetPath`, `prompt`, `savePath` when supported |
| `GenerateMaterial` | texture-backed material generation | `prompt`, `savePath`, optional composition reference |
| `AddPbrToMaterial` | add PBR maps to an existing generated material | `targetAssetPath`, `prompt` when needed |
| `GenerateTerrainLayer` | terrain surfaces | `prompt`, `savePath`, optional composition reference |
| `AddPbrToTerrainLayer` | add PBR maps to a terrain layer | `targetAssetPath` |
| `GenerateMesh` | props, characters, environmental 3D assets | `prompt`, `savePath`, optional reference images |
| `RetopologyMesh` | improve topology of an existing mesh | `targetAssetPath` |
| `TextureMesh` | texture an existing mesh | `targetAssetPath`, `prompt` and/or reference image |
| `RigMesh` | add rigging to an existing mesh | `targetAssetPath` |
| `GenerateSound` | sound effects, ambience, loops | `prompt`, `savePath`, `durationInSeconds`, `loop` |
| `GenerateHumanoidAnimation` | humanoid motion clips | `prompt`, `savePath`, `durationInSeconds`, `loop` |
| `GenerateCubemap` / `UpscaleCubemap` | skyboxes and environment maps | `prompt` or `targetAssetPath`, `savePath` |

For material and terrain generation, call the composition-pattern listing tool first when the user needs a tileable or patterned surface and no reference pattern is provided.

### Non-generative conversion tools

Use conversion tools when the user already has a source asset and wants a Unity-ready derivative without generating new content:

| Tool | Use for | Required source |
|------|---------|-----------------|
| `AssetGeneration_ConvertToMaterial` | create a `.mat` from an existing Texture2D or Cubemap | `referenceImagePath`, `savePath` |
| `AssetGeneration_ConvertToTerrainLayer` | create a `.terrainlayer` from an existing Texture2D | `referenceImagePath`, `savePath` |
| `AssetGeneration_ConvertSpriteSheetToAnimationClip` | create an `.anim` from a pre-sliced Texture2D sprite sheet | `referenceImagePath`, `savePath` |
| `AssetGeneration_CreateAnimatorController` | create a `.controller` whose default state uses an existing clip | `animationClipPath`, `savePath` |
| `AssetGeneration_EditAnimationClip` | make humanoid clips stationary or trim them to a loop | `inputAnimationClipPath`, command-specific settings |
| `AudioClip_Edit` | trim silence, trim range, change volume, or loop an audio clip | `inputAudioClipPath`, command-specific settings |
| `ImportExternalModel` | import an FBX and optional albedo texture, instantiate it, and save a prefab | `FbxUrl`, `Name`, `Height`, optional albedo texture |

Do not describe conversion tools as generative. They transform existing assets and require valid source paths.

## Step 4 — Execute Safely

1. Confirm the target `savePath` is under `Assets/` and does not already exist unless replacement was explicitly requested.
2. Use a specific prompt that names style, subject, view, resolution needs, transparency, tileability, loopability, or scale requirements.
3. Generate independent assets in parallel only when they do not depend on each other.
4. For sprites and icons, prefer transparent backgrounds; if the generation tool does not produce transparency, run background removal afterward.
5. For meshes, inspect the generated prefab path, scale, and material assignment before placing it in scenes.
6. For sounds, trim silence before making seamless loops when applicable.
7. For animations, make root motion stationary or trim to best loop when the user asks for idle, walk, run, or looping motions.
8. Do not modify scenes unless the user asked to place or preview the asset in a scene.

## Step 5 — Validate Outputs

After every generation or conversion:

1. **Asset existence** — verify the target asset exists with `ManageAsset(GetInfo)` or project asset search.
2. **Import status** — check Unity console logs for import errors, failed model imports, texture issues, or asset-generation failures.
3. **Type validation** — confirm the generated asset type matches the request, such as Material, TerrainLayer, AudioClip, AnimationClip, AnimatorController, Prefab, Texture2D, or Cubemap.
4. **Reference validation** — for converted materials/controllers/terrain layers, confirm the expected source texture or animation clip is assigned.
5. **Scene or inspector verification** — when the user asks for placement, preview, scale, or visual quality, use scene hierarchy, object component inspection, scene capture, or camera capture as appropriate.
6. **Console check** — read Unity console errors and warnings before claiming completion.

If validation fails, make one targeted correction at a time: adjust prompt, path, dimensions, model operation, conversion source, import setting, scale, or post-processing command.

## Rules

- Skill name is `unity-asset-generation`; do not rename it.
- All generated, converted, or edited Unity project assets must be saved under `Assets/`.
- Use clear asset names and type-based folders before invoking generation tools.
- Never overwrite existing assets unless the user explicitly asks for replacement.
- Distinguish generative tools from non-generative conversion/edit tools in both plan and handoff.
- Use `AssetGeneration_GetModels` when the user asks which generation models are available or when model selection affects quality.
- Use `AssetGeneration_ManageInterrupted` before restarting if a previous generation was interrupted.
- For material and terrain generation, prefer composition-pattern references when the user requests repeatable surfaces.
- For multiview mesh generation, label reference images by view such as `front`, `back`, `left`, or `right`.
- Do not claim an asset is ready until existence, import status, and relevant inspector or scene checks have passed.

## Handoff

Report:

- **Assets created** — each path and asset type.
- **Tools used** — generative versus non-generative operations.
- **Validation** — existence check, import/console result, and inspector or scene verification when relevant.
- **Follow-up** — any recommended manual art review, prompt iteration, import-setting adjustment, or prefab placement step.

## Standards

Load on demand via `read_skill_file("unity-standards", "references/<path>")`:

- `other/unity-mcp-routing-matrix.md` — MCP tool selection, Unity console checks, asset operations, and capture tools.
- `code-standards/architecture-systems.md` — Unity project organization and asset folder conventions.
- `optimization/memory-settings.md` — texture, audio, mesh, and asset lifecycle considerations when optimizing generated assets.

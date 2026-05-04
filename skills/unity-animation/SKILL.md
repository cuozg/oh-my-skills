---
name: unity-animation
description: "Create, convert, clean up, trim, loop, and wire Unity animation assets through Unity MCP tools. MUST use for sprite-sheet animation clips, humanoid animation cleanup, stationary/root-motion conversion, loop trimming, generated humanoid animation, AnimatorController creation, and validation of `.anim` or `.controller` assets. Do not use for general runtime animation code unless the task is primarily asset preparation."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-animation

Prepare Unity animation assets and controllers safely with MCP animation and asset tools.

## When to use

Use for:

- Creating `.anim` clips from pre-sliced sprite sheets.
- Generating humanoid animation clips from prompts.
- Making humanoid clips stationary by removing root motion.
- Trimming humanoid clips to their best loop section.
- Creating AnimatorController assets from existing clips.
- Validating generated `.anim` and `.controller` assets.

## Prerequisites

- Sprite-sheet conversion requires an existing pre-sliced Texture2D asset under `Assets/`.
- Humanoid clip editing only supports Unity humanoid animation clips.
- Animator controller creation requires an existing `.anim` clip path.
- Save paths must be under `Assets/` and use clear names such as `Assets/Animations/HeroIdle.anim` or `Assets/Animations/Hero.controller`.
- Do not change source animation assets unless the user explicitly asks; create derivative assets when possible.

## MCP tool usage

- Use `AssetGeneration_GenerateAsset` with `GenerateHumanoidAnimation` for prompted humanoid motion.
- Use `AssetGeneration_ConvertSpriteSheetToAnimationClip` for sprite-sheet-to-clip conversion.
- Use `AssetGeneration_CreateAnimatorController` to create a controller with a clip as the default state.
- Use `AssetGeneration_EditAnimationClip` with `MakeStationary` for stationary humanoid clips.
- Use `AssetGeneration_EditAnimationClip` with `TrimToBestLoop` for loop trimming.
- Use `ManageAsset(GetInfo/Search)` to validate created clips and controllers.
- Use `ReadConsole` or `GetConsoleLogs` after generation, conversion, or controller creation.

## Execution rules

1. Confirm source and output paths before asset operations.
2. Verify source assets exist and match tool requirements.
3. Prefer new output assets over overwriting source clips.
4. Use descriptive clip/controller names that include character, action, and loop/stationary status when relevant.
5. Only place or preview animations in a scene if the user asks.

## Validation

Verify:

- `.anim` or `.controller` asset exists at the requested path.
- Source sprite sheet, humanoid clip, or input clip was valid.
- AnimatorController default state references the intended clip.
- Loop/stationary edits were applied to the intended humanoid clip derivative.
- Unity console contains no animation import, asset generation, or controller errors.
- Scene or inspector verification is performed when the user asks for visual confirmation.

## Boundaries

- Delegate runtime animation state-machine code to `unity-code`.
- Delegate custom animation editor tooling to `unity-editor`.
- Delegate generated sprites or meshes to `unity-asset-generation` when animation is not the main task.

## Handoff

Report asset paths, source paths, tools used, whether operations were generative or conversion/edit operations, and validation evidence.

---
name: unity-audio
description: "Generate, edit, clean up, loop, normalize-by-factor, and validate Unity AudioClip assets with Unity MCP tools. MUST use for placeholder SFX, music loops, ambience loops, trimming silence, trimming ranges, volume changes, loop processing, and audio asset preparation. Do not use for gameplay audio systems or mixer code unless the work is primarily AudioClip preparation."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-audio

Prepare Unity audio assets with generation, editing, and validation steps.

## When to use

Use for:

- Placeholder SFX, ambience, UI sounds, and short music loops.
- Generating AudioClip assets from prompts.
- Trimming silence from generated or imported clips.
- Trimming a clip to an exact time range.
- Changing volume by an explicit factor.
- Creating seamless loops from an existing AudioClip.
- Validating generated or edited AudioClip assets.

## Required inputs

- Source path for edits, such as `Assets/Audio/Raw/Impact.wav`.
- Output path or clear replacement instruction for destructive or transformative edits.
- Duration and loop intent for generated sounds.
- Start/end times for range trimming.
- Volume factor for volume changes.

Do not apply volume or loop changes without clear user intent.

## MCP tool usage

- Use `AssetGeneration_GenerateAsset` with `GenerateSound` for prompted sound generation.
- Use `AudioClip_Edit` with `TrimSilence` before loop processing when source clips have leading or trailing silence.
- Use `AudioClip_Edit` with `TrimSound` for explicit start/end range trimming.
- Use `AudioClip_Edit` with `ChangeVolume` for explicit volume-factor changes.
- Use `AudioClip_Edit` with `LoopSound` after silence trimming when a seamless loop is requested.
- Use `ManageAsset(GetInfo/Search)` to validate AudioClip existence and type.
- Use `ReadConsole` or `GetConsoleLogs` after generation or edits.

## Recommended order

1. Verify the source AudioClip exists.
2. Trim silence if the clip will be looped or if silence cleanup was requested.
3. Trim to the requested time range if needed.
4. Adjust volume only with explicit factor or target intent.
5. Create a seamless loop last, after silence and range edits.
6. Validate the output asset and console state.

## Safety rules

- Require explicit source and output paths for destructive or transformative edits.
- Prefer creating a new edited asset over overwriting source audio.
- Keep generated audio under `Assets/Audio/Generated/` or a user-provided `Assets/` path.
- Do not infer licensing or production readiness from generated placeholder audio.

## Validation

Verify:

- AudioClip asset exists at the output path.
- Unity imports it as an AudioClip.
- Console has no import, generation, or audio processing errors.
- Looping, trim range, duration, and volume intent are reflected in the operation performed.
- Any remaining manual listening check is clearly called out.

## Boundaries

- Delegate runtime audio playback, mixers, event systems, or settings UI to `unity-code` or `unity-uitoolkit`.
- Delegate mobile audio build issues to `unity-mobile` or `unity-build-pipeline`.

## Handoff

Report source path, output path, tool commands used, edit order, validation result, and whether a manual listen pass is still recommended.

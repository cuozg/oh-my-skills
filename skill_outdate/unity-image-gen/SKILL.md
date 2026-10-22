---
name: unity-image-gen
description: "Generate Unity raster image assets through Unity MCP: game sprites, item art, backgrounds, UI icons, portraits, concept images, transparent cutouts, image edits, upscales, background removal, and Unity scene or Game View screenshots. Use when a Unity project needs image files imported under Assets or screenshots captured from the editor. Do not use for meshes, audio, animation, materials, gameplay code, UI Toolkit layout, or generic non-Unity image generation."
metadata:
  author: kuozg
  version: "1.0"
---

# unity-image-gen

Generate Unity-ready raster images and screenshots through Unity MCP, then verify that the files exist, import cleanly, and are usable in the project.

This is the Unity-specific image workflow. Use it when the output belongs in a Unity project or must be captured from Unity. For non-Unity bitmap work, use `imagegen`. For broader Unity asset types such as meshes, audio, animations, terrain layers, or PBR material pipelines, use `unity-asset-generation`.

## Scope

Use this skill for:
- 2D game assets: sprites, item art, pickups, ability icons, portraits, cards, decals, UI art.
- Backgrounds: menu backgrounds, loading screens, splash art, parallax layers, environment plates.
- Icons: app icons, achievement badges, shop icons, inventory icons, skill icons.
- Image edits: recolor, upscale, remove background, prompt-based edits to an existing image.
- Screenshots: Game View, camera, Scene View, multiview, orbit, or surround captures through Unity MCP.

Do not use this skill for:
- Runtime gameplay code, editor windows, UI Toolkit layout, scene construction, or tests.
- Meshes, rigs, animations, terrain layers, audio clips, or material authoring beyond image texture files.
- Generic images that are not intended to be imported into a Unity project.
- Vector/SVG asset systems where deterministic repo-native editing is better.

## Assumptions

- A Unity project is open and reachable through Unity MCP.
- Final generated image assets should live under `Assets/`.
- Existing files are not overwritten unless the user explicitly asks for replacement.
- If the user does not specify a folder, save under `Assets/Generated/Images/<asset-type>/`.
- If exact style, size, or platform constraints are missing and do not block the work, choose conservative game-ready defaults and state them in the handoff.

Ask before proceeding only when a missing detail affects the generated file contract: overwrite permission, target path outside `Assets/`, required exact text, platform icon size, or whether a screenshot should come from Game View, Scene View, or a specific camera.

## Workflow

1. Define the asset contract:
   - asset kind: sprite, background, icon, portrait, edit, screenshot.
   - intended use: placeholder, production, UI, gameplay, store art, documentation.
   - save path under `Assets/`.
   - dimensions or aspect ratio.
   - transparency requirement.
   - overwrite policy.
2. Inspect current Unity state when needed:
   - use `manage_scene` for loaded scenes and hierarchy context.
   - use `manage_camera` with `list_cameras` or screenshot actions for camera-dependent captures.
   - use `manage_asset` search/get_info to avoid collisions and verify existing references.
3. Build a concise image prompt from the user's request.
4. Execute through Unity MCP:
   - use project asset-generation custom tools for image creation and editing when available.
   - use `manage_camera` for screenshots and multiview captures.
   - use `manage_asset` for import, search, and metadata verification.
   - use `refresh_unity` after filesystem-visible asset changes.
   - use `read_console` to check import or generation errors.
5. Validate the result before claiming completion:
   - file exists under `Assets/`.
   - Unity imports it as the expected type, usually `Texture2D` or `Sprite`.
   - transparent assets have alpha where expected.
   - screenshots are nonblank and from the intended source.
   - Unity console has no new relevant errors.
6. Report paths, tools used, prompt, assumptions, and validation evidence.

## Tool Routing

Prefer Unity MCP asset-generation tools exposed by the project. Common commands may include:

| Need | Preferred Unity MCP command |
| --- | --- |
| Sprite, item art, transparent icon | `GenerateSprite` |
| Background, splash, portrait, concept image | `GenerateImage` |
| Sprite sheet | `GenerateSpritesheet` |
| Remove sprite background | `RemoveSpriteBackground` |
| Remove image background | `RemoveImageBackground` |
| Upscale sprite | `UpscaleSprite` |
| Upscale image | `UpscaleImage` |
| Recolor sprite | `RecolorSprite` |
| Recolor image | `RecolorImage` |
| Prompt edit of a sprite | `EditSpriteWithPrompt` |
| Prompt edit of an image | `EditImageWithPrompt` |
| Game View or camera screenshot | `manage_camera` screenshot |
| Scene View documentation screenshot | `manage_camera` screenshot with `capture_source='scene_view'` |
| Orbit or surround contact sheet | `manage_camera` screenshot with batch options |

If the asset-generation tool is exposed only through custom tools, call it with `execute_custom_tool` and the project-specific parameters. If no Unity MCP image-generation capability is available, state that Unity-side generation is unavailable and ask whether to fall back to the generic `imagegen` skill; do not silently switch.

## Prompt Contract

Use the minimum structured prompt needed for a good game asset:

```text
Use case: <sprite | background | icon | portrait | edit | screenshot>
Unity asset type: <Texture2D | Sprite | screenshot PNG>
Primary request: <user request>
Intended use: <where this appears in the game>
Style: <art direction>
Composition: <view, framing, padding, silhouette>
Lighting and color: <mood, contrast, palette>
Transparency: <opaque | transparent alpha | removable background>
Dimensions: <width x height or aspect ratio>
Constraints: <must keep, must avoid, exact text>
Save path: <Assets/...>
```

Keep augmentation conservative:
- Add framing, padding, and silhouette guidance for sprites and icons.
- Add safe negative space only when a UI background or loading image needs it.
- Do not invent characters, logos, brand text, or story details.
- Quote exact text and require verbatim rendering when text is part of the asset.
- For edits, list invariants: what changes and what must remain unchanged.

## Defaults By Asset Type

### Sprites and Item Art

- Save path: `Assets/Generated/Images/Sprites/<Name>.png`.
- Prefer transparent alpha.
- Use centered composition, clean silhouette, full object visible, generous padding.
- Avoid cast shadows unless the target art style requires them.
- After import, verify sprite usability. If needed, set importer metadata through Unity MCP or report that sprite import settings need adjustment.

### UI Icons

- Save path: `Assets/Generated/Images/Icons/<Name>.png`.
- Default size: square, power-of-two when the generator supports it.
- Prompt for legibility at small sizes, strong silhouette, limited detail, no background unless requested.
- Avoid text in icons unless the user provides exact text.
- Validate against transparent corners and readable shape.

### Backgrounds

- Save path: `Assets/Generated/Images/Backgrounds/<Name>.png`.
- Preserve the requested aspect ratio. If missing, choose the target UI orientation:
  - landscape game/menu: `16:9`.
  - portrait mobile: `9:16`.
  - square card or tile: `1:1`.
- Include safe negative space only if UI overlay is expected.
- Avoid watermarks, logos, and unreadable pseudo-text.

### Screenshots

- Save path: `Assets/Screenshots/` unless the user names another project folder.
- Use `manage_camera`:
  - Game View or full UI: omit `camera` when overlay UI must be visible.
  - Specific viewpoint: specify `camera` or `view_position` / `view_rotation`.
  - Scene documentation: set `capture_source='scene_view'`.
  - Inspection sets: use `screenshot_multiview` or screenshot batch options.
- Validate that the capture is nonblank, framed on the intended object or scene, and saved at the reported path.

### Existing Image Edits

- Read or inspect the source asset first.
- Save non-destructively with a suffix unless replacement is explicitly requested.
- Prompt with clear invariants: preserve subject, perspective, canvas size, and transparent areas unless the user requests otherwise.
- Verify the edited asset imports cleanly and the original remains intact.

## Transparent Assets

Prefer native transparent sprite/image generation through Unity MCP when available. If the generated file has an unwanted flat background, run the Unity MCP background removal command for the asset type.

For transparent sprites and icons:
- Request transparent alpha directly.
- Keep subject separated from edges with padding.
- Avoid glow, soft shadows, glass, smoke, hair-like edges, and fine particles unless the user explicitly wants them.
- Verify transparent corners or alpha channel after import.

If Unity MCP cannot produce or remove transparency, ask before falling back to generic image generation or local chroma-key processing.

## Path And Overwrite Rules

- Require final project assets under `Assets/`.
- Never leave a Unity-consumed asset only in a temp folder or external generated-images directory.
- Before generating, check whether the target path exists.
- If the path exists and the user did not request replacement, create a versioned sibling such as `<Name>-v2.png`.
- Use descriptive PascalCase filenames for Unity assets unless the project uses another convention.
- Keep discarded drafts out of `Assets/` unless the user asks to keep variants.

## Validation Checklist

Before final response:
- `manage_asset` search or get_info confirms the output path.
- Unity import type matches the intended asset.
- `refresh_unity` completed if a file was created or moved.
- `read_console` has no relevant import, generation, or serialization errors.
- For screenshots, captured image is nonblank and from the expected source.
- For transparent assets, alpha exists and corners/background are transparent.
- For exact text, inspect the output; if text is wrong, either regenerate once with stronger text constraints or report the limitation.

## Handoff Format

Report:
- Created files with Unity paths.
- Asset type and intended use.
- Unity MCP tool or custom tool used.
- Final prompt or screenshot capture parameters.
- Validation evidence.
- Any assumptions or limitations that remain.

Keep the response concise. Do not claim production readiness unless the generated asset was visually inspected and the Unity import state was verified.

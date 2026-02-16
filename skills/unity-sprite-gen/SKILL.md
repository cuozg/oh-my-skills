---
name: unity-sprite-gen
description: "Generate 2D sprite and icon assets for Unity games using AI image generation (CoPlay MCP). Creates game-ready sprites with transparent backgrounds, power-of-2 sizing, and auto-configured Unity import settings. Supports icons, characters, environment tiles, UI elements, and VFX sprites. Use when (1) Creating placeholder or production sprite assets, (2) Generating item/weapon/skill icons, (3) Building character portrait sprites, (4) Creating tileable environment textures, (5) Generating UI element graphics, (6) Batch generating sprite sets with consistent style. Triggers: 'generate sprite', 'create icon', 'sprite asset', 'game icon', '2D asset', 'generate texture', 'item icon', 'character sprite', 'tile texture', 'UI graphic', 'sprite generation', 'asset sprite'."
---

# Unity Sprite Generator

Generate game-ready 2D sprite assets using CoPlay MCP's AI image generation, with automatic Unity TextureImporter configuration.

## Input

User describes the sprite(s) needed: type, style, size, quantity, and art direction.

## Output

- PNG sprite file(s) in the Unity Assets folder with transparent backgrounds
- Unity TextureImporter auto-configured (Sprite mode, filter, compression, power-of-2)
- Organized in `Assets/_Project/Textures/Generated/` (or user-specified path)

## Workflow

### Step 1: Gather Requirements

Determine from user request:
- **Category**: icon, character, environment, UI, VFX (affects prompt template)
- **Style**: pixel-art, stylized, realistic, toon, low-poly-render (affects prompt engineering)
- **Size**: 64, 128, 256, 512 (power-of-2, default 256 for icons, 512 for characters)
- **Count**: single or batch (batch = consistent style across set)
- **Save path**: default `Assets/_Project/Textures/Generated/{Category}/`

If unclear, ask ONE question covering missing info. Default to: stylized, 256px, transparent bg.

### Step 2: Engineer the Prompt

Build the image generation prompt following these rules:

**Prompt Structure** (ALWAYS follow this order):
```
{subject description}, {art style}, {view/angle}, {background instruction}, {technical constraints}
```

**Mandatory Suffixes** (append to ALL prompts):
- `on a solid transparent background` or `isolated on transparent background`
- `clean edges, no artifacts`
- `game asset, sprite sheet ready`
- `centered composition`

**Category-Specific Templates** — Load from `references/prompt-templates.md`.

### Step 3: Generate the Image

Use `coplay-mcp_generate_or_edit_images` with these settings:

```
provider: gpt_image_1 (default) or gemini (for higher detail)
format: png (ALWAYS — required for transparency)
transparent_background: true (ALWAYS)
quality: high (for production) or medium (for placeholders)
size: auto (let provider choose best)
save_path: Assets/_Project/Textures/Generated/{Category}/{filename}.png
```

**Object Size Mapping** (use `object_size` parameter):
| Target Size | object_size | scale_mode |
|:---|:---|:---|
| 64x64 | "64,64" | fit_canvas |
| 128x128 | "128,128" | fit_canvas |
| 256x256 | "256,256" | fit_canvas |
| 512x512 | "512,512" | fit_canvas |

### Step 4: Configure Unity Import Settings

After generation, run the TextureImporter configuration script via `coplay-mcp_execute_script`:

```
filePath: Assets/_Project/Scripts/Editor/SpriteImportConfigurator.cs
arguments: {"path": "<generated_sprite_path>", "spriteMode": "single", "pixelsPerUnit": 100, "filterMode": "Bilinear", "maxSize": 256, "compression": "Normal"}
```

**Parameter Defaults by Category**:
| Category | spriteMode | pixelsPerUnit | filterMode | maxSize | compression |
|:---|:---|:---|:---|:---|:---|
| Icon | single | 100 | Bilinear | 256 | Normal |
| Character | single | 100 | Bilinear | 512 | Normal |
| Environment | single | 100 | Point | 256 | Normal |
| UI | single | 100 | Bilinear | 512 | High |
| VFX | single | 100 | Bilinear | 256 | Low |

For **pixel-art style**, ALWAYS override filterMode to `Point` and compression to `None`.

### Step 5: Verify

1. Confirm the file exists at the save path
2. Report: filename, dimensions, file size, import settings applied
3. If batch: list all generated files

## Batch Generation

For sets (e.g., "generate 6 potion icons"):

1. Create a naming convention: `{category}_{name}_{variant}.png`
   - Example: `icon_potion_health.png`, `icon_potion_mana.png`
2. Generate each with consistent style prompt prefix
3. Apply same import settings to all
4. Report summary table:

```
| # | File | Size | Status |
|---|------|------|--------|
| 1 | icon_potion_health.png | 256x256 | OK |
| 2 | icon_potion_mana.png | 256x256 | OK |
```

## Style Consistency

When generating multiple sprites in a set, prefix ALL prompts with a **style anchor**:

```
Style: {art_style}, {color_palette}, {outline_style}, {shading_style}
```

**Example Style Anchors**:
- Stylized RPG: `stylized hand-painted, vibrant saturated colors, dark outline, soft cel shading`
- Pixel Art: `pixel art 16-bit style, limited palette, no outline, flat shading`
- Toon: `cartoon style, bright primary colors, thick black outline, flat fill`
- Realistic: `semi-realistic painted, muted natural colors, no outline, soft gradient shading`

## Error Handling

- **Generation fails**: Retry once with simplified prompt. If still fails, report error.
- **Wrong size**: Re-generate with explicit `object_size` parameter.
- **Bad transparency**: Add `isolated object, no background elements, pure transparent` to prompt.
- **Inconsistent style in batch**: Prepend identical style anchor to every prompt in the set.

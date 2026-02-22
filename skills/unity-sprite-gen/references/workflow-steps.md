# Workflow Steps 2-5: Prompt Engineering, Generation, Import Configuration

## Step 2: Engineer the Prompt

Build image generation prompt following this structure:

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

## Step 3: Generate the Image

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

## Step 4: Configure Unity Import Settings

After generation, run TextureImporter configuration script via `coplay-mcp_execute_script`:

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

## Step 5: Verify

1. Confirm the file exists at the save path
2. Report: filename, dimensions, file size, import settings applied
3. If batch: list all generated files

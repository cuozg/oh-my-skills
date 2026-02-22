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

### Step 2-5: Detailed Workflow

Full instructions for prompt engineering, image generation, import configuration, and verification in [workflow-steps.md](references/workflow-steps.md).

## Batch Generation, Style Consistency, Error Handling

When generating sprite sets or handling edge cases, see [batch-and-style.md](references/batch-and-style.md) for:
- Batch naming and generation strategies
- Style anchors for consistency across sets
- Error handling and recovery procedures

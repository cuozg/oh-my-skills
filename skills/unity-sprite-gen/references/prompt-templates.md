# Prompt Templates for Sprite Generation

Load this file when constructing image generation prompts. Each category has a base template and example expansions.

## Template Structure

Every prompt follows: `{subject}, {style}, {view}, {background}, {technical}`

---

## Icons (Items, Skills, Equipment)

**Base Template:**
```
{item_description}, {art_style}, front-facing view, isolated on transparent background, clean edges no artifacts, game asset sprite sheet ready, centered composition, {size}x{size} pixels
```

**Examples:**
- `a glowing red health potion in a glass flask, stylized hand-painted vibrant colors dark outline cel shading, front-facing view, isolated on transparent background, clean edges no artifacts, game asset sprite sheet ready, centered composition`
- `a legendary golden sword with blue gem in hilt, stylized hand-painted vibrant colors dark outline cel shading, front-facing view, isolated on transparent background, clean edges no artifacts, game asset sprite sheet ready, centered composition`
- `a wooden treasure chest slightly open with gold coins, stylized hand-painted vibrant colors dark outline cel shading, three-quarter view, isolated on transparent background, clean edges no artifacts, game asset sprite sheet ready, centered composition`
- `a purple magic scroll with glowing runes, stylized hand-painted vibrant colors dark outline cel shading, front-facing view, isolated on transparent background, clean edges no artifacts, game asset sprite sheet ready, centered composition`

**Skill Icon Variant:**
```
{skill_effect_description} inside a {shape} frame, {art_style}, front-facing flat design, isolated on transparent background, clean edges no artifacts, game icon, centered composition
```

---

## Characters (Heroes, Enemies, NPCs)

**Base Template:**
```
{character_description}, {art_style}, {pose} pose, full body visible, isolated on transparent background, clean edges no artifacts, game character sprite, centered composition
```

**Examples:**
- `a heroic female archer with green hood and quiver, stylized low-poly toon shading, idle standing pose, full body visible, isolated on transparent background, clean edges no artifacts, game character sprite, centered composition`
- `a skeleton warrior with rusted sword and shield, stylized dark fantasy toon shading, combat ready pose, full body visible, isolated on transparent background, clean edges no artifacts, game character sprite, centered composition`
- `a friendly merchant NPC with large backpack and hat, stylized cartoon bright colors, welcoming pose, full body visible, isolated on transparent background, clean edges no artifacts, game character sprite, centered composition`

**Portrait Variant (for UI):**
```
{character_description} portrait, {art_style}, face and shoulders visible, slight three-quarter angle, isolated on transparent background, clean edges, game UI portrait, centered composition
```

---

## Environment (Tiles, Decorations, Obstacles)

**Base Template:**
```
{environment_object}, {art_style}, top-down three-quarter isometric view, isolated on transparent background, clean edges no artifacts, game environment asset, centered composition
```

**Examples:**
- `a stone dungeon floor tile with cracks and moss, stylized low-poly hand-painted, top-down view, isolated on transparent background, clean edges no artifacts, tileable game asset, centered composition`
- `a wooden barrel with metal bands, stylized hand-painted vibrant colors, three-quarter isometric view, isolated on transparent background, clean edges no artifacts, game prop asset, centered composition`
- `a glowing magical crystal formation blue and purple, stylized fantasy art, three-quarter view, isolated on transparent background, clean edges no artifacts, game decoration asset, centered composition`

**Tileable Variant:**
```
{surface_description}, {art_style}, top-down view, seamless tileable texture, isolated on transparent background, clean edges, game tile asset
```

---

## UI Elements (Buttons, Frames, Backgrounds)

**Base Template:**
```
{ui_element_description}, {art_style}, flat front-facing view, isolated on transparent background, clean edges no artifacts, mobile game UI element, centered composition
```

**Examples:**
- `a fantasy-themed button frame with golden ornate border, stylized medieval game UI, flat front-facing view, isolated on transparent background, clean edges no artifacts, mobile game UI element, centered composition`
- `a health bar frame with red heart emblem on left, stylized cartoon game UI, flat front-facing horizontal, isolated on transparent background, clean edges no artifacts, mobile game UI element`
- `a rounded dialog box frame with parchment texture, stylized RPG game UI, flat front-facing view, isolated on transparent background, clean edges no artifacts, mobile game UI element, centered composition`
- `a star rating icon 5 stars in a row, stylized golden metallic, flat front-facing view, isolated on transparent background, clean edges, game UI icon`

## Advanced Techniques

For style anchor presets, batch generation patterns, seasonal variants, and negative prompt guidance, see prompt-templates-advanced.md.

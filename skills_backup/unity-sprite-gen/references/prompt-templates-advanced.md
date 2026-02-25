# Prompt Templates - Advanced & Custom Generation

## Batch Generation Strategy

### Style Consistency Across Asset Set

When generating a full game's assets, use a **master style anchor**:

```
Master Style: "stylized hand-painted vibrant colors dark outline cel shading"
```

Then variations:
- **Icons**: `{item}, master_style, front-facing view, centered, transparent`
- **Characters**: `{char}, master_style, idle pose, full body, centered, transparent`
- **Environment**: `{obj}, master_style, isometric view, centered, transparent`

### Seasonal Variants

For game seasons with color themes:

**Winter Season**:
```
{base_description}, stylized hand-painted with cool icy blues and whites, dark outline cel shading, front-facing view, isolated on transparent background
```

**Fire Season**:
```
{base_description}, stylized hand-painted with warm oranges and reds, dark outline cel shading, front-facing view, isolated on transparent background
```

## Advanced Customization

### Lighting Direction Control

```
{description}, professional digital painting, single light source from top-left, dramatic shadows, no background, game asset
```

### Texture & Surface Detail

```
{description}, weathered metal texture with rust and scratches, stylized painting, front-facing view, transparent background
```

### Emotional Tone Modifiers

- "Menacing": Add "angry expression, sharp features, dark color palette"
- "Cute": Add "round proportions, soft colors, sweet expression"
- "Majestic": Add "ornate details, gold accents, noble bearing"

## Quality Control Checklist

After generation:
- [ ] Transparent background complete (no artifacts at edges)
- [ ] Object centered in frame
- [ ] No text, watermarks, or signatures
- [ ] Art style matches master anchor
- [ ] File size reasonable (< 500KB for icon, < 2MB for character)
- [ ] Color palette within expected range

# Batch Generation, Style Consistency, Error Handling

## Batch Generation

For sets (e.g., "generate 6 potion icons"):

1. Create naming convention: `{category}_{name}_{variant}.png`
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

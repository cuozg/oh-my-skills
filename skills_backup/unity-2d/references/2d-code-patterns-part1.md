# 2D Code Patterns & Project Setup

## Project Setup

### Sorting Layers (Back to Front)
```
Background → Midground → Default → Foreground → UI
Priority: Sorting Layer > Order in Layer > Z position
```

### Sprite Import Settings

| Art Style | Filter | Compression | PPU | Max Size |
|:--|:--|:--|:--|:--|
| Pixel 16x16 | Point | None | 16 | 256–512 |
| Pixel 32x32 | Point | None | 32 | 512–1024 |
| HD hand-drawn | Bilinear | ASTC 6x6 / BC7 | 100 | 2048–4096 |
| Vector-style | Bilinear | ASTC 4x4 / BC7 | 100 | 2048 |

Sprite sheet: Mode=Multiple, Mesh=FullRect (pixel) or Tight (HD), Generate Physics Shape=Yes.

## Key Patterns

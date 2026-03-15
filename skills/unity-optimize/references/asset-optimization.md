# Asset Optimization Patterns

## Texture Optimization

### Size Audit Checklist

| Asset Type | Max Recommended Size | Notes |
|-----------|---------------------|-------|
| UI Icons | 128-256px | Power-of-2 not required for UI |
| UI Backgrounds | 512-1024px | Tile or 9-slice when possible |
| Character textures | 1024-2048px | Multiple maps: albedo + normal + mask |
| Environment props | 512-1024px | Atlas shared textures for batching |
| Terrain splat maps | 512-1024px | More layers = more draw calls |
| Skybox | 2048-4096px | Procedural skybox saves memory |

### Import Settings Quick Fixes

```
For each texture, verify:
- [ ] Max Size matches actual display size (not default 2048)
- [ ] Read/Write Enabled: OFF (doubles memory when ON)
- [ ] Generate Mip Maps: ON for 3D world, OFF for UI/2D sprites
- [ ] Compression: platform-appropriate (ASTC for mobile, BC7 for PC)
- [ ] sRGB: ON for color, OFF for data textures (normal, mask)
- [ ] Alpha Source: None if texture has no transparency
```

### Memory Impact

```
Uncompressed RGBA32: width × height × 4 bytes
ASTC 6×6:            width × height × 3.56 bpp / 8
BC7/DXT5:            width × height × 8 bpp / 8

Example 2048×2048:
  RGBA32 = 16 MB (uncompressed)
  BC7    = 4 MB
  ASTC   = 1.8 MB
```

## Audio Optimization

### Load Type Decision Tree

```
Duration < 1 second?     → Decompress On Load (fast playback, small memory)
Duration 1-10 seconds?   → Compressed In Memory (Vorbis Q=70)
Duration > 10 seconds?   → Streaming (minimal memory footprint)
Music/Ambient?           → Streaming always
```

### Quick Wins

- [ ] Force Mono on SFX (50% memory reduction, barely noticeable)
- [ ] Sample Rate: 22050 Hz for SFX, 44100 Hz only for music
- [ ] Compression Quality: 50-70 for SFX, 70-80 for music
- [ ] Preload Audio Data: OFF for streaming, ON for decompress-on-load

## Mesh Optimization

### Import Settings

- [ ] Mesh Compression: Low-Medium for static (Off for animated — prevents artifacts)
- [ ] Read/Write Enabled: OFF (halves runtime memory)
- [ ] Optimize Mesh Data: ON in Player Settings (strips unused vertex channels)
- [ ] Import Normals: Only if shader uses them
- [ ] Import Tangents: Only if using normal maps
- [ ] Index Format: 16-bit if mesh < 65K vertices

### LOD Budget Guidelines

| LOD Level | Triangle Count | Screen % |
|-----------|---------------|----------|
| LOD0 | Full mesh | > 50% |
| LOD1 | 50% of LOD0 | 25-50% |
| LOD2 | 25% of LOD0 | 10-25% |
| LOD3/Cull | 10% or culled | < 10% |

## Animation Optimization

- [ ] Anim Compression: Optimal (Unity auto-selects best)
- [ ] Remove unused curves (scale curves on non-scaled bones)
- [ ] Reduce keyframe density for subtle animations
- [ ] Disable "Resample Curves" if animation was authored at target frame rate

## Shader Optimization

- [ ] Strip unused shader variants (shader_feature vs multi_compile)
- [ ] Limit multi_compile keywords — each doubles variant count
- [ ] Remove unused passes (e.g., Meta pass if no lightmapping)
- [ ] Use shader LOD for mobile fallbacks

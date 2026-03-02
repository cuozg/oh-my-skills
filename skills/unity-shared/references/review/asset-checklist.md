# Asset Review Checklist

## Textures

- [ ] Max size appropriate: mobile ≤1024, desktop ≤2048, UI ≤512
- [ ] Power-of-two dimensions for tiling textures
- [ ] Compression format set per platform (ASTC mobile, BC7 desktop)
- [ ] Mipmaps enabled for 3D textures, disabled for UI sprites
- [ ] Read/Write disabled (halves memory) unless CPU access needed
- [ ] sRGB enabled for color textures, disabled for data (normal maps)

| Use Case | Format | Max Size | Mipmaps |
|----------|--------|----------|---------|
| 3D diffuse | ASTC/BC7 | 2048 | On |
| Normal map | ASTC/BC5 | 2048 | On |
| UI sprite | ASTC/BC7 | 512 | Off |
| Lightmap | ASTC/BC6H | 1024 | Off |

## Shaders

- [ ] Variant count checked (`#pragma multi_compile` explosion)
- [ ] No unnecessary passes (shadow, depth, forward)
- [ ] Mobile: no complex math in fragment shader
- [ ] Shader errors/warnings clean in console
- [ ] Fallback shader specified for unsupported platforms

## Animation

- [ ] Rig type matches model (Generic vs Humanoid)
- [ ] Compression set to Optimal or Keyframe Reduction
- [ ] Unnecessary curves removed (scale if unused)
- [ ] Anim events reference existing methods
- [ ] Loop time set correctly for looping clips

## Audio

| Type | Load Type | Compression |
|------|-----------|-------------|
| Short SFX (<1s) | Decompress On Load | PCM or ADPCM |
| Medium SFX (1-5s) | Compressed In Memory | Vorbis |
| Music/Ambient | Streaming | Vorbis/AAC |
| Voice lines | Compressed In Memory | Vorbis |

- [ ] Force Mono for non-spatial SFX (halves memory)
- [ ] Sample rate override: 22050 Hz for SFX, 44100 Hz for music
- [ ] Preload Audio Data off for large files (load on demand)

## Mesh

- [ ] Read/Write disabled unless runtime mesh modification needed
- [ ] Normals: Import for lit meshes, None for particles
- [ ] Tangents: Import only if normal maps used
- [ ] Mesh Compression: Low-Medium for static props
- [ ] LOD groups configured for high-poly meshes (>5k tris)

## Materials

- [ ] No runtime `Renderer.material` access (creates instance — use `sharedMaterial`)
- [ ] `MaterialPropertyBlock` for per-instance variation
- [ ] Unused material properties removed
- [ ] GPU Instancing enabled where applicable

## Missing References

- [ ] No `Missing (Mono Script)` on any prefab/scene object
- [ ] No broken material/texture/mesh references
- [ ] No missing sprite references in UI
- [ ] Addressable assets have valid addresses
- [ ] Asset bundle dependencies resolved

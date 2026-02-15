# Asset Review — Materials, Textures, Animation, Audio

Load when PR modifies `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, or audio files. Every issue MUST have **Issue + Why + Suggestion**.

## 🔴 Critical — Materials

| Pattern | Issue | Fix |
|:--------|:------|:----|
| `m_Shader: {fileID: 0}` | Pink/magenta at runtime | Assign correct shader |
| `{fileID: 10303}` in m_Materials | Default Unity material | Assign project material |
| Custom shader not in Always Included & no scene ref | Pink in builds only | Add to Always Included or ensure ref chain |

## 🟡 Major

**Materials**: `renderer.material` instead of `sharedMaterial` → leak. Unused `multi_compile` → build size. Desktop shader on mobile → fail. `_MainTex` vs `_BaseMap` (URP) mismatch.

**Textures (.meta)**:

| Meta Pattern | Issue | Fix |
|:-------------|:------|:----|
| `isReadable: 1` | Doubles memory | Disable unless GetPixels needed |
| `enableMipMap: 1` on UI sprite | +33% memory | Disable |
| `textureCompression: 0` / RGBA32 mobile | 4x+ memory | ASTC (iOS), ETC2 (Android) |
| NPOT dimensions | Can't compress | Resize to POT |
| 4096 for small asset | Wastes VRAM | Match maxTextureSize to display size |

**Animation**: Empty `m_Controller` → assign or remove. `CullingMode: 0` → CullCompletely. `WriteDefaultValues: 1` → disable. Unintended `ApplyRootMotion` → disable. Pause-immune UI → UnscaledTime.

**Audio**: Unintended `PlayOnAwake` → disable. `SpatialBlend: 1` on UI → set 2D. Large clip uncompressed → Streaming+Vorbis. `loadInBackground: 0` on large clips → enable.

**Components**: Camera depth conflicts, light shadow resolution `-1`, ParticleSystem `prewarm: 1` on heavy system, NavMeshAgent on disabled GO.

## 🔵 Minor

Tiling/offset mismatch, render queue override, maxTextureSize > source, wrong filterMode pixel art, missing sprite atlas tag, redundant animator layers, default audio import settings.

## Grep

```bash
# Materials — missing shader / default material
grep -n "m_Shader: {fileID: 0}\|{fileID: 10303}" <changed .mat/.asset files>
# Textures — memory issues
grep -n "isReadable: 1\|enableMipMap: 1\|textureCompression: 0" <changed .meta files>
# Animator/Audio in prefabs
grep -n "m_Controller: {fileID: 0}\|m_CullingMode: 0\|m_PlayOnAwake: 1" <changed .prefab/.unity files>
```

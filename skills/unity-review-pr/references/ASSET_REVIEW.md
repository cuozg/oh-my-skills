# Asset Review — Materials, Textures, Animation, Audio, Models

Load when PR modifies `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, `.fbx`, `.asset`, or audio files. Every issue MUST have **Issue + Why + Suggestion**.

## 🔴 Critical — Materials & Shaders

| Pattern | Issue | Fix |
|:--------|:------|:----|
| `m_Shader: {fileID: 0}` | Pink/magenta at runtime | Assign correct shader |
| `{fileID: 10303}` in m_Materials | Default Unity material | Assign project material |
| Custom shader not in Always Included & no scene ref | Pink in builds only | Add to Always Included or ensure ref chain |
| Shader with unbounded `multi_compile` variants | Exponential build size + compile time | Use `shader_feature` for per-material keywords |
| Shader changed from opaque to transparent queue | Sorting + performance change — may break layering | Verify render queue and camera sorting |

## 🟡 Major — Materials

`renderer.material` instead of `sharedMaterial` → leak. Unused `multi_compile` → build size. Desktop shader on mobile → fail. `_MainTex` vs `_BaseMap` (URP) mismatch. Material with missing texture slot (null `_MainTex`). Shader LOD set higher than target platform supports.

## 🔴 Critical — Textures (.meta)

| Meta Pattern | Issue | Fix |
|:-------------|:------|:----|
| `isReadable: 1` | Doubles memory | Disable unless GetPixels needed |
| `textureCompression: 0` / RGBA32 mobile | 4x+ memory | ASTC (iOS), ETC2 (Android) |
| NPOT dimensions | Can't compress | Resize to POT |

## 🟡 Major — Textures

| Meta Pattern | Issue | Fix |
|:-------------|:------|:----|
| `enableMipMap: 1` on UI sprite | +33% memory | Disable |
| 4096 for small asset | Wastes VRAM | Match maxTextureSize to display size |
| `spritePackingTag` missing on atlas candidate | Extra draw calls | Add packing tag or use SpriteAtlas |
| `sRGBTexture: 0` on color texture | Washed out colors | Enable sRGB for diffuse/albedo |
| `sRGBTexture: 1` on normal/mask map | Incorrect lighting | Disable sRGB for non-color data |
| `filterMode: 0` (Point) on non-pixel-art | Blocky rendering | Use Bilinear or Trilinear |
| No platform override for mobile | Desktop settings shipped to mobile | Add Android/iOS override with ASTC |

## 🟡 Major — Animation

Empty `m_Controller` → assign or remove. `CullingMode: 0` → CullCompletely. `WriteDefaultValues: 1` → disable. Unintended `ApplyRootMotion` → disable. Pause-immune UI → UnscaledTime. Animator on GO that never animates → remove for CPU save. Transition duration 0 on blended animations → add transition time.

## 🟡 Major — Audio

Unintended `PlayOnAwake` → disable. `SpatialBlend: 1` on UI → set 2D. Large clip uncompressed → Streaming+Vorbis. `loadInBackground: 0` on large clips → enable. `forceToMono: 0` on 3D SFX → enable (stereo in 3D is wasted). Clip > 1MB as `DecompressOnLoad` → use `CompressedInMemory` or `Streaming`.

## 🟡 Major — Models (.fbx/.meta)

| Pattern | Issue | Fix |
|:--------|:------|:----|
| `meshCompression: 0` on static mesh | Larger build size | Set to Medium or High |
| `isReadable: 1` on mesh | Doubles memory | Disable unless runtime mesh access needed |
| `importNormals: 0` (Import) on flat model | Unnecessary data | Set to None or Calculate |
| `importAnimation: 1` on non-animated model | Phantom clips, build bloat | Disable Import Animation |
| `animationType: 2` (Generic) when Humanoid expected | Retarget won't work | Match rig type to skeleton |
| `materialImportMode: 1` (Import) from DCC | Creates unmanaged materials | Set to None, assign manually |

## 🟡 Major — ScriptableObject Assets

SO with serialized scene references → null at runtime. SO with `HideFlags.DontSave` checked in → won't persist. Large data SO (>1MB) not in Addressables → bloats initial load.

## 🟡 Major — Components (Prefab/Scene context)

Camera depth conflicts, light shadow resolution `-1`, ParticleSystem `prewarm: 1` on heavy system, NavMeshAgent on disabled GO, Canvas `overrideSorting` without unique sortingOrder.

## 🔵 Minor

Tiling/offset mismatch, render queue override, maxTextureSize > source, wrong filterMode pixel art, missing sprite atlas tag, redundant animator layers, default audio import settings, model with unused BlendShapes.

## Grep

```bash
# Materials — missing shader / default material
grep -n "m_Shader: {fileID: 0}\|{fileID: 10303}" <changed .mat/.asset files>
# Textures — memory issues
grep -n "isReadable: 1\|enableMipMap: 1\|textureCompression: 0" <changed .meta files>
# Animator/Audio in prefabs
grep -n "m_Controller: {fileID: 0}\|m_CullingMode: 0\|m_PlayOnAwake: 1" <changed .prefab/.unity files>
# Model import settings
grep -n "meshCompression: 0\|isReadable: 1\|importAnimation: 1" <changed .meta files for .fbx>
```

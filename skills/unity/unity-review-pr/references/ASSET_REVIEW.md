# Asset Review — Materials, Textures, Animation, Audio

Load when PR modifies `.mat`, `.shader`, `.meta`, `.controller`, `.anim`, or audio files. Every asset issue MUST have **Issue + Why + Suggestion** (no exceptions).

## 🔴 Critical — Materials

| Pattern | Issue | Fix |
|:--------|:------|:----|
| `m_Shader: {fileID: 0}` | Pink/magenta at runtime | Assign correct shader |
| `{fileID: 10303}` in m_Materials | Default Unity material | Assign project material |
| Custom shader not in Always Included & no scene ref | Pink in builds only | Add to Always Included or ensure ref chain |

## 🟡 Major — Materials

`renderer.material` instead of `sharedMaterial` → memory leak. Unused `multi_compile` keywords → build size. Desktop shader on mobile → perf/fail. `_MainTex` vs `_BaseMap` (URP) mismatch → invisible texture.

## 🟡 Major — Textures (.meta)

| Meta Pattern | Issue | Fix |
|:-------------|:------|:----|
| `isReadable: 1` | Doubles memory (CPU+GPU copy) | Disable unless GetPixels needed |
| `enableMipMap: 1` on UI sprite | +33% memory, no benefit | Disable |
| `textureCompression: 0` / RGBA32 on mobile | 4x+ memory | ASTC (iOS), ETC2 (Android) |
| NPOT dimensions | Can't compress efficiently | Resize to POT |
| 4096x4096 for small asset | Wastes VRAM | Match maxTextureSize to display size |

Mobile targets: iOS=ASTC 6×6/8×8, Android=ETC2/ASTC, maxSize UI=512–1024, World=1024–2048.

## 🟡 Major — Animation

| Pattern | Fix |
|:--------|:----|
| `m_Controller: {fileID: 0}` | Assign controller or remove Animator |
| `m_CullingMode: 0` (Always Animate) | Use CullCompletely (2) |
| `m_WriteDefaultValues: 1` | Disable, set all props per state |
| `m_ApplyRootMotion: 1` unintended | Set to 0 |
| `m_UpdateMode: 0` on pause-immune UI | Use UnscaledTime (1) |

## 🟡 Major — Audio

| Pattern | Fix |
|:--------|:----|
| `m_PlayOnAwake: 1` unintended | Set to 0 |
| `m_SpatialBlend: 1` on UI AudioSource | Set to 0 (2D) |
| Large clip uncompressed | Streaming/CompressedInMemory + Vorbis |
| `loadInBackground: 0` on large clips | Enable |

## 🟡 Major — Components

Camera depth conflicts, light shadow resolution `-1`, ParticleSystem `prewarm: 1` on heavy system, NavMeshAgent on disabled GO.

## 🔵 Minor

Tiling/offset mismatch, render queue override undocumented, maxTextureSize > source size, wrong filterMode on pixel art, missing sprite atlas tag, redundant animator layers, missing exit time, default audio import settings.

## Grep

```bash
# Materials
for f in $(gh pr diff <N> --name-only | grep -E '\.(mat|asset)$'); do
  grep -n "m_Shader: {fileID: 0}\|{fileID: 10303}" "$f"
done
# Textures
for f in $(gh pr diff <N> --name-only | grep -E '\.(png|jpg|tga|psd|wav|mp3)\.meta$'); do
  grep -n "isReadable: 1\|enableMipMap: 1\|textureCompression: 0" "$f"
done
# Animator/Audio in prefabs
for f in $(gh pr diff <N> --name-only | grep -E '\.(prefab|unity)$'); do
  grep -n "m_Controller: {fileID: 0}\|m_CullingMode: 0\|m_PlayOnAwake: 1" "$f"
done
```

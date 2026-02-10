# Asset Review Checklist

Load this reference when PR modifies `.mat`, `.shader`, `.meta` (textures), `.controller`, `.anim`, or audio files. Each issue follows: **Issue → Evidence → Why → Fix → Priority**.

---

## Table of Contents

1. [Material & Shader](#1-material--shader)
2. [Texture & Import Settings](#2-texture--import-settings)
3. [Animation & Animator](#3-animation--animator)
4. [Audio](#4-audio)
5. [Component Properties (Non-Code)](#5-component-properties-non-code)
6. [Grep Patterns](#6-grep-patterns)

---

## 1. Material & Shader

### 🔴 Critical

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Missing shader** | `m_Shader: {fileID: 0}` in `.mat` file | Pink/magenta rendering at runtime | Assign correct shader | 🔴 Critical |
| **Default-Material on shipped asset** | `m_Materials` referencing `{fileID: 10303}` | Wrong appearance; builds may strip it | Assign proper project material | 🔴 Critical |
| **Shader not in build** | Custom shader not in "Always Included Shaders" and not referenced by any material in a scene/Resources | Works in Editor, pink in builds | Add to Always Included Shaders or ensure reference chain | 🔴 Critical |

### 🟡 Major

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Material instance leak** | Code uses `renderer.material` (creates instance) instead of `renderer.sharedMaterial` | New material instance per access; memory leak | Use `sharedMaterial` for reads; manage instances explicitly with `Destroy()` | 🟡 Major |
| **Unused shader variants** | Material references shader with many `multi_compile` keywords | Increased build size and shader compile time | Use `shader_feature` for material-local keywords; strip unused variants | 🟡 Major |
| **Wrong shader for platform** | Desktop-only shader (e.g., tessellation) on mobile asset | Performance regression or rendering failure on target platform | Use mobile-appropriate shader variant | 🟡 Major |
| **Texture property mismatch** | Material has `_MainTex` but shader expects `_BaseMap` (URP) | Texture appears missing despite being assigned | Match property names to shader expectations | 🟡 Major |

### 🔵 Minor

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Tiling/offset defaults** | `_MainTex_ST: {x: 1, y: 1, z: 0, w: 0}` when art spec differs | Visual mismatch | Verify tiling matches art spec | 🔵 Minor |
| **Render queue override** | `m_CustomRenderQueue` set without clear reason | Unexpected render order | Document why or reset to shader default | 🔵 Minor |

### Example

```yaml
# BAD — missing shader renders pink
m_Shader: {fileID: 0}

# BAD — default material (Unity built-in)
m_Materials:
  - {fileID: 10303, guid: 0000000000000000f000000000000000, type: 0}

# FIX: Assign project-specific material/shader
m_Shader: {fileID: 4800000, guid: abc123def456, type: 3}
```

---

## 2. Texture & Import Settings

### 🟡 Major

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Read/Write enabled** | `isReadable: 1` in `.meta` for textures not read from CPU | Doubles memory (GPU + CPU copy) | Disable unless scripts call `GetPixels()`/`ReadPixels()` | 🟡 Major |
| **Mipmaps on UI sprite** | `enableMipMap: 1` on Sprite/UI texture | +33% memory; unnecessary for screen-space rendering | Disable mipmaps for UI sprites | 🟡 Major |
| **Uncompressed on mobile** | `textureCompression: 0` or format `RGBA32` for mobile platform | 4x+ memory vs compressed format | Set platform override: ASTC (iOS), ETC2 (Android) | 🟡 Major |
| **NPOT texture** | Dimensions not power of 2 (e.g., 300×400) | Can't compress efficiently; wastes memory on mobile | Resize to POT or set NPOT import to nearest POT | 🟡 Major |
| **Oversized texture** | 4096×4096 for UI icon or small prop | Wastes VRAM; longer load times | Downsize `maxTextureSize` to match actual display size | 🟡 Major |

### 🔵 Minor

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Max size too high** | `maxTextureSize: 2048` for a 64×64 source texture | No visual benefit; wasted import setting | Set max size to source size | 🔵 Minor |
| **Wrong filter mode** | `filterMode: 1` (Bilinear) on pixel art | Blurry pixel art | Use `filterMode: 0` (Point) for pixel art | 🔵 Minor |
| **Missing sprite packing tag** | Sprite without atlas/packing tag | Missed draw call batching opportunity | Assign atlas for batching | 🔵 Minor |

### Platform Override Checklist

When reviewing `.meta` files for textures targeting mobile:

| Platform | Recommended Format | Max Size (UI) | Max Size (World) |
|:---------|:-------------------|:-------------|:-----------------|
| iOS | ASTC 6×6 or 8×8 | 512–1024 | 1024–2048 |
| Android | ETC2 or ASTC 6×6 | 512–1024 | 1024–2048 |
| WebGL | DXT5 / ETC2 | 512–1024 | 1024–2048 |

---

## 3. Animation & Animator

### 🟡 Major

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Animator no controller** | `m_Controller: {fileID: 0}` | Component overhead with no function; confusing | Assign controller or remove Animator component | 🟡 Major |
| **Always Animate on off-screen** | `m_CullingMode: 0` (Always Animate) | CPU wasted animating invisible objects | Use `CullUpdateTransforms` (1) or `CullCompletely` (2) | 🟡 Major |
| **Write Defaults enabled** | State `m_WriteDefaultValues: 1` | Properties bleed between states; inconsistent animation behavior | Disable Write Defaults; explicitly set all properties per state | 🟡 Major |
| **Apply Root Motion unintended** | `m_ApplyRootMotion: 1` on non-root-motion animation | Object moves based on animation clips unexpectedly | Set `m_ApplyRootMotion: 0` | 🟡 Major |
| **Animator updateMode mismatch** | `m_UpdateMode: 0` (Normal) on UI that should animate during pause | UI animation freezes when `Time.timeScale = 0` | Use `UnscaledTime` (1) for pause-immune UI | 🟡 Major |

### 🔵 Minor

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Redundant animator layers** | Multiple layers with identical state machines | Wasted evaluation; confusing | Consolidate or remove duplicate layers | 🔵 Minor |
| **Missing exit time** | Transition with `m_HasExitTime: 0` and no condition | Transition never fires | Add condition or enable exit time | 🔵 Minor |

---

## 4. Audio

### 🟡 Major

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **AudioSource playOnAwake** | `m_PlayOnAwake: 1` unintentionally | Sound plays immediately on load/instantiate | Set `m_PlayOnAwake: 0` unless designed to auto-play | 🟡 Major |
| **3D sound on UI** | AudioSource with `m_SpatialBlend: 1` on UI element | Sound attenuates based on camera distance from Canvas | Set `m_SpatialBlend: 0` for UI audio | 🟡 Major |
| **Uncompressed audio clip** | Large `.wav`/`.aiff` without compression in import settings | Massive memory footprint; long load times | Set `loadType` to Streaming or CompressedInMemory; use Vorbis/ADPCM | 🟡 Major |
| **Load In Background disabled** | `loadInBackground: 0` on large audio clips | Blocks main thread during loading | Enable `loadInBackground: 1` for large clips | 🟡 Major |

### 🔵 Minor

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Default audio import settings** | No platform override set | Sub-optimal quality/size tradeoff for target platform | Set platform-specific quality and sample rate | 🔵 Minor |

---

## 5. Component Properties (Non-Code)

These are serialized component settings found in `.prefab`/`.unity` files — not C# code issues.

### 🟡 Major

| Issue | Component | Evidence | Why | Fix | Priority |
|:------|:----------|:---------|:----|:----|:---------|
| **Camera depth conflict** | Camera | Multiple cameras with same `m_Depth` | Undefined render order | Assign unique depth values | 🟡 Major |
| **Light shadow resolution** | Light | `m_ShadowResolution: -1` on perf-critical light | May pick expensive default from Quality Settings | Set explicit resolution | 🟡 Major |
| **ParticleSystem prewarm** | ParticleSystem | `prewarm: 1` on heavy system | Frame spike on first enable | Disable prewarm or reduce emission count | 🟡 Major |
| **NavMeshAgent on inactive** | NavMeshAgent | Agent on disabled GO still registered | NavMesh overhead on disabled object | Disable component, not just GO | 🟡 Major |

### 🔵 Minor

| Issue | Component | Evidence | Why | Fix | Priority |
|:------|:----------|:---------|:----|:----|:---------|
| **Default physics material** | Collider | `m_Material: {fileID: 0}` | Uses global default; may not match intent | Assign explicit physics material if bounce/friction needed | 🔵 Minor |
| **Canvas pixel perfect** | Canvas | `m_PixelPerfect: 1` with CanvasScaler | Can cause visual artifacts with dynamic scaling | Disable if using CanvasScaler | 🔵 Minor |

---

## 6. Grep Patterns

Run against changed `.mat`, `.meta`, `.prefab`, `.controller`, and `.asset` files:

```bash
CHANGED_ASSETS=$(gh pr diff <number> --name-only | grep -E '\.(mat|asset|controller)$')
CHANGED_META=$(gh pr diff <number> --name-only | grep -E '\.(png|jpg|tga|psd|wav|mp3|ogg|aiff)\.meta$')

echo "=== Material & Shader ==="
for f in $CHANGED_ASSETS; do
  grep -n "m_Shader: {fileID: 0}" "$f" 2>/dev/null           # missing shader
  grep -n "{fileID: 10303}" "$f" 2>/dev/null                   # default material
done

echo "=== Texture Import ==="
for f in $CHANGED_META; do
  grep -n "isReadable: 1" "$f" 2>/dev/null                    # read/write enabled
  grep -n "enableMipMap: 1" "$f" 2>/dev/null                   # mipmaps (check if UI)
  grep -n "textureCompression: 0" "$f" 2>/dev/null             # uncompressed
  grep -n "maxTextureSize:" "$f" 2>/dev/null                    # check oversized
done

echo "=== Animator ==="
for f in $(gh pr diff <number> --name-only | grep -E '\.(prefab|unity)$'); do
  grep -n "m_Controller: {fileID: 0}" "$f" 2>/dev/null        # no controller
  grep -n "m_CullingMode: 0" "$f" 2>/dev/null                 # always animate
  grep -n "m_PlayOnAwake: 1" "$f" 2>/dev/null                 # audio auto-play
done
```

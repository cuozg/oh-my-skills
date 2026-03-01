# Asset Review — PR Checklist

> Authoritative for: materials, shaders, textures, animation, audio, models, ScriptableObject assets.
> Cross-ref: `review-prefab-patterns.md` (prefab YAML), `review-architecture-patterns.md` (SO channels)

---

## 🔴 Critical — Materials & Shaders

| Name | Issue | Fix |
|------|-------|-----|
| Missing Shader Fallback | Shader has no `Fallback` — renders pink on unsupported hardware | Add `Fallback "Mobile/Diffuse"` or appropriate fallback |
| Shader Compilation Error | Shader fails on target platform (e.g., metal vs GLES) | Test on all target platforms; use `#pragma multi_compile` carefully |
| Unbounded Texture Samples | Shader samples 10+ textures per pass — exceeds mobile limits | Merge textures (channel-packing), reduce passes, use atlas |
| Material Leak | `new Material()` at runtime without `Destroy()` | Cache materials; destroy runtime-created materials in `OnDestroy` |
| Negative Scale on Renderer | Mesh rendered inside-out due to negative scale | Fix scale to positive; flip normals in model if needed |

## 🔴 Critical — Textures

| Name | Issue | Fix |
|------|-------|-----|
| Uncompressed Texture | 4K RGBA uncompressed = 64MB VRAM per texture | Set platform compression: ASTC (mobile), BC7 (desktop) |
| Non-PoT Texture | Non-power-of-2 dimensions disable mipmaps and compression | Resize to PoT (256, 512, 1024, 2048) or enable `Non-Power of 2: ToNearest` |
| Missing Mipmaps | 3D textures without mipmaps cause aliasing at distance | Enable mipmaps for all 3D-rendered textures; disable only for UI |
| Excessive Resolution | 4K texture on a small prop that renders at 50px on screen | Match texture resolution to screen coverage; most props need ≤512 |
| Read/Write Enabled | Doubles memory — CPU copy kept alongside GPU copy | Disable `Read/Write Enabled` unless runtime pixel access needed |

## 🟡 Major — Materials & Shaders

| Name | Issue | Fix |
|------|-------|-----|
| Duplicate Materials | Same material duplicated across folders — wastes memory, inconsistent | Consolidate to single shared material; reference via SO or addressable |
| Overdraw from Transparency | Overlapping transparent objects cause excessive fill rate | Minimize transparent layers; use alpha-test (cutout) where possible |
| Missing GPU Instancing | Same material drawn 100+ times without instancing | Enable `GPU Instancing` on material; ensure shader supports `UNITY_INSTANCING_BUFFER` |
| Shader Variant Explosion | `multi_compile` with 5+ keywords = 2^5 variants = slow build | Use `shader_feature` for editor-only keywords; strip unused variants |
| Unlit Shader Misuse | Using Unlit shader on objects that should receive lighting | Switch to Lit/Standard; reserve Unlit for UI, particles, sky |

## 🟡 Major — Textures

| Name | Issue | Fix |
|------|-------|-----|
| Wrong sRGB Setting | Linear texture in sRGB slot (normal maps, masks) or vice versa | Normal maps, masks, data textures → Linear; albedo, UI → sRGB |
| Max Size Too High | Platform max size set to 4096 but texture is 256px source | Set `Max Size` to match source resolution; don't upscale |
| Missing Sprite Atlas | 50+ individual sprites loaded separately — draw call explosion | Pack into Sprite Atlas; use `SpriteAtlas` asset with packing tag |
| Texture Streaming Disabled | Large textures fully loaded even when not visible | Enable `Streaming Mipmaps` for 3D textures >512px |

## 🟡 Major — Animation

| Name | Issue | Fix |
|------|-------|-----|
| Unoptimized Animation Curves | Keyframe on every frame for constant values | Use `Anim. Compression: Optimal`; remove constant curves |
| Missing Animation Events Cleanup | Animation events fire on destroyed objects | Guard event handlers with null checks; unregister on destroy |
| Humanoid Rig Misconfigured | Wrong bone mapping causes retargeting glitches | Verify Avatar bone assignments; use T-pose reference |
| Excessive Animator Layers | 5+ animator layers all active — CPU cost compounds | Disable unused layers; merge simple layers; use `AnimationPlayableGraph` for complex blending |
| Animation Clip Not Looping | Walk/idle clip plays once and freezes | Set `Loop Time` on clip; verify `Wrap Mode = Loop` |

## 🟡 Major — Audio

| Name | Issue | Fix |
|------|-------|-----|
| Uncompressed Audio in Build | WAV files shipped uncompressed — massive build size | Set `Load Type: Compressed In Memory` or `Streaming`; use Vorbis/ADPCM |
| Long Clip as Decompress on Load | 2-minute music clip fully decompressed to memory on load | Use `Streaming` for clips >10 seconds; `Compressed In Memory` for SFX |
| Missing Audio Mixer | All audio at flat volume, no ducking or grouping | Route through AudioMixer groups (Music, SFX, UI, Ambient) |
| 3D Audio on UI Sounds | UI clicks affected by spatial positioning | Set `Spatial Blend = 0` (2D) for all UI audio sources |
| Sample Rate Mismatch | 96kHz source file — wasteful for game audio | Re-export at 44.1kHz (music) or 22kHz (SFX); set `Sample Rate Setting: Override` |

## 🟡 Major — Models

| Name | Issue | Fix |
|------|-------|-----|
| Excessive Polygon Count | 50K-poly prop that could be 5K without visual difference | Decimate in DCC tool; use LOD Group for distance-based switching |
| Missing LOD Group | High-poly mesh rendered at full detail regardless of distance | Add LOD Group with 2-3 levels; LOD0=full, LOD1=50%, LOD2=25% |
| Unnecessary Mesh Read/Write | `Read/Write Enabled` doubles mesh memory | Disable unless runtime mesh modification needed (e.g., procedural) |
| Broken Normals / UVs | Import shows seams, lighting artifacts, UV stretching | Fix in DCC tool; check `Normals: Import` vs `Calculate`; verify UV2 for lightmaps |
| Missing Mesh Compression | Large mesh files inflate build size | Set `Mesh Compression: Medium` or `High`; verify visual quality after |

## 🟡 Major — ScriptableObjects

| Name | Issue | Fix |
|------|-------|-----|
| Runtime SO Mutation | SO asset modified at runtime — changes persist in Editor, lost in build | Clone with `Instantiate()` for runtime mutation; keep asset as read-only template |
| Missing `[CreateAssetMenu]` | SO class has no menu entry — designers can't create instances | Add `[CreateAssetMenu(fileName, menuName, order)]` |
| Large SO Array | SO holds 10K+ entries inline — slow to load, hard to diff | Split into multiple SOs or use external data source (JSON, FlatBuffers) |
| SO Cross-Reference Cycle | SO_A references SO_B which references SO_A — fragile to reorder | Break cycle with ID-based lookup or event channel |
| Null Asset References | SO field assigned in editor cleared after reimport or branch switch | Use Addressable reference or validate references in `OnValidate` |

## 🔵 Medium

| Name | Issue | Fix |
|------|-------|-----|
| Inconsistent Asset Naming | Mixed `PascalCase`, `snake_case`, `camelCase` across folders | Enforce naming convention per type: `T_AlbedoName_D`, `M_MaterialName`, `SFX_ActionName` |
| Missing Asset Labels | No labels or tags for addressable grouping | Add labels for build groups; use folder-based or label-based addressable loading |
| Orphaned Assets | Assets in project not referenced by any scene or prefab | Run `Editor > Find References In Scene`; remove confirmed orphans |
| Unused Shader Keywords | Material has enabled keywords for features not in use | Remove unused keywords; use `Material.DisableKeyword()` or reset in inspector |

## 🟢 Minor

| Name | Issue | Fix |
|------|-------|-----|
| Missing Asset Preview | Custom SO has no preview in Project window | Override `OnInspectorGUI` or add `[PreviewField]` attribute |
| No Material Property Documentation | Team doesn't know what each material property controls | Add `[Header]` and `[Tooltip]` in shader properties |
| Inconsistent Audio Volume | SFX volume varies wildly between clips | Normalize audio in DAW; use AudioMixer groups with consistent output levels |

---

## PR Grep Commands

```bash
# Find uncompressed textures
grep -rn "textureCompression: 0" Assets/**/*.meta

# Find Read/Write enabled meshes
grep -rn "isReadable: 1" Assets/**/*.meta

# Find materials without GPU instancing
grep -rn "m_EnableInstancingVariants: 0" Assets/**/*.mat

# Find textures with streaming disabled
grep -rn "streamingMipmaps: 0" Assets/**/*.meta
```

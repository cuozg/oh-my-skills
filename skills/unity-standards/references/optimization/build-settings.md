# Build Optimization Settings

## Managed Code Stripping

| Level | Effect | Risk | Recommended |
|-------|--------|------|-------------|
| Disabled | No stripping | None | Never in release |
| Minimal | Strips unreachable BCL | Low | Debug builds |
| Low | Strips most unused BCL | Low-Medium | Safe default |
| Medium | Strips unused user + BCL | Medium | Most projects |
| High | Aggressive — strips everything unproven reachable | High | Size-critical mobile |

**Preserve via `link.xml`:**
```xml
<linker>
  <assembly fullname="Assembly-CSharp" preserve="all"/>
  <type fullname="MyNamespace.ReflectedType" preserve="all"/>
</linker>
```

High stripping + reflection = runtime `MissingMethodException`. Test thoroughly.

## IL2CPP vs Mono

| Aspect | Mono | IL2CPP |
|--------|------|--------|
| Build time | Fast (seconds) | Slow (minutes) |
| Runtime perf | Baseline | 1.5-3x faster (AOT + C++ opt) |
| Build size | Larger runtime | Smaller final binary |
| Platform | PC, Android | All (required for iOS, WebGL) |
| Debugging | Easy | Harder (generated C++) |

**Guideline:** Use Mono for iteration, IL2CPP for release builds. iOS/WebGL/consoles require IL2CPP.

## IL2CPP Code Generation

| Option | Use Case |
|--------|----------|
| Faster runtime | Release builds — optimizes generated C++ |
| Faster build | Development — reduces compile time |

## Build Compression

| Platform | Format | Setting |
|----------|--------|---------|
| Android | LZ4 (default) or LZ4HC | LZ4HC for release (better ratio, same decompress speed) |
| iOS | LZ4 | Default, Apple handles app thinning |
| WebGL | Brotli (best) > Gzip > None | Server must serve correct Content-Encoding |
| Standalone | LZ4HC | Best balance |

## Asset Bundle / Addressables Size

- **Duplicate dependency check:** Addressables Analyze → "Check Duplicate Bundle Dependencies"
- **Group by load pattern:** co-loaded assets in same bundle, avoid cross-bundle dependencies
- **Bundle size target:** 1-5 MB per bundle (network), 5-20 MB per bundle (local)
- **Catalog size:** minimize label count, avoid per-asset labels
- **Content update:** use "Can Change Post Release" groups for patchable content

## Texture Compression Per Platform

| Platform | Format | Quality | Notes |
|----------|--------|---------|-------|
| Android | ASTC 6x6 | Good balance | ASTC 4x4 for UI/text, 8x8 for backgrounds |
| iOS | ASTC 6x6 | Same as Android | Universal since A8 chip |
| PC/Console | BC7 (quality) or DXT5 (compat) | High quality | BC7 for modern GPUs |
| WebGL | DXT5/BC7 (desktop) / ASTC (mobile) | Varies | Check WebGL browser support |

**Size formula:** `width * height * bpp / 8` — ASTC 6x6 = 3.56 bpp, DXT5 = 8 bpp, BC7 = 8 bpp, RGBA32 = 32 bpp.

## Audio Compression

| Type | Load Type | Compression | Typical Size |
|------|-----------|-------------|-------------|
| Short SFX (< 1s) | Decompress On Load | Vorbis/ADPCM | Small in memory |
| Medium SFX (1-5s) | Compressed In Memory | Vorbis Q=70 | Moderate |
| Music/Ambient | Streaming | Vorbis Q=50-70 | Minimal memory |
| Voice lines | Streaming or Compressed | Vorbis Q=80 | Quality-dependent |

**Mobile:** Force mono for SFX (50% size reduction). Reduce sample rate to 22050Hz for non-music.

## Mesh Optimization

- **Mesh Compression:** Low/Medium for static, Off for animated (can cause artifacts)
- **Read/Write Enabled:** OFF unless runtime mesh modification needed (halves memory)
- **Optimize Mesh Data:** ON in Player Settings → strips unused vertex channels
- **Import settings:** disable tangents/normals if unused by shader

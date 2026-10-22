# Build Optimization Settings

## Build Profiles And CLI Builds

- Unity 6 replaces the Build Settings window with **File > Build Profiles**. Each
  profile can carry its own scene list, platform settings, and Player Settings
  overrides; check the active profile before reading Player Settings.
- Build from the terminal with `unity build <project> --target <target> --execute-method <Class.Method>`
  (adds batch mode itself; never pass `-batchmode`/`-quit`). See
  `references/other/unity-cli-routing.md`.
- Size evidence: after a build, `grep -A 30 "Build Report" <project>/Logs/Editor.log`
  (or the global Editor.log) for the per-category size breakdown.

## Managed Code Stripping

| Level | Effect | Risk | Recommended |
|-------|--------|------|-------------|
| Disabled | No stripping (Mono only) | None | Never in release |
| Minimal | Strips .NET class libraries and UnityEngine only; user assemblies untouched | Low | IL2CPP default |
| Low | Also strips unreachable user code, conservative rules | Low-Medium | Safe default |
| Medium | Less conservative reachability analysis | Medium | Most projects |
| High | Aggressive - strips everything unproven reachable | High | Size-critical mobile/web |

**Preserve via `link.xml`:**
```xml
<linker>
  <assembly fullname="Assembly-CSharp" preserve="all"/>
  <type fullname="MyNamespace.ReflectedType" preserve="all"/>
</linker>
```

Or mark individual members with `[UnityEngine.Scripting.Preserve]`. High stripping +
reflection (serializers, DI, JSON) = runtime `MissingMethodException`; test the
release build, not the Editor.

## IL2CPP vs Mono

| Aspect | Mono | IL2CPP |
|--------|------|--------|
| Build time | Fast (seconds) | Slow (minutes) |
| Runtime perf | Baseline (JIT) | Usually faster (AOT + C++ opt) |
| Build size | Smaller binary | Larger native binary; offset with stripping |
| Platform | Standalone, Android (no ARM64) | All (required for iOS, Web, consoles, Android ARM64) |
| Debugging | Easy | Harder (generated C++) |

**Guideline:** Use Mono for iteration, IL2CPP for release builds. Store builds for
iOS, Web, consoles, and Android ARM64 require IL2CPP.

## IL2CPP Code Generation

| Option | Use Case |
|--------|----------|
| Faster runtime | Release builds - optimizes generated C++ |
| Faster (smaller) builds | Development - reduces C++ compile time and binary size |

## Build Compression

| Platform | Format | Setting |
|----------|--------|---------|
| Android | LZ4 (default) or LZ4HC | LZ4HC for release (better ratio, same decompress speed) |
| iOS | LZ4 | Default, Apple handles app thinning |
| Web | Brotli (best) > Gzip > None | Server must serve correct Content-Encoding; see `unity:optimize-web` |
| Standalone | LZ4HC | Best balance |

## Asset Bundle / Addressables Size

- **Duplicate dependency check:** Addressables Analyze -> "Check Duplicate Bundle Dependencies"
- **Bundle size target:** 1-5 MB per bundle (network), 5-20 MB per bundle (local)
- **Catalog size:** minimize label count, avoid per-asset labels
- Grouping, labels, and content-update strategy live in
  `references/asset-management/addressables-asset-manager.md`.

## Texture Compression Per Platform

| Platform | Format | Quality | Notes |
|----------|--------|---------|-------|
| Android | ASTC 6x6 | Good balance | ASTC 4x4 for UI/text, 8x8 for backgrounds |
| iOS | ASTC 6x6 | Same as Android | Universal since A8 chip |
| PC/Console | BC7 (quality) or DXT5 (compat) | High quality | BC7 for modern GPUs |
| Web | DXT5/BC7 (desktop) / ASTC (mobile) | Varies | Check browser support; see `unity:optimize-web` |

**Size formula:** `width * height * bpp / 8` - ASTC 6x6 = 3.56 bpp, DXT5 = 8 bpp, BC7 = 8 bpp, RGBA32 = 32 bpp.

## Audio Compression

Load type, codec, sample rate, and mono rules: see `memory-settings.md` (Audio
Memory) and the `unity:optimize-audio` skill.

## Mesh Optimization

- **Mesh Compression:** Low/Medium for static, Off for animated (can cause artifacts)
- **Read/Write Enabled:** OFF unless runtime mesh modification needed (halves memory)
- **Optimize Mesh Data:** ON in Player Settings -> strips unused vertex channels
- **Import settings:** disable tangents/normals if unused by shader

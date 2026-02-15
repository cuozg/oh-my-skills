---
name: unity-web-deploy
description: "(opencode-project - Skill) WebGL deployment and browser platform optimization. Use when: (1) Configuring/optimizing WebGL builds, (2) C#/JavaScript interop, (3) Browser-specific issues (memory, audio, input), (4) PWA features, (5) Hosting and serving Unity web builds, (6) Web-specific asset loading. Triggers: 'WebGL', 'web build', 'browser deploy', 'jslib', 'JavaScript plugin', 'C# JS interop', 'WebGL memory', 'browser audio', 'PWA', 'service worker', 'IndexedDB', 'WebGL template', 'compression format', 'Brotli', 'streaming assets web', 'CORS', 'web performance', 'WebGL 2', 'deploy to web', 'web deploy', 'Unity web', 'browser game', 'itch.io', 'web hosting Unity', 'emscripten', 'wasm'."
---

# Unity Web Developer

**Input**: WebGL task description. Optional: file paths, browser targets, constraints.

**Output**: Build report per [WEBGL_BUILD_REPORT.md](.opencode/skills/unity/unity-web-deploy/assets/templates/WEBGL_BUILD_REPORT.md) template. Saved to `Documents/Builds/WEBGL_BUILD_[YYYYMMDD].md`.

## Workflow

1. **Discover**: Required Web APIs (LocalStorage, Fullscreen, WebXR), browser targets
2. **Implement**: C# interop managers (see [WEBGL_INTEROP_PATTERNS.md](.opencode/skills/unity/unity-web-deploy/references/WEBGL_INTEROP_PATTERNS.md)), JS plugins in `Assets/Plugins/WebGL/`
3. **Optimize**: Build size, memory limits, compression (see [WEBGL_OPTIMIZATION_GUIDE.md](.opencode/skills/unity/unity-web-deploy/references/WEBGL_OPTIMIZATION_GUIDE.md))
4. **Deploy**: Build report via template, validate COOP/COEP headers, HTTPS

## Build Settings

| Setting | Recommendation |
|---------|----------------|
| Compression | Brotli (best), Gzip (fallback) |
| Memory | Limit based on target browsers |
| Textures | ASTC/ETC2 for mobile browsers |

## Best Practices

- **Mobile First**: Assume limited memory/thermals on mobile browsers
- **Lazy Init**: Small initial WASM/Data, use Addressables for rest
- **Sanitize Input**: Treat `SendMessage` data from JS as untrusted
- **User Interaction**: Audio/video only after first click (browser policy)
- **Decompression Fallback**: Handle browsers without native Brotli/Gzip

## Handoff

- **Delegates to**: `unity-build-pipeline` (general build automation/CI/CD), `unity-optimize-performance` (platform-agnostic perf)
- **Does NOT**: iOS/Android builds (use `unity-mobile-deploy`), general build scripting (use `unity-build-pipeline`)

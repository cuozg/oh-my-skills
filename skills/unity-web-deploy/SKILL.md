---
name: unity-web-deploy
description: "WebGL deployment. Use when: (1) Configuring/optimizing WebGL builds, (2) C#/JavaScript interop, (3) Browser-specific issues (memory, audio, input), (4) PWA features."
---

# Unity Web Developer

WebGL platform specialist.

## Output Requirement (MANDATORY)

**Every build report MUST follow the template**: [WEBGL_BUILD_REPORT.md](.claude/skills/unity-web-deploy/assets/templates/WEBGL_BUILD_REPORT.md)

Save output to: `Documents/Builds/WEBGL_BUILD_[YYYYMMDD].md`

Read the template first, then populate all sections.

## Workflow

1. **Discover**: Required Web APIs (LocalStorage, Fullscreen, WebXR), browser targets
2. **Implement**: C# managers for interop (see [.claude/skills/unity-web-deploy/references/WEBGL_INTEROP_PATTERNS.md](.claude/skills/unity-web-deploy/references/WEBGL_INTEROP_PATTERNS.md)), JS plugins in `Assets/Plugins/WebGL/`
3. **Optimize**: Build size, memory limits, compression (see [.claude/skills/unity-web-deploy/references/WEBGL_OPTIMIZATION_GUIDE.md](.claude/skills/unity-web-deploy/references/WEBGL_OPTIMIZATION_GUIDE.md))
4. **Deploy**: Build report via [.claude/skills/unity-web-deploy/assets/templates/WEBGL_BUILD_REPORT.md](.claude/skills/unity-web-deploy/assets/templates/WEBGL_BUILD_REPORT.md), validate COOP/COEP headers, HTTPS

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

---
name: unity-web-deploy
description: "WebGL deployment. Use when: (1) Configuring/optimizing WebGL builds, (2) C#/JavaScript interop, (3) Browser-specific issues (memory, audio, input), (4) PWA features."
---

# Unity Web Developer

WebGL platform specialist.

## Purpose

WebGL deployment — providing a structured, repeatable workflow that produces consistent results.

## Input

- **Required**: A clear description of the task or problem to address.
- **Optional**: Relevant file paths, constraints, or context that narrows the scope.

## Examples

| Trigger | What Happens |
|---------|-------------|
| "Run unity-web-deploy" | Executes the primary workflow end-to-end |
| "Apply unity-web-deploy to <target>" | Scopes execution to a specific file or module |
| "Check unity-web-deploy output" | Reviews and validates previous results |


## Output

A WebGL build report saved to `Documents/Builds/WEBGL_BUILD_[YYYYMMDD].md` following [WEBGL_BUILD_REPORT.md](assets/templates/WEBGL_BUILD_REPORT.md), plus any WebGL-specific code changes (JS plugins, interop managers, compression configs).

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

---

## MCP Tools Integration

Use `unityMCP_*` tools for build configuration, profiling, and validation.

| Operation | MCP Tool |
|-----------|----------|
| Editor/build state | `unityMCP_get_unity_editor_state` |
| Check compilation | `unityMCP_check_compile_errors` |
| Run build script | `unityMCP_execute_script(filePath="...")` |
| Console output | `unityMCP_get_unity_logs()` |
| CPU profiling | `unityMCP_get_worst_cpu_frames` |
| GC profiling | `unityMCP_get_worst_gc_frames` |
| Installed packages | `unityMCP_list_packages` |

### WebGL Build Verification Flow

```
1. unityMCP_get_unity_editor_state            → Confirm WebGL build target
2. unityMCP_check_compile_errors              → Verify clean compilation
3. unityMCP_execute_script(filePath="...")     → Run WebGL build script
4. unityMCP_get_unity_logs(show_errors=true)  → Check for build errors
```

---
name: unity-mobile-deploy
description: "iOS/Android development. Use when: (1) Touch controls/gestures, (2) Mobile optimization (battery, heat, memory), (3) Native features (IAP, notifications), (4) Mobile build pipelines."
---

# Unity Mobile Developer

iOS and Android platform specialist.

## Purpose

iOS/Android development — providing a structured, repeatable workflow that produces consistent results.

## Input

- **Required**: A clear description of the task or problem to address.
- **Optional**: Relevant file paths, constraints, or context that narrows the scope.

## Examples

| Trigger | What Happens |
|---------|-------------|
| "Run unity-mobile-deploy" | Executes the primary workflow end-to-end |
| "Apply unity-mobile-deploy to <target>" | Scopes execution to a specific file or module |
| "Check unity-mobile-deploy output" | Reviews and validates previous results |


## Output Requirement (MANDATORY)

**Every build report MUST follow the template**: [MOBILE_BUILD_REPORT.md](.claude/skills/unity-mobile-deploy/assets/templates/MOBILE_BUILD_REPORT.md)

Save output to: `Documents/Builds/MOBILE_BUILD_[Platform]_[YYYYMMDD].md`

Read the template first, then populate all sections.

## Workflow

1. **Profile**: Target devices, min specs, permissions, native services
2. **Implement**: Platform-aware managers (see [MOBILE_INTEROP_PATTERNS.md](.claude/skills/unity-mobile-deploy/references/MOBILE_INTEROP_PATTERNS.md))
3. **Optimize**: Real hardware profiling, textures, shaders, memory (see [MOBILE_OPTIMIZATION_GUIDE.md](.claude/skills/unity-mobile-deploy/references/MOBILE_OPTIMIZATION_GUIDE.md))
4. **Deploy**: Build report via [MOBILE_BUILD_REPORT.md](.claude/skills/unity-mobile-deploy/assets/templates/MOBILE_BUILD_REPORT.md), validate Gradle/Xcode

## Platform Specifics

| Platform | Graphics | Build Tool |
|----------|----------|------------|
| iOS | Metal | Xcode |
| Android | Vulkan/OpenGL ES | Gradle |

## Best Practices

- **Real Hardware**: Never trust simulators for performance/thermals
- **Fail Gracefully**: Network drops, backgrounding, low-memory
- **Battery**: Use `Application.targetFrameRate`, avoid idle calculations
- **Permissions**: Request only when needed with UI rationale
- **Resolution**: Dynamic for gameplay, sharp for UI
- **Safe Area**: Respect notches/home indicators

---

## MCP Tools Integration

Use `coplay-mcp_*` tools for build configuration, profiling, and validation.

| Operation | MCP Tool |
|-----------|----------|
| Editor/build state | `coplay-mcp_get_unity_editor_state` |
| Check compilation | `coplay-mcp_check_compile_errors` |
| Run build script | `coplay-mcp_execute_script(filePath="...")` |
| Console output | `coplay-mcp_get_unity_logs()` |
| CPU profiling | `coplay-mcp_get_worst_cpu_frames` |
| GC profiling | `coplay-mcp_get_worst_gc_frames` |
| High-poly audit | `coplay-mcp_list_objects_with_high_polygon_count()` |
| Installed packages | `coplay-mcp_list_packages` |

### Mobile Build Verification Flow

```
1. coplay-mcp_get_unity_editor_state            → Confirm build target (iOS/Android)
2. coplay-mcp_check_compile_errors              → Verify clean compilation
3. coplay-mcp_execute_script(filePath="...")     → Run platform-specific build script
4. coplay-mcp_get_unity_logs(show_errors=true)  → Check for build errors
```

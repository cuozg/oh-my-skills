---
name: unity-mobile-deploy
description: "(opencode-project - Skill) iOS/Android development. Use when: (1) Touch controls/gestures, (2) Mobile optimization (battery, heat, memory), (3) Native features (IAP, notifications), (4) Mobile build pipelines, (5) Platform-specific player settings, (6) Device testing and profiling. Triggers: 'build for iOS', 'deploy Android', 'mobile build', 'touch input', 'swipe gesture', 'IAP', 'in-app purchase', 'push notification', 'battery optimization', 'thermal throttling', 'mobile memory', 'Xcode', 'Gradle', 'Android manifest', 'provisioning profile', 'APK', 'IPA', 'App Store', 'Google Play', 'IL2CPP', 'ARM64', 'mobile deploy', 'iOS build', 'Android build', 'target device', 'mobile profiling', 'screen resolution mobile', 'notch', 'safe area inset'."
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


## Output

A mobile build report saved to `Documents/Builds/MOBILE_BUILD_[Platform]_[YYYYMMDD].md` following [MOBILE_BUILD_REPORT.md](assets/templates/MOBILE_BUILD_REPORT.md), plus any platform-specific code changes (touch controls, native plugins, optimization patches).

## Output Requirement (MANDATORY)

**Every build report MUST follow the template**: [MOBILE_BUILD_REPORT.md](.opencode/skills/unity/unity-mobile-deploy/assets/templates/MOBILE_BUILD_REPORT.md)

Save output to: `Documents/Builds/MOBILE_BUILD_[Platform]_[YYYYMMDD].md`

Read the template first, then populate all sections.

## Workflow

1. **Profile**: Target devices, min specs, permissions, native services
2. **Implement**: Platform-aware managers (see [MOBILE_INTEROP_PATTERNS.md](.opencode/skills/unity/unity-mobile-deploy/references/MOBILE_INTEROP_PATTERNS.md))
3. **Optimize**: Real hardware profiling, textures, shaders, memory (see [MOBILE_OPTIMIZATION_GUIDE.md](.opencode/skills/unity/unity-mobile-deploy/references/MOBILE_OPTIMIZATION_GUIDE.md))
4. **Deploy**: Build report via [MOBILE_BUILD_REPORT.md](.opencode/skills/unity/unity-mobile-deploy/assets/templates/MOBILE_BUILD_REPORT.md), validate Gradle/Xcode

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

Use `unityMCP_*` tools for build configuration, profiling, and validation.

| Operation | MCP Tool |
|-----------|----------|
| Editor/build state | `unityMCP_get_unity_editor_state` |
| Check compilation | `unityMCP_check_compile_errors` |
| Run build script | `unityMCP_execute_script(filePath="...")` |
| Console output | `unityMCP_get_unity_logs()` |
| CPU profiling | `unityMCP_get_worst_cpu_frames` |
| GC profiling | `unityMCP_get_worst_gc_frames` |
| High-poly audit | `unityMCP_list_objects_with_high_polygon_count()` |
| Installed packages | `unityMCP_list_packages` |

### Mobile Build Verification Flow

```
1. unityMCP_get_unity_editor_state            → Confirm build target (iOS/Android)
2. unityMCP_check_compile_errors              → Verify clean compilation
3. unityMCP_execute_script(filePath="...")     → Run platform-specific build script
4. unityMCP_get_unity_logs(show_errors=true)  → Check for build errors
```

## Handoff & Boundaries

- **OWNS**: iOS/Android-specific development — touch controls, mobile optimization (battery, heat, memory), native features (IAP, notifications), and mobile build pipelines.
- **Delegates to**: `unity-build-pipeline` for general build automation and CI/CD. `unity-optimize-performance` for platform-agnostic performance optimization.
- **Does NOT**: Handle WebGL builds (use `unity-web-deploy`). Does not handle general build scripting (use `unity-build-pipeline`).

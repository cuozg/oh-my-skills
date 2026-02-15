---
name: unity-mobile-deploy
description: "(opencode-project - Skill) iOS/Android development. Use when: (1) Touch controls/gestures, (2) Mobile optimization (battery, heat, memory), (3) Native features (IAP, notifications), (4) Mobile build pipelines, (5) Platform-specific player settings, (6) Device testing and profiling. Triggers: 'build for iOS', 'deploy Android', 'mobile build', 'touch input', 'swipe gesture', 'IAP', 'in-app purchase', 'push notification', 'battery optimization', 'thermal throttling', 'mobile memory', 'Xcode', 'Gradle', 'Android manifest', 'provisioning profile', 'APK', 'IPA', 'App Store', 'Google Play', 'IL2CPP', 'ARM64', 'mobile deploy', 'iOS build', 'Android build', 'target device', 'mobile profiling', 'screen resolution mobile', 'notch', 'safe area inset'."
---

# Unity Mobile Developer

**Input**: Mobile task description. Optional: file paths, target platform, constraints.

**Output**: Build report per [MOBILE_BUILD_REPORT.md](.opencode/skills/unity/unity-mobile-deploy/assets/templates/MOBILE_BUILD_REPORT.md) template. Saved to `Documents/Builds/MOBILE_BUILD_[Platform]_[YYYYMMDD].md`.

## Workflow

1. **Profile**: Target devices, min specs, permissions, native services
2. **Implement**: Platform-aware managers (see [MOBILE_INTEROP_PATTERNS.md](.opencode/skills/unity/unity-mobile-deploy/references/MOBILE_INTEROP_PATTERNS.md))
3. **Optimize**: Real hardware profiling, textures, shaders, memory (see [MOBILE_OPTIMIZATION_GUIDE.md](.opencode/skills/unity/unity-mobile-deploy/references/MOBILE_OPTIMIZATION_GUIDE.md))
4. **Deploy**: Build report via template, validate Gradle/Xcode

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
- **Safe Area**: Respect notches/home indicators

## Handoff

- **Delegates to**: `unity-build-pipeline` (general build automation/CI/CD), `unity-optimize-performance` (platform-agnostic perf)
- **Does NOT**: WebGL builds (use `unity-web-deploy`), general build scripting (use `unity-build-pipeline`)

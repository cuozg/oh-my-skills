---
name: unity-mobile-deploy
description: "iOS/Android development. Use when: (1) Touch controls/gestures, (2) Mobile optimization (battery, heat, memory), (3) Native features (IAP, notifications), (4) Mobile build pipelines."
---

# Unity Mobile Developer

iOS and Android platform specialist.

## Output Requirement (MANDATORY)

**Every build report MUST follow the template**: [MOBILE_BUILD_REPORT.md](assets/templates/MOBILE_BUILD_REPORT.md)

Save output to: `Documents/Builds/MOBILE_BUILD_[Platform]_[YYYYMMDD].md`

Read the template first, then populate all sections.

## Workflow

1. **Profile**: Target devices, min specs, permissions, native services
2. **Implement**: Platform-aware managers (see [MOBILE_INTEROP_PATTERNS.md](references/MOBILE_INTEROP_PATTERNS.md))
3. **Optimize**: Real hardware profiling, textures, shaders, memory (see [MOBILE_OPTIMIZATION_GUIDE.md](references/MOBILE_OPTIMIZATION_GUIDE.md))
4. **Deploy**: Build report via [MOBILE_BUILD_REPORT.md](assets/templates/MOBILE_BUILD_REPORT.md), validate Gradle/Xcode

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

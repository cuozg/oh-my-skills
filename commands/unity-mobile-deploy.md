---
description: Workflow for optimizing, building, and deploying Unity projects to mobile platforms (iOS/Android).
---

# Workflow: Unity Mobile Deployment

Transform your Unity project into a high-performance mobile application for iOS and Android.

1.  **Requirement Mapping**: 
    - Identify target minimum OS versions and hardware tiers.
    - List required native features (In-App Purchases, Push Notifications, Social Services).
2.  **Interop Setup**:
    - Use instructions in `.claude/skills/unity-mobile-deploy/references/MOBILE_INTEROP_PATTERNS.md` to bridge C# and native code.
    - Setup platform-specific managers for IAP or notifications.
3.  **Build Optimization**:
    - Audit texture compression (use ASTC), shader complexity, and build settings.
    - Use `.claude/skills/unity-mobile-deploy/references/MOBILE_OPTIMIZATION_GUIDE.md` to ensure smooth performance.
4.  **Execute Build**:
    // turbo
    - Run building processes for the target platform (iOS Xcode project or Android APK/AAB).
5.  **Technical Audit**:
    - Use the `MOBILE_BUILD_REPORT.md` template from `.claude/skills/unity-mobile-deploy/assets/templates/`.
    - Save to `Documents/MobileBuilds/REPORT_[BuildName]_[Timestamp].md`.
6.  **Verification**:
    - Profile on real hardware and verify touch input, IAP flows, and background behavior.

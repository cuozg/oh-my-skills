# Mobile Build & Performance Report: [Project Name]

## 1. Build Summary
- **Unity Version**: [e.g., 6000.x.x]
- **Target Platform**: [iOS / Android]
- **Scripting Backend**: [IL2CPP]
- **API Compatibility**: [.NET Standard 2.1 / .NET Framework]
- **Build Size**: [Total APK/IPA MB]

## 2. Device Compatibility Analysis
- **Minimum OS Version**: [e.g., Android 8.0 / iOS 14.0]
- **Recommended RAM**: [e.g., 4GB+]
- **Supported Graphics APIs**: [Vulkan/OpenGL ES 3.1 / Metal]
- **Architectures**: [ARM64, ARMv7]

## 3. Performance Metrics (Device: [Model Name])
- **Initial Load Time**: [Seconds]
- **Average FPS (Gameplay)**: [FPS]
- **Memory Usage (Baseline)**: [MB]
- **Battery Drain Rate**: [% per 30 mins]
- **Peak Temperature**: [Celsius]

## 4. Optimization Checklist
### Implemented
- [ ] Switched to ASTC texture compression
- [ ] Optimized shader variants for mobile
- [ ] Set `Application.targetFrameRate` to 30/60
- [ ] Integrated Addressables for remote assets

### Recommended
- [ ] Reduce Draw Calls from [Current] to [Target]
- [ ] Implement manual memory management for large VFX
- [ ] Use Object Pooling for [Specific System]

## 5. Deployment Status
- **Store Icons**: [Configured]
- **Splash Screen**: [Verified]
- **Platform Services (IAP/Social)**: [Tested]
- **Crash Reporting (e.g., Unity Cloud Diagnostics)**: [Active]

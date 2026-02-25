# Mobile Optimization Guide

Comprehensive guide for optimizing Unity games for iOS and Android platforms.

## 1. Graphics & Rendering

- **Texture Compression**: Use `ASTC` (6x6 or 8x8) for modern devices to save memory and improve performance.
- **Draw Call Reduction**: 
  - Use **SRP Batcher** (if using URP).
  - Use **Dynamic Batching** for small meshes.
  - Implement **GPU Instancing** for repetitive environmental objects.
- **Shader Optimization**:
  - Use `URP/SimpleLit` for low-end devices.
  - Avoid `Alpha Blending` where possible; prefer `Alpha Testing` (cutoff) or opaque materials.
  - Minimize the number of unique materials to improve batching.
- **Resolution Scaling**: Scale internal render resolution (e.g., 0.8x or 0.9x) while keeping UI at native resolution.

## 2. Memory Management

- **Asset Bundles / Addressables**: Move massive assets out of the initial build to reduce APK/IPA size and manage runtime memory.
- **Garbage Collection (GC)**:
  - Avoid `Update()` allocations (e.g., string concatenation, `GetComponent`, `new` objects).
  - Use **Object Pooling** for frequently spawned items (bullets, VFX, UI elements).
  - Use `Incremental GC` to reduce frame spikes.
- **Audio Optimization**: 
  - Set small clips to `Decompress on Load`.
  - Set large music tracks to `Compressed in Memory` or `Streaming`.

## 3. Physical Performance

- **Target Frame Rate**: Use `Application.targetFrameRate = 30` or `60`. 30 FPS is often better for battery life and thermal stability on mid-range devices.
- **Thermal Throttling**: Monitor device temperature and dynamically reduce quality if the device starts to overheat.
- **Battery Life**: Avoid high-frequency network requests and excessive sensor usage (GPS, Gyro) when not needed.

## 4. Platform-Specific Optimization

### Android
- Use **Vulkan** for better multi-threading and lower CPU overhead on supported devices.
- Profile using **Android GPU Inspector** or Qualcomm **Snapdragon Profiler**.

### iOS
- Use **Metal** graphics API.
- Profile using **Xcode Instruments** (Time Profiler, Leaks, Metal System Trace).

## 5. UI Optimization
- Disable `Raycast Target` on UI elements that don't need interaction.
- Break large Canvases into smaller ones to minimize the "re-batching" cost when a single element changes.
- Avoid using `Layout Groups` in moving UI elements if possible.

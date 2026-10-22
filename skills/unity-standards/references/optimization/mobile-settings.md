# Mobile Optimization Settings

## Target Frame Rate

```csharp
// Set explicitly - iOS/Android default to 30 fps when targetFrameRate is -1
Application.targetFrameRate = 60; // or 30 for battery-conscious experiences

// Menus/idle screens: keep 60 Hz input/Update but render every 2nd frame
UnityEngine.Rendering.OnDemandRendering.renderFrameInterval = 2;
```

| Target | Use Case | Battery Impact |
|--------|----------|----------------|
| 30 fps | Casual, puzzle, turn-based | Low |
| 60 fps | Action, racing, shooter | High |
| Adaptive | Games with thermal concern | Medium |

## Thermal Throttling Management

Sustained GPU and CPU load causes thermal throttling. Read thermal warnings
through the Adaptive Performance package
(`com.unity.adaptiveperformance`, provider per platform) and lower the target
frame rate or quality when it reports throttling. Check the installed package
version for the exact API and supported devices.

**Budget with throttling factor:**
- Peak performance: 16.67ms frame budget at 60 FPS
- After sustained load: budget can effectively widen to 25-30ms on weak devices
- Design for headroom instead of shipping right at the thermal edge

**Mitigation strategies:**
- Reduce particle counts when throttling is imminent
- Lower LOD bias dynamically
- Disable expensive post-processing first
- Reduce shadow resolution or distance

## Resolution Scaling

Prefer URP **Render Scale** (URP Asset > Quality) over `Screen.SetResolution`:
it scales 3D rendering only, keeps Screen Space - Overlay UI at native
resolution, and can be changed at runtime per quality tier. Upscaling Filter
options include FSR 1 and STP (Unity 6); STP needs compute shader support and
costs GPU time, so measure it on low-end mobile before enabling.

| Scale | Visual Impact | Max GPU Savings (fill-bound) |
|-------|--------------|-----------------|
| 100% | Native | Baseline |
| 85% | Barely noticeable | up to ~25% |
| 75% | Slight softening | up to ~40% |
| 50% | Noticeably blurry | up to ~70% |

**Pattern:** Scale down when frame time exceeds budget, scale up when headroom exists.

## Mobile Quality Settings

### Recommended Player Settings

| Setting | Value | Why |
|---------|-------|-----|
| Scripting Backend | IL2CPP | Required for iOS and Android ARM64 |
| Managed Stripping Level | Medium-High | Reduce binary size (see `build-settings.md`) |
| Target Architecture | ARM64 only | Store requirement and simpler QA |
| Rendering Path (URP Renderer) | Forward, or Forward+ for many real-time lights | Deferred is usually too expensive |
| Color Space | Linear | Better lighting consistency |
| Use Incremental GC | ON | Avoids long GC spikes |

### Recommended Quality Settings

In URP, MSAA, shadows, and light limits live on the URP Asset assigned to each
Quality level; the rest are in Project Settings > Quality.

| Setting | Where | Mobile Value | Why |
|---------|-------|-------------|-----|
| VSync Count | Quality | Don't Sync | Prefer explicit `targetFrameRate` |
| Anti-Aliasing | URP Asset | 2x MSAA or Off | 4x and 8x are often too expensive |
| Shadow Resolution | URP Asset | 512-1024 | High resolutions are costly |
| Shadow Distance | URP Asset | 20-50m | Reduces shadow map work |
| Additional Lights (per object limit) | URP Asset | 1-2, or Disabled | Limit real-time lights |
| Global Mipmap Limit | Quality | Half Res for low-end | Reduces memory pressure |
| LOD Bias | Quality | 0.5-0.7 | More aggressive LOD switching |
| Particle Raycast Budget | Quality | 16-64 | Limit collision checks |

## Mobile-Specific Code Patterns

```csharp
// Use cheaper math in hot paths
Vector3.SqrMagnitude(a - b) < threshold * threshold;
```

`Camera.main` is cached internally in Unity 6; still pass or cache the intended
camera in multi-camera scenes for clarity. UI raycast-target and Canvas rules:
`canvas-ui-drawcalls-batching.md`.

## Battery-Conscious Design

- Lower frame rate or `OnDemandRendering.renderFrameInterval` during menus,
  inventory, and pause screens
- Disable unnecessary sensors when not used
- Reduce network polling when the app is backgrounded or idle
- Audio import rules: `memory-settings.md` (Audio Memory)

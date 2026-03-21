# Mobile Optimization Settings

## Target Frame Rate

```csharp
// Set explicitly - mobile often defaults lower than desktop expectations
Application.targetFrameRate = 60; // or 30 for battery-conscious experiences

void Update()
{
    if (SystemInfo.thermalStatus >= ThermalStatus.Throttling)
        Application.targetFrameRate = 30;
    else
        Application.targetFrameRate = 60;
}
```

| Target | Use Case | Battery Impact |
|--------|----------|----------------|
| 30 fps | Casual, puzzle, turn-based | Low |
| 60 fps | Action, racing, shooter | High |
| Adaptive | Games with thermal concern | Medium |

## Thermal Throttling Management

Sustained GPU and CPU load causes thermal throttling.

**Budget with throttling factor:**
- Peak performance: 16.67ms frame budget at 60 FPS
- After sustained load: budget can effectively widen to 25-30ms on weak devices
- Design for headroom instead of shipping right at the thermal edge

**Mitigation strategies:**
- Reduce particle counts when `SystemInfo.thermalStatus >= Warning`
- Lower LOD bias dynamically
- Disable expensive post-processing first
- Reduce shadow resolution or distance

## Resolution Scaling

```csharp
Screen.SetResolution(
    (int)(Screen.width * scaleFactor),
    (int)(Screen.height * scaleFactor),
    true);

// URP dynamic resolution is usually the better long-term option.
```

| Scale | Visual Impact | Performance Gain |
|-------|--------------|-----------------|
| 100% | Native | Baseline |
| 85% | Barely noticeable | 20-30% GPU savings |
| 75% | Slight softening | 40-50% GPU savings |
| 50% | Noticeably blurry | 60-70% GPU savings |

**Pattern:** Scale down when frame time exceeds budget, scale up when headroom exists.

## Mobile Quality Settings

### Recommended Player Settings

| Setting | Value | Why |
|---------|-------|-----|
| Scripting Backend | IL2CPP | Required for iOS and generally faster |
| Managed Stripping Level | Medium-High | Reduce binary size |
| Target Architecture | ARM64 only | Modern store requirement and simpler QA |
| Rendering Path | Forward | Deferred is usually too expensive |
| Color Space | Linear | Better lighting consistency |

### Recommended Quality Settings

| Setting | Mobile Value | Why |
|---------|-------------|-----|
| VSync Count | Don't Sync | Prefer explicit `targetFrameRate` |
| Anti-Aliasing | 2x MSAA or Off | 4x and 8x are often too expensive |
| Shadow Resolution | 512-1024 | High resolutions are costly |
| Shadow Distance | 20-50m | Reduces shadow map work |
| Pixel Light Count | 1-2 | Limit real-time lights |
| Texture Quality | Half Res for low-end | Reduces memory pressure |
| LOD Bias | 0.5-0.7 | More aggressive LOD switching |
| Particle Raycast Budget | 16-64 | Limit collision checks |

## Mobile-Specific Code Patterns

```csharp
// Decorative UI should not block raycasts
image.raycastTarget = false;

// Prefer caching globals used every frame
private int _screenWidth;
void Start() => _screenWidth = Screen.width;

// Use cheaper math in hot paths
Vector3.SqrMagnitude(a - b) < threshold * threshold;
```

`Camera.main` is safer on newer Unity versions than it used to be, but repeated global lookups still reduce clarity in multi-camera scenes. Cache the intended camera when the code path is hot or the scene is not trivial.

## Battery-Conscious Design

- Lower frame rate during menus, inventory, and pause screens
- Disable unnecessary sensors when not used
- Reduce network polling when the app is backgrounded or idle
- OLED-friendly dark UI can help on some devices
- Use mono SFX, lower sample rates where acceptable, and stream music

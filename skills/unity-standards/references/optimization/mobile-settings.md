# Mobile Optimization Settings

## Target Frame Rate

```csharp
// Set explicitly — mobile defaults to 30fps
Application.targetFrameRate = 60; // or 30 for battery-conscious

// Adaptive frame rate based on thermal state (Unity 2022+)
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
| Adaptive | Any game with thermal concern | Medium |

## Thermal Throttling Management

Sustained GPU/CPU load causes thermal throttling — device drops clocks by 30-50%.

**Budget with throttling factor:**
- Peak performance: 16.67ms frame budget (60fps)
- After 5-10 min sustained load: budget effectively 25-30ms
- **Design for 0.65x of peak** to avoid frame drops after warmup

**Mitigation strategies:**
- Reduce particle counts when `SystemInfo.thermalStatus >= Warning`
- Lower LOD bias dynamically
- Disable post-processing effects
- Reduce shadow resolution or disable shadows

## Resolution Scaling

```csharp
// Dynamic resolution scaling
Screen.SetResolution(
    (int)(Screen.width * scaleFactor),
    (int)(Screen.height * scaleFactor),
    true);

// URP Dynamic Resolution (preferred)
// In URP Asset: enable Dynamic Resolution
// Camera → Allow Dynamic Resolution: ON
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
| Scripting Backend | IL2CPP | Required for iOS, 1.5-3x faster |
| Managed Stripping Level | Medium-High | Reduce binary size |
| Target Architecture | ARM64 only | Google Play requires ARM64, drop ARMv7 |
| Rendering Path | Forward | Deferred too expensive for most mobile |
| Color Space | Linear | Correct lighting (Gamma acceptable for simple 2D) |

### Recommended Quality Settings

| Setting | Mobile Value | Why |
|---------|-------------|-----|
| VSync Count | Don't Sync (use targetFrameRate) | VSync on mobile = unpredictable |
| Anti-Aliasing | 2x MSAA or Off | 4x/8x too expensive |
| Shadow Resolution | 512-1024 | 2048+ destroys mobile GPU |
| Shadow Distance | 20-50m | Reduces shadow map coverage |
| Pixel Light Count | 1-2 | Limit real-time lights |
| Texture Quality | Half Res for low-end | Reduces memory pressure |
| LOD Bias | 0.5-0.7 | More aggressive LOD switching |
| Particle Raycast Budget | 16-64 | Limit collision particle checks |

## Mobile-Specific Code Patterns

```csharp
// Reduce texture fillrate pressure
// UI: disable raycast target on non-interactive elements
image.raycastTarget = false; // on decorative UI images

// Avoid Camera.main in Update (cached since 2020.2 but verify)
// Cache heavy system calls
private int _screenWidth;
void Start() => _screenWidth = Screen.width;

// Use simpler math on mobile
Vector3.SqrMagnitude(a - b) < threshold * threshold // instead of Vector3.Distance < threshold
```

## Battery-Conscious Design

- Lower frame rate during menus, inventory, pause (30fps or lower)
- Disable unnecessary sensors (gyroscope, accelerometer) when not used
- Reduce network polling frequency when app is backgrounded
- Use dark UI themes on OLED devices (pixels off = power saved)
- Audio: mono SFX, lower sample rates, streaming for music

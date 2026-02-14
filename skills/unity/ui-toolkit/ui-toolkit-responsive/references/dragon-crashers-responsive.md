# Dragon Crashers Responsive Patterns

> Extracted from [SKILL.md](../SKILL.md) — concrete responsive patterns from the Dragon Crashers UIToolkit demo project.

---

The following sections document concrete responsive patterns from the Dragon Crashers UIToolkit demo project. All file paths are relative to the project root.

## MediaQuery: Aspect Ratio Detection

> **Source**: `Assets/Scripts/Utilities/MediaQuery.cs`, `Assets/Scripts/UI/Events/MediaQueryEvents.cs`

Dragon Crashers uses a `MediaQuery` MonoBehaviour (`[ExecuteInEditMode]`) to detect orientation changes via aspect ratio threshold (`width/height >= 1.2f`), firing static events. Uses `GeometryChangedEvent` on UIDocument root — no `Update()` polling.

```csharp
public enum MediaAspectRatio { Undefined, Landscape, Portrait }

// Static delegates (MediaQueryEvents.cs) — subscribe to track orientation
public class MediaQueryEvents
{
    public static Action<Vector2> ResolutionUpdated;
    public static Action<MediaAspectRatio> AspectRatioUpdated;
}

// Detection (MediaQuery.cs): Landscape when aspect >= 1.2
public const float k_LandscapeMin = 1.2f;
public static MediaAspectRatio CalculateAspectRatio(Vector2 resolution)
    => (resolution.x / resolution.y >= k_LandscapeMin) ? MediaAspectRatio.Landscape : MediaAspectRatio.Portrait;

// Usage: subscribe in OnEnable, unsubscribe in OnDisable
void OnEnable() => MediaQueryEvents.AspectRatioUpdated += OnAspectRatioUpdated;
void OnDisable() => MediaQueryEvents.AspectRatioUpdated -= OnAspectRatioUpdated;
```

> **Cross-ref**: [ui-toolkit-theming](../../ui-toolkit-theming/SKILL.md) for how `ThemeManager` consumes these events.

## SafeAreaBorder: borderWidth Approach

> **Source**: `Assets/Scripts/Utilities/SafeAreaBorder.cs`

Dragon Crashers implements safe area using **`borderWidth`** (not `padding`), allowing visible colored bars behind the notch. Key details:

- Uses `Screen.safeArea` insets applied as `borderTopWidth`, `borderLeftWidth`, etc.
- Configurable `m_Multiplier` (`[Range(0, 1)]`) and `m_BorderColor` via Inspector
- `[ExecuteInEditMode]` — re-applies on `OnValidate()` and `GeometryChangedEvent`
- `ExtensionMethods.GetScreenCoordinate()` compensates for border widths in coordinate conversions

| Safe Area Approach | Mechanism | Use When |
|-------------------|-----------|----------|
| **borderWidth** (DC) | `borderTopWidth` + `borderColor` | Need visible colored bars behind notch |
| **padding** (generic) | `paddingTop` as percentage | Children naturally inset, no visible border |

> **Cross-ref**: [ui-toolkit-mobile](../../ui-toolkit-mobile/SKILL.md) for device-specific safe area considerations. Full code in [Dragon Crashers Insights](../../references/dragon-crashers-insights.md).

## ThemeManager: Orientation-Aware Theming

> **Source**: `Assets/Scripts/UI/Themes/ThemeManager.cs`

Instead of toggling USS classes, Dragon Crashers swaps **entire PanelSettings + ThemeStyleSheet (TSS)** assets per orientation. Theme naming: `{Orientation}--{Variation}` (e.g., `Portrait--Default`). On `AspectRatioUpdated`, builds new theme name and calls `ApplyTheme()` which sets both `panelSettings` and `themeStyleSheet` on the `UIDocument`. **Why swap PanelSettings?** Portrait/Landscape need different reference resolutions, scale modes, or DPI settings.

> **Cross-ref**: [ui-toolkit-theming](../../ui-toolkit-theming/SKILL.md) for TSS structure, custom properties, and seasonal theme variations.

## GeometryChangedEvent Patterns

Dragon Crashers uses `GeometryChangedEvent` as the primary layout trigger — never `Update()` polling. Used by `MediaQuery` (resolution/aspect), `SafeAreaBorder` (border widths), `PositionToVisualElement` (3D repositioning).

```csharp
// Pattern: Register in OnEnable, unregister in OnDisable, run initial setup immediately
void OnEnable()
{
    m_Root = m_Document.rootVisualElement.Q<VisualElement>(m_ElementName);
    m_Root.RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);
    ApplyLayout(); // Initial setup
}
void OnDisable() => m_Root?.UnregisterCallback<GeometryChangedEvent>(OnGeometryChanged);
void OnGeometryChanged(GeometryChangedEvent evt) => ApplyLayout();
```

Fires on: screen resize, orientation change, parent layout change, element added/removed, style changes affecting layout. Does **not** fire every frame.

## PositionToVisualElement: World-to-UI Alignment

> **Source**: `Assets/Scripts/Utilities/PositionToVisualElement.cs`, `Assets/Scripts/Utilities/ExtensionMethods.cs`

Aligns a 3D `GameObject` to a `VisualElement` across orientation changes. **Conversion chain**: `VisualElement.worldBound` → `GetScreenCoordinate()` (adjusts for borderWidth) → `Camera.ScreenToWorldPoint` → `transform.position`. Re-runs on `GeometryChangedEvent` and `ThemeEvents.CameraUpdated` (camera swaps on orientation change). Full code in [Dragon Crashers Insights](../../references/dragon-crashers-insights.md) (section: Screen Implementations).

# Dragon Crashers Responsive Patterns

> Concrete responsive patterns from Dragon Crashers UIToolkit demo. All paths relative to project root.

## MediaQuery: Aspect Ratio Detection

> **Source**: `Assets/Scripts/Utilities/MediaQuery.cs`, `Assets/Scripts/UI/Events/MediaQueryEvents.cs`

`[ExecuteInEditMode]` MonoBehaviour detecting orientation via `width/height >= 1.2f`. Uses `GeometryChangedEvent` — no `Update()` polling.

```csharp
public enum MediaAspectRatio { Undefined, Landscape, Portrait }
public class MediaQueryEvents
{
    public static Action<Vector2> ResolutionUpdated;
    public static Action<MediaAspectRatio> AspectRatioUpdated;
}
// Landscape when aspect >= 1.2
public static MediaAspectRatio CalculateAspectRatio(Vector2 res)
    => (res.x / res.y >= 1.2f) ? MediaAspectRatio.Landscape : MediaAspectRatio.Portrait;
// Subscribe in OnEnable, unsubscribe in OnDisable
```

> **Cross-ref**: [ui-toolkit-theming](../../ui-toolkit-theming/SKILL.md) for ThemeManager consumption.

## SafeAreaBorder: borderWidth Approach

> **Source**: `Assets/Scripts/Utilities/SafeAreaBorder.cs`

Uses `borderWidth` (not padding) for visible colored bars behind notch. `Screen.safeArea` insets → `borderTopWidth` etc. Configurable multiplier + color. `[ExecuteInEditMode]`, reapplies on `OnValidate()` and `GeometryChangedEvent`.

| Approach | Use When |
|----------|----------|
| **borderWidth** (DC) | Need visible colored bars behind notch |
| **padding** | Children naturally inset, no visible border |

> **Cross-ref**: [ui-toolkit-mobile](../../ui-toolkit-mobile/SKILL.md), [Dragon Crashers Insights](../../references/dragon-crashers-insights.md)

## ThemeManager: Orientation-Aware Theming

> **Source**: `Assets/Scripts/UI/Themes/ThemeManager.cs`

Swaps **entire PanelSettings + TSS** per orientation (not USS class toggle). Theme naming: `{Orientation}--{Variation}`. On `AspectRatioUpdated` → builds theme name → `ApplyTheme()` sets both `panelSettings` and `themeStyleSheet`. Separate PanelSettings needed for different reference resolutions per orientation.

> **Cross-ref**: [ui-toolkit-theming](../../ui-toolkit-theming/SKILL.md) for TSS structure and seasonal themes.

## GeometryChangedEvent Patterns

Primary layout trigger — never `Update()` polling. Used by MediaQuery, SafeAreaBorder, PositionToVisualElement.

```csharp
void OnEnable()
{
    m_Root = m_Document.rootVisualElement.Q<VisualElement>(m_ElementName);
    m_Root.RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);
    ApplyLayout(); // Initial setup
}
void OnDisable() => m_Root?.UnregisterCallback<GeometryChangedEvent>(OnGeometryChanged);
```

Fires on: screen resize, orientation change, parent layout change, element add/remove, style changes. Not every frame.

## PositionToVisualElement: World-to-UI Alignment

> **Source**: `Assets/Scripts/Utilities/PositionToVisualElement.cs`

Aligns 3D GameObject to VisualElement across orientations. Chain: `worldBound` → `GetScreenCoordinate()` (adjusts for borderWidth) → `Camera.ScreenToWorldPoint` → `transform.position`. Re-runs on `GeometryChangedEvent` + `ThemeEvents.CameraUpdated`. Full code in [Dragon Crashers Insights](../../references/dragon-crashers-insights.md).

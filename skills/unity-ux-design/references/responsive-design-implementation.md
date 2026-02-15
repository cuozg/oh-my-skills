# Responsive Design Implementation for Mobile Game UI

## 1. Canvas Scaler Configuration

```
[CanvasScaler]
  UI Scale Mode: Scale With Screen Size
  Reference Resolution: 1048 x 2048       // Portrait mobile
  Screen Match Mode: Match Width Or Height
  Match: 0 (Width)                         // Prevents horizontal overflow
```

| Target | Resolution | Match | Best For |
|--------|-----------|-------|----------|
| Portrait standard | 1048×2048 | Width (0) | Super-casual portrait |
| iPhone standard | 1080×1920 | Width (0) | General portrait |
| iPad adaptive | 1536×2048 | 0.5 | Tablet-first / universal |
| Landscape | 1920×1080 | Height (1) | Landscape games |

## 2. Anchor Presets

| Pattern | Anchors | Pivot | Use For |
|---------|---------|-------|---------|
| **Center** | {0.5,0.5}→{0.5,0.5} | (0.5,0.5) | Icons, buttons, cards, fixed-size |
| **Full Stretch** | {0,0}→{1,1} | (0.5,0.5) | Backgrounds, overlays, viewports |
| **Top-Left** | {0,1}→{0,1} | (0,1) | Back buttons, status indicators |
| **Bottom Stretch-H** | {0,0}→{1,0} | (0.5,0) | Bottom nav bars, footers |
| **Top Stretch-H** | {0,1}→{1,1} | (0.5,1) | Top bars, resource headers |
| **Corner** | TL:{0,1} TR:{1,1} BL:{0,0} BR:{1,0} | Match corner | Corner-pinned elements |
| **Left Stretch-V** | {0,0}→{0,1} | (0,0.5) | Left side panels (rare) |

## 3. Layout Groups

### HorizontalLayoutGroup

| Property | Resource Bar | Nav Bar | Price Group |
|----------|-------------|---------|-------------|
| Spacing | 100 | 0 | 8 |
| Alignment | UpperCenter | MiddleCenter | MiddleLeft |
| Control Width/Height | false/false | false/false | false/false |
| Force Expand W | false | true | false |

### VerticalLayoutGroup (scroll content)
```
Spacing: 12, Alignment: UpperCenter
Control Child Size: Width=true, Height=false
Padding: 20,20,10,10
```

### GridLayoutGroup

| Property | Button Grid | Calendar | Item Grid |
|----------|------------|----------|-----------|
| Cell Size | 409×105 | 140×160 | 180×200 |
| Spacing | 36×25 | 12×12 | 16×16 |
| Constraint | FixedColumnCount | FixedColumnCount | FixedColumnCount |
| Columns | 2 | 6 | 3-4 |

**Alignment enum**: 0=UpperLeft, 1=UpperCenter, 2=UpperRight, 3=MiddleLeft, 4=MiddleCenter, 5=MiddleRight, 6=LowerLeft, 7=LowerCenter, 8=LowerRight

## 4. ContentSizeFitter

**Scroll content**: Anchor top-stretch {0,1}→{1,1}, Pivot (0.5,1), `Vertical Fit: PreferredSize`
**Auto-size text**: Pair with LayoutGroup, both fits = PreferredSize
Never on root elements. Only on children of LayoutGroups or scroll content.

## 5. Safe Area

```csharp
[RequireComponent(typeof(RectTransform))]
public class SafeArea : MonoBehaviour
{
    RectTransform rectTransform;
    Rect lastSafeArea;
    Vector2Int lastScreenSize;
    ScreenOrientation lastOrientation;

    void Awake() { rectTransform = GetComponent<RectTransform>(); ApplySafeArea(); }

    void Update()
    {
        if (lastSafeArea != Screen.safeArea || lastScreenSize.x != Screen.width
            || lastScreenSize.y != Screen.height || lastOrientation != Screen.orientation)
            ApplySafeArea();
    }

    void ApplySafeArea()
    {
        var sa = Screen.safeArea;
        var canvas = GetComponentInParent<Canvas>().rootCanvas;
        rectTransform.anchorMin = new Vector2(sa.x / canvas.pixelRect.width, sa.y / canvas.pixelRect.height);
        rectTransform.anchorMax = new Vector2((sa.x + sa.width) / canvas.pixelRect.width, (sa.y + sa.height) / canvas.pixelRect.height);
        lastSafeArea = sa;
        lastScreenSize = new Vector2Int(Screen.width, Screen.height);
        lastOrientation = Screen.orientation;
    }
}
```

**Hierarchy**: Canvas → SafeAreaPanel (full stretch + script) → all screens. Backgrounds/dim overlays outside SafeArea.

## 6. ScrollRect Configuration

```
Horizontal: false, Vertical: true
Movement Type: Elastic, Elasticity: 0.1
Inertia: true, Deceleration: 0.135
Scrollbar Visibility: AutoHideAndExpandViewport
```

**Required structure**: ScrollView → Viewport (Mask/RectMask2D, full stretch) → Content (top-anchor, pivot top, VLG/GLG + ContentSizeFitter)

**Mask vs RectMask2D**: Use RectMask2D for rectangular clips (better perf). Use Mask only for rounded/shaped clips.

## 7. Layout Recipes

### Resource Bar (top)
Top Stretch-H, H=80. HLG spacing=20, Force Expand Width=true, padding 40,40,0,0. Children: LayoutElement flexibleWidth=1.

### Scrollable Card List (middle)
Full Stretch with offsets for header/footer. ScrollView → Viewport (RectMask2D) → Content (VLG spacing=16, ContentSizeFitter vertical=PreferredSize).

### Bottom Tab Bar
Bottom Stretch-H, H=120. HLG spacing=0, Force Expand Width=true. Children: LayoutElement flexibleWidth=1 (center tab=1.5).

### Centered Popup
Center anchor. VLG padding=40,40,30,30, spacing=20. ContentSizeFitter vertical=PreferredSize. Header(80) + Body(flex) + Footer(100).

## 8. Resolution Test Checklist

| Device | Resolution | Check |
|--------|-----------|-------|
| iPhone SE | 750×1334 | Narrow width |
| iPhone 15 | 1179×2556 | Tall + notch |
| Galaxy S24 | 1080×2340 | Android standard |
| iPad Mini | 1488×2266 | Tablet proportions |
| iPad Pro 12.9 | 2048×2732 | Largest tablet |

Verify: no clipping/overlap, touch ≥44pt, safe area, smooth scroll, full bg coverage.

# UI Component Reference for Mobile Game UI

## Component Census

| Component | Count | Role |
|-----------|-------|------|
| Image | 3,755 | Backgrounds, icons, borders, decorations |
| TextMeshProUGUI | 1,142 | All text rendering |
| Shadow | 611 | Drop shadow effects |
| Mask | 247 | Content clipping |
| Button | 230 | Tap interactions |
| HorizontalLayoutGroup | 184 | Horizontal auto-layout |
| LayoutElement | 170 | Layout size control |
| ContentSizeFitter | 71 | Auto-sizing containers |
| VerticalLayoutGroup | 48 | Vertical auto-layout |
| Slider | 37 | Progress bars, volume |
| GridLayoutGroup | 16 | Grid layouts |
| ScrollRect | 15 | Scrollable areas |
| RectMask2D | 7 | Rectangular clipping (perf) |
| TMP_InputField | 7 | Text input |
| Toggle | 4 | On/off switches |

## 1. Image

Naming: `Bg`, `Icon_*`, `Border_*`, `Image_*`. Types: Simple (icons), Sliced (panels/buttons, 9-slice), Filled (progress bars).

```
[Image]
  Raycast Target: false         // Disable on non-interactive
  Image Type: Sliced            // For panels/buttons
  Pixels Per Unit: 100
```

**Perf**: Disable Raycast Target on decorative images. Use sprite atlases. Prefer Sliced for panels.

## 2. TextMeshProUGUI

Naming: `Text_Title`, `Text_Price`, `Text_Level`. Always bold, outlined, with shadow for readability.

| Tier | Size | Usage |
|------|------|-------|
| Display | 48-72 | Level numbers, "VICTORY!" |
| Heading | 36-48 | Screen titles, popup headers |
| Body | 24-32 | Descriptions, dialog |
| Caption | 16-20 | Timestamps, helper text |
| Badge | 14-18 | Notification counts |

```
[TextMeshProUGUI]
  Font Style: Bold
  Overflow: Ellipsis
  Raycast Target: false
  // Material: Outline width 0.2-0.4, dark color. Shadow offset (1,-1)
```

## 3. Button

All 230 use ColorTint transition. Min touch size: 120px (primary), 80px (standard), 60×60 (icon).

```
[Button]
  Transition: Color Tint
  Normal: (1,1,1,1)  Highlighted: (0.96,0.96,0.96,1)
  Pressed: (0.784,0.784,0.784,1)  Disabled: (0.784,0.784,0.784,0.5)
  Fade Duration: 0.1
```

**Hierarchy**: Button_Play → [Image(sliced)] [Button] [Shadow] → Text_Label + Icon (optional)

| Type | Color | Size | Examples |
|------|-------|------|----------|
| Primary CTA | Yellow/Gold | 400×120 | Play, Claim |
| Secondary | Cyan/Blue | 300×80 | Go, Buy |
| Destructive | Red | 80×80 | Close (X) |
| Navigation | Blue/Dark | 80×80 | Back, Next |
| Tab | Varies | Flex×60 | Tab bar |
| Utility | Gray/Blue | 60×60 | Add (+), settings |

## 4. Shadow

```
[Shadow]
  Effect Color: (0,0,0,0.3)
  Effect Distance: (2,-2)
  Use Graphic Alpha: true
```

Applied to buttons, panels, cards. Not on small icons or backgrounds.

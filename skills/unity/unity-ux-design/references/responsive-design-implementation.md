# Responsive Design Implementation for Mobile Game UI

> Derived from Layer Lab GUI Pro-SuperCasual DemoScene.unity analysis and mobile UI best practices

## 1. Canvas Scaler Configuration

### Layer Lab Production Settings

```
Canvas
  [Canvas]
    Render Mode: Screen Space - Camera      // m_RenderMode: 1
    
  [CanvasScaler]
    UI Scale Mode: Scale With Screen Size   // m_UiScaleMode: 1
    Reference Resolution: 1048 x 2048      // Portrait mobile (≈9:16 aspect)
    Screen Match Mode: Match Width Or Height
    Match Width Or Height: 0               // Match WIDTH (0 = width, 1 = height)
    
  [GraphicRaycaster]
    // Default settings
```

### Why These Settings Work

| Setting | Value | Reasoning |
|---------|-------|-----------|
| **Render Mode** | Screen Space - Camera | Allows post-processing, depth sorting with 3D elements |
| **Scale Mode** | Scale With Screen Size | Adapts to all mobile resolutions |
| **Reference Resolution** | 1048×2048 | Portrait 9:19.5 ratio, covers modern phones |
| **Match** | 0 (Width) | Width-matching prevents horizontal overflow; vertical overflow is handled by scrolling |

### Common Reference Resolutions

| Target | Resolution | Match | Best For |
|--------|-----------|-------|----------|
| Layer Lab Standard | 1048×2048 | Width (0) | Super-casual portrait games |
| iPhone Standard | 1080×1920 | Width (0) | General portrait games |
| iPad Adaptive | 1536×2048 | 0.5 (balanced) | Tablet-first or universal |
| Landscape Game | 1920×1080 | Height (1) | Landscape-oriented games |

## 2. Anchor Presets — Complete Reference

### The 5 Core Anchor Patterns (from Layer Lab)

#### Pattern 1: Center (2,036 instances — most common)
```
AnchorMin: (0.5, 0.5)
AnchorMax: (0.5, 0.5)
Pivot: (0.5, 0.5)
```
- **Use for**: Icons, buttons, cards, fixed-size elements
- **Behavior**: Element stays centered, size is fixed via `sizeDelta`
- **Layer Lab examples**: Most `Icon_`, `Button_`, decorative elements

#### Pattern 2: Full Stretch (1,433 instances)
```
AnchorMin: (0, 0)
AnchorMax: (1, 1)
Pivot: (0.5, 0.5)
Left/Right/Top/Bottom: 0 (or small padding)
```
- **Use for**: Backgrounds, overlays, dim layers, viewports, panels
- **Behavior**: Element fills entire parent, scales with parent
- **Layer Lab examples**: `Bg`, `Dim`, `Viewport`, `Background`

#### Pattern 3: Top-Left (895 instances)
```
AnchorMin: (0, 1)
AnchorMax: (0, 1)
Pivot: (0, 1)
```
- **Use for**: Back buttons, status indicators, labels positioned from top-left
- **Behavior**: Fixed distance from top-left corner
- **Layer Lab examples**: Navigation elements, sequential list items

#### Pattern 4: Bottom Stretch-H (198 instances)
```
AnchorMin: (0, 0)
AnchorMax: (1, 0)
Pivot: (0.5, 0)
```
- **Use for**: Bottom navigation bars, footer action panels
- **Behavior**: Full width at bottom, fixed height
- **Layer Lab examples**: `BottomBar_Menu`, action button rows

#### Pattern 5: Top Stretch-H (171 instances)
```
AnchorMin: (0, 1)
AnchorMax: (1, 1)
Pivot: (0.5, 1)
```
- **Use for**: Top status bars, resource headers, title bars
- **Behavior**: Full width at top, fixed height
- **Layer Lab examples**: `Topbar`, `Group_ResourceBar`

### Anchor Decision Matrix

```
┌─────────────────────────────────────────────┐
│              Should element...               │
│                                             │
│  Fill parent entirely?                      │
│    → Full Stretch {0,0}→{1,1}              │
│                                             │
│  Span full width?                           │
│    At top?    → Top Stretch-H {0,1}→{1,1}  │
│    At bottom? → Bottom Stretch-H {0,0}→{1,0}│
│                                             │
│  Stay fixed size?                           │
│    Centered?  → Center {0.5,0.5}            │
│    In corner? → Corner anchor               │
│                (TL: {0,1}, TR: {1,1},       │
│                 BL: {0,0}, BR: {1,0})       │
│                                             │
│  Span full height? (rare in mobile)         │
│    Left edge?  → Left Stretch-V {0,0}→{0,1}│
│    Right edge? → Right Stretch-V {1,0}→{1,1}│
└─────────────────────────────────────────────┘
```

## 3. Layout Groups — Configuration Guide

### HorizontalLayoutGroup (184 instances in Layer Lab)

**Resource Bar Example** (Layer Lab: `Group_ResourceBar`):
```
[HorizontalLayoutGroup]
  Spacing: 100              // Large gap between currency items
  Child Alignment: UpperCenter  // alignment=5
  Control Child Size: Width=false, Height=false
  Child Force Expand: Width=false, Height=false
  Padding: 0,0,0,0
```

**Bottom Navigation Example** (Layer Lab: `BottomBar_Menu`):
```
[HorizontalLayoutGroup]
  Spacing: 0                // Tabs touch each other
  Child Alignment: MiddleCenter  // alignment=7 (see below)
  Control Child Size: Width=false, Height=false
  Child Force Expand: Width=true, Height=false  // Distribute evenly
```

**Price Group Example** (Layer Lab: `Group_Price`):
```
[HorizontalLayoutGroup]
  Spacing: 8                // Tight icon-to-text gap
  Child Alignment: MiddleLeft  // alignment=4
  Control Child Size: Width=false, Height=false
  Child Force Expand: Width=false, Height=false
```

### VerticalLayoutGroup (48 instances in Layer Lab)

**Scroll Content Example**:
```
[VerticalLayoutGroup]
  Spacing: 12               // Consistent row gap
  Child Alignment: UpperCenter
  Control Child Size: Width=true, Height=false  // Full-width rows
  Child Force Expand: Width=false, Height=false
  Padding: 20,20,10,10      // Left, Right, Top, Bottom
```

### GridLayoutGroup (16 instances in Layer Lab)

**Button Grid Example** (Layer Lab: `Group_Buttons`):
```
[GridLayoutGroup]
  Cell Size: (409, 105)     // Fixed cell dimensions
  Spacing: (36, 25)         // Horizontal gap, Vertical gap
  Start Corner: UpperLeft
  Start Axis: Horizontal
  Child Alignment: MiddleCenter
  Constraint: FixedColumnCount
  Constraint Count: 2       // 2-column grid
```

**Daily Bonus Calendar Example**:
```
[GridLayoutGroup]
  Cell Size: (140, 160)     // Square-ish reward cells
  Spacing: (12, 12)         // Equal gaps
  Start Corner: UpperLeft
  Start Axis: Horizontal
  Constraint: FixedColumnCount
  Constraint Count: 6       // 6 columns for 30-day calendar
```

### Child Alignment Values Reference

| Value | Enum | Visual Position |
|-------|------|----------------|
| 0 | UpperLeft | Top-left |
| 1 | UpperCenter | Top-center |
| 2 | UpperRight | Top-right |
| 3 | MiddleLeft | Center-left |
| 4 | MiddleCenter | Dead center |
| 5 | MiddleRight | Center-right |
| 6 | LowerLeft | Bottom-left |
| 7 | LowerCenter | Bottom-center |
| 8 | LowerRight | Bottom-right |

## 4. ContentSizeFitter (71 instances in Layer Lab)

### Dynamic Scroll Content
```
Content                      // Inside ScrollRect > Viewport
  [RectTransform]
    AnchorMin: (0, 1)       // Top-left anchor
    AnchorMax: (1, 1)       // Top-right anchor (stretch width)
    Pivot: (0.5, 1)         // Top-center pivot
  [VerticalLayoutGroup]
    Spacing: 12
    Control Child Size: Width=true, Height=false
  [ContentSizeFitter]
    Horizontal Fit: Unconstrained
    Vertical Fit: PreferredSize   // Grows vertically with content
```

### Auto-Sizing Text Container
```
Group_TextBlock
  [RectTransform]
  [VerticalLayoutGroup]
  [ContentSizeFitter]
    Horizontal Fit: PreferredSize  // Shrink-wrap to text width
    Vertical Fit: PreferredSize    // Grow with text lines
```

### ContentSizeFitter Rules
1. **Scroll content**: Always use `Vertical Fit: PreferredSize` on the `Content` GameObject
2. **Text wrapping**: Use with LayoutGroup to auto-size containers around text
3. **Never on root-level elements**: Only on children of Layout Groups or Scroll content
4. **Pair with LayoutElement**: Use `[LayoutElement]` on children to set min/preferred/flexible sizes

## 5. Safe Area Implementation

> **Note**: Layer Lab DemoScene does NOT implement SafeArea. This section provides the standard implementation that should be added to any production mobile UI.

### SafeArea Script
```csharp
using UnityEngine;

/// <summary>
/// Adjusts RectTransform to respect device safe area (notches, home indicators).
/// Attach to a panel that should be inset from screen edges.
/// </summary>
[RequireComponent(typeof(RectTransform))]
public class SafeArea : MonoBehaviour
{
    private RectTransform rectTransform;
    private Rect lastSafeArea;
    private Vector2Int lastScreenSize;
    private ScreenOrientation lastOrientation;

    private void Awake()
    {
        rectTransform = GetComponent<RectTransform>();
        ApplySafeArea();
    }

    private void Update()
    {
        if (lastSafeArea != Screen.safeArea 
            || lastScreenSize.x != Screen.width 
            || lastScreenSize.y != Screen.height
            || lastOrientation != Screen.orientation)
        {
            ApplySafeArea();
        }
    }

    private void ApplySafeArea()
    {
        Rect safeArea = Screen.safeArea;
        
        Vector2 anchorMin = safeArea.position;
        Vector2 anchorMax = safeArea.position + safeArea.size;
        
        Canvas canvas = GetComponentInParent<Canvas>().rootCanvas;
        anchorMin.x /= canvas.pixelRect.width;
        anchorMin.y /= canvas.pixelRect.height;
        anchorMax.x /= canvas.pixelRect.width;
        anchorMax.y /= canvas.pixelRect.height;
        
        rectTransform.anchorMin = anchorMin;
        rectTransform.anchorMax = anchorMax;
        
        lastSafeArea = safeArea;
        lastScreenSize = new Vector2Int(Screen.width, Screen.height);
        lastOrientation = Screen.orientation;
    }
}
```

### SafeArea Hierarchy Integration
```
Canvas
  +-- SafeAreaPanel            // Full stretch anchors + SafeArea script
  |     +-- Panel              // All screens go here (inside safe area)
  |           +-- Screen_Lobby
  |           +-- Screen_Shop
  |           +-- ...
  +-- UnsafeContent            // Content that SHOULD extend to edges
        +-- Background         // Full-bleed backgrounds
        +-- Dim                // Full-screen overlays
```

### What Goes Inside vs Outside SafeArea

| Inside SafeArea | Outside SafeArea (full-bleed) |
|----------------|------------------------------|
| All interactive buttons | Background images |
| Text content | Dim/overlay layers |
| Navigation bars | Decorative edge elements |
| Resource bars | Status bar tints |
| Scroll content | |
| Input fields | |

## 6. ScrollRect Configuration

### Layer Lab Standard Config (all 15 instances)
```
[ScrollRect]
  Content: {Content RectTransform}
  Horizontal: false            // Vertical-only scrolling
  Vertical: true
  Movement Type: Elastic       // m_MovementType: 1
  Elasticity: 0.1              // Tight bounce-back
  Inertia: true
  Deceleration Rate: 0.135     // Default
  Scroll Sensitivity: 1
  Viewport: {Viewport RectTransform}
  Vertical Scrollbar: {optional}
  Vertical Scrollbar Visibility: AutoHideAndExpandViewport
```

### ScrollRect Hierarchy (mandatory structure)
```
ScrollView
  [ScrollRect]                // References Viewport and Content
  [Image]                     // Optional background
  +-- Viewport               // MUST have Mask or RectMask2D
  |     [RectTransform]      // Full stretch: {0,0}→{1,1}
  |     [Mask]               // Clips content (247 Mask instances in Layer Lab)
  |     [Image]              // Required by Mask component
  |     +-- Content          // Dynamic size container
  |           [RectTransform] // Top-anchored, pivot top: (0.5, 1)
  |           [VerticalLayoutGroup]
  |           [ContentSizeFitter]  // Vertical: PreferredSize
  +-- Scrollbar_Vertical     // Optional
        [Scrollbar]
        +-- Sliding_Area
              +-- Handle
```

### Mask vs RectMask2D

| Feature | Mask (Layer Lab uses) | RectMask2D |
|---------|----------------------|------------|
| Count in Layer Lab | 247 | 7 |
| Shape | Any (follows Image shape) | Rectangle only |
| Performance | Slower (extra draw calls) | Faster (no extra draw calls) |
| Recommendation | Rounded/shaped clips | Rectangular scroll views |

**Production tip**: Replace `Mask` with `RectMask2D` on rectangular scroll views for better performance.

## 7. Responsive Layout Recipes

### Recipe 1: Adaptive Resource Bar
```
Group_ResourceBar             // Top of screen
  [RectTransform]
    Anchor: Top Stretch-H {0,1}→{1,1}
    Height: 80
  [HorizontalLayoutGroup]
    Spacing: 20
    Child Force Expand Width: true  // Distribute evenly
    Padding: 40,40,0,0             // Side margins
  +-- Item_Energy
  |     [LayoutElement]
  |       Flexible Width: 1
  +-- Item_Coins
  |     [LayoutElement]
  |       Flexible Width: 1
  +-- Item_Gems
        [LayoutElement]
          Flexible Width: 1
```

### Recipe 2: Scrollable Card List
```
Middle                        // Content section
  [RectTransform]
    Anchor: Full Stretch {0,0}→{1,1}
    Offsets: Top=-200, Bottom=120  // Leave room for header/footer
  +-- ScrollView
        [ScrollRect] (vertical, elastic 0.1)
        +-- Viewport
        |     [RectMask2D]    // Use RectMask2D for performance
        |     +-- Content
        |           [VerticalLayoutGroup] spacing=16
        |           [ContentSizeFitter] vertical=PreferredSize
        |           +-- Card_Item (prefab instances)
        +-- Scrollbar_Vertical (optional)
```

### Recipe 3: Bottom Tab Bar
```
BottomBar_Menu
  [RectTransform]
    Anchor: Bottom Stretch-H {0,0}→{1,0}
    Height: 120
  [HorizontalLayoutGroup]
    Spacing: 0
    Child Force Expand Width: true
  +-- Tab_Home
  |     [LayoutElement] Flexible Width: 1
  +-- Tab_Shop
  |     [LayoutElement] Flexible Width: 1
  +-- Tab_Play       // Center tab (often larger)
  |     [LayoutElement] Flexible Width: 1.5
  +-- Tab_Social
  |     [LayoutElement] Flexible Width: 1
  +-- Tab_Profile
        [LayoutElement] Flexible Width: 1
```

### Recipe 4: Centered Popup with Margins
```
Popup_Content
  [RectTransform]
    Anchor: Center {0.5,0.5}
    Size: relative to parent using LayoutElement
  [VerticalLayoutGroup]
    Padding: 40,40,30,30
    Spacing: 20
  [ContentSizeFitter]
    Vertical: PreferredSize
  +-- Header
  |     [LayoutElement] Preferred Height: 80
  +-- Body
  |     [LayoutElement] Flexible Height: 1
  +-- Footer
        [LayoutElement] Preferred Height: 100
```

## 8. Testing Responsive Layouts

### Resolution Checklist (test in Unity Game view)

| Device | Resolution | Aspect Ratio | Key Check |
|--------|-----------|-------------|-----------|
| iPhone SE | 750×1334 | 9:16 | Narrow width |
| iPhone 15 | 1179×2556 | 9:19.5 | Tall with notch |
| iPhone 15 Pro Max | 1290×2796 | 9:19.5 | Widest modern phone |
| Samsung Galaxy S24 | 1080×2340 | 9:19.5 | Android standard |
| iPad Mini | 1488×2266 | ~2:3 | Tablet proportions |
| iPad Pro 12.9 | 2048×2732 | 3:4 | Largest tablet |

### What to Verify
1. **No clipping**: Text and buttons don't overflow their containers
2. **No overlap**: Adjacent elements maintain spacing at all resolutions
3. **Touch targets**: Buttons remain ≥44pt (≈80px at 2x) at narrowest resolution
4. **Safe area**: Content avoids notch/home indicator regions
5. **Scroll behavior**: Lists scroll smoothly, content doesn't jump
6. **Background coverage**: Backgrounds fill screen without letterboxing

---

*Reference: Layer Lab GUI Pro-SuperCasual DemoScene.unity — CanvasScaler 1048×2048 match-width, 2036 center anchors, 1433 stretch anchors, 184 HLG, 48 VLG, 16 GLG, 71 ContentSizeFitter, 15 ScrollRect*

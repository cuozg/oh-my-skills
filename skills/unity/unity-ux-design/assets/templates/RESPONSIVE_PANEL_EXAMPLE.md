# Responsive Panel Example Template

> Demonstrates responsive Layout Group configurations that adapt to different screen sizes, based on Layer Lab GUI Pro-SuperCasual patterns

## Overview

This template shows how to build panels that respond to different screen widths using Layout Groups, LayoutElements, and ContentSizeFitters — without hardcoding pixel positions.

## Example 1: Adaptive Resource Bar

A horizontal bar that distributes currency items evenly across any screen width.

```
Group_ResourceBar                                 // Adaptive resource bar
│ [RectTransform]
│   Anchor: TopStretch {0,1}→{1,1}              // Full width at top
│   Height: 80
│   Pivot: (0.5, 1)
│ [Image] sprite=resource_bar_bg (sliced)
│   Raycast Target: false
│ [HorizontalLayoutGroup]
│   Spacing: 20
│   Padding: 40, 40, 8, 8                       // Side margins for safe area
│   Child Alignment: MiddleCenter
│   Control Child Size: Width=false, Height=true
│   Child Force Expand: Width=true, Height=false // Distribute evenly
│
├── Item_Energy
│   │ [LayoutElement]
│   │   Flexible Width: 1                        // Equal share
│   │   Min Width: 100                           // Never collapse below 100px
│   │ [HorizontalLayoutGroup] Spacing=6, MiddleCenter
│   │
│   ├── Icon_Energy [Image] 36×36
│   │   [LayoutElement] preferredWidth=36, preferredHeight=36
│   ├── Text_Energy [TextMeshProUGUI] "25/30"
│   │   [LayoutElement] flexibleWidth=1, minWidth=40
│   │   Size: 20, Bold
│   └── Button_Add [Button+Image] 28×28
│       [LayoutElement] preferredWidth=28, preferredHeight=28
│       └── Icon_Plus [Image] 16×16
│
├── Item_Coins
│   │ [LayoutElement] Flexible Width: 1, Min Width: 100
│   │ [HorizontalLayoutGroup] Spacing=6, MiddleCenter
│   ├── Icon_Coin [Image] 36×36
│   ├── Text_Coins [TextMeshProUGUI] "12,345"
│   └── Button_Add [Button+Image] 28×28
│
└── Item_Gems
    │ [LayoutElement] Flexible Width: 1, Min Width: 100
    │ [HorizontalLayoutGroup] Spacing=6, MiddleCenter
    ├── Icon_Gem [Image] 36×36
    ├── Text_Gems [TextMeshProUGUI] "500"
    └── Button_Add [Button+Image] 28×28
```

### Why This Is Responsive
- `Child Force Expand Width: true` distributes available width equally
- `Flexible Width: 1` on each item gives equal share of remaining space
- `Min Width: 100` prevents items from becoming too small on narrow screens
- `Padding: 40,40` provides side margins that work with safe area

---

## Example 2: Flexible Card Grid

A grid that maintains consistent card sizes with flexible column count.

```
Panel_CardGrid                                    // Responsive card grid
│ [RectTransform]
│   Anchor: Stretch {0,0}→{1,1}
│   Padding from edges
│
└── ScrollView_Cards
    │ [ScrollRect] vertical=true, elastic 0.1
    │
    ├── Viewport
    │   │ [RectMask2D]
    │   │ [RectTransform] Stretch {0,0}→{1,1}
    │   │
    │   └── Content
    │       │ [RectTransform]
    │       │   Anchor: Top {0,1}→{1,1}
    │       │   Pivot: (0.5, 1)
    │       │ [GridLayoutGroup]
    │       │   Cell Size: (200, 240)            // Fixed cell size
    │       │   Spacing: (16, 16)
    │       │   Start Corner: UpperLeft
    │       │   Start Axis: Horizontal
    │       │   Child Alignment: UpperCenter
    │       │   Constraint: Flexible              // Auto-fit columns!
    │       │ [ContentSizeFitter]
    │       │   Vertical Fit: PreferredSize
    │       │
    │       ├── Card_Item_1
    │       │   │ [Image] sprite=card_bg (sliced)
    │       │   │ [Button]
    │       │   │ [Shadow]
    │       │   ├── Icon_Item [Image] 80×80
    │       │   │   [LayoutElement]
    │       │   ├── Text_Name [TextMeshProUGUI] size=18 bold
    │       │   ├── Text_Level [TextMeshProUGUI] size=14
    │       │   └── Image_RarityBorder [Image]
    │       │
    │       ├── Card_Item_2 (same structure)
    │       ├── Card_Item_3
    │       └── ... (more cards)
    │
    └── Scrollbar_Vertical (optional)
```

### Constraint Options

| Constraint | Behavior | Best For |
|-----------|----------|----------|
| `Flexible` | Auto-calculates columns from available width | Universal responsive |
| `FixedColumnCount: 3` | Always 3 columns, cells stretch | Known content density |
| `FixedRowCount: 2` | Always 2 rows, horizontal scroll | Horizontal carousels |

### Column Calculation for Flexible Constraint
```
Available Width = Parent Width - Padding.Left - Padding.Right
Columns = Floor((Available Width + Spacing.x) / (Cell Size.x + Spacing.x))

Example at 1048px width:
  Available = 1048 - 20 - 20 = 1008
  Columns = Floor((1008 + 16) / (200 + 16)) = Floor(1024/216) = 4 columns
  
Example at 750px width (iPhone SE):
  Available = 750 - 20 - 20 = 710  
  Columns = Floor((710 + 16) / (200 + 16)) = Floor(726/216) = 3 columns
```

---

## Example 3: Stretch-Aware Popup Panel

A popup that scales its width proportionally but caps at a maximum.

```
Popup_Responsive                                  // Responsive popup
│ [RectTransform] Stretch {0,0}→{1,1}
│
├── Dim [Image] Color=(0,0,0,0.7)
│
└── Panel_Wrapper                                 // Width constrainer
    │ [RectTransform]
    │   Anchor: Stretch {0.1, 0.15}→{0.9, 0.85} // 80% of screen width, 70% height
    │   // This makes the panel proportional to screen size
    │
    └── Panel
        │ [RectTransform] Stretch {0,0}→{1,1}    // Fill the wrapper
        │ [Image] sprite=popup_bg (sliced)
        │ [VerticalLayoutGroup]
        │   Padding: 24, 24, 16, 16
        │   Spacing: 12
        │
        ├── Header [LayoutElement] preferredHeight=80
        ├── Body [LayoutElement] flexibleHeight=1
        └── Footer [LayoutElement] preferredHeight=80
```

### Responsive Anchor Technique
Instead of fixed pixel sizes, use proportional anchors:
```
80% width centered:  AnchorMin(0.1, y)  AnchorMax(0.9, y)
70% width centered:  AnchorMin(0.15, y) AnchorMax(0.85, y)
90% width centered:  AnchorMin(0.05, y) AnchorMax(0.95, y)
```

---

## Example 4: Bottom Navigation with Flexible Tabs

```
BottomBar_Navigation                              // Responsive tab bar
│ [RectTransform]
│   Anchor: BottomStretch {0,0}→{1,0}
│   Height: 100
│   Pivot: (0.5, 0)
│ [Image] sprite=navbar_bg (dark)
│ [HorizontalLayoutGroup]
│   Spacing: 0                                   // Tabs touch each other
│   Padding: 0, 0, 0, 0
│   Child Alignment: MiddleCenter
│   Control Child Size: Width=false, Height=true
│   Child Force Expand: Width=true, Height=false
│
├── Tab_Home
│   │ [LayoutElement] Flexible Width: 1
│   │ [Button]
│   │ [VerticalLayoutGroup] Spacing=4, MiddleCenter
│   ├── Icon_Home [Image] 32×32
│   │   Tint: active=white, inactive=gray
│   └── Text_Home [TextMeshProUGUI] "Home" size=12
│       Visible only when active
│
├── Tab_Shop
│   │ [LayoutElement] Flexible Width: 1
│   │ ... (same structure)
│
├── Tab_Play                                      // Center tab (weighted)
│   │ [LayoutElement] Flexible Width: 1.5        // 50% wider than others
│   │ ... (same structure, possibly with special icon bg)
│
├── Tab_Social
│   │ [LayoutElement] Flexible Width: 1
│   │ ... (same structure)
│   └── Badge_Notification [Image] top-right of icon
│
└── Tab_Profile
    │ [LayoutElement] Flexible Width: 1
    │ ... (same structure)
```

### Tab Width Distribution
With 5 tabs and weights [1, 1, 1.5, 1, 1] = total 5.5:
```
Screen width 1048px:
  Standard tab: 1048 * (1/5.5) = 190px
  Center tab:   1048 * (1.5/5.5) = 286px

Screen width 750px (narrow):
  Standard tab: 750 * (1/5.5) = 136px  ← still > 44px minimum
  Center tab:   750 * (1.5/5.5) = 204px
```

---

## Example 5: Mixed Layout with Nested Groups

```
Panel_MixedContent                                // Complex responsive panel
│ [VerticalLayoutGroup] Spacing=16, Padding=24
│
├── Section_Header                                // Full-width header
│   │ [LayoutElement] preferredHeight=60
│   │ [HorizontalLayoutGroup] Spacing=12
│   ├── Icon_Section [Image] 40×40
│   └── Text_SectionTitle [TextMeshProUGUI]
│       [LayoutElement] flexibleWidth=1
│
├── Section_Stats                                 // 2-column stat display
│   │ [LayoutElement] preferredHeight=120
│   │ [HorizontalLayoutGroup] Spacing=16
│   │   Control Child Size: Width=false
│   │   Child Force Expand: Width=true
│   │
│   ├── Card_Stat_Attack
│   │   │ [LayoutElement] Flexible Width: 1
│   │   │ [Image] sprite=stat_card_bg
│   │   │ [VerticalLayoutGroup] Spacing=4, MiddleCenter
│   │   ├── Text_StatLabel "ATK" size=16
│   │   └── Text_StatValue "1,234" size=28 bold yellow
│   │
│   └── Card_Stat_Defense
│       │ [LayoutElement] Flexible Width: 1
│       │ [Image] sprite=stat_card_bg
│       │ [VerticalLayoutGroup] Spacing=4, MiddleCenter
│       ├── Text_StatLabel "DEF" size=16
│       └── Text_StatValue "890" size=28 bold cyan
│
└── Section_Description                           // Full-width text
    │ [LayoutElement] minHeight=40, flexibleHeight=1
    └── Text_Description [TextMeshProUGUI]
        Wrapping=enabled, Overflow=Ellipsis
        Size: 20, Color: light gray
```

---

## Responsive Design Rules Summary

| Rule | Implementation | Example |
|------|---------------|---------|
| **Never hardcode X/Y positions** | Use anchors + Layout Groups | All examples above |
| **Use flexible widths** | `LayoutElement.flexibleWidth` | Resource bar items |
| **Set minimum sizes** | `LayoutElement.minWidth` | Prevent collapse |
| **Stretch backgrounds** | Anchor: {0,0}→{1,1} | Screen backgrounds |
| **Proportional panels** | Anchor percentages (0.1→0.9) | Popup Panel_Wrapper |
| **Auto-fit grids** | `GridLayoutGroup.Constraint=Flexible` | Card grids |
| **Distribute evenly** | `Child Force Expand Width=true` | Tab bars, resource bars |

---

*Based on Layer Lab GUI Pro-SuperCasual responsive patterns: HLG(184), VLG(48), GLG(16), LayoutElement(170), ContentSizeFitter(71) — all working together for device-adaptive layouts*

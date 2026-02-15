# Responsive Panel Example Template

> Responsive Layout Group patterns for device-adaptive layouts (Layer Lab GUI Pro-SuperCasual)

## Example 1: Adaptive Resource Bar

```
Group_ResourceBar                                 // Full width, distributes evenly
│ [RectTransform] TopStretch, Height=80
│ [Image] sprite=resource_bar_bg (sliced), raycast=false
│ [HorizontalLayoutGroup] Spacing=20, Padding=40,40,8,8
│   ChildForceExpand Width=true
│
├── Item_Energy [LE flexW=1, minW=100]
│   │ [HorizontalLayoutGroup] Spacing=6, MiddleCenter
│   ├── Icon_Energy [Image] 36×36
│   ├── Text_Energy [TMP] "25/30" [LE flexW=1, minW=40]
│   └── Button_Add 28×28
├── Item_Coins [LE flexW=1, minW=100] (same structure)
└── Item_Gems [LE flexW=1, minW=100] (same structure)
```

**Why responsive**: `ChildForceExpandWidth` + equal `flexibleWidth` distributes space; `minWidth` prevents collapse on narrow screens.

## Example 2: Flexible Card Grid

```
ScrollView_Cards [ScrollRect vert, elastic=0.1]
└── Viewport [RectMask2D]
    └── Content [top-stretch, pivot=(0.5,1)]
        [GridLayoutGroup] cell=(200,240) spacing=(16,16) Constraint=Flexible
        [ContentSizeFitter] vertFit=Preferred
        ├── Card_Item [Image card_bg, Button, Shadow]
        │   Icon[80×80] + Name[18] + Level[14] + RarityBorder
        └── ...
```

| Constraint | Behavior | Use Case |
|-----------|----------|----------|
| `Flexible` | Auto-calculates columns | Universal responsive |
| `FixedColumnCount` | Fixed columns, cells stretch | Known density |
| `FixedRowCount` | Fixed rows, horizontal scroll | Carousels |

**Column formula**: `Floor((AvailableWidth + Spacing.x) / (CellSize.x + Spacing.x))`

## Example 3: Stretch-Aware Popup

```
Popup_Responsive [Stretch]
├── Dim [Image] (0,0,0,0.7)
└── Panel_Wrapper                                 // Proportional anchors
    │ [RectTransform] Anchor: {0.1,0.15}→{0.9,0.85}  // 80% width, 70% height
    └── Panel [Stretch, Image popup_bg, VLG pad=24 spacing=12]
        ├── Header [LE prefH=80]
        ├── Body [LE flexH=1]
        └── Footer [LE prefH=80]
```

**Proportional anchors**: 80%→{0.1,0.9} | 70%→{0.15,0.85} | 90%→{0.05,0.95}

## Example 4: Bottom Navigation Tabs

```
BottomBar_Navigation [BottomStretch h=100]
│ [HorizontalLayoutGroup] ChildForceExpandWidth=true
├── Tab_Home [LE flexW=1] Icon+Text "Home"
├── Tab_Shop [LE flexW=1]
├── Tab_Play [LE flexW=1.5]              // Center tab 50% wider
├── Tab_Social [LE flexW=1] + Badge
└── Tab_Profile [LE flexW=1]
```

## Example 5: Mixed Nested Layout

```
Panel_MixedContent [VLG spacing=16 pad=24]
├── Section_Header [LE prefH=60, HLG] Icon 40×40 + Title[flexW=1]
├── Section_Stats [LE prefH=120, HLG ChildForceExpandWidth=true]
│   ├── Card_Stat_Attack [LE flexW=1] "ATK" + "1,234"
│   └── Card_Stat_Defense [LE flexW=1] "DEF" + "890"
└── Section_Description [LE minH=40 flexH=1] TMP wrap+ellipsis
```

## Responsive Rules

| Rule | Implementation |
|------|---------------|
| Never hardcode X/Y | Anchors + Layout Groups |
| Use flexible widths | `LayoutElement.flexibleWidth` |
| Set minimum sizes | `LayoutElement.minWidth` |
| Proportional panels | Anchor percentages (0.1→0.9) |
| Auto-fit grids | `GridLayoutGroup.Constraint=Flexible` |
| Distribute evenly | `ChildForceExpandWidth=true` |

# HTML to Prefab Patterns - Advanced Layouts

## Safe Area & Adaptive Layouts

```
Canvas (Canvas Scaler, ScreenMatchMode=MatchWidthOrHeight)
  ├── SafeArea_Panel (SafeAreaLayoutGroup — custom or LayoutElement)
  │   ├── Panel_TopBar (HLG, childForceExpandHeight=false)
  │   └── Panel_Content (VLG, childForceExpandHeight=true)
  └── Panel_BottomTab (HLG, childForceExpandWidth=true)
```

Safe area handling: Use a custom component or nest RectTransform offsets to Screen.safeArea.

## Complex Nested Layouts

### Inventory Grid with Search & Filters

```
Panel_InventoryRoot (VLG)
  ├── Panel_SearchSection (HLG, spacing=8)
  │   ├── InputField_Search
  │   └── Button_Filter
  ├── Panel_FilterTags (HLG, childForceExpandWidth=true, spacing=4)
  │   ├── Toggle_Quality → Text
  │   └── ... (repeat per tag)
  └── ScrollView_Items (ScrollRect, vertical only)
      └── Viewport → Content (GridLayoutGroup, cellSize=(100,100))
          ├── Panel_Item (LayoutElement) → Image, Text
          └── ... (repeat)
```

## Responsive Typography

Use TMP font asset size variants:
- **Mobile small**: Font size 18-24
- **Mobile large**: Font size 28-36
- **Tablet**: Font size 32-48
- **Desktop**: Font size 40-56

Use LayoutElement + ContentSizeFitter for auto-sizing text containers.

## Advanced Scrolling

### Horizontal Scroll with Snap

```
ScrollView (ScrollRect, horizontal=true, vertical=false, inertia=true)
  ├── Viewport (RectMask2D)
  │   └── Content (HLG, childForceExpandWidth=false, spacing=10)
  │       ├── Item_Card (LayoutElement, preferredWidth=300)
  │       └── ...
  └── Scrollbar_Horizontal
```

Script: Snap to item on scroll stop.

### Infinite List (Pooling)

Pool items, recycle on scroll. Recalculate size via Content height + extra padding.

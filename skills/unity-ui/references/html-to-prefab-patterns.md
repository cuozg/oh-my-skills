# HTML to Prefab Patterns

## Button Patterns

### Icon + Text Button
```
Button_StartGame (Button, HorizontalLayoutGroup)
  ├── Image_Icon (Image, preserveAspect=true)
  └── Text_Label (TMP)
```
- HorizontalLayoutGroup: spacing from design, childAlignment=MiddleCenter
- ContentSizeFitter if auto-sizing needed

### Button Group
```
Panel_ButtonGroup (HorizontalLayoutGroup)
  ├── Button_OptionA → Text_Label
  ├── Button_OptionB → Text_Label
  └── Button_OptionC → Text_Label
```

## Panel/Card Structures

### Card with Header/Footer
```
Panel_Card (Image: bg, VerticalLayoutGroup)
  ├── Panel_Header (Image: header bg) → Text_Title
  ├── Panel_Body (VLG, padding) → Text_Content
  └── Panel_Footer (HorizontalLayoutGroup) → Button_Action → Text_Label
```

## Form Layouts

### Input Field
```
Panel_FormGroup (VLG, spacing=4)
  ├── Text_Label (TMP: "Username")
  └── InputField_Username (TMP_InputField)
      ├── Text Area → Placeholder + Text
      └── Image_Background
```

### Toggle/Checkbox
```
Toggle_RememberMe (Toggle)
  ├── Image_Background → Image_Checkmark
  └── Text_Label (TMP)
```

### Dropdown
```
Dropdown_Selection (TMP_Dropdown)
  ├── Text_Label, Image_Arrow
  └── Template (ScrollRect) → Viewport → Content → Item (Toggle)
```

## Navigation Patterns

### Bottom Tab Bar
```
Panel_TabBar (Image: bg, HLG, childForceExpandWidth=true)
  ├── Button_Tab (VLG, childAlignment=MiddleCenter)
  │   ├── Image_Icon
  │   └── Text_Label
  └── ... (repeat per tab)
```

## List/Grid Layouts

### Vertical List
```
ScrollView_List (ScrollRect, vertical only)
  └── Viewport (Mask) → Content (VLG, ContentSizeFitter: preferredHeight)
      ├── Panel_Item1 (LayoutElement)
      └── ...
```

### Grid Layout
```
ScrollView_Grid (ScrollRect)
  └── Viewport (Mask) → Content (GridLayoutGroup)
```
GridLayoutGroup: cellSize from design, constraint=FixedColumnCount, ContentSizeFitter: verticalFit=PreferredSize

## Modal/Popup Patterns

```
Panel_ModalOverlay (Image: semi-transparent black, stretch-all, Button for dismiss)
  └── Panel_Modal (Image: bg, centered anchors)
      ├── Panel_Header (HLG) → Text_Title + Button_Close
      ├── Panel_Body (VLG, padding) → Text_Content
      └── Panel_Footer (HLG, spacing=12) → Button_Cancel + Button_Confirm
```

## Tab Systems

```
Panel_TabSystem (VLG)
  ├── Panel_TabHeaders (HLG)
  │   ├── Toggle_Tab1 (Toggle, ToggleGroup, isOn=true)
  │   └── Toggle_Tab2 (Toggle, ToggleGroup)
  └── Panel_TabContent
      ├── Panel_TabPane1 (active)
      └── Panel_TabPane2 (inactive)
```
Use Toggle + ToggleGroup. Script controls pane visibility.

## Scroll Content

```
ScrollView (ScrollRect, vertical=true, horizontal=false)
  ├── Viewport (RectMask2D) → Content (VLG, ContentSizeFitter: preferredHeight)
  └── Scrollbar_Vertical (Scrollbar, direction=BottomToTop) → Handle
```

## Responsive Anchoring

| Element Type | Anchor Pattern |
|---|---|
| Full-screen overlay | Stretch all (0,0)-(1,1) |
| Centered popup | Center (0.5,0.5)-(0.5,0.5) |
| Top/Bottom bar | Stretch horizontal, fixed height |
| Side panel | Left/Right stretch, fixed width |

- SafeArea offsets on root UI panels
- ContentSizeFitter for variable text
- LayoutElement.preferredWidth/Height for fixed items
- flexibleWidth/Height for proportional sizing

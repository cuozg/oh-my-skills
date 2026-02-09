# Unity UI Best Practices

## Table of Contents
- [Canvas Setup](#canvas-setup)
- [RectTransform Fundamentals](#recttransform-fundamentals)
- [Anchor and Pivot Patterns](#anchor-and-pivot-patterns)
- [Layout Groups](#layout-groups)
- [TextMeshPro Usage](#textmeshpro-usage)
- [Image Component Patterns](#image-component-patterns)
- [Interaction Components](#interaction-components)
- [Performance Optimization](#performance-optimization)
- [Naming Conventions](#naming-conventions)
- [Prefab Organization](#prefab-organization)
- [Event Handling](#event-handling)
- [Common Pitfalls](#common-pitfalls)

---

## Canvas Setup

### Canvas Render Modes
- **Screen Space - Overlay**: Default for most game UI. Always on top.
- **Screen Space - Camera**: When UI needs to interact with 3D world or post-processing.
- **World Space**: For in-world UI (health bars, name tags).

### Canvas Scaler Settings
```
UI Scale Mode: Scale With Screen Size
Reference Resolution: Match design document (e.g., 1920x1080)
Screen Match Mode: Match Width Or Height
Match: 0.5 (balanced) or based on design orientation
```

### Canvas Hierarchy Rules
- Separate canvases for elements with different update frequencies
- Static UI on one canvas, animated UI on another
- Minimize canvas rebuilds by isolating dynamic elements

---

## RectTransform Fundamentals

### Key Properties
- **anchorMin / anchorMax**: Define relative position to parent (0-1 range)
- **anchoredPosition**: Offset from anchor center point
- **sizeDelta**: Size adjustment relative to anchor spread
- **pivot**: Point around which rotation/scaling occurs (0-1 range)
- **offsetMin / offsetMax**: Distance from anchors to edges

### Size Calculation Rules
- When anchors are together (min == max): sizeDelta = absolute size
- When anchors are spread: sizeDelta = size adjustment from anchor distance
- Stretched element: sizeDelta represents negative insets (padding from parent)

### Common RectTransform Setups
```
Full stretch:     anchorMin(0,0) anchorMax(1,1) offsetMin(0,0) offsetMax(0,0)
Center fixed:     anchorMin(0.5,0.5) anchorMax(0.5,0.5) sizeDelta(width,height)
Top-left corner:  anchorMin(0,1) anchorMax(0,1) pivot(0,1)
Bottom-center:    anchorMin(0.5,0) anchorMax(0.5,0) pivot(0.5,0)
```

---

## Anchor and Pivot Patterns

### Anchor Presets by Use Case

| Use Case | anchorMin | anchorMax | Pivot |
|---|---|---|---|
| Center popup | (0.5, 0.5) | (0.5, 0.5) | (0.5, 0.5) |
| Top bar | (0, 1) | (1, 1) | (0.5, 1) |
| Bottom bar | (0, 0) | (1, 0) | (0.5, 0) |
| Left panel | (0, 0) | (0, 1) | (0, 0.5) |
| Right panel | (1, 0) | (1, 1) | (1, 0.5) |
| Full screen | (0, 0) | (1, 1) | (0.5, 0.5) |
| Top-left badge | (0, 1) | (0, 1) | (0, 1) |
| Bottom-right FAB | (1, 0) | (1, 0) | (1, 0) |

### Pivot Rules
- Pivot determines the "origin" point for position, rotation, and scale
- For elements that grow downward (lists): pivot (0.5, 1)
- For elements that grow rightward: pivot (0, 0.5)
- For centered elements: pivot (0.5, 0.5)
- For corner-anchored elements: match pivot to anchor corner

---

## Layout Groups

### HorizontalLayoutGroup
- Use for rows of elements (button bars, nav items)
- Set `childAlignment` to control vertical positioning within row
- Set `spacing` from design spec
- `childForceExpandWidth`: true for equal-width children, false for natural sizing
- `childControlWidth`: true to let layout control child width

### VerticalLayoutGroup
- Use for stacked elements (forms, lists, card content)
- Same properties as Horizontal but for vertical axis
- Common: `childControlHeight=false` with `LayoutElement.preferredHeight` on children

### GridLayoutGroup
- Use for grid/tile layouts
- `cellSize`: exact dimensions from design
- `constraint`: FixedColumnCount for known column grids
- `startAxis`: Horizontal (fill rows first) or Vertical (fill columns first)
- `startCorner`: UpperLeft for most UI patterns

### ContentSizeFitter
- `horizontalFit` / `verticalFit`: Unconstrained, MinSize, PreferredSize
- ALWAYS pair with layout groups for scrollable content
- On ScrollRect content: verticalFit = PreferredSize for vertical scroll

### LayoutElement
- Override layout calculations for specific children
- `preferredWidth/Height`: target size
- `flexibleWidth/Height`: proportional fill (0 = don't flex, 1+ = flex)
- `minWidth/Height`: minimum guaranteed size
- `ignoreLayout`: exclude from layout calculations

---

## TextMeshPro Usage

### When to Use
- ALWAYS use TextMeshPro (TMP) over legacy Text component
- Use `TextMeshProUGUI` for Canvas UI text
- Use `TextMeshPro` for world-space 3D text

### Configuration Patterns
```
Font Asset: Project-specific TMP font asset
Font Size: Match design spec exactly (in points)
Font Style: Bold, Italic, etc. as specified
Color: Match design hex/RGBA
Alignment: Match design (Left, Center, Right + Top, Middle, Bottom)
Text Overflow: Ellipsis for constrained areas, Overflow for auto-sizing
Auto Size: Enable only when design specifies responsive text
Raycast Target: FALSE unless text needs to receive clicks
```

### Best Practices
- Create font assets at appropriate sizes for quality
- Use rich text tags for inline styling: `<b>`, `<color>`, `<size>`
- Set `raycastTarget = false` on all non-interactive text to improve performance

---

## Image Component Patterns

### Image Types
- **Simple**: For solid backgrounds, icons
- **Sliced**: For 9-slice backgrounds (buttons, panels) - requires sprite with borders
- **Tiled**: For repeating patterns
- **Filled**: For progress bars, health bars, cooldown indicators

### Configuration
```
Source Image: Assigned sprite
Color: Tint color (white = no tint)
Material: Usually None (default UI material)
Raycast Target: FALSE unless clickable
Preserve Aspect: TRUE for icons/photos, FALSE for backgrounds
```

### Background Patterns
- Solid color: Image component with no sprite, just color
- 9-slice: Image with Sliced type, sprite with border settings
- Gradient: Use sprite or shader-based approach
- Rounded corners: Use 9-slice sprite with rounded corner texture

---

## Interaction Components

### Button
- Transition modes: ColorTint (simple), SpriteSwap (visual states), Animation (complex)
- Navigation: Set to None for most game UI (prevents keyboard/gamepad navigation issues)
- Always add onClick listener target reference or script handler

### Toggle
- Use with ToggleGroup for radio-button behavior
- `isOn`: initial state
- Graphic: checkmark/indicator image reference

### Slider
- Direction: LeftToRight, RightToLeft, BottomToTop, TopToBottom
- `wholeNumbers`: true for discrete values
- `minValue` / `maxValue`: range from design spec

### ScrollRect
- `horizontal` / `vertical`: enable only needed directions
- `movementType`: Elastic (bouncy), Clamped (hard stop), Unrestricted
- `elasticity`: 0.1 for subtle, higher for bouncier
- `scrollSensitivity`: adjust for touch vs mouse
- `inertia`: true for momentum scrolling
- `decelerationRate`: 0.135 default, lower = stops faster

### TMP_InputField
- `contentType`: Standard, IntegerNumber, Name, EmailAddress, Password, etc.
- `characterLimit`: from design spec
- `placeholder`: hint text with reduced alpha

---

## Performance Optimization

### Raycast Target
- Set `raycastTarget = false` on ALL non-interactive elements
- Only elements needing clicks/touches should have raycastTarget enabled
- This is the single most impactful optimization for complex UI

### Canvas Separation
- Put frequently updating elements on a separate canvas
- Animations, timers, progress bars on their own sub-canvas
- Static frames/backgrounds on main canvas

### Layout Group Optimization
- Disable layout groups after initial layout if content is static
- Use `LayoutRebuilder.ForceRebuildLayoutImmediate()` sparingly
- Consider manual positioning for performance-critical UIs

### Object Pooling
- Pool list items in scrollable content
- Pool popup/dialog instances
- Use `SetActive(false)` rather than Destroy for reusable elements

### Overdraw Reduction
- Avoid overlapping transparent images
- Use `CanvasGroup.alpha` instead of individual Image.alpha for groups
- Minimize full-screen overlays
- Use `RectMask2D` instead of `Mask` when possible (no stencil buffer)

---

## Naming Conventions

### GameObject Naming Pattern
```
{Type}_{Purpose}

Types:
  Panel_    → Container/group (Image or empty GameObject with layout)
  Button_   → Button component
  Text_     → TextMeshProUGUI
  Image_    → Image (non-background)
  Toggle_   → Toggle component
  Slider_   → Slider component
  InputField_ → TMP_InputField
  ScrollView_ → ScrollRect
  Dropdown_ → TMP_Dropdown

Examples:
  Panel_Header
  Button_Submit
  Text_Title
  Image_Avatar
  Toggle_Sound
  ScrollView_PlayerList
```

### Hierarchy Organization
```
Root_ScreenName
  ├── Panel_Header
  ├── Panel_Content
  │   ├── ... content elements ...
  └── Panel_Footer
```

---

## Prefab Organization

### Structure Rules
- One prefab per screen/panel
- Shared elements as nested prefab variants
- Keep hierarchy depth ≤ 5 levels where possible
- Group related elements under Panel_ containers

### Prefab Variants
- Use for screen variations (portrait/landscape)
- Use for themed versions (light/dark)
- Use for state variations (empty state, loaded state)

### Asset Organization
```
Assets/
  UI/
    Prefabs/
      Screens/         → Full screen prefabs
      Components/      → Reusable UI components
      Popups/          → Modal/dialog prefabs
    Sprites/
      Icons/
      Backgrounds/
      Buttons/
    Fonts/
    Materials/
```

---

## Event Handling

### UnityEvent (Inspector-wired)
- Use for simple button clicks wired in Inspector
- Pros: Visible in Inspector, no code needed
- Cons: Fragile, hard to track, breaks on refactor

### Script-Based Event Binding
- Preferred for production code
- Register in OnEnable, unregister in OnDisable
- Use `AddListener` / `RemoveListener` pattern

### Event Bus Pattern
- Decouple UI from game logic
- UI fires events, game systems listen
- Avoids tight coupling between UI prefabs and game code

---

## Common Pitfalls

### DO NOT
- Use legacy Text component (always use TextMeshPro)
- Leave raycastTarget=true on non-interactive elements
- Nest layout groups more than 2-3 levels deep
- Use Update() for UI state — use event-driven updates
- Hardcode positions when layout groups should be used
- Ignore the design spec's spacing, sizing, or color values
- Create deeply nested hierarchies (>6 levels)
- Put all UI on a single canvas
- Use Mask when RectMask2D suffices

### ALWAYS
- Match design spec values exactly (colors, sizes, spacing)
- Set raycastTarget=false on decorative elements
- Use layout groups for repeated/aligned elements
- Test at multiple resolutions
- Use ContentSizeFitter for dynamic text containers
- Verify anchor/pivot setup matches intended responsive behavior

---
name: unity-ui
description: "Implement UX designs from HTML documents into fully functional Unity UI prefabs with 100% fidelity to the design specification. Use when: (1) Translating HTML/CSS design documents into Unity prefab hierarchies, (2) Creating UI prefabs from UX specifications or mockups, (3) Mapping design specs (colors, typography, spacing, interactions) to Unity components, (4) Building complex multi-screen UI layouts from design documents, (5) Implementing form layouts, navigation bars, modals, card layouts from HTML specs, (6) Ensuring pixel-perfect fidelity between design and Unity implementation. Triggers: 'implement this design', 'create UI from spec', 'build prefab from HTML', 'translate UX to Unity', 'UI implementation', 'design to prefab'."
---

# Unity UI: UX Design → Prefab Implementation

Translate HTML/CSS UX design documents into Unity UI prefabs with 100% design fidelity.

## Purpose

Convert UX design documents (HTML/CSS) into fully functional Unity UI prefabs with pixel-perfect fidelity — every color, size, spacing, font, and interaction matches the spec exactly.

## Input

- **Required**: HTML/CSS design document specifying the UI screen or component
- **Optional**: Sprite assets, font files, target resolution, platform constraints (mobile/desktop)

## Core Principle

> **The design document is the source of truth.** Every color, size, spacing value, font, and interaction specified in the design MUST appear exactly in the prefab. Never approximate, assume, or skip.

## Workflow Overview

Implementing a UX design into a Unity prefab follows this sequential process:

1. **Analyze** the design document → extract all elements, specs, and interactions
2. **Structure** the prefab hierarchy → map HTML elements to GameObjects
3. **Configure** components → apply all visual and interaction properties
4. **Validate** against the design → verify 100% fidelity

## Step 1: Analyze the Design Document

Read the HTML design document. Extract:

### 1.1 Element Inventory
Catalog every visible element. For each element identify:
- **Type**: button, text, image, panel, input, toggle, dropdown, slider, scroll area
- **Content**: text strings, image references, placeholder text
- **Interactive?**: does it respond to user input?
- **Parent-child relationships**: nesting structure

### 1.2 Visual Specifications
Extract exact values for:
- **Colors**: all hex/rgba values → map to Unity Color. See [specification-mapping.md](references/specification-mapping.md) § Color Mapping
- **Typography**: font family, size, weight, alignment, line-height, letter-spacing → map to TMP properties. See [specification-mapping.md](references/specification-mapping.md) § Typography Mapping
- **Spacing**: padding, margins, gaps → map to LayoutGroup settings. See [specification-mapping.md](references/specification-mapping.md) § Spacing and Layout Mapping
- **Sizes**: widths, heights, min/max constraints → map to RectTransform/LayoutElement

### 1.3 Interaction Specifications
For each interactive element:
- What triggers it (click, toggle, input, scroll)?
- What happens (navigate, toggle state, submit, animate)?
- What are the states (normal, hover, pressed, disabled)?

### 1.4 Layout Specifications
- Screen orientation and target resolution
- Responsive behavior (stretch, scale, fixed)
- Scroll regions and directions
- Element ordering and z-index stacking

**Output**: Use the template at [assets/templates/UX_IMPLEMENTATION_TEMPLATE.md](assets/templates/UX_IMPLEMENTATION_TEMPLATE.md) to document the analysis.

## Step 2: Structure the Prefab Hierarchy

Map the HTML structure to Unity GameObjects:

### Naming Convention
```
{Type}_{Purpose}

Types: Panel_, Button_, Text_, Image_, Toggle_, Slider_,
       InputField_, ScrollView_, Dropdown_
```

### Mapping Rules

| HTML Element | Unity GameObject |
|---|---|
| `<div>` (container) | Panel_ with Image (if has background) or empty GO |
| `<button>` | Button_ with Button component |
| `<span>`, `<p>`, `<h1-6>` | Text_ with TextMeshProUGUI |
| `<img>` | Image_ with Image component |
| `<input>` | InputField_ with TMP_InputField |
| `<input type="checkbox">` | Toggle_ with Toggle component |
| `<select>` | Dropdown_ with TMP_Dropdown |
| `<input type="range">` | Slider_ with Slider component |
| `<div style="overflow:scroll">` | ScrollView_ with ScrollRect |
| `<ul>/<ol>` with items | ScrollView_ or Panel_ with VerticalLayoutGroup |
| `<div style="display:flex">` | Panel_ with HorizontalLayoutGroup or VerticalLayoutGroup |
| `<div style="display:grid">` | Panel_ with GridLayoutGroup |

### Hierarchy Depth Rules
- Maximum 5-6 levels deep
- Group related elements under Panel_ containers
- Mirror the HTML nesting structure

### Common Pattern References
For detailed HTML → Prefab hierarchy examples (buttons, cards, forms, navigation, modals, tabs, grids):
→ See [references/html-to-prefab-patterns.md](references/html-to-prefab-patterns.md)

## Step 3: Configure Components

Apply the extracted specifications to each GameObject.

### 3.1 RectTransform Setup
For each element, configure anchors, pivot, size, and position:

**Anchor selection by element role:**
- Full-screen background → stretch all: anchors (0,0)-(1,1)
- Centered popup → center: anchors (0.5,0.5)-(0.5,0.5)
- Top bar → top stretch: anchors (0,1)-(1,1)
- Bottom bar → bottom stretch: anchors (0,0)-(1,0)

→ Full anchor/pivot reference: [references/unity-ui-best-practices.md](references/unity-ui-best-practices.md) § Anchor and Pivot Patterns

### 3.2 Layout Groups
Match CSS layout to Unity layout components:
- `flex-direction: row` → HorizontalLayoutGroup
- `flex-direction: column` → VerticalLayoutGroup
- `display: grid` → GridLayoutGroup

Configure spacing, padding, child alignment from design values.

→ Full flexbox mapping: [references/specification-mapping.md](references/specification-mapping.md) § Spacing and Layout Mapping

### 3.3 Visual Properties
Apply all visual specs:
- **Image.color** = design background-color (hex → Unity Color)
- **TextMeshProUGUI**: fontSize, fontStyle, color, alignment from design
- **Image.type** = Sliced for scalable backgrounds, Simple for icons
- **Image.preserveAspect** = true for icons/photos

### 3.4 Interaction Components
- **Buttons**: transition type, state colors/sprites, navigation = None
- **Toggles**: ToggleGroup for radio behavior, checkmark graphic reference
- **InputFields**: contentType, characterLimit, placeholder text
- **ScrollRects**: scroll direction, inertia, elasticity
- **Dropdowns**: options list, template configuration

### 3.5 Performance Settings (CRITICAL)
Apply to EVERY element:
- `raycastTarget = false` on ALL non-interactive Image and Text components
- Only interactive elements (Button, Toggle, InputField, Slider, Dropdown, ScrollRect) keep raycastTarget enabled
- Use RectMask2D instead of Mask for scroll views

→ Full best practices: [references/unity-ui-best-practices.md](references/unity-ui-best-practices.md)

## Step 4: Validate

Before declaring implementation complete, verify against the design using the checklist:
→ [assets/templates/PREFAB_CREATION_CHECKLIST.md](assets/templates/PREFAB_CREATION_CHECKLIST.md)

### Critical Validation Points

1. **Every element from design exists in prefab** — count them
2. **Every color matches** — compare hex values
3. **Every font size matches** — compare point values
4. **Every spacing value matches** — compare padding/spacing/gap
5. **Every interaction works** — buttons, toggles, inputs configured
6. **raycastTarget=false** on all non-interactive elements
7. **Anchors correct** for intended responsive behavior
8. **No missing references** — sprites, fonts, materials all assigned

## Concrete Example: Login Screen

### Input (HTML design excerpt):
```html
<div class="login-screen" style="background: #1A1A2E;">
  <div class="logo-area" style="padding-top: 60px;">
    <img src="game-logo.png" style="width: 200px; height: auto;" />
  </div>
  <div class="form" style="padding: 40px 24px; gap: 16px; display: flex; flex-direction: column;">
    <input type="text" placeholder="Username"
      style="height: 48px; font-size: 16px; background: #16213E; color: #E0E0E0; border-radius: 8px; padding: 0 16px;" />
    <input type="password" placeholder="Password"
      style="height: 48px; font-size: 16px; background: #16213E; color: #E0E0E0; border-radius: 8px; padding: 0 16px;" />
    <button style="height: 52px; background: #E94560; color: white; font-size: 18px; font-weight: bold; border-radius: 12px; margin-top: 8px;">
      LOG IN
    </button>
  </div>
  <a style="color: #0F3460; font-size: 14px; text-align: center;">Forgot Password?</a>
</div>
```

### Output (Prefab hierarchy):
```
Root_LoginScreen (Image: color=#1A1A2E, stretch-all)
  ├── Panel_LogoArea (VerticalLayoutGroup, padding-top=60, childAlignment=UpperCenter)
  │   └── Image_Logo (Image: game-logo sprite, preserveAspect=true, sizeDelta=200x[auto])
  │       raycastTarget=false
  ├── Panel_Form (VerticalLayoutGroup, spacing=16, padding=40/24/40/24)
  │   ├── InputField_Username (TMP_InputField, contentType=Standard)
  │   │   ├── Image_BG (Image: 9-slice rounded-8px sprite, color=#16213E)
  │   │   └── Text Area
  │   │       ├── Placeholder (TMP: "Username", color=#E0E0E0@50%, size=16)
  │   │       └── Text (TMP: color=#E0E0E0, size=16)
  │   │   LayoutElement: preferredHeight=48
  │   ├── InputField_Password (TMP_InputField, contentType=Password)
  │   │   ├── Image_BG (Image: 9-slice rounded-8px sprite, color=#16213E)
  │   │   └── Text Area
  │   │       ├── Placeholder (TMP: "Password", color=#E0E0E0@50%, size=16)
  │   │       └── Text (TMP: color=#E0E0E0, size=16)
  │   │   LayoutElement: preferredHeight=48
  │   ├── Spacer (LayoutElement: preferredHeight=8)
  │   └── Button_Login (Button: transition=ColorTint, navigation=None)
  │       ├── Image_BG (Image: 9-slice rounded-12px sprite, color=#E94560)
  │       └── Text_Label (TMP: "LOG IN", size=18, Bold, color=#FFFFFF, align=Center)
  │           raycastTarget=false
  │       LayoutElement: preferredHeight=52
  └── Button_ForgotPassword (Button: transparent bg, navigation=None)
      └── Text_Label (TMP: "Forgot Password?", size=14, color=#0F3460, align=Center)
          raycastTarget=false
```

## Handling Ambiguous or Incomplete Designs

When the design document is unclear or incomplete:

1. **Missing spacing values**: Use 8px grid system (8, 16, 24, 32, 40)
2. **Missing interaction states**: Default to ColorTint with standard Unity multipliers
3. **Missing font specification**: Document the assumption and use project default font
4. **Ambiguous layout**: Prefer LayoutGroup-based approach over manual positioning
5. **Missing responsive behavior**: Default to center-anchored with fixed size
6. **Missing colors**: Flag as TODO, use placeholder magenta (#FF00FF) to make it obvious

**ALWAYS document assumptions** in the implementation notes section of the template.

## Anti-Patterns

### NEVER DO
- **Hardcode positions** when layout groups should be used
- **Skip design values** — every spec value must be applied exactly
- **Leave raycastTarget=true** on decorative elements
- **Use legacy Text** component — always use TextMeshProUGUI
- **Approximate colors** — always use exact hex from design
- **Ignore spacing** — padding and gaps are not optional
- **Create deep nesting** (>6 levels) without justification
- **Mix interaction/decoration** — interactive elements get Button/Toggle, decorative do not

### ALWAYS DO
- **Inventory every element** before starting implementation
- **Use the template** for structured implementation
- **Set raycastTarget=false** on non-interactive elements
- **Match every value** from the design spec
- **Validate with checklist** before marking complete
- **Document assumptions** when design is ambiguous

## Reference Files

Load these as needed during implementation:

| Reference | When to Load | Content |
|---|---|---|
| [html-to-prefab-patterns.md](references/html-to-prefab-patterns.md) | Mapping HTML patterns to prefab hierarchies | Buttons, cards, forms, nav, modals, tabs, grids, scroll |
| [unity-ui-best-practices.md](references/unity-ui-best-practices.md) | Setting up canvas, anchors, layout, performance | Canvas setup, RectTransform, layout groups, TMP, performance |
| [specification-mapping.md](references/specification-mapping.md) | Converting CSS values to Unity properties | Colors, typography, spacing, sizing, borders, interactions |

## Output

Successful implementation produces:
1. **Unity prefab** — saved to the project's prefab directory, matching the design hierarchy exactly
2. **All components configured** — RectTransform, LayoutGroups, Image, TextMeshProUGUI, Button, etc. with exact values from the design spec
3. **Performance settings applied** — `raycastTarget=false` on all non-interactive elements, RectMask2D for scroll views
4. **Validation passed** — all items in `PREFAB_CREATION_CHECKLIST.md` verified
5. **Assumptions documented** — any design ambiguities noted in implementation notes

No separate report files are generated. The prefab itself is the deliverable.

## Templates

Use these for structured output:

| Template | When to Use |
|---|---|
| [UX_IMPLEMENTATION_TEMPLATE.md](assets/templates/UX_IMPLEMENTATION_TEMPLATE.md) | Document analysis and configuration for each screen/component |
| [PREFAB_CREATION_CHECKLIST.md](assets/templates/PREFAB_CREATION_CHECKLIST.md) | Final validation before marking implementation complete |

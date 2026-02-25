---
name: unity-ui
description: "Implement UX designs from HTML documents into fully functional Unity UI prefabs with 100% fidelity to the design specification. Use when: (1) Translating HTML/CSS design documents into Unity prefab hierarchies, (2) Creating UI prefabs from UX specifications or mockups, (3) Mapping design specs (colors, typography, spacing, interactions) to Unity components, (4) Building complex multi-screen UI layouts from design documents, (5) Implementing form layouts, navigation bars, modals, card layouts from HTML specs, (6) Ensuring pixel-perfect fidelity between design and Unity implementation. Triggers: 'implement this design', 'create UI from spec', 'build prefab from HTML', 'translate UX to Unity', 'UI implementation', 'design to prefab'."
---

# Unity UI: UX Design → Prefab Implementation

**Input**: HTML/CSS design document, optional sprite assets, fonts, target resolution, platform constraints

## Output
Unity UI prefabs with 100% fidelity to the design specification document. **The design document is the source of truth** — every color, size, spacing, font, and interaction must match exactly.

## Workflow

1. **Analyze** design document → extract elements, specs, interactions
2. **Structure** prefab hierarchy → map HTML to GameObjects (see [component-mapping-reference.md](references/component-mapping-reference.md))
3. **Configure** components → apply visual and interaction properties
4. **Validate** against design → verify 100% fidelity

## Step 1: Analyze the Design Document

### Element Inventory
For each element: type (button/text/image/panel/input/toggle/dropdown/slider/scroll), content, interactive?, parent-child relationships.

### Visual Specifications
Extract exact values — see [specification-mapping.md](references/specification-mapping.md):
- **Colors**: hex/rgba → Unity Color
- **Typography**: font, size, weight, alignment → TMP properties
- **Spacing**: padding, margins, gaps → LayoutGroup settings
- **Sizes**: widths, heights, min/max → RectTransform/LayoutElement

### Interaction & Layout Specs
- Triggers, states (normal/hover/pressed/disabled), responses
- Orientation, responsive behavior, scroll regions, z-index
- Use [UX_IMPLEMENTATION_TEMPLATE.md](assets/templates/UX_IMPLEMENTATION_TEMPLATE.md) for the analysis output.

## Step 2: Structure Prefab Hierarchy

Map HTML elements to GameObjects using [component-mapping-reference.md](references/component-mapping-reference.md). Use `{Type}_{Purpose}` naming: `Panel_`, `Button_`, `Text_`, `Image_`, `Toggle_`, `Slider_`, `InputField_`, `ScrollView_`, `Dropdown_`

Maximum hierarchy depth: 5-6 levels. See [html-to-prefab-patterns.md](references/html-to-prefab-patterns.md) for detailed layout examples (buttons, cards, forms, nav, modals, tabs, grids, scroll).

## Step 3: Configure Components

### RectTransform Anchors
- Full-screen bg → stretch all: (0,0)-(1,1)
- Centered popup → center: (0.5,0.5)-(0.5,0.5)
- Top/Bottom bar → top/bottom stretch
- See [unity-ui-best-practices.md](references/unity-ui-best-practices.md)

### Layout Groups
Map CSS properties to LayoutGroups via [specification-mapping.md](references/specification-mapping.md):
- `flex-direction: row` → HorizontalLayoutGroup
- `flex-direction: column` → VerticalLayoutGroup
- `display: grid` → GridLayoutGroup

### Performance (CRITICAL)
- `raycastTarget = false` on ALL non-interactive Image/Text
- Only Button/Toggle/InputField/Slider/Dropdown/ScrollRect keep raycastTarget
- Use RectMask2D instead of Mask for scroll views

## Step 4: Validate

Use [PREFAB_CREATION_CHECKLIST.md](assets/templates/PREFAB_CREATION_CHECKLIST.md):
1. Every design element exists in prefab
2. Every color, font size, spacing matches exactly
3. Every interaction configured
4. `raycastTarget=false` on non-interactive elements
5. Anchors correct for responsive behavior
6. No missing references

## Handling Ambiguous Designs

- Missing spacing → 8px grid (8, 16, 24, 32, 40)
- Missing interaction states → ColorTint with Unity defaults
- Missing font → document assumption, use project default
- Missing colors → placeholder magenta (#FF00FF)
- **ALWAYS document assumptions**

## Anti-Patterns

**NEVER**: Hardcode positions (use LayoutGroups), skip design values, leave raycastTarget=true on decorative elements, use legacy Text (use TMP), approximate colors, ignore spacing, nest >6 levels

**ALWAYS**: Inventory every element first, use the template, set raycastTarget=false on non-interactive, match every spec value, validate with checklist

## Reference Files

- [component-mapping-reference.md](references/component-mapping-reference.md) — HTML→Unity mapping, naming, hierarchy depth
- [html-to-prefab-patterns.md](references/html-to-prefab-patterns.md) — Buttons, cards, forms, nav, modals, tabs, grids, scroll
- [unity-ui-best-practices.md](references/unity-ui-best-practices.md) — Canvas, RectTransform, layout groups, TMP, performance
- [specification-mapping.md](references/specification-mapping.md) — Colors, typography, spacing, sizing, borders, interactions

## Templates

- [UX_IMPLEMENTATION_TEMPLATE.md](assets/templates/UX_IMPLEMENTATION_TEMPLATE.md) — Document analysis and config per screen
- [PREFAB_CREATION_CHECKLIST.md](assets/templates/PREFAB_CREATION_CHECKLIST.md) — Final validation checklist

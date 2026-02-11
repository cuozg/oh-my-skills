---
name: unity-ux-design
description: "Generate UX screen specification documents for Unity UI/UX design. Use when: (1) Creating UX screen specs from requirements, (2) Documenting UI layouts, navigation flows, and interaction patterns, (3) Defining touch targets, animations, and responsive behavior, (4) Generating spec documents that feed into unity-ui for implementation. Triggers: 'UX spec', 'screen specification', 'design document', 'UI spec', 'UX design'."
---

# Unity UX Design

Generate structured UX screen specification documents that define UI layouts, interactions, and responsive behavior for Unity projects.

## Purpose

Generate UX screen specification documents for Unity UI/UX design — providing a structured, repeatable workflow that produces consistent results.


## Workflow

1. **Gather Requirements** - Understand the screen purpose, target device, and aspect ratio
2. **Define Screen Structure** - Map out sections, components, and navigation
3. **Specify Interactions** - Touch targets, animations, transitions, state changes
4. **Document Responsive Behavior** - Anchoring, scaling, aspect ratio adaptations
5. **Output Spec Document** - Generate HTML specification using the template

## Reference Files

- **Example Specifications**: See [example-specifications.md](./references/example-specifications.md) for 4 production-ready screen spec examples (Main Menu, Settings Dialog, Game HUD, iPad Adaptation)
- **Unity UI Best Practices**: See [unity-ui-best-practices.md](./references/unity-ui-best-practices.md) for canvas, layout, touch target, and performance guidelines

## Template

Use the interactive HTML template at [assets/templates/INTERACTIVE_DEMO.html](./assets/templates/INTERACTIVE_DEMO.html) as the base for generating spec documents.

## Input

| Source | Details |
|--------|---------|
| Feature requirements | User story, product brief, or verbal description of the screen/component |
| Target device | Phone, tablet, desktop — determines touch targets and layout |
| Aspect ratio | Portrait (9:16), landscape (16:9), or adaptive |
| Existing assets | (Optional) Sprites, icons, fonts already in the project |

## Output

A self-contained HTML specification document saved to `Documents/UXSpecs/{ScreenName}_Spec.html`.

The document must include:
1. **Screen overview** — purpose, entry/exit points, context
2. **Element inventory** — every visible element with type, content, states
3. **Visual specifications** — exact colors (hex), sizes (px/dp), spacing, typography
4. **Interaction map** — touch targets, transitions, animations, state changes
5. **Responsive rules** — anchoring, scaling, breakpoints
6. **Navigation flow** — how this screen connects to other screens

Use the interactive HTML template at `assets/templates/INTERACTIVE_DEMO.html` as the base.

## Examples

### Example 1: Simple screen spec request
```
User: "Create a UX spec for a Settings dialog with audio, graphics, and account sections"
```
→ Investigate existing settings patterns in the project
→ Generate `Documents/UXSpecs/SettingsDialog_Spec.html` with:
  - Tab navigation (Audio | Graphics | Account)
  - Slider controls for volume, toggle for mute
  - Dropdown for quality presets
  - Button layout for Save/Cancel

### Example 2: Responsive layout spec
```
User: "Design a game HUD spec that works on both phone and tablet"
```
→ Define anchor strategies for each element (health bar top-left, score top-center, etc.)
→ Specify minimum touch target sizes (44×44dp)
→ Document scaling behavior per aspect ratio

## Integration

The output specification documents are designed to be consumed by the `unity-ui` skill for implementation into Unity prefabs.
---
name: unity-ux-design
description: "Generate UX screen specification documents and production-ready Unity scene/prefab hierarchies for mobile game UI/UX design. Use when: (1) Creating UX screen specs from requirements, (2) Building mobile game UI scenes with proper Canvas, SafeArea, and Layout Groups, (3) Generating lobby, shop, leaderboard, popup, or any mobile game screen, (4) Documenting UI layouts, navigation flows, and interaction patterns, (5) Defining touch targets, animations, and responsive behavior, (6) Generating spec documents that feed into unity-ui for implementation. Triggers: 'UX spec', 'screen specification', 'design document', 'UI spec', 'UX design', 'mobile game UI', 'lobby screen', 'popup modal', 'game menu'."
---

# Unity UX Design — Mobile Game UI

**Input**: Feature requirements, target device, existing assets, optional screen pattern

## Output
UX screen specification document (HTML) and production-ready Unity scene/prefab hierarchy. All patterns derived from Layer Lab GUI Pro-SuperCasual (81 screens, 5,624 GameObjects).

## Workflow

1. **Gather requirements** — screen purpose, target device, aspect ratio, existing assets
2. **Select pattern** — match from design patterns reference
3. **Build hierarchy** — Canvas setup template → screen-specific template (see [canvas-and-naming-reference.md](references/canvas-and-naming-reference.md))
4. **Configure components** — standard uGUI components per component reference
5. **Apply responsive rules** — anchoring, Layout Groups, ContentSizeFitter
6. **Add interactions** — touch feedback, transitions, navigation
7. **Output** — scene hierarchy, prefab structure, or HTML spec

## Reference Files

### Screen Design & Patterns
- **[Mobile UI Design Patterns](./references/mobile-ui-design-patterns.md)** — 10 screen patterns with hierarchy blueprints
- **[Mobile Design System](./references/mobile-design-system.md)** — Color palette, typography, spacing, icons

### Implementation
- **[Canvas Configuration & Naming](./references/canvas-and-naming-reference.md)** — Canvas structure, layer organization, naming conventions
- **[GameObject Hierarchy Best Practices](./references/gameobject-hierarchy-best-practices.md)** — Naming, anchors, sizing
- **[Responsive Design Implementation](./references/responsive-design-implementation.md)** — CanvasScaler, anchoring, Layout Groups, SafeArea
- **[UI Component Reference](./references/ui-component-reference.md)** — Full component census with configs

### Interaction & UX
- **[Mobile UX Interaction Patterns](./references/mobile-ux-interaction-patterns.md)** — Touch, navigation, modal, scroll, feedback

### Examples & Legacy
- **[Example Specifications](./references/example-specifications.md)** — 4 HTML spec examples
- **[Unity UI Best Practices](references/unity-ui-best-practices.md)** — General guidelines

## Templates

| Template | Use When |
|----------|----------|
| **[Canvas Setup](./assets/templates/CANVAS_SETUP_TEMPLATE.md)** | Starting any new UI scene |
| **[Lobby Screen](./assets/templates/SCREEN_TEMPLATE_LOBBY.md)** | Main menu / lobby |
| **[Scrollable List](./assets/templates/SCREEN_TEMPLATE_LIST_SCROLLABLE.md)** | Leaderboard, collection, friends list |
| **[Popup Modal](./assets/templates/COMPONENT_POPUP_MODAL.md)** | Centered popup over dimmed background |
| **[Confirmation Dialog](./assets/templates/COMPONENT_DIALOG_CONFIRMATION.md)** | Yes/no or accept/cancel dialog |
| **[Responsive Panel](./assets/templates/RESPONSIVE_PANEL_EXAMPLE.md)** | 5 responsive layout recipes |
| **[Interactive Demo HTML](./assets/templates/INTERACTIVE_DEMO.html)** | HTML spec document generation |

## Example Lobby Screen

Follow [Canvas Setup](./assets/templates/CANVAS_SETUP_TEMPLATE.md) + [Lobby Template](./assets/templates/SCREEN_TEMPLATE_LOBBY.md):

```
Screen_Lobby
├── Panel_Header (top-stretch)
│   ├── Group_PlayerInfo (HorizontalLayoutGroup)
│   └── Group_ResourceBar (HorizontalLayoutGroup, spacing=20)
├── Panel_Content (middle-stretch, VerticalLayoutGroup)
│   ├── Group_FeaturedBanner
│   └── Group_QuickActions (HorizontalLayoutGroup)
├── Panel_Bottom (bottom-stretch)
│   └── Button_Play (large CTA, centered)
└── Background (full-stretch)
```

## Full Example Outputs
- **[ExampleLobbyMenu](./assets/examples/ExampleLobbyMenu.md)** — Full lobby (32 Images, 19 TMP, 12 Buttons)
- **[ExampleItemListScreen](./assets/examples/ExampleItemListScreen.md)** — Leaderboard with ScrollRect
- **[ExampleRewardPopup](./assets/examples/ExampleRewardPopup.md)** — Reward popup with animation

## Integration

- Output hierarchies implementable by `unity-ui` skill
- HTML spec documents feed into `unity-ui` for prefab generation
- All patterns follow Layer Lab conventions validated against 81 production screens

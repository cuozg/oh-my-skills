---
name: unity-ux-design
description: "Generate UX screen specification documents and production-ready Unity scene/prefab hierarchies for mobile game UI/UX design. Use when: (1) Creating UX screen specs from requirements, (2) Building mobile game UI scenes with proper Canvas, SafeArea, and Layout Groups, (3) Generating lobby, shop, leaderboard, popup, or any mobile game screen, (4) Documenting UI layouts, navigation flows, and interaction patterns, (5) Defining touch targets, animations, and responsive behavior, (6) Generating spec documents that feed into unity-ui for implementation. Triggers: 'UX spec', 'screen specification', 'design document', 'UI spec', 'UX design', 'mobile game UI', 'lobby screen', 'popup modal', 'game menu'."
---

# Unity UX Design — Mobile Game UI

**Input**: Feature requirements, target device, existing assets, optional screen pattern
**Output**: Unity scene hierarchy, prefab structure, or HTML spec at `Documents/UXSpecs/{ScreenName}_Spec.html`

All patterns derived from Layer Lab GUI Pro-SuperCasual (81 screens, 5,624 GameObjects).

## Workflow

1. **Gather requirements** — screen purpose, target device, aspect ratio, existing assets
2. **Select pattern** — match from design patterns reference
3. **Build hierarchy** — Canvas setup template → screen-specific template
4. **Configure components** — standard uGUI components per component reference
5. **Apply responsive rules** — anchoring, Layout Groups, ContentSizeFitter
6. **Add interactions** — touch feedback, transitions, navigation
7. **Output** — scene hierarchy, prefab structure, or HTML spec

## Reference Files

### Screen Design & Patterns
- **[Mobile UI Design Patterns](./references/mobile-ui-design-patterns.md)** — 10 screen patterns with hierarchy blueprints
- **[Mobile Design System](./references/mobile-design-system.md)** — Color palette, typography, spacing, icons

### Implementation
- **[GameObject Hierarchy Best Practices](./references/gameobject-hierarchy-best-practices.md)** — Canvas structure, naming, anchors
- **[Responsive Design Implementation](./references/responsive-design-implementation.md)** — CanvasScaler, anchoring, Layout Groups, SafeArea
- **[UI Component Reference](./references/ui-component-reference.md)** — Full component census with configs

### Interaction & UX
- **[Mobile UX Interaction Patterns](./references/mobile-ux-interaction-patterns.md)** — Touch, navigation, modal, scroll, feedback

### Legacy
- **[Example Specifications](./references/example-specifications.md)** — 4 HTML spec examples
- **[Unity UI Best Practices](../unity-ui/references/unity-ui-best-practices.md)** — General guidelines

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

## Canvas Configuration

```
Canvas (Screen Space - Camera)
├── CanvasScaler: ScaleWithScreenSize, ref 1080×1920, matchWidthOrHeight=0.5
├── GraphicRaycaster
└── SafeArea (stretch all, script adjusts for notch)
    ├── Screen_Lobby (one per screen, toggle active)
    ├── Screen_Shop
    └── PopupLayer
```

- `matchWidthOrHeight`: 0=portrait, 0.5=mixed, 1=landscape
- Screens are direct children of SafeArea, activated/deactivated for navigation
- Popups in separate PopupLayer above all screens
- Never hardcode pixel positions — use Layout Groups and anchoring

## Naming Conventions

| Prefix | Example |
|--------|---------|
| `Screen_` | `Screen_Lobby`, `Screen_Shop` |
| `Panel_` | `Panel_Header`, `Panel_Content` |
| `Group_` | `Group_ResourceBar`, `Group_Buttons` |
| `Button_` | `Button_Play`, `Button_Close` |
| `Text_` | `Text_Title`, `Text_Score` |
| `Icon_` | `Icon_Coin`, `Icon_Star` |
| `Popup_` | `Popup_Reward`, `Popup_Settings` |
| `Item_` | `Item_LeaderboardRow`, `Item_ShopCard` |

## Examples

### Lobby screen
→ Read [Canvas Setup](./assets/templates/CANVAS_SETUP_TEMPLATE.md) + [Lobby Template](./assets/templates/SCREEN_TEMPLATE_LOBBY.md)
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

### Full Example Outputs
- **[ExampleLobbyMenu](./assets/examples/ExampleLobbyMenu.md)** — Full lobby (32 Images, 19 TMP, 12 Buttons)
- **[ExampleItemListScreen](./assets/examples/ExampleItemListScreen.md)** — Leaderboard with ScrollRect
- **[ExampleRewardPopup](./assets/examples/ExampleRewardPopup.md)** — Reward popup with animation

## Integration

- Output hierarchies implementable by `unity-ui` skill
- HTML spec documents feed into `unity-ui` for prefab generation
- All patterns follow Layer Lab conventions validated against 81 production screens

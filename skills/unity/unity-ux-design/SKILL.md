---
name: unity-ux-design
description: "Generate UX screen specification documents and production-ready Unity scene/prefab hierarchies for mobile game UI/UX design. Use when: (1) Creating UX screen specs from requirements, (2) Building mobile game UI scenes with proper Canvas, SafeArea, and Layout Groups, (3) Generating lobby, shop, leaderboard, popup, or any mobile game screen, (4) Documenting UI layouts, navigation flows, and interaction patterns, (5) Defining touch targets, animations, and responsive behavior, (6) Generating spec documents that feed into unity-ui for implementation. Triggers: 'UX spec', 'screen specification', 'design document', 'UI spec', 'UX design', 'mobile game UI', 'lobby screen', 'popup modal', 'game menu'."
---

# Unity UX Design — Mobile Game UI

Generate structured UX screen specifications and production-ready Unity scene/prefab hierarchies for mobile game UI. All patterns derived from the Layer Lab GUI Pro-SuperCasual asset — a production-quality mobile game UI kit with 81 screens, 5,624 GameObjects, and comprehensive uGUI component coverage.

## Purpose

Produce mobile game UI that is:
1. **Structurally correct** — proper Canvas → SafeArea → Screen → Section → Component hierarchy
2. **Responsive** — CanvasScaler (Scale With Screen Size), Layout Groups, flexible anchoring
3. **Touch-friendly** — minimum 44×44dp touch targets, thumb-zone-aware placement
4. **Production-quality** — semantic PascalCase naming, consistent component configuration

## Workflow

1. **Gather requirements** — screen purpose, target device, aspect ratio, existing assets
2. **Select pattern** — match to a screen pattern from the design patterns reference
3. **Build hierarchy** — follow Canvas setup template, then screen-specific template
4. **Configure components** — apply standard uGUI components per the component reference
5. **Apply responsive rules** — anchoring, Layout Groups, ContentSizeFitter per responsive reference
6. **Add interactions** — touch feedback, transitions, navigation per interaction patterns reference
7. **Output** — Unity scene hierarchy, prefab structure, or HTML spec document

## Reference Files

Load references as needed based on the task:

### Screen Design & Patterns
- **[Mobile UI Design Patterns](./references/mobile-ui-design-patterns.md)** — 10 screen patterns (Lobby, Shop, Collection, Leaderboard, Settings, etc.) with hierarchy blueprints and cross-pattern rules
- **[Mobile Design System](./references/mobile-design-system.md)** — Color palette, rarity system, typography, spacing scale, icon conventions

### Implementation
- **[GameObject Hierarchy Best Practices](./references/gameobject-hierarchy-best-practices.md)** — Canvas structure, naming conventions, anchor presets, depth guidelines
- **[Responsive Design Implementation](./references/responsive-design-implementation.md)** — CanvasScaler config, anchoring strategies, Layout Groups, SafeArea, ScrollRect
- **[UI Component Reference](./references/ui-component-reference.md)** — Full component census with exact configurations (Button, ScrollRect, LayoutGroup, etc.)

### Interaction & UX
- **[Mobile UX Interaction Patterns](./references/mobile-ux-interaction-patterns.md)** — Touch, navigation, modal, scroll, and feedback patterns

### Legacy (kept for compatibility)
- **[Example Specifications](./references/example-specifications.md)** — 4 HTML spec examples (Main Menu, Settings, Game HUD, iPad)
- **[Unity UI Best Practices](./references/unity-ui-best-practices.md)** — General canvas, layout, and performance guidelines

## Templates

Reusable hierarchy blueprints in `assets/templates/`. Copy and adapt for each screen:

| Template | Use When |
|----------|----------|
| **[Canvas Setup](./assets/templates/CANVAS_SETUP_TEMPLATE.md)** | Starting any new UI scene — Canvas + SafeArea + ScreenManager |
| **[Lobby Screen](./assets/templates/SCREEN_TEMPLATE_LOBBY.md)** | Main menu / lobby with header, content cards, bottom nav |
| **[Scrollable List](./assets/templates/SCREEN_TEMPLATE_LIST_SCROLLABLE.md)** | Leaderboard, collection, friends list, any scrolling content |
| **[Popup Modal](./assets/templates/COMPONENT_POPUP_MODAL.md)** | Centered popup over dimmed background with open/close animation |
| **[Confirmation Dialog](./assets/templates/COMPONENT_DIALOG_CONFIRMATION.md)** | Compact yes/no or accept/cancel dialog |
| **[Responsive Panel](./assets/templates/RESPONSIVE_PANEL_EXAMPLE.md)** | 5 responsive layout recipes (resource bar, card grid, etc.) |
| **[Interactive Demo HTML](./assets/templates/INTERACTIVE_DEMO.html)** | HTML spec document generation (legacy workflow) |

## Quick Start — Canvas Configuration

Every mobile game UI scene starts with this Canvas setup:

```
Canvas (Screen Space - Camera)
├── CanvasScaler: ScaleWithScreenSize, ref 1080×1920, matchWidthOrHeight=0.5
├── GraphicRaycaster
└── SafeArea (stretch all, script adjusts for notch)
    ├── Screen_Lobby (one per screen, toggle active)
    ├── Screen_Shop
    └── PopupLayer
```

**Key rules:**
- `matchWidthOrHeight = 0` for portrait-dominant, `0.5` for mixed, `1` for landscape
- Every screen is a direct child of SafeArea, activated/deactivated for navigation
- Popups live in a separate PopupLayer above all screens
- Never hardcode pixel positions — use Layout Groups and anchoring

## Naming Conventions

| Prefix | Usage | Example |
|--------|-------|---------|
| `Screen_` | Top-level screen container | `Screen_Lobby`, `Screen_Shop` |
| `Panel_` | Major section within screen | `Panel_Header`, `Panel_Content` |
| `Group_` | Layout group container | `Group_ResourceBar`, `Group_Buttons` |
| `Button_` | Interactive button | `Button_Play`, `Button_Close` |
| `Text_` | Text element | `Text_Title`, `Text_Score` |
| `Icon_` | Icon image | `Icon_Coin`, `Icon_Star` |
| `Bg` / `Background` | Background element | `BgPanel`, `Background` |
| `Popup_` | Modal/popup container | `Popup_Reward`, `Popup_Settings` |
| `Item_` | Repeatable list/grid item | `Item_LeaderboardRow`, `Item_ShopCard` |

## Input

| Source | Details |
|--------|---------|
| Feature requirements | User story, product brief, or verbal description of the screen |
| Target device | Phone (portrait 9:16), tablet, or adaptive |
| Existing assets | Sprites, icons, fonts already in the project |
| Screen pattern | (Optional) Specific pattern from the design patterns reference |

## Output

One of:

1. **Unity scene hierarchy** — complete GameObject tree with components, ready to build in editor
2. **Prefab structure** — reusable prefab with component configuration
3. **HTML spec document** — saved to `Documents/UXSpecs/{ScreenName}_Spec.html` (legacy workflow, use INTERACTIVE_DEMO.html template)

The output must include:
- Complete hierarchy with semantic names
- All uGUI components with configuration values
- Anchor/pivot settings for every RectTransform
- Layout Group settings where applicable
- Touch target sizing (minimum 44×44dp)
- Navigation flow notes

## Examples

### Example 1: Lobby screen
```
User: "Create a lobby screen with player info, resource bar, and play button"
```
→ Read [Canvas Setup](./assets/templates/CANVAS_SETUP_TEMPLATE.md) + [Lobby Template](./assets/templates/SCREEN_TEMPLATE_LOBBY.md)
→ Read [Mobile UI Design Patterns](./references/mobile-ui-design-patterns.md) §Lobby/Main-Menu
→ Generate hierarchy:
```
Screen_Lobby
├── Panel_Header (top-stretch)
│   ├── Group_PlayerInfo (HorizontalLayoutGroup)
│   │   ├── Image_Avatar
│   │   ├── Text_PlayerName
│   │   └── Text_Level
│   └── Group_ResourceBar (HorizontalLayoutGroup, spacing=20)
│       ├── Group_Coins [Icon_Coin + Text_CoinCount]
│       └── Group_Gems [Icon_Gem + Text_GemCount]
├── Panel_Content (middle-stretch, VerticalLayoutGroup)
│   ├── Group_FeaturedBanner (Image + overlay text)
│   └── Group_QuickActions (HorizontalLayoutGroup)
│       ├── Button_Shop
│       ├── Button_Collection
│       └── Button_Social
├── Panel_Bottom (bottom-stretch)
│   └── Button_Play (large CTA, centered)
└── Background (full-stretch, behind all)
```

### Example 2: Popup modal
```
User: "Create a reward popup that shows earned items"
```
→ Read [Popup Modal Template](./assets/templates/COMPONENT_POPUP_MODAL.md)
→ Read [Mobile UX Interaction Patterns](./references/mobile-ux-interaction-patterns.md) §Modal
→ Generate popup hierarchy with dimmer overlay, reward card grid, and claim button

### Example 3: Scrollable list
```
User: "Build a leaderboard screen with player rankings"
```
→ Read [Scrollable List Template](./assets/templates/SCREEN_TEMPLATE_LIST_SCROLLABLE.md)
→ Read [UI Component Reference](./references/ui-component-reference.md) §ScrollRect
→ Generate ScrollRect with vertical content, row prefab template, and pagination

### Full Example Outputs

Complete scene hierarchy examples with every component configured:
- **[ExampleLobbyMenu](./assets/examples/ExampleLobbyMenu.md)** — Full lobby with header, resources, content cards, bottom nav (32 Images, 19 TMP, 12 Buttons)
- **[ExampleItemListScreen](./assets/examples/ExampleItemListScreen.md)** — Leaderboard with tabs, player rank, ScrollRect, row prefab (ScrollRect + GridLayout variant)
- **[ExampleRewardPopup](./assets/examples/ExampleRewardPopup.md)** — Reward popup with dimmer, item card grid, claim/double CTA, animation sequence

## Integration

- Output hierarchies are directly implementable by the `unity-ui` skill
- HTML spec documents feed into `unity-ui` for prefab generation
- All patterns follow Layer Lab conventions validated against 81 production screens

## Layer Lab Reference

All patterns in this skill are derived from analyzing the **Layer Lab GUI Pro-SuperCasual** asset:
- 81 screen designs covering every common mobile game UI pattern
- 5,624 GameObjects with consistent hierarchy and naming
- 3,755 Image, 1,142 TextMeshProUGUI, 230 Button, 184 HorizontalLayoutGroup components
- Canvas: Screen Space - Camera, ScaleWithScreenSize at 1048×2048 reference resolution
- Authoritative source for naming, hierarchy depth, component configuration, and responsive anchoring
# Mobile Game Design System

> Visual design tokens, color palette, typography, spacing, iconography, and rarity system derived from Layer Lab GUI Pro-SuperCasual screenshots and DemoScene.unity analysis

## 1. Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **CTA Yellow** | `#FFD700` | (255, 215, 0) | Primary action buttons (Play, Claim, Buy) |
| **Info Cyan** | `#00CFFF` | (0, 207, 255) | Secondary buttons, info panels, links |
| **Alert Red** | `#FF3333` | (255, 51, 51) | Close buttons, notification badges, warnings |
| **Success Green** | `#33CC33` | (51, 204, 51) | Progress fills, success states, online status |
| **Nav Dark** | `#1A2040` | (26, 32, 64) | Navigation bars, panel backgrounds, headers |
| **Panel Blue** | `#2A3A6A` | (42, 58, 106) | Popup panels, card backgrounds |

### Neutral Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **White** | `#FFFFFF` | (255, 255, 255) | Text, icons on dark backgrounds |
| **Light Gray** | `#CCCCCC` | (204, 204, 204) | Disabled text, placeholder text |
| **Mid Gray** | `#808080` | (128, 128, 128) | Disabled buttons, dividers |
| **Dark Gray** | `#333333` | (51, 51, 51) | Text outlines, shadows |
| **Near Black** | `#1A1A2E` | (26, 26, 46) | Deep backgrounds, dim overlays |
| **Dim Overlay** | `#000000B3` | (0, 0, 0, 0.7) | Popup dim background |

### Semantic Colors

| Context | Color | When Used |
|---------|-------|-----------|
| **Positive** | Green `#33CC33` | Stat increases, success, health full |
| **Negative** | Red `#FF3333` | Stat decreases, errors, health low |
| **Warning** | Orange `#FF8800` | Low resources, energy depleting |
| **Highlight** | Yellow `#FFD700` | Active selection, current progress |
| **Information** | Cyan `#00CFFF` | Tips, descriptions, secondary actions |
| **Premium** | Purple `#9933FF` | Premium currency, special offers |

### Button Color Themes (from Component Sheet analysis)

| Theme Name | Background | Text | Usage |
|-----------|-----------|------|-------|
| **Sky** | Light blue gradient | White | General secondary buttons |
| **Blue** | Medium blue | White | Navigation, info buttons |
| **Dark** | Navy/dark blue | White | Header buttons, settings |
| **Green** | Bright green | White | Confirm, accept, equip |
| **Yellow** | Gold/yellow gradient | Dark text | Primary CTA, play, claim |
| **Red** | Bright red | White | Close, delete, destructive |
| **Purple** | Rich purple | White | Premium, special features |
| **Pink** | Hot pink | White | Social, gift features |
| **Mint** | Teal/mint green | White | Refresh, new features |
| **Gray** | Medium gray | White | Disabled, skip, cancel |

## 2. Rarity Color System

### Rarity Tiers

| Tier | Name | Border Color | Background Tint | Glow | Hex Code |
|------|------|-------------|-----------------|------|----------|
| 1 | **Common** | Gray | Light gray | None | `#808080` |
| 2 | **Uncommon** | Green | Light green | Subtle | `#33CC33` |
| 3 | **Rare** | Blue | Light blue | Medium | `#3399FF` |
| 4 | **Epic** | Purple | Light purple | Strong | `#9933FF` |
| 5 | **Legendary** | Yellow/Gold | Light gold | Intense | `#FFD700` |
| 6 | **Mythic** | Red/Pink | Light red | Maximum + particles | `#FF3366` |

### Rarity Application Pattern
```
Card_Item_Rare
  +-- Border_Rarity [Image]
  |     Color: Rare Blue (#3399FF)
  |     Sprite: card_border_glow (sliced)
  +-- Background [Image]
  |     Color: Rare Blue tinted (#3399FF, alpha 0.15)
  +-- Icon_Item [Image]
  +-- Text_Name [TextMeshProUGUI]
  |     Color: White
  +-- Group_Stars
        +-- Star_1 [Image] (filled)
        +-- Star_2 [Image] (filled)
        +-- Star_3 [Image] (filled)
        +-- Star_4 [Image] (empty)
        +-- Star_5 [Image] (empty)
```

### Rarity in Equipment Info Popups (Layer Lab: 7 variants)
- **Header panel color** changes to match rarity
- **Item border glow** intensity increases with rarity
- **Background particle effects** appear at Legendary and above
- **Star count** visible below item icon matches rarity tier

## 3. Typography System

### Font Selection
- **Primary font**: Bold rounded sans-serif (super-casual cartoon style)
- **Font weight**: Predominantly Bold — nearly all game UI text uses bold weight
- **Text rendering**: TextMeshProUGUI with outline and shadow materials

### Type Scale

| Level | Name | Size (px) | Weight | Line Height | Usage |
|-------|------|----------|--------|-------------|-------|
| H0 | **Display** | 64-72 | ExtraBold | 1.1× | Level numbers, "VICTORY!", milestone badges |
| H1 | **Title** | 48-56 | Bold | 1.2× | Screen titles, popup headers |
| H2 | **Heading** | 36-44 | Bold | 1.2× | Section headers, card titles |
| H3 | **Subheading** | 28-32 | Bold | 1.3× | Subtitles, category labels |
| B1 | **Body Large** | 24-28 | Bold | 1.4× | Descriptions, dialog text |
| B2 | **Body** | 20-24 | Regular | 1.4× | Secondary descriptions, stats |
| C1 | **Caption** | 16-20 | Regular | 1.3× | Timestamps, helper text, version |
| C2 | **Micro** | 12-14 | Bold | 1.2× | Badge numbers, tiny labels |

### Text Styling Patterns

#### Outlined Text (most common in Layer Lab)
```
[TextMeshProUGUI]
  Font Style: Bold
  Color: White (1, 1, 1, 1)
  Material Preset: Outline
    Outline Width: 0.2-0.4
    Outline Color: Dark (#333333)
```

#### Shadow Text
```
[TextMeshProUGUI]
  Font Style: Bold
  Color: White
  + [Shadow] component
    Effect Color: (0, 0, 0, 0.3)
    Effect Distance: (2, -2)
```

#### Colored Value Text
```
Positive stat: Color = Green (#33CC33)
Negative stat: Color = Red (#FF3333)
Currency amount: Color = Yellow (#FFD700) for gold, Purple (#9933FF) for gems
```

### Text Hierarchy Rules
1. **One Display/Title per screen** — never two competing large texts
2. **Numbers are often larger than labels** — "1,234" is more prominent than "Coins:"
3. **White text with dark outline** ensures readability on any background
4. **Numerical values use tabular/monospace** figures to prevent layout shift
5. **Truncate with ellipsis** — never let text overflow its container

## 4. Spacing System

### Base Unit: 8px Grid

| Token | Value | Usage |
|-------|-------|-------|
| `space-2xs` | 4px | Icon-to-text tight gap, badge offset |
| `space-xs` | 8px | Group_Price spacing, inline elements |
| `space-sm` | 12px | List item spacing, card internal padding |
| `space-md` | 16px | Section spacing, card grid gaps |
| `space-lg` | 24px | Section dividers, major content gaps |
| `space-xl` | 36px | GridLayoutGroup spacing (Layer Lab: 36×25) |
| `space-2xl` | 48px | Section padding, large container margins |
| `space-3xl` | 100px | Resource bar spacing (Layer Lab: Group_ResourceBar) |

### Container Padding

| Container | Padding (L, R, T, B) |
|-----------|---------------------|
| Screen safe area | 0, 0, 44, 34 (iPhone safe area) |
| Popup panel | 40, 40, 30, 30 |
| Card content | 20, 20, 16, 16 |
| List row | 24, 24, 12, 12 |
| Button internal | 24, 24, 8, 8 |
| Input field | 16, 16, 8, 8 |

### Spacing Between Screen Sections

```
┌──────────────────────────────┐
│  Top (height: 80-120)        │  ← 0px from safe area top
│  Resource bar, title         │
├──────────────────────────────┤  ← 8-16px gap
│                              │
│  Middle (flexible height)    │  ← Main content area
│  Content, scroll views       │
│                              │
├──────────────────────────────┤  ← 8-16px gap
│  Bottom (height: 100-140)    │  ← 0px from safe area bottom
│  Navigation, action buttons  │
└──────────────────────────────┘
```

## 5. Icon System

### Icon Categories (from Component Sheets 0-7)

| Category | Style | Size | Examples |
|----------|-------|------|----------|
| **Currency** | Full-color 3D render | 48-64px | Coins, gems, energy, keys |
| **Navigation** | White silhouette on transparent | 32-48px | Home, shop, play, profile, settings |
| **Status** | Color-coded | 24-36px | Online (green), offline (gray), busy (orange) |
| **Action** | White silhouette | 32-40px | Add (+), close (X), share, gift, info |
| **Rarity stars** | Gold filled / gray empty | 16-20px | ★★★☆☆ (3/5 stars) |
| **Notification** | Red circle + white text | 24-36px | Badge with count |
| **Tutorial** | Cartoon hand pointer | 48-64px | Finger tap, finger drag |
| **Localization** | Country flag | 32-48px | Language selection |
| **Utility** | Monochrome line icons | 32-48px | Search, filter, sort, refresh |

### Icon Usage Guidelines
1. **Always provide alt-text** via accessible name or tooltip
2. **Consistent sizing** within the same context (all nav icons same size)
3. **Color-code meaning** — don't rely on shape alone (colorblind accessibility)
4. **Touch-size wrapper** — even small icons should have ≥44px touch target
5. **Native resolution** — use 2x assets for Retina, import at correct PPI

### Icon + Text Patterns

```
Horizontal (most common):
  [Icon 32px] [8px gap] [Text]     // Group_Price: icon + amount

Vertical (tab bar):
  [Icon 32px]
  [4px gap]
  [Text 12px]                      // Bottom nav tabs

Badge overlay:
  [Icon 48px]
    [Badge 24px at top-right]      // Notification badge
```

## 6. Card & Panel Design

### Card Anatomy
```
┌─────────────────────────────────────┐
│  ┌───────────────────────────────┐  │  ← Border (rarity colored, 3-5px)
│  │  ┌─────────────┐  Title      │  │
│  │  │   ICON      │  Subtitle   │  │  ← Content area (padding: 16px)
│  │  │   64×64     │  Value      │  │
│  │  └─────────────┘             │  │
│  │  [Button_Action]             │  │  ← Action area (bottom)
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Card Styles

| Style | Shape | Shadow | Border | Usage |
|-------|-------|--------|--------|-------|
| **Flat** | Rounded rect | None | 1px light | List rows, simple items |
| **Elevated** | Rounded rect | Shadow(2,-2) | None | Cards, floating panels |
| **Outlined** | Rounded rect | None | 3-5px colored | Rarity items, equipment |
| **Glossy** | Rounded rect | Shadow | Highlight top edge | Buttons, premium cards |
| **Banner** | Wide rect/ribbon | Shadow | Decorative edges | Rank banners, titles |

### Panel Depth Levels

| Level | Shadow | Background | Usage |
|-------|--------|-----------|-------|
| 0 | None | Transparent | Layout containers |
| 1 | None | Solid color | Screen sections |
| 2 | Subtle | Lighter color | Cards within sections |
| 3 | Medium | White/bright | Popups, modals |
| 4 | Strong | White + glow | Focused/active popup |

## 7. Progress & Status Indicators

### Progress Bar Anatomy
```
ProgressBar_XP
  +-- Background [Image]
  |     Color: Dark gray (#333333)
  |     Sprite: bar_bg (sliced, rounded)
  |     Size: flexible width × 30-40 height
  +-- Fill [Image]
  |     Color: Green (#33CC33) or themed
  |     Sprite: bar_fill (sliced, rounded)
  |     Image Type: Filled, Fill Method: Horizontal
  +-- Text_Progress [TextMeshProUGUI]
  |     Text: "1,234 / 2,000"
  |     Anchor: Center of bar
  +-- Icon_Cap [Image]  // Optional decorative end cap
```

### Status Indicator Types

| Indicator | Visual | Size | Usage |
|-----------|--------|------|-------|
| **Dot** | Colored circle | 12-16px | Online/offline status |
| **Badge** | Red circle + number | 24-36px | Notification count |
| **Star rating** | ★★★☆☆ | 16-20px per star | Rarity, difficulty |
| **Progress bar** | Horizontal fill | Flexible × 30-40px | XP, energy, timer |
| **Radial** | Circular fill | 48-64px | Cooldown, loading |
| **Step indicator** | Dots or segments | 8-12px per dot | Tutorial, onboarding |

## 8. Animation & Motion Tokens

### Duration Scale

| Token | Duration | Easing | Usage |
|-------|---------|--------|-------|
| `instant` | 0.05s | Linear | Toggle states |
| `fast` | 0.1-0.15s | EaseOut | Button press feedback, color tint |
| `normal` | 0.2-0.3s | EaseOutCubic | Screen transitions, popup open/close |
| `slow` | 0.4-0.6s | EaseOutBack | Reward reveal, celebration |
| `dramatic` | 0.8-1.2s | Custom | Level up, victory sequence |

### Common Animation Patterns

| Pattern | Properties | Values |
|---------|-----------|--------|
| **Pop in** | Scale | 0→1.2→1.0 (overshoot) |
| **Fade in** | Alpha | 0→1 |
| **Slide in** | Position | OffScreen→Final |
| **Bounce** | Scale | 1.0→0.95→1.05→1.0 |
| **Pulse** | Scale (loop) | 1.0→1.1→1.0 |
| **Shake** | Position | Rapid small X offsets |
| **Spin** | Rotation Z | 0→360 (loading) |

## 9. Design System Checklist

When creating a new mobile game UI screen, verify:

### Layout
- [ ] Canvas uses Scale With Screen Size (1048×2048, match width)
- [ ] SafeArea panel wraps all interactive content
- [ ] Screen follows Top/Middle/Bottom section pattern
- [ ] Backgrounds use Full Stretch anchors
- [ ] Headers use Top Stretch-H anchors
- [ ] Footers use Bottom Stretch-H anchors

### Components
- [ ] All text uses TextMeshProUGUI (never legacy Text)
- [ ] All buttons use ColorTint transition (Layer Lab standard)
- [ ] Raycast Target disabled on non-interactive Images and Text
- [ ] ScrollRects are vertical-only with elastic movement
- [ ] Layout Groups used instead of manual positioning

### Visual Style
- [ ] Colors match the semantic palette (yellow CTA, red alert, etc.)
- [ ] Rarity colors correctly applied (gray→green→blue→purple→gold→red)
- [ ] Text has outline or shadow for readability
- [ ] Buttons meet minimum touch target sizes (≥60×60 for icons, ≥80 height for standard)
- [ ] Icons are consistent size within same context

### Spacing
- [ ] Spacing follows 8px grid system
- [ ] Consistent padding within similar containers
- [ ] No overlapping elements at any test resolution
- [ ] Notification badges positioned at top-right of parent

### Naming
- [ ] All GameObjects use PascalCase with prefix convention
- [ ] Screens: `Screen_`, `Popup_`, `PopupDim_`, `PopupFull_`
- [ ] Elements: `Text_`, `Button_`, `Icon_`, `Image_`, `Bg`, `Border`, `Group_`

---

*Reference: Layer Lab GUI Pro-SuperCasual — visual analysis of 50+ screenshots across all screen types, component sheets 0-7, and DemoScene.unity structural data*

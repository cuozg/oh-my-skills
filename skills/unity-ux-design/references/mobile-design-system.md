# Mobile Game Design System

> From Layer Lab GUI Pro-SuperCasual analysis.

## 1. Color Palette

### Primary
| Name | Hex | Usage |
|---|---|---|
| CTA Yellow | `#FFD700` | Primary action (Play, Claim) |
| Info Cyan | `#00CFFF` | Secondary buttons, info |
| Alert Red | `#FF3333` | Close, notifications |
| Success Green | `#33CC33` | Progress, success |
| Nav Dark | `#1A2040` | Nav bars, headers |
| Panel Blue | `#2A3A6A` | Popups, cards |

### Neutral: White `#FFF`, Light Gray `#CCC` (disabled), Mid Gray `#808080` (dividers), Dim Overlay `#000000B3` (70%)

### Semantic: Positive=Green, Negative=Red, Warning=Orange `#FF8800`, Premium=Purple `#9933FF`

### Button Themes
Sky (light blue), Blue, Dark (navy), Green (confirm), Yellow (CTA), Red (destructive), Purple (premium), Pink (social), Mint (refresh), Gray (disabled)

## 2. Rarity System

| Tier | Name | Color | Hex |
|---|---|---|---|
| 1 | Common | Gray | `#808080` |
| 2 | Uncommon | Green | `#33CC33` |
| 3 | Rare | Blue | `#3399FF` |
| 4 | Epic | Purple | `#9933FF` |
| 5 | Legendary | Gold | `#FFD700` |
| 6 | Mythic | Red/Pink | `#FF3366` |

Apply via: border color, bg tint (0.15 alpha), glow, star count.

## 3. Typography

Font: Bold rounded sans-serif. Rendering: TMP with outline (0.2-0.4, #333) or shadow.

| Level | Size (px) | Usage |
|---|---|---|
| H0 Display | 64-72 | "VICTORY!", level numbers |
| H1 Title | 48-56 | Screen titles, popup headers |
| H2 Heading | 36-44 | Section headers |
| H3 Subheading | 28-32 | Category labels |
| B1 Body Large | 24-28 | Descriptions |
| B2 Body | 20-24 | Secondary text |
| C1 Caption | 16-20 | Timestamps, helper |
| C2 Micro | 12-14 | Badge numbers |

One Display/screen. Numbers > labels. White + dark outline. Truncate with ellipsis.

## 4. Spacing System (8px Grid)

| Token | Value | Usage |
|---|---|---|
| 2xs | 4px | Icon-text tight gap |
| xs | 8px | Inline elements |
| sm | 12px | List spacing, card padding |
| md | 16px | Section spacing |
| lg | 24px | Section dividers |
| xl | 36px | Grid spacing |
| 2xl | 48px | Container margins |

### Container Padding (L,R,T,B)
Screen safe area: 0,0,44,34 | Popup: 40,40,30,30 | Card: 20,20,16,16 | List row: 24,24,12,12 | Button: 24,24,8,8

## 5. Icons

| Category | Style | Size |
|---|---|---|
| Currency | Full-color 3D | 48-64px |
| Navigation | White silhouette | 32-48px |
| Action | White silhouette | 32-40px |
| Status | Color-coded | 24-36px |
| Notification | Red circle + white text | 24-36px |

Touch wrapper ≥44px. Consistent sizing per context.

## 6. Cards & Panels

| Style | Shadow | Border | Usage |
|---|---|---|---|
| Flat | None | 1px | List rows |
| Elevated | Shadow(2,-2) | None | Cards |
| Outlined | None | 3-5px colored | Rarity items |
| Glossy | Shadow | Highlight edge | Buttons, premium |

## 7. Animation Tokens

| Token | Duration | Usage |
|---|---|---|
| instant | 0.05s | Toggle states |
| fast | 0.1-0.15s | Button press |
| normal | 0.2-0.3s | Screen transitions |
| slow | 0.4-0.6s | Reward reveal |
| dramatic | 0.8-1.2s | Victory sequence |

Patterns: Pop in (0→1.2→1.0), Fade, Slide, Bounce (1→0.95→1.05→1), Pulse (loop 1→1.1→1), Shake

## 8. Design Checklist

- [ ] Canvas: Scale With Screen Size (1048×2048), SafeArea wraps content
- [ ] Top/Middle/Bottom section pattern, stretch anchors on backgrounds
- [ ] All text TMP, buttons ColorTint, raycastTarget off on non-interactive
- [ ] Colors match semantic palette, rarity colors correct
- [ ] Text has outline/shadow, touch targets ≥60×60 (icons) / ≥80h (standard)
- [ ] 8px grid spacing, consistent padding
- [ ] PascalCase naming: `Screen_`, `Popup_`, `Text_`, `Button_`, `Icon_`, `Group_`

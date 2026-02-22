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

<!-- See also: mobile-design-system-part2.md -->

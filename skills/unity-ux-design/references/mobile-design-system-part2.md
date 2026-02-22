# Mobile Game Design System (Continued)

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

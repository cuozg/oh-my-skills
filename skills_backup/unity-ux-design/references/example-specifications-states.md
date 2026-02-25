# UX Screen Specification Examples — States & Interactions

## Example A (continued): States and Interactions

### States
- **Loading:** Skeleton placeholders for avatar/name/currency. Carousel shimmer.
- **Maintenance:** Play button grey, text="Maintenance", glow stops.
- **Daily Reward Available:** Pulsing glow badge on DailyRewardBtn.

### Interactions
1. **Tap Play** → Battle Select (if not disabled/loading). Error: "Connection Error" toast.
2. **Tap Settings** → Settings modal overlay.
3. **Swipe Carousel** → Next/prev banner, update dots. Pauses auto-rotate 10s.
4. **Tap Tab** → Switch section (Battle/Shop/Social).
5. **Tap Inbox** → Inbox screen, clear badge.
6. **Tap Daily Reward** → Claim popup (if available). Already claimed: "Come Back Tomorrow" toast.

### Data

| Field | Source | Type | Update | Fallback |
|---|---|---|---|---|
| `player_name` | Server | string | On load | "Player" |
| `player_level` | Server | int | On load | 1 |
| `currency_coins` | Server | int | Real-time event | 0 |
| `currency_gems` | Server | int | On load | 0 |
| `promo_banners` | CDN | List\<BannerData\> | Cached 1hr | Default banner |
| `unread_inbox_count` | Server | int | Poll 30s | 0 |
| `daily_reward_available` | Server | bool | On load/foreground | false |

### Rules
- **R-MM-001** 🔴 Play button always visible without scrolling (primary CTA, never below fold)
- **R-MM-002** 🔴 Currency updates real-time via events, not polling
- **R-MM-003** 🟡 Carousel handles 0 banners (default), 1 (no dots/scroll), up to 8
- **R-MM-004** 🟡 Inbox badge caps at "99+", red circle white text
- **R-MM-005** 🟢 Tab icons: outlined unselected, filled selected

### Accessibility & Layout
- Touch targets: 44x44pt minimum. Text scaling: up to 1.5x dynamic text.
- RTL: mirror layout, carousel swipe inverts.
- SafeArea: top bar below notch, tab bar above home indicator.
- Canvas Scaler: Scale With Screen Size, ref 1080x1920, match 0.5. Portrait only.
- Aspect ratios: 9:16 (base), 9:19.5 (extra vertical space), 3:4 (2-col grid, carousel 240pt).

### Canvas Hierarchy
```
Canvas (Screen Space - Overlay)
+-- CanvasScaler (ref: 1080x1920, match: 0.5)
+-- SafeArea
    +-- TopBar (H:80) [Avatar 120x120 | PlayerInfo | CurrencyGroup]
    +-- SettingsBtn (48x48)
    +-- ContentArea (pad: top 90, bottom 120)
    |   +-- PromoCarousel (H:180)
    |   +-- ButtonGrid (GridLayout 2col) [Daily|Shop|Events|Friends]
    |   +-- PlayButton (stretch-x, H:56)
    |   +-- InboxBtn
    +-- BottomTabBar (H:56) [Home|Battle|Shop|Social 25% each]
```

### Animations
- **Entry:** Fade from black, elements stagger from bottom (0.5s, 0.05s stagger, EaseOutQuad)
- **Exit:** Slide left (forward nav) or fade out (modal), 0.3s EaseInQuad
- **Play Glow:** Scale 1.0→1.02, opacity 0.6→1.0, 2s loop EaseInOutSine

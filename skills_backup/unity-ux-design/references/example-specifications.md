# UX Screen Specification Examples

Two production-ready examples demonstrating how to fill out the UX Screen Spec template. Example A = full screen (mobile portrait), Example C = real-time HUD (landscape).

## Example A: Main Menu Screen (Mobile Portrait 9:16)

### Overview
| Field | Value |
|---|---|
| Screen ID | SCR-MAINMENU-001 |
| Purpose | Primary hub for navigation to all game features |
| Device | Mobile (iPhone/Android), 9:16 |
| Priority | P0 - Critical |
| Elements: 18 | States: 6 | Entry Points: 3 |

**Nav:** App Launch / Battle Result / Settings Back → Main Menu → Battle Select / Settings / Shop / Inbox

### Wireframe
```
+=========================================+
| [Safe Area Top]                         |
| (Avatar) PlayerName Lv.42 [Coins][Gems] |
| [Settings Gear]                         |
| [PROMO CAROUSEL * o o]                  |
| [Daily Rewards][Shop]                   |
| [Events][Friends]                       |
| [========= PLAY =========]             |
| [Inbox (3)]                             |
| [Home] [Battle] [Shop] [Social]         |
| [Safe Area Bottom]                      |
+=========================================+
```

### UI Elements

| ID | Type | States | Constraints |
|---|---|---|---|
| `MM_AvatarImage` | Image | Default | 120x120pt, circular mask, fallback: default_avatar.png |
| `MM_PlayerName` | Text | Default | Max 16 chars, ellipsis |
| `MM_LevelBadge` | Text | Default | Max "Lv.999", gold on dark |
| `MM_PlayButton` | Button | Default/Pressed/Disabled/Loading | Full width, 56pt, blue glow |
| `MM_SettingsBtn` | Button | Default/Pressed | 48x48pt touch, 24x24 icon |
| `MM_PromoCarousel` | Scroll | Default/Scrolling | Auto-rotate 5s, dots, 180pt |
| `MM_DailyRewardBtn` | Button | Default/Available/Claimed | Badge dot when claimable |
| `MM_ShopBtn` | Button | Default/Pressed | 44x44pt min |
| `MM_EventsBtn` | Button | Default/Pressed | Red dot if active event |
| `MM_FriendsBtn` | Button | Default/Pressed | Online count badge |
| `MM_InboxBtn` | Button | Default/Pressed | Badge max "99+", red circle |
| `MM_CoinDisplay` | Text | Default | Comma-separated, 20x20 icon |
| `MM_GemDisplay` | Text | Default | Comma-separated, 20x20 icon |
| `MM_Tab*` | Tab | Default/Selected | 44pt height, icon+underline |
| `MM_BackgroundImg` | Image | Default | Aspect fill, blur behind UI |

### Key Interactive Details
- **PlayButton:** Scale 0.95 press (0.1s), glow pulse 2s loop. Disabled=grey "Maintenance". Loading=spinner.
- **PromoCarousel:** Auto-rotate 5s (0.4s slide). Pauses 10s after user swipe. 0 banners=default placeholder.
- **DailyRewardBtn:** Bounce badge when available (3s loop). Dimmed when claimed.
- **TabBar:** Underline slides 0.2s EaseInOut. Grey→Blue+underline on select.

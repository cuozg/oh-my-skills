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

## Example C: Game HUD (Landscape 16:9)

### Overview
| Field | Value |
|---|---|
| Screen ID | SCR-HUD-001 |
| Purpose | Real-time battle HUD: health, abilities, timer, score, controls |
| Device | Mobile (Landscape), 16:9/19.5:9 |
| Priority | P0 - Critical |

**Performance paramount:** No layout recalculations or GC allocations during battle. All client-driven, no server calls.
**Safe Area:** Left/right 44pt inset on notched devices.

**Nav:** Battle loading / countdown → HUD → Victory/Defeat / Pause quit / Disconnect

### Wireframe
```
+------------------------------------------------------------------+
| [Portrait] [====HP====] [==Enemy HP==] [Timer]    [Score] [Pause]|
|            [====MP====] [Boss Name   ]            [Auto] [Speed] |
|            [buff icons]                                          |
|                         (3D Battle Scene)              x12       |
|                                                         [Ult]   |
| [MiniMap]                                         [A1-A4 cluster]|
+------------------------------------------------------------------+
```

### UI Elements

| ID | Type | Required | Key Notes |
|---|---|---|---|
| `HUD_HPBar` | Slider | Yes | Gradient green→yellow→red by %, numeric value |
| `HUD_MPBar` | Slider | Yes | Blue fill, depletes on ability use |
| `HUD_Portrait` | Image | Yes | 64x64pt circular |
| `HUD_EnemyHP` | Slider | Yes | Red fill, boss name above, multi-phase support |
| `HUD_Timer` | TMP | Yes | Red <30s, pulse <10s |
| `HUD_Score` | TMP | No | Pop+settle on change |
| `HUD_PauseBtn` | Button | Yes | 44x44pt |
| `HUD_Ability1-4` | Button | Yes | 72x72pt, cooldown radial fill, MP cost check |
| `HUD_UltimateBtn` | Button | Yes | 88x88pt, charge % ring, golden glow at 100% |
| `HUD_MiniMap` | RawImage | No | 120x120pt, rotates with camera |
| `HUD_ComboCounter` | TMP | No | Fades after 2s idle, milestones at x5/x10/x25 |
| `HUD_BuffIcons` | HLayout | No | 24x24pt icons with duration overlay |
| `HUD_AutoPlayToggle` | Toggle | No | Unlocks at level 10 |
| `HUD_SpeedToggle` | Button | No | Cycles 1x→2x→3x, requires auto-play |

### Key Interactive Details
- **HPBar:** Fill animates 0.3s EaseOut. Damage flash white 0.1s. Critical (<20%): red + pulse 0.5s loop.
- **Abilities:** Ready=full color. Cooldown=grey radial wipe+timer. Not enough MP=desaturated, red cost. Ready flash once.
- **Ultimate:** Charging=grey+%. Fully charged=golden burst+glow loop. Activation=screen-wide flash 0.2s.
- **Timer:** >30s white, <30s yellow, <10s red+scale pulse 1.0→1.1 (0.5s loop).
- **Combo:** Scale pop 1.0→1.3→1.0 (0.15s). Milestones: color flash+particle burst.

### Interactions
1. **Tap Ability** → Activate, start cooldown, deduct MP. On cooldown: shake 0.2s. No MP: flash MP bar red.
2. **Tap Ultimate** → Cinematic trigger, reset charge. Not charged: show % tooltip.
3. **Tap Pause** → Pause time, dim HUD 40%, show pause menu.
4. **Toggle Auto-Play** → Enable/disable AI play. Locked <Lv10: "Unlock at Level 10" toast.
5. **Cycle Speed** → 1x→2x→3x→1x. Requires auto-play enabled.

### Data
All client-side. HP/MP/Timer/Cooldowns update per-frame via cached refs. Combo/Score on events. Buffs on add/remove. Object pool buff icons and combo text.

### Rules
- **R-HUD-001** 🔴 Zero GC allocs per frame. Pre-allocated StringBuilders, no concat/boxing/LINQ.
- **R-HUD-002** 🔴 HP/MP bars update same frame as damage event (LateUpdate sync).
- **R-HUD-003** 🔴 Clear visual distinction: cooldown vs not-enough-MP vs ready.
- **R-HUD-004** 🟡 Combo auto-hides after 2s. Milestones (x5/x10/x25/x50/x100) get special VFX.
- **R-HUD-005** 🟡 Respect landscape safe areas, no interactive element within 44pt of edges.
- **R-HUD-006** 🟢 Speed toggle only when auto-play on. Disabling auto-play resets to 1x.

### Canvas Hierarchy
```
Canvas (Screen Space - Overlay)
+-- CanvasScaler (ref: 1920x1080, match: 0.5)
+-- SafeArea (landscape insets)
    +-- TopLeftGroup [Portrait 64x64 | HPBar 200x16 | MPBar 180x12 | BuffIcons]
    +-- TopCenterGroup [EnemyHP 300x16 | EnemyName | Timer]
    +-- TopRightGroup [Score | PauseBtn 44x44 | AutoPlay 44x44 | Speed 44x44]
    +-- CenterRight [ComboCounter]
    +-- BottomLeft [MiniMap 120x120]
    +-- BottomRight [UltimateBtn 88x88 | Ability1-4 72x72]
```

### Animations
- **Battle Start:** Slide in from edges, 0.4s staggered 0.05s, EaseOutBack
- **Damage:** HP fill 0.3s EaseOut + white flash 0.1s + red vignette 0.2s
- **Cooldown:** Radial clockwise grey overlay (linear). Ready: golden flash 0.3s.
- **Ultimate Charged:** Golden burst 0.5s + glow loop 1.5s + bob 2s
- **Battle End:** HUD fades 0.5s. Victory: fly up+confetti. Defeat: darken+sink.

## Template Usage Guide

1. Copy Sections 1-14 + 5B from template, replace `[PLACEHOLDERS]`
2. Fill: Overview (SCR-XXXX-NNN), Nav Flow, Wireframe, States, Elements, Interactions
3. Fill: Data, Rules (RULE-NNN), Accessibility, Responsive, Animations, Acceptance (AC-NNN)

### Element States Checklist

| Type | States | Key |
|---|---|---|
| Button | Default/Pressed/Disabled | ≥44pt tap target |
| Toggle | On/Off/Disabled | Track color, transition |
| Slider | Default/Dragging/Disabled | Fill, thumb, range |
| Dropdown | Closed/Open/Disabled | Max height, scroll |
| Tab | Active/Inactive | Indicator, anim |
| Progress | Empty/Filling/Full | Gradient, label |
| Timer | Running/Paused/Expired/Warning | Threshold, pulse |
| Input | Empty/Focused/Filled/Error/Disabled | Char limit, validation |

### Best Practices
- Consistent IDs: `SCR-[FEATURE]-[NNN]`, `RULE-NNN`, `AC-NNN`
- Document all states: Loading, Empty, Populated, Error, Offline minimum
- Exact values (pt, hex, ms) — no vague terms ("large", "bright")
- Tap targets ≥44x44pt (iOS) / ≥48x48dp (Android)
- Fallback values for every data-driven field
- Version specs, cross-reference Screen IDs in nav flow

### Unity UI Performance
- Separate Canvases for static/dynamic (rebuild is O(n))
- Disable `Raycast Target` on non-interactive, Layout Groups when static
- Pool spawned UI; atlas sprites by screen; use TMP with pre-gen atlases
- Minimize overdraw; prefer DOTween over Animator for simple tweens
- **Budget:** <2ms/frame UI on mid-range devices

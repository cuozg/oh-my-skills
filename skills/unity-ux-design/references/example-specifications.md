# UX Screen Specification Examples

This document contains four production-ready example screen specifications converted from the UX Screen Spec HTML template. These examples demonstrate how to fill out each section of the template for different screen types, devices, and use cases. Use them as reference when creating new screen specifications for your Unity project.

**Examples included:**
- **Example A:** Main Menu Screen (Mobile Portrait 9:16)
- **Example B:** Settings Dialog (Modal, Responsive)
- **Example C:** Game HUD (Landscape 16:9)
- **Example D:** iPad Main Menu (3:4 Adaptation)

Following the examples, a **Template Usage Guide** provides step-by-step instructions, checklists, best practices, and Unity-specific performance notes.

---

## Example A: Main Menu Screen (Mobile Portrait 9:16)

### Section 1: Screen Overview

| Field         | Value                                              |
| ------------- | -------------------------------------------------- |
| Screen Name   | Main Menu                                          |
| Screen ID     | SCR-MAINMENU-001                                   |
| Purpose       | Primary hub screen for navigation to all game features |
| Type          | Screen                                             |
| Date          | 2026-02-09                                         |
| Version       | 1.0                                                |
| Device        | Mobile (iPhone/Android)                            |
| Aspect Ratio  | 9:16                                               |

**Summary Cards:**

| UI Elements | States | Entry Points | Priority     |
| ----------- | ------ | ------------ | ------------ |
| 18          | 6      | 3            | P0 - Critical |

### Section 2: Navigation Flow

**Entry Points:**
- App Launch → Main Menu
- Battle Result → Main Menu
- Settings (Back) → Main Menu

**Exit Points:**
- Main Menu → Battle Select
- Main Menu → Settings
- Main Menu → Shop
- Main Menu → Inbox

### Section 3: Visual Layout / Wireframe

```
+=========================================+
|  [Safe Area Top]                        |
|  +-----------------------------------+  |
|  | (Avatar) PlayerName    Lv.42      |  |
|  |          [Coins: 12,500] [Gems: 8]|  |
|  +-----------------------------------+  |
|  |        [Settings Gear]             |  |
|  +-----------------------------------+  |
|                                         |
|  +-----------------------------------+  |
|  |        PROMO CAROUSEL              |  |
|  |  [< Banner 1 | Banner 2 | ... >]  |  |
|  |          * o o  (dots)             |  |
|  +-----------------------------------+  |
|                                         |
|  +-----------------------------------+  |
|  |                                   |  |
|  |     +-----------+-----------+     |  |
|  |     |  Daily    |   Shop    |     |  |
|  |     | Rewards   |           |     |  |
|  |     +-----------+-----------+     |  |
|  |     |  Events   |  Friends  |     |  |
|  |     |           |   List    |     |  |
|  |     +-----------+-----------+     |  |
|  |                                   |  |
|  +-----------------------------------+  |
|                                         |
|  +===================================+  |
|  |         >>> PLAY <<<               |  |
|  +===================================+  |
|                                         |
|  +---[Inbox (3)]---------------------+  |
|                                         |
|  +-----------------------------------+  |
|  | [Home]  [Battle]  [Shop]  [Social]|  |
|  +-----------------------------------+  |
|  [Safe Area Bottom]                     |
+=========================================+
```

### Section 5: UI Elements Inventory

| ID                 | Type       | Label / Content                     | States                              | Constraints                                              |
| ------------------ | ---------- | ----------------------------------- | ----------------------------------- | -------------------------------------------------------- |
| `MM_AvatarImage`   | **Image**  | Player avatar portrait              | Default                             | 120x120 pt, circular mask, fallback: default_avatar.png  |
| `MM_PlayerName`    | **Text**   | Player display name                 | Default                             | Max 16 chars, truncate with ellipsis                     |
| `MM_LevelBadge`    | **Text**   | Player level display (e.g. "Lv.42") | Default                             | Max "Lv.999", gold text on dark bg                       |
| `MM_PlayButton`    | **Button** | "PLAY" - Primary CTA                | Default, Pressed, Disabled, Loading | Full width minus margins, height 56pt, blue glow effect  |
| `MM_SettingsBtn`   | **Button** | Gear icon - opens settings          | Default, Pressed                    | 48x48 pt touch target, icon 24x24                        |
| `MM_PromoCarousel` | **Scroll** | Horizontal promo banner carousel    | Default, Scrolling                  | Auto-rotate every 5s, dot indicators below, height 180pt |
| `MM_DailyRewardBtn`| **Button** | "Daily Rewards" with reward icon    | Default, Available, Claimed         | Shows badge dot when claimable                           |
| `MM_ShopBtn`       | **Button** | "Shop" with cart icon               | Default, Pressed                    | Grid button, 44x44 pt minimum                            |
| `MM_EventsBtn`     | **Button** | "Events" with calendar icon         | Default, Pressed                    | Grid button, shows red dot if active event               |
| `MM_FriendsBtn`    | **Button** | "Friends" with people icon          | Default, Pressed                    | Grid button, shows online count badge                    |
| `MM_InboxBtn`      | **Button** | "Inbox" with mail icon              | Default, Pressed                    | Shows notification count badge (red circle, max "99+")   |
| `MM_CoinDisplay`   | **Text**   | Currency: coin count                | Default                             | Format: comma-separated, icon 20x20, tap opens shop      |
| `MM_GemDisplay`    | **Text**   | Currency: gem count                 | Default                             | Format: comma-separated, icon 20x20, tap opens shop      |
| `MM_TabHome`       | **Tab**    | Home tab (selected)                 | Selected                            | Icon + underline when selected, 44pt height              |
| `MM_TabBattle`     | **Tab**    | Battle tab                          | Default, Selected                   | Icon + text, 44pt height                                 |
| `MM_TabShop`       | **Tab**    | Shop tab                            | Default, Selected                   | Icon + text, 44pt height                                 |
| `MM_TabSocial`     | **Tab**    | Social tab                          | Default, Selected                   | Icon + text, 44pt height                                 |
| `MM_BackgroundImg` | **Image**  | Full-screen background image        | Default                             | Aspect fill, blur layer behind UI, z-order: back         |

### Section 5B: Interactive Element Details

#### `MM_PlayButton` — **Button**

- **States:**
  - Default: Blue glow effect
  - Pressed: Scale 0.95
  - Disabled: Grey, text changes to "Maintenance"
  - Loading: Spinner animation
- **Touch Target:** Full width x 56 pt
- **Animation:** Scale to 0.95 on press (0.1s EaseOut), glow pulse loop 2s

#### `MM_SettingsBtn` — **Button**

- **States:**
  - Default: Standard appearance
  - Pressed: Rotate 90deg
- **Touch Target:** 48x48 pt
- **Animation:** Gear icon rotates 90deg on tap (0.2s)

#### `MM_PromoCarousel` — **Scroll**

- **States:**
  - Default: Auto-rotate
  - User Scrolling: Manual scroll active
- **Touch Target:** Full width x 180 pt
- **Animation:** Auto-rotate every 5s (0.4s slide), dot indicator fades

#### `MM_DailyRewardBtn` — **Button**

- **States:**
  - Default: Standard appearance
  - Available: Glow badge
  - Claimed: Dimmed
- **Touch Target:** 140x80 pt
- **Animation:** Bounce badge when available (loop 3s), scale 0.95 on press

#### `MM_InboxBtn` — **Button**

- **States:**
  - Default: No badge
  - Has Unread: Red badge
  - Pressed: Standard press state
- **Touch Target:** Full width x 48 pt
- **Animation:** Badge pulse on new messages

#### `MM_TabBar` — **Tab**

- **States:**
  - Unselected: Grey icon
  - Selected: Blue + Underline
- **Touch Target:** 25% width x 56 pt per tab
- **Animation:** Underline slides to selected tab (0.2s EaseInOut)

### Section 4: States & Visual Behavior

#### Loading State

- **Trigger:** Screen opens, data fetching
- **Visual:** Skeleton placeholders for avatar, name, currency. Carousel shows shimmer.
- **Elements affected:** `MM_AvatarImage`, `MM_PlayerName`, `MM_CoinDisplay`, `MM_GemDisplay`, `MM_PromoCarousel`

#### Play Button — Disabled (Maintenance)

- **Trigger:** Server returns maintenance flag
- **Visual:** Button turns grey, text changes to "Maintenance", glow effect stops.
- **Elements affected:** `MM_PlayButton`

#### Daily Reward Available

- **Trigger:** `daily_reward_available == true`
- **Visual:** Pulsing glow badge on Daily Rewards button, attention-grabbing shine.
- **Elements affected:** `MM_DailyRewardBtn`

### Section 6: Interactions & Actions

#### 1. Tap Play Button

- **Trigger:** Tap `MM_PlayButton`
- **Result:** Navigate to Battle Select screen
- **Conditions:** Button not in disabled/loading state
- **Error:** If server unreachable, show "Connection Error" toast, button stays

#### 2. Tap Settings

- **Trigger:** Tap `MM_SettingsBtn`
- **Result:** Open Settings modal overlay
- **Conditions:** None
- **Error:** N/A

#### 3. Swipe Promo Carousel

- **Trigger:** Horizontal swipe on `MM_PromoCarousel`
- **Result:** Scroll to next/prev banner, update dot indicator
- **Conditions:** Pauses auto-rotate for 10s after user swipe
- **Error:** If no banners loaded, show default placeholder banner

#### 4. Tap Tab Bar Item

- **Trigger:** Tap any tab in `MM_TabBar`
- **Result:** Switch to corresponding section (Battle/Shop/Social)
- **Conditions:** Currently on Home tab
- **Error:** N/A

#### 5. Tap Inbox

- **Trigger:** Tap `MM_InboxBtn`
- **Result:** Navigate to Inbox screen, clear badge count
- **Conditions:** None
- **Error:** N/A

#### 6. Tap Daily Reward

- **Trigger:** Tap `MM_DailyRewardBtn` when available
- **Result:** Open Daily Reward claim popup
- **Conditions:** `daily_reward_available == true`
- **Error:** If already claimed, show "Come Back Tomorrow" toast

### Section 7: Data Requirements

| Data Field               | Source | Type               | Update Strategy                   | Fallback              |
| ------------------------ | ------ | ------------------ | --------------------------------- | --------------------- |
| `player_name`            | Server | string             | On screen load                    | "Player"              |
| `player_level`           | Server | int                | On screen load                    | 1                     |
| `currency_coins`         | Server | int                | Real-time (event-driven)          | 0                     |
| `currency_gems`          | Server | int                | On screen load                    | 0                     |
| `promo_banners`          | CDN    | List\<BannerData\> | Cached 1hr, refresh on foreground | Single default banner |
| `unread_inbox_count`     | Server | int                | Polled every 30s                  | 0                     |
| `daily_reward_available` | Server | bool               | On screen load, on foreground     | false                 |

### Screen Flow Logic

```
    [App Launch / Return]
            |
            v
      Load Player Data -------+
            |                 |
       +----+----+         Timeout
       |         |            |
    Success   Error           v
       |         |        Show Cached
       v         v        (if available)
    Populate   Retry
    All UI     Dialog
       |         |
       v         |
    LOADED       v
    (Idle)    [Retry or Quit]
       |
       v
    User Interacts
       |
    +--+--+--+--+--+
    |  |  |  |  |  |
    v  v  v  v  v  v
  Play Set Inbox Tab Carousel DailyReward
    |   |   |   |     |         |
    v   v   v   v     v         v
  Battle Settings Inbox Section Swipe   Reward
  Select  Modal  Screen Switch  Anim    Popup
```

### Section 8: Rules & Constraints

- **R-MM-001** 🔴 HIGH: Play button must always be visible without scrolling on any supported device. It is the primary CTA and must never be pushed below the fold.
- **R-MM-002** 🔴 HIGH: Currency displays must update in real-time when coins/gems change (purchase, reward claim). Use event-driven updates, not polling.
- **R-MM-003** 🟡 MEDIUM: Promo carousel must gracefully handle 0 banners (show default), 1 banner (no dots, no auto-scroll), or up to 8 banners.
- **R-MM-004** 🟡 MEDIUM: Inbox badge count must cap at "99+" for values over 99. Badge must be red circle with white text.
- **R-MM-005** 🟢 LOW: Tab bar icons must use outlined style when unselected and filled style when selected, matching platform conventions.

### Section 9: Accessibility & Localization

**Touch Targets:**
- 44x44 pt minimum for all interactive elements

**Text Scaling:**
- Player name, currency, and button labels support up to 1.5x dynamic text

**Localization:**
- Keys: `main_menu.play`, `main_menu.daily_rewards`, `main_menu.shop`, `main_menu.events`, `main_menu.friends`, `main_menu.inbox`
- RTL: mirror layout, carousel swipe direction inverts

**Safe Area:**
- Content inset from all edges using SafeArea rect
- Top bar below notch
- Tab bar above home indicator

### Section 10: Responsive Layout

- **Canvas Scaler:** Scale With Screen Size, reference 1080x1920, Match Width or Height (0.5)
- **Orientation:** Portrait only
- **Aspect Ratios:** 9:16, 9:19.5, 3:4 (iPad)
- **Notch/Cutout:** SafeArea component on root container, inset top/bottom

#### Aspect Ratio Breakdown

**9:16 (Standard):**
Base layout, all elements visible. Carousel height: 180pt. Button grid: single column.

**9:19.5 (Tall phones):**
Extra vertical space absorbed by content area. Carousel height: 180pt (same). More spacing between button rows.

**3:4 (iPad):**
Wider layout, 2-column button grid. Carousel height: 240pt. See Example D for full iPad adaptation.

### Section 12: Canvas Hierarchy

```
Canvas (Screen Space - Overlay)
+-- CanvasScaler (Scale With Screen Size, ref: 1080x1920, match: 0.5)
+-- SafeArea (stretch all edges)
    +-- TopBar (top-anchored, height: 80)
    |   +-- AvatarImage (left-anchored, 120x120)
    |   +-- PlayerInfoGroup (left-anchored, offset: 130px)
    |   |   +-- PlayerName (TextMeshPro)
    |   |   +-- LevelBadge (TextMeshPro)
    |   +-- CurrencyGroup (right-anchored)
    |       +-- CoinDisplay (HorizontalLayout)
    |       +-- GemDisplay (HorizontalLayout)
    +-- SettingsBtn (top-right, 48x48)
    +-- ContentArea (stretch, padding: top 90, bottom 120)
    |   +-- PromoCarousel (top-anchored, height: 180)
    |   +-- ButtonGrid (GridLayout, 2 cols)
    |   |   +-- DailyRewardBtn
    |   |   +-- ShopBtn
    |   |   +-- EventsBtn
    |   |   +-- FriendsBtn
    |   +-- PlayButton (bottom, stretch-x, height: 56)
    |   +-- InboxBtn (below PlayButton)
    +-- BottomTabBar (bottom-anchored, height: 56)
        +-- TabHome (25% width)
        +-- TabBattle (25% width)
        +-- TabShop (25% width)
        +-- TabSocial (25% width)
```

### Section 11: Animation & Transitions

#### Screen Entry

- **Animation:** Fade in from black (post-loading), elements stagger in from bottom
- **Duration:** 0.5s total, 0.05s stagger per element
- **Easing:** EaseOutQuad

#### Screen Exit

- **Animation:** Slide out to left (when navigating forward), fade out (when opening modal)
- **Duration:** 0.3s
- **Easing:** EaseInQuad

#### Play Button Glow

- **Animation:** Pulsing blue glow, scale 1.0 to 1.02, opacity 0.6 to 1.0
- **Duration:** 2.0s loop
- **Easing:** EaseInOutSine

### Section 14: Notes & Open Questions

> ⚠️ **Q:** Should the promo carousel support deep-linking to in-app screens or only external URLs?

> ⚠️ **Q:** Confirm maximum number of simultaneous notification badges across all buttons (perf concern with animating many badges).

---

## Example B: Settings Dialog (Modal, Responsive)

### Section 1: Screen Overview

| Field         | Value                                              |
| ------------- | -------------------------------------------------- |
| Screen Name   | Settings Dialog                                    |
| Screen ID     | SCR-SETTINGS-001                                   |
| Priority      | P1 - Core                                          |
| Status        | Draft                                              |
| Device        | Mobile + Tablet                                    |
| Aspect Ratio  | 9:16, 9:19.5, 3:4                                 |

**Purpose:** Full-featured settings modal allowing players to configure audio, graphics, notifications, and account options. Presented as an overlay on any parent screen.

**Entry Points:**
- Settings gear button on Main Menu (`MM_SettingsBtn`)
- Pause menu in gameplay
- Profile screen

**Exit Points:**
- Close button (X)
- Save + Close
- Cancel
- System back gesture

**Screen Purpose:** The Settings Dialog provides centralized configuration for all player-facing options. It is a modal overlay that dims the parent screen and prevents interaction with underlying elements until dismissed. Changes are staged locally and only persisted on explicit Save.

### Section 5: UI Element Inventory

| Element ID               | Type             | Description                                       | Required | Notes                                                      |
| ------------------------ | ---------------- | ------------------------------------------------- | -------- | ---------------------------------------------------------- |
| `SET_Backdrop`           | Image            | Semi-transparent overlay dimming parent screen     | Yes      | Black, 60% opacity. Tap dismisses if no unsaved changes    |
| `SET_Panel`              | Panel            | Modal container with rounded corners               | Yes      | Mobile: full-screen. Tablet: centered, 70% width           |
| `SET_CloseBtn`           | Button           | X button top-right corner                          | Yes      | Triggers unsaved changes check                             |
| `SET_Title`              | TextMeshPro      | "Settings" header text                             | Yes      | 24pt bold, centered                                        |
| `SET_TabBar`             | HorizontalLayout | Tab navigation: General, Audio, Graphics, Account  | Yes      | Underline indicator on active tab                          |
| `SET_SoundToggle`        | Toggle           | Master sound on/off                                | Yes      | Audio tab. Disables SFX + Music sliders when off           |
| `SET_MusicToggle`        | Toggle           | Background music on/off                            | Yes      | Audio tab                                                  |
| `SET_SFXSlider`          | Slider           | SFX volume 0-100%                                  | Yes      | Audio tab. Plays sample SFX on release                     |
| `SET_MusicSlider`        | Slider           | Music volume 0-100%                                | Yes      | Audio tab. Live preview while dragging                     |
| `SET_GraphicsDropdown`   | Dropdown         | Quality: Low, Medium, High, Ultra                  | Yes      | Graphics tab. Shows warning on Ultra for low-end devices   |
| `SET_FPSToggle`          | Toggle           | FPS cap: 30 / 60                                   | Yes      | Graphics tab. Label updates to show current value          |
| `SET_NotifToggle`        | Toggle           | Push notifications on/off                          | Yes      | General tab. Triggers OS permission dialog if first enable |
| `SET_HapticsToggle`      | Toggle           | Haptic feedback on/off                             | Yes      | General tab. iOS only, hidden on Android                   |
| `SET_LangDropdown`       | Dropdown         | Language selection                                 | Yes      | General tab. Requires restart confirmation                 |
| `SET_LinkAccountBtn`     | Button           | Link to social account                             | Yes      | Account tab. Shows linked status if already linked         |
| `SET_LogoutBtn`          | Button           | Log out of current account                         | Yes      | Account tab. Requires confirmation dialog                  |
| `SET_DeleteAccountBtn`   | Button           | Delete account permanently                         | Yes      | Account tab. Red text, double confirmation required        |
| `SET_VersionText`        | TextMeshPro      | App version string                                 | Yes      | Bottom of Account tab, grey, non-interactive               |
| `SET_SaveBtn`            | Button           | Save and close                                     | Yes      | Bottom action bar. Enabled only if changes exist           |
| `SET_CancelBtn`          | Button           | Discard changes and close                          | Yes      | Bottom action bar                                          |
| `SET_RestoreDefaultsBtn` | Button           | Reset all settings to defaults                     | No       | Bottom action bar. Requires confirmation                   |
| `SET_UnsavedDialog`      | Panel            | Confirmation dialog for unsaved changes            | Yes      | Nested modal: "Save Changes?" with Save/Discard/Cancel     |

### Section 3: Visual Layout / Wireframe

```
[Wireframe: Settings Dialog - Full-screen modal on mobile]
+-----------------------------------------------+
| [X]           SETTINGS                          |
| ----------------------------------------------- |
| [General] [Audio] [Graphics] [Account]          |
| =============================================== |
|                                                 |
| Notifications        [====== ON]                |
| Push Alerts           [====== ON]               |
| Haptic Feedback       [===== OFF]               |
|                                                 |
| Language              [English  v]              |
|                                                 |
|                                                 |
|                                                 |
|                                                 |
| ----------------------------------------------- |
| [Restore Defaults]   [Cancel]   [Save]          |
+-----------------------------------------------+
```

### Section 5B: Interactive Element Details

#### `SET_TabBar` — **Tab**

- **States:**
  - Unselected: Grey text
  - Selected: White text + Underline
- **Touch Target:** 25% width x 48pt per tab
- **Animation:** Underline slides to active tab (0.2s EaseInOut)

#### `SET_SoundToggle` — **Toggle**

- **States:**
  - ON: Green track, white thumb
  - OFF: Grey track, grey thumb
- **Touch Target:** Full row width x 48pt
- **Animation:** Thumb slides with spring physics (0.15s)

#### `SET_SFXSlider` — **Slider**

- **States:**
  - Active: Blue fill + white thumb
  - Disabled: Grey, non-interactive
- **Touch Target:** Full row width x 48pt, thumb 28x28pt
- **Animation:** Thumb scales 1.2x while dragging, percentage label follows thumb

#### `SET_GraphicsDropdown` — **Dropdown**

- **States:**
  - Collapsed: Shows current value
  - Expanded: Shows all options
- **Touch Target:** Full row width x 48pt
- **Animation:** Dropdown expands with slide-down (0.2s), selected item check mark

#### `SET_DeleteAccountBtn` — **Button**

- **States:**
  - Default: Red text, no fill
  - Pressed: Red fill, white text
- **Touch Target:** Full width x 48pt
- **Animation:** None (destructive action, no playful animation)

#### `SET_SaveBtn` — **Button**

- **States:**
  - Enabled: Blue fill, white text
  - Disabled: Grey, no changes
  - Pressed: Darker blue
- **Touch Target:** 120x48pt minimum
- **Animation:** Scale 0.95 on press, subtle glow when enabled

### Section 4: States & Visual Behavior

#### Modal Lifecycle

```
    [Modal Lifecycle]

    Closed ----(open trigger)----> Opening
                                      |
                                 Fade backdrop 0->60%
                                 Scale panel 0.9->1.0
                                 Duration: 0.3s
                                      |
                                      v
                                    Open
                                      |
                             +--------+--------+
                             |                 |
                          Has Changes     No Changes
                             |                 |
                        Save/Discard       Close (X)
                             |                 |
                             v                 v
                          Closing <-----------+
                             |
                        Fade backdrop 60->0%
                        Scale panel 1.0->0.95
                        Duration: 0.25s
                             |
                             v
                           Closed
```

### Section 6: Interactions & Actions

#### 1. Switch Tab

- **Trigger:** Tap any tab in `SET_TabBar`
- **Result:** Content area crossfades to selected tab's options (0.2s)
- **Conditions:** None
- **Error:** N/A

#### 2. Toggle Sound Off

- **Trigger:** Tap `SET_SoundToggle` to OFF
- **Result:** SFX and Music sliders become disabled (greyed out). All game audio mutes immediately (preview).
- **Conditions:** Sound is currently ON
- **Error:** N/A

#### 3. Adjust SFX Volume

- **Trigger:** Drag `SET_SFXSlider` thumb
- **Result:** Percentage label updates in real-time. On release, plays a sample SFX at new volume.
- **Conditions:** Sound toggle is ON
- **Error:** N/A

#### 4. Change Graphics Quality

- **Trigger:** Select option in `SET_GraphicsDropdown`
- **Result:** Dropdown closes, shows selected value. If "Ultra" on low-end device, show warning toast.
- **Conditions:** None
- **Error:** Device capability check fails: show "Not recommended for your device" warning

#### 5. Change Language

- **Trigger:** Select new language in `SET_LangDropdown`
- **Result:** Show confirmation: "Changing language requires restart. Continue?" with OK/Cancel.
- **Conditions:** Selected language differs from current
- **Error:** N/A

#### 6. Tap Save

- **Trigger:** Tap `SET_SaveBtn`
- **Result:** Persist all changed settings to local storage + server. Show brief spinner, then close modal.
- **Conditions:** At least one setting has been changed
- **Error:** Server save fails: save locally, show "Settings saved locally" toast, queue server sync

#### 7. Tap Close with Unsaved Changes

- **Trigger:** Tap `SET_CloseBtn` or `SET_CancelBtn` when changes exist
- **Result:** Show `SET_UnsavedDialog`: "You have unsaved changes" with Save / Discard / Cancel buttons.
- **Conditions:** Dirty flag is true
- **Error:** N/A

#### 8. Delete Account

- **Trigger:** Tap `SET_DeleteAccountBtn`
- **Result:** First confirmation: "Are you sure?" Second confirmation: "Type DELETE to confirm". On confirm, server call to delete, then redirect to login.
- **Conditions:** User is logged in
- **Error:** Server error: show "Could not delete account. Contact support." dialog

### Section 7: Data Requirements

| Data Field              | Source         | Type           | Update Strategy | Fallback        |
| ----------------------- | -------------- | -------------- | --------------- | --------------- |
| `sound_enabled`         | Local          | bool           | On modal open   | true            |
| `music_enabled`         | Local          | bool           | On modal open   | true            |
| `sfx_volume`            | Local          | float (0-1)    | On modal open   | 0.8             |
| `music_volume`          | Local          | float (0-1)    | On modal open   | 0.6             |
| `graphics_quality`      | Local          | enum           | On modal open   | Medium          |
| `fps_cap`               | Local          | int (30/60)    | On modal open   | 30              |
| `notifications_enabled` | Local + Server | bool           | On modal open   | true            |
| `haptics_enabled`       | Local          | bool           | On modal open   | true (iOS only) |
| `language`              | Local + Server | string         | On modal open   | Device locale   |
| `linked_accounts`       | Server         | List\<string\> | On modal open   | [] (empty)      |
| `app_version`           | Local          | string         | Static          | "1.0.0"         |

### Screen Flow Logic

```
    [Open Settings]
            |
            v
      Load Current Settings
      from Local Storage
            |
            v
      Display General Tab (default)
            |
      +-----+-----+-----+-----+
      |     |     |     |     |
      v     v     v     v     v
   General Audio Graphics Account [Tab Switch]
      |     |     |     |
      v     v     v     v
   Modify Values (staged, not saved)
      |     dirty_flag = true
      v     SET_SaveBtn enabled
      |
   +--+--+
   |     |
   v     v
  Save  Close/Cancel
   |     |
   |     +--> dirty? --> UnsavedDialog
   |                      |     |     |
   |                    Save  Discard Cancel
   |                      |     |     |
   v                      v     v     |
  Persist ---------> Close Modal <----+
  (Local + Server)
```

### Section 8: Rules & Constraints

- **R-SET-001** 🔴 HIGH: Settings changes must be staged locally and only persisted on explicit Save. Closing without saving must discard all changes (with confirmation if dirty).
- **R-SET-002** 🔴 HIGH: Audio toggles and sliders must provide immediate preview (live audio change) but revert if user cancels without saving.
- **R-SET-003** 🔴 HIGH: Delete Account must require double confirmation (dialog + type "DELETE") to prevent accidental data loss.
- **R-SET-004** 🟡 MEDIUM: Modal must block interaction with parent screen. Backdrop tap only dismisses if no unsaved changes.
- **R-SET-005** 🟡 MEDIUM: Haptic feedback toggle must only appear on iOS devices. On Android, the row must be hidden entirely (not disabled).
- **R-SET-006** 🟢 LOW: Language change requires app restart. Show confirmation dialog before staging the change.

### Section 9: Accessibility & Localization

**Touch Targets:**
- All toggles, sliders, buttons: 48pt row height minimum
- Slider thumb: 28pt diameter

**Text Scaling:**
- Labels and values support 1.5x dynamic text
- Tab labels truncate with ellipsis at 2x

**Localization:**
- Keys: `settings.title`, `settings.tab.general`, `settings.tab.audio`, `settings.tab.graphics`, `settings.tab.account`, `settings.save`, `settings.cancel`, `settings.restore_defaults`
- RTL: tabs reorder right-to-left, slider direction inverts

**Screen Reader:**
- Toggles announce "ON/OFF" state
- Sliders announce percentage
- Destructive buttons announce "caution" role

### Section 10: Responsive Layout

**Mobile (9:16, 9:19.5):**
Full-screen modal. Tab bar scrollable if needed. Content area scrollable.

**Tablet (3:4):**
Centered panel at 70% screen width, 80% height. Rounded corners (16px). Drop shadow on panel.

### Section 12: Canvas Hierarchy

```
Canvas (Screen Space - Overlay, sorting order: 100)
+-- CanvasScaler (Scale With Screen Size, ref: 1080x1920, match: 0.5)
+-- SET_Backdrop (stretch all, Image color: 0,0,0,0.6)
+-- SET_Panel (centered, mobile: stretch all, tablet: 70%x80%)
    +-- Header (top-anchored, height: 56)
    |   +-- SET_Title (center, TextMeshPro "Settings")
    |   +-- SET_CloseBtn (right-anchored, 44x44)
    +-- SET_TabBar (below header, height: 48)
    |   +-- TabGeneral (25% width)
    |   +-- TabAudio (25% width)
    |   +-- TabGraphics (25% width)
    |   +-- TabAccount (25% width)
    |   +-- UnderlineIndicator (bottom-anchored, height: 3)
    +-- ContentArea (stretch, ScrollRect)
    |   +-- GeneralContent (VerticalLayout, spacing: 8)
    |   |   +-- NotifToggleRow
    |   |   +-- PushToggleRow
    |   |   +-- HapticsToggleRow (iOS only)
    |   |   +-- LangDropdownRow
    |   +-- AudioContent (VerticalLayout, spacing: 8)
    |   |   +-- SoundToggleRow
    |   |   +-- MusicToggleRow
    |   |   +-- SFXSliderRow
    |   |   +-- MusicSliderRow
    |   +-- GraphicsContent (VerticalLayout, spacing: 8)
    |   |   +-- QualityDropdownRow
    |   |   +-- FPSToggleRow
    |   +-- AccountContent (VerticalLayout, spacing: 8)
    |       +-- LinkAccountBtn
    |       +-- LogoutBtn
    |       +-- DeleteAccountBtn
    |       +-- VersionText
    +-- ActionBar (bottom-anchored, height: 56)
        +-- SET_RestoreDefaultsBtn (left-anchored)
        +-- SET_CancelBtn (right, offset: -130)
        +-- SET_SaveBtn (right-anchored)
```

### Section 11: Animation & Transitions

#### Modal Open

- **Animation:** Backdrop fades in (0 to 60% opacity). Panel scales from 0.9 to 1.0 with fade in.
- **Duration:** 0.3s
- **Easing:** EaseOutBack (slight overshoot on panel scale)

#### Modal Close

- **Animation:** Panel scales from 1.0 to 0.95 with fade out. Backdrop fades to 0.
- **Duration:** 0.25s
- **Easing:** EaseInQuad

#### Tab Switch

- **Animation:** Underline slides horizontally to new tab. Old content fades out, new content fades in.
- **Duration:** 0.2s
- **Easing:** EaseInOutQuad

#### Toggle Switch

- **Animation:** Thumb slides with spring damping. Track color crossfades.
- **Duration:** 0.15s
- **Easing:** Spring (damping: 0.7)

### Section 14: Notes & Open Questions

> ⚠️ **Q:** Should audio preview (while adjusting sliders) be immediate or debounced?

> ⚠️ **Q:** For language change requiring restart, should we force-restart or let the user restart manually?

> ℹ️ **Note:** Graphics quality "Ultra" should show estimated battery impact on mobile devices.

---

## Example C: Game HUD (Landscape 16:9)

### Section 1: Screen Overview

| Field         | Value                                              |
| ------------- | -------------------------------------------------- |
| Screen Name   | Game HUD                                           |
| Screen ID     | SCR-HUD-001                                        |
| Priority      | P0 - Critical                                      |
| Status        | Draft                                              |
| Device        | Mobile (Landscape)                                 |
| Aspect Ratio  | 16:9, 19.5:9                                       |

**Purpose:** Real-time battle HUD displaying player/enemy health, abilities, timer, score, and controls during active gameplay. All elements must be visible without obscuring the action area.

**Entry Points:**
- Battle loading screen completes
- Pre-battle countdown ends

**Exit Points:**
- Victory/Defeat result screen
- Pause menu quit
- Disconnect timeout

**Screen Purpose:** The Game HUD is the primary interface during active battle. It overlays the 3D gameplay scene and must convey critical real-time information (health, abilities, timer) without distracting from the action. Performance is paramount — no layout recalculations or GC allocations during battle. All data is client-driven with no server calls during combat.

**Landscape Safe Area:** Content must be inset from left/right edges on notched devices (iPhone X+). Left safe area inset: 44pt. Right safe area inset: 44pt. Top/bottom: minimal (landscape orientation).

### Section 5: UI Element Inventory

| Element ID           | Type             | Description                                             | Required | Notes                                                                        |
| -------------------- | ---------------- | ------------------------------------------------------- | -------- | ---------------------------------------------------------------------------- |
| `HUD_HPBar`          | Slider (custom)  | Player health bar with gradient fill (green>yellow>red)  | Yes      | Top-left. Gradient shifts based on %. Shows numeric value.                   |
| `HUD_MPBar`          | Slider (custom)  | Player MP/energy bar (blue fill)                         | Yes      | Below HP bar. Depletes on ability use, regenerates over time.                |
| `HUD_Portrait`       | Image            | Player character portrait with level badge               | Yes      | Top-left corner, circular frame 64x64pt                                      |
| `HUD_EnemyHP`        | Slider (custom)  | Enemy health bar (red fill)                              | Yes      | Top-center. Shows boss name above bar. Multiple bars for multi-phase bosses. |
| `HUD_Timer`          | TextMeshPro      | Battle timer / countdown                                 | Yes      | Top-center, below enemy HP. Turns red below 30s. Pulses below 10s.          |
| `HUD_Score`          | TextMeshPro      | Current score / combo multiplier                         | No       | Top-right. Animates on score change (pop + settle).                          |
| `HUD_PauseBtn`       | Button           | Pause button (hamburger icon)                            | Yes      | Top-right corner, 44x44pt                                                    |
| `HUD_Ability1`       | Button           | Ability slot 1 (circular)                                | Yes      | Bottom-right. Shows cooldown radial fill. 72x72pt.                           |
| `HUD_Ability2`       | Button           | Ability slot 2 (circular)                                | Yes      | Bottom-right. Same pattern as Ability1.                                      |
| `HUD_Ability3`       | Button           | Ability slot 3 (circular)                                | Yes      | Bottom-right. Same pattern as Ability1.                                      |
| `HUD_Ability4`       | Button           | Ability slot 4 (circular)                                | Yes      | Bottom-right. Same pattern as Ability1.                                      |
| `HUD_UltimateBtn`    | Button           | Ultimate ability with charge % ring                      | Yes      | Bottom-right, larger (88x88pt). Glows when fully charged. Shows charge %.    |
| `HUD_MiniMap`        | RawImage         | Mini-map showing arena overview                          | No       | Bottom-left, 120x120pt. Rotates with camera. Shows player + enemy dots.      |
| `HUD_ComboCounter`   | TextMeshPro      | Combo hit counter                                        | No       | Center-right. Large text, fades after 2s of no hits. "x5", "x10" etc.       |
| `HUD_BuffIcons`      | HorizontalLayout | Active buff/debuff icon strip                            | No       | Below HP bar. Small icons 24x24pt with duration timer overlay.               |
| `HUD_AutoPlayToggle` | Toggle           | Auto-play on/off                                         | No       | Top-right area. Greyed icon when off, blue when on.                          |
| `HUD_SpeedToggle`    | Button           | Speed toggle: 1x / 2x / 3x                              | No       | Next to auto-play. Cycles through speeds on tap.                             |

### Section 3: Visual Layout / Wireframe

```
[Wireframe: Game HUD - Landscape 16:9]
+------------------------------------------------------------------+
| [Portrait] [====HP====] [==Enemy HP==] [Timer]    [Score] [Pause]|
|            [====MP====] [Boss Name   ]            [Auto] [Speed] |
|            [buff icons]                                          |
|                                                                  |
|                                                                  |
|                         (3D Battle Scene)              x12       |
|                                                      (combo)    |
|                                                                  |
|                                                         [Ult]   |
| +--------+                                        [A3]  [  ]    |
| |MiniMap |                                    [A1]  [A4]        |
| +--------+                                      [A2]            |
+------------------------------------------------------------------+
```

### Section 5B: Interactive Element Details

#### `HUD_HPBar` — **Progress**

- **States:**
  - Full: Green gradient
  - Mid (<50%): Yellow gradient
  - Critical (<20%): Red gradient, pulse
- **Touch Target:** Non-interactive (display only)
- **Animation:** Fill animates on damage (0.3s EaseOut). Damage flash (white overlay 0.1s). Critical pulse (0.5s loop).

#### `HUD_Ability1-4` — **Button**

- **States:**
  - Ready: Full color, interactable
  - On Cooldown: Grey, radial fill overlay, timer text
  - Pressed: Scale 0.9, darker
  - Not Enough MP: Desaturated, MP cost shown in red
- **Touch Target:** 72x72pt circle, 8pt spacing between buttons
- **Animation:** Cooldown radial wipe (clockwise). Ready flash (glow pulse once). Press scale 0.9 (0.1s).

#### `HUD_UltimateBtn` — **Button**

- **States:**
  - Charging: Grey, % text overlay
  - Fully Charged: Golden glow, pulsing ring
  - Activated: White flash, cinematic trigger
- **Touch Target:** 88x88pt circle
- **Animation:** Charge ring fills gradually. At 100%: golden burst + persistent glow loop. Activation: screen-wide flash (0.2s).

#### `HUD_Timer` — **Timer**

- **States:**
  - Normal (>30s): White text
  - Warning (<30s): Yellow text
  - Critical (<10s): Red text, scale pulse
- **Touch Target:** Non-interactive (display only)
- **Animation:** Scale pulse at critical (1.0 to 1.1, 0.5s loop). Color transition is instant.

#### `HUD_ComboCounter` — **Text**

- **States:**
  - Active: Large white text, visible
  - Fading: Opacity decreasing after 2s idle
- **Touch Target:** Non-interactive (display only)
- **Animation:** Each hit: scale pop 1.0->1.3->1.0 (0.15s). Milestone combos (x5, x10, x25): color flash + particle burst.

#### `HUD_SpeedToggle` — **Button**

- **States:**
  - 1x: Normal speed
  - 2x: Double speed, yellow text
  - 3x: Triple speed, orange text
- **Touch Target:** 44x44pt
- **Animation:** Text rotates on cycle (0.15s flip). Speed lines appear at 2x/3x.

### Section 4: States & Visual Behavior

#### Battle States

```
    [Battle States]

    Pre-Battle -----> Battle Active -----> Result
        |                  |                  |
    Countdown          Active HUD         Victory/Defeat
    3, 2, 1            All elements        Score tally
    HUD hidden         visible             HUD fades out
        |                  |
        |              +---+---+
        |              |       |
        |           Paused  Active
        |              |       |
        |           Dim HUD    |
        |           Show menu  |
        |              |       |
        |           Resume ----+
        |              |
        |           Quit --> Confirm --> Exit
        |
        v
    Battle Active
```

### Section 6: Interactions & Actions

#### 1. Tap Ability Button

- **Trigger:** Tap `HUD_Ability1/2/3/4`
- **Result:** Activate ability, start cooldown timer, deduct MP cost
- **Conditions:** Ability not on cooldown, sufficient MP
- **Error:** On cooldown: button shakes (0.2s). Insufficient MP: flash MP bar red (0.3s).

#### 2. Tap Ultimate

- **Trigger:** Tap `HUD_UltimateBtn` when fully charged
- **Result:** Trigger ultimate cinematic, apply ultimate effect, reset charge to 0%
- **Conditions:** Charge at 100%
- **Error:** Not charged: show charge % tooltip briefly

#### 3. Tap Pause

- **Trigger:** Tap `HUD_PauseBtn`
- **Result:** Pause game time, dim HUD to 40% opacity, show pause menu overlay
- **Conditions:** Battle is active (not in result screen)
- **Error:** N/A

#### 4. Toggle Auto-Play

- **Trigger:** Tap `HUD_AutoPlayToggle`
- **Result:** Enable/disable AI auto-play. When on, ability buttons show auto-fire indicator.
- **Conditions:** Feature unlocked (player level 10+)
- **Error:** Not unlocked: show "Unlock at Level 10" toast

#### 5. Cycle Speed

- **Trigger:** Tap `HUD_SpeedToggle`
- **Result:** Cycle 1x -> 2x -> 3x -> 1x. Game time scale changes immediately.
- **Conditions:** Auto-play is enabled
- **Error:** Auto-play off: button is disabled (greyed)

### Section 7: Data Requirements

| Data Field             | Source              | Type             | Update Strategy    | Fallback       |
| ---------------------- | ------------------- | ---------------- | ------------------ | -------------- |
| `player_hp`            | Client (battle sim) | float            | Per-frame          | N/A (critical) |
| `player_mp`            | Client (battle sim) | float            | Per-frame          | N/A (critical) |
| `enemy_hp`             | Client (battle sim) | float            | Per-frame          | N/A (critical) |
| `ability_cooldowns[4]` | Client (battle sim) | float[4]         | Per-frame          | 0 (ready)      |
| `ultimate_charge`      | Client (battle sim) | float (0-100)    | On damage dealt    | 0              |
| `battle_timer`         | Client              | float (seconds)  | Per-frame          | N/A (critical) |
| `combo_count`          | Client (battle sim) | int              | On hit event       | 0              |
| `score`                | Client (battle sim) | int              | On score event     | 0              |
| `active_buffs`         | Client (battle sim) | List\<BuffData\> | On buff add/remove | [] (empty)     |
| `auto_play_enabled`    | Client              | bool             | On toggle          | false          |
| `speed_multiplier`     | Client              | int (1/2/3)      | On toggle          | 1              |

> **Performance Note:** All battle data is client-side. No server calls during active combat. HP/MP/Timer update via cached references (no GetComponent per frame). Use object pooling for buff icons and combo text.

### Screen Flow Logic

```
    [Battle Start]
            |
            v
      Pre-Battle (HUD hidden)
      Countdown: 3... 2... 1... FIGHT!
            |
            v
      Battle Active (HUD visible)
            |
      +-----+-----+-----+
      |     |     |     |
      v     v     v     v
   Player  Ability Timer  Pause
   Takes   Used   Hits 0  Tapped
   Damage    |      |      |
      |      v      v      v
   Update  Start  TIME   Show
   HP Bar  Cool-  UP!    Pause
   + Flash down   (Draw) Menu
      |      |      |      |
      v      v      |      v
   HP=0?  Ready   Result Resume
      |   Flash   Screen  or Quit
      v
   Defeat
   Screen
```

### Section 8: Rules & Constraints

- **R-HUD-001** 🔴 HIGH: HUD must not allocate memory during battle. All text updates via pre-allocated StringBuilders. No string concatenation, no boxing, no LINQ. Target: 0 GC allocs per frame from HUD.
- **R-HUD-002** 🔴 HIGH: HP/MP bars must update visually within the same frame as the damage/heal event. No 1-frame delay. Use LateUpdate for bar fill sync.
- **R-HUD-003** 🔴 HIGH: Ability buttons must have clear visual distinction between "on cooldown", "not enough MP", and "ready". Players must never be confused about why a button is not responding.
- **R-HUD-004** 🟡 MEDIUM: Combo counter must auto-hide after 2 seconds of no new hits. Reset combo to 0 when it hides. Milestone combos (x5, x10, x25, x50, x100) get special visual treatment.
- **R-HUD-005** 🟡 MEDIUM: All HUD elements must respect landscape safe areas on notched devices. No interactive element may be within 44pt of left/right screen edges on iPhone X+ class devices.
- **R-HUD-006** 🟢 LOW: Speed toggle (2x/3x) only available when auto-play is enabled. When auto-play is disabled, speed resets to 1x.

### Section 9: Accessibility & Localization

**Touch Targets:**
- Ability buttons 72pt diameter (exceeds 44pt minimum)
- Pause button 44x44pt
- Speed/Auto toggles 44x44pt

**Color Independence:**
- HP states use color AND shape/animation (pulse for critical)
- Cooldown uses radial fill AND text timer, not color alone

**Localization:**
- Minimal text on HUD. Timer is numeric only. Combo counter uses "x" prefix (universal). Buff icons are visual.
- Only pause menu requires localized strings.

**Safe Area:**
- Left/right insets on notched landscape devices
- All interactive elements within safe bounds

### Section 10: Responsive Layout

- **Canvas Scaler:** Scale With Screen Size, reference 1920x1080, Match Width or Height (0.5)
- **Orientation:** Landscape only (locked)
- **Aspect Ratios:** 16:9 (standard), 19.5:9 (tall phones in landscape = wider), 4:3 (iPad landscape)

#### Aspect Ratio Breakdown

**16:9 (Standard):**
Base layout, all elements positioned. Mini-map 120x120pt bottom-left. Abilities cluster bottom-right.

**19.5:9 (Wide phones):**
Extra horizontal space on sides. Safe area insets push content inward. More room between left/right element groups.

**4:3 (iPad Landscape):**
Less horizontal space, more vertical. Mini-map may overlap action area. Consider auto-hiding mini-map on 4:3.

### Section 12: Canvas Hierarchy

```
Canvas (Screen Space - Overlay)
+-- CanvasScaler (Scale With Screen Size, ref: 1920x1080, match: 0.5)
+-- SafeArea (stretch all edges, landscape insets)
    +-- TopLeftGroup (top-left anchored)
    |   +-- HUD_Portrait (64x64, circular mask)
    |   +-- BarGroup (VerticalLayout, right of portrait)
    |   |   +-- HUD_HPBar (width: 200, height: 16)
    |   |   +-- HUD_MPBar (width: 180, height: 12)
    |   +-- HUD_BuffIcons (HorizontalLayout, below bars)
    +-- TopCenterGroup (top-center anchored)
    |   +-- HUD_EnemyHP (width: 300, height: 16)
    |   +-- EnemyName (TextMeshPro, above bar)
    |   +-- HUD_Timer (below enemy HP)
    +-- TopRightGroup (top-right anchored)
    |   +-- HUD_Score (TextMeshPro)
    |   +-- HUD_PauseBtn (44x44)
    |   +-- HUD_AutoPlayToggle (44x44)
    |   +-- HUD_SpeedToggle (44x44)
    +-- CenterRight (center-right anchored)
    |   +-- HUD_ComboCounter (TextMeshPro, large)
    +-- BottomLeftGroup (bottom-left anchored)
    |   +-- HUD_MiniMap (RawImage, 120x120)
    +-- BottomRightGroup (bottom-right anchored)
        +-- HUD_UltimateBtn (88x88, center of cluster)
        +-- HUD_Ability1 (72x72, positioned around ultimate)
        +-- HUD_Ability2 (72x72)
        +-- HUD_Ability3 (72x72)
        +-- HUD_Ability4 (72x72)
```

### Section 11: Animation & Transitions

#### Battle Start

- **Animation:** HUD elements slide in from edges (top bars from top, abilities from right, mini-map from left)
- **Duration:** 0.4s, staggered by 0.05s per group
- **Easing:** EaseOutBack

#### Damage Taken

- **Animation:** HP bar fill decreases (0.3s EaseOut). White damage flash overlay on bar (0.1s). Screen edge vignette flash red (0.2s, opacity 0.3).
- **Duration:** 0.3s
- **Easing:** EaseOut

#### Ability Cooldown

- **Animation:** Radial fill (clockwise, grey overlay) decreases over cooldown duration. When ready: golden flash pulse (once, 0.3s).
- **Duration:** Matches cooldown time
- **Easing:** Linear (cooldown fill), EaseOutQuad (ready flash)

#### Ultimate Charged

- **Animation:** Golden particle burst around button. Persistent glow ring pulse. Button slightly bobs up/down.
- **Duration:** Burst: 0.5s. Glow loop: 1.5s. Bob loop: 2s.
- **Easing:** EaseInOutSine (bob), Linear (glow pulse)

#### Battle End

- **Animation:** HUD fades out (0.5s). Victory: elements fly upward with confetti. Defeat: elements darken and sink.
- **Duration:** 0.5s
- **Easing:** EaseInQuad

### Section 14: Notes & Open Questions

> ⚠️ **Q:** Should the mini-map be always visible or toggle-able? On smaller devices it may obscure gameplay.

> ⚠️ **Q:** Multi-phase bosses: should enemy HP bar show total HP across all phases, or reset per phase?

> ℹ️ **Performance target:** HUD update must complete within 0.5ms per frame. Profile with Unity Profiler to verify.

---

## Example D: iPad Main Menu (3:4 Adaptation)

### Section 1: Screen Overview

| Field         | Value                                              |
| ------------- | -------------------------------------------------- |
| Screen Name   | iPad Main Menu                                     |
| Screen ID     | SCR-MAINMENU-001-IPAD                              |
| Priority      | P1 - Core                                          |
| Status        | Draft                                              |
| Device        | iPad (Tablet)                                      |
| Aspect Ratio  | 3:4 (Portrait), 4:3 (Landscape)                   |

**Purpose:** iPad-specific adaptation of the Main Menu (Example A). Same functionality and elements, but with layout adjustments to utilize the wider screen real estate of tablets. This document focuses only on differences from the base mobile spec (SCR-MAINMENU-001).

**Base Spec:** SCR-MAINMENU-001 (Example A). All elements, interactions, data requirements, rules, and accessibility from the base spec apply unless explicitly overridden here.

**Screen Purpose:** This is an adaptation spec, not a standalone screen spec. It documents the specific layout and sizing changes needed when the Main Menu renders on iPad (3:4 aspect ratio). The wider viewport allows larger touch targets, 2-column button grids, and more generous spacing. All business logic, data requirements, and interaction behaviors remain identical to the base mobile spec.

### Section 5: UI Element Inventory (Differences Only)

| Element ID         | Mobile (9:16)       | iPad (3:4)                                 | Change Rationale                                     |
| ------------------ | ------------------- | ------------------------------------------ | ---------------------------------------------------- |
| `MM_AvatarImage`   | 120x120 pt          | 160x160 pt                                 | Larger screen allows bigger avatar for visual impact  |
| `MM_PlayButton`    | Width: 280 pt       | Width: 360 pt                              | Wider CTA button fills proportionally                 |
| `MM_PromoCarousel` | Height: 180 pt      | Height: 240 pt                             | More vertical space available, bigger banner images   |
| `MM_TabBar`        | Icon only, H: 56 pt | Icon + Text label, H: 72 pt               | More horizontal space allows text labels under icons  |
| `ButtonGrid`       | Single column        | 2 columns, 16pt gap                        | Wider viewport accommodates side-by-side buttons      |
| `MM_DailyRewardBtn`| Full width x 80 pt  | 50% width x 88 pt                          | Grid item in 2-column layout                          |
| `MM_ShopBtn`       | Full width x 80 pt  | 50% width x 88 pt                          | Grid item in 2-column layout                          |
| `MM_EventsBtn`     | Full width x 80 pt  | 50% width x 88 pt                          | Grid item in 2-column layout                          |
| `MM_FriendsBtn`    | Full width x 80 pt  | 50% width x 88 pt                          | Grid item in 2-column layout                          |
| `TopBar`           | Height: 80 pt       | Height: 96 pt                              | More breathing room for header elements               |
| `CurrencyGroup`    | Compact layout       | Spacious layout, 16pt gap between coin/gem | Utilize horizontal space                              |
| `MM_SettingsBtn`   | 44x44 pt             | 48x48 pt                                   | Slightly larger for tablet ergonomics                 |

### Section 3: Visual Layout / Wireframe

```
[Wireframe: iPad Main Menu - 3:4 Portrait]
+--------------------------------------------------+
| [Avatar 160px]  Player Name    [Coins]  [Gems]   |
|                 Lv. 42         [Settings 48px]    |
|--------------------------------------------------|
|                                                  |
|        +------------------------------------+    |
|        |     Promo Carousel (240pt tall)     |    |
|        |          * * * (dots)               |    |
|        +------------------------------------+    |
|                                                  |
|     +------------------+ +------------------+    |
|     | Daily Rewards    | | Shop             |    |
|     +------------------+ +------------------+    |
|     +------------------+ +------------------+    |
|     | Events           | | Friends          |    |
|     +------------------+ +------------------+    |
|                                                  |
|     +----------------------------------------+   |
|     |         PLAY (360pt wide)              |   |
|     +----------------------------------------+   |
|                                                  |
|     [ Inbox ]                                    |
|                                                  |
|--------------------------------------------------|
| [Home]  Home  | [Battle] Battle | [Shop] | [Social]|
|   (icon+text)                                     |
+--------------------------------------------------+
```

### Section 5B: Interactive Element Details

#### `MM_TabBar (iPad)` — **Tab**

- **States:**
  - Unselected: Grey icon + grey text
  - Selected: Blue icon + blue text + underline
- **Touch Target:** 25% width x 72pt per tab
- **Animation:** Same as mobile. Text fades in with icon color change.

#### `ButtonGrid (iPad)` — **Grid**

- **States:** 2-column grid with 16pt gap
- **Touch Target:** Each button: ~50% container width x 88pt
- **Animation:** Same press/release animations as mobile, slightly larger scale range (0.97 vs 0.95)

### Section 4: States & Visual Behavior

All states and visual behaviors are identical to Example A (SCR-MAINMENU-001). No iPad-specific state changes.

### Section 6: Interactions & Actions

All interactions are identical to Example A (SCR-MAINMENU-001). No iPad-specific interaction changes.

### Section 7: Data Requirements

All data requirements are identical to Example A (SCR-MAINMENU-001). No iPad-specific data changes.

### Screen Flow Logic

Screen flow is identical to Example A (SCR-MAINMENU-001). No iPad-specific flow changes.

### Section 8: Rules & Constraints

All rules from Example A (SCR-MAINMENU-001) apply. Additional iPad-specific rules:

- **R-IPAD-001** 🟡 MEDIUM: Button grid must switch from 1-column to 2-column layout when aspect ratio width exceeds 768pt effective width. Use GridLayoutGroup with constraint: FixedColumnCount = 2.
- **R-IPAD-002** 🟡 MEDIUM: Tab bar must show icon + text label on iPad. Mobile shows icon only. Use CanvasScaler reference resolution to detect tablet mode.
- **R-IPAD-003** 🟢 LOW: iPad supports both portrait (3:4) and landscape (4:3) orientations. In landscape, the button grid may expand to 3 or 4 columns. Play button width caps at 480pt.

### Section 9: Accessibility & Localization

**Touch Targets:**
- All targets scale up proportionally on iPad. Minimum 48pt (vs 44pt on mobile) due to expected finger-based interaction on larger screens.

**Text Scaling:**
- Same dynamic text support as mobile. iPad has more room so text truncation is less likely.

**Localization:**
- Same keys as mobile. Tab bar text labels add localization keys: `tab.home`, `tab.battle`, `tab.shop`, `tab.social`.

**Safe Area:**
- iPad has minimal safe area concerns (no notch on most models). Home indicator area at bottom still applies on newer iPads.

### Section 10: Responsive Layout

- **Canvas Scaler:** Scale With Screen Size, reference 2048x2732, Match Width or Height (0.5)
- **Orientation:** Portrait primary, landscape supported
- **Resolution:** iPad Air: 2360x1640, iPad Pro 11": 2388x1668, iPad Pro 12.9": 2732x2048

#### Aspect Ratio Breakdown

**3:4 (iPad Portrait):**
Primary tablet layout. 2-column button grid. Tab bar with icon + text labels. Carousel height: 240pt.

**4:3 (iPad Landscape):**
Rotated layout with wider viewport. 3-4 column button grid possible. Play button width capped at 480pt. Carousel may use side margins.

### Section 12: Canvas Hierarchy

```
Canvas (Screen Space - Overlay)
+-- CanvasScaler (Scale With Screen Size, ref: 2048x2732, match: 0.5)
+-- SafeArea (stretch all edges)
    +-- TopBar (top-anchored, height: 96)
    |   +-- AvatarImage (left-anchored, 160x160)
    |   +-- PlayerInfoGroup (left-anchored, offset: 176px)
    |   |   +-- PlayerName (TextMeshPro, 20pt)
    |   |   +-- LevelBadge (TextMeshPro, 16pt)
    |   +-- CurrencyGroup (right-anchored, spacing: 16)
    |       +-- CoinDisplay (HorizontalLayout)
    |       +-- GemDisplay (HorizontalLayout)
    +-- SettingsBtn (top-right, 48x48)
    +-- ContentArea (stretch, padding: top 106, bottom 82)
    |   +-- PromoCarousel (top-anchored, height: 240)
    |   +-- ButtonGrid (GridLayout, 2 cols, cellSize: 50%x88, spacing: 16)
    |   |   +-- DailyRewardBtn
    |   |   +-- ShopBtn
    |   |   +-- EventsBtn
    |   |   +-- FriendsBtn
    |   +-- PlayButton (bottom area, width: 360, height: 60)
    |   +-- InboxBtn (below PlayButton)
    +-- BottomTabBar (bottom-anchored, height: 72)
        +-- TabHome (25% width, icon + "Home")
        +-- TabBattle (25% width, icon + "Battle")
        +-- TabShop (25% width, icon + "Shop")
        +-- TabSocial (25% width, icon + "Social")
```

### Section 11: Animation & Transitions

All animations are identical to Example A (SCR-MAINMENU-001). iPad may use slightly longer durations for transitions to feel more fluid on the larger screen (optional: multiply all durations by 1.1x).

### Section 14: Notes & Open Questions

> ⚠️ **Q:** Should iPad landscape mode use a completely different layout (e.g., sidebar navigation) or just reflow the portrait layout?

> ⚠️ **Q:** iPad Pro 12.9" has significantly more space. Should we introduce a 3-column button grid at that size?

> ℹ️ **Note:** iPad Multitasking (Split View, Slide Over) may reduce available width to phone-like dimensions. Consider falling back to mobile layout when width drops below 768pt.

---

## Template Usage Guide

### How to Use This Template

| Step | Action                                                             | Details                                                                                                                                                                                                      |
| ---- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1    | Copy the Template Sections (1-14 + 5B)                             | Start from "Section 1: Screen Overview" through "Section 14: Notes & Open Questions". Include Section 5B between Sections 5 and 6.                                                                           |
| 2    | Replace All Placeholder Tokens                                     | Search for all `[BRACKETED_PLACEHOLDERS]` and replace with actual values. Key tokens: `[SCREEN_NAME]`, `[SCREEN_ID]`, `[SCREEN_PURPOSE]`, `[DEVICE]`, `[ASPECT_RATIO]`.                                     |
| 3    | Fill Section 1: Screen Overview                                    | Define the screen name, unique ID (format: SCR-XXXX-NNN), purpose, target device, and aspect ratio. Set the priority badge and version.                                                                      |
| 4    | Fill Section 2: User Flow Context                                  | Document how users arrive at this screen (entry points), what actions they can take, and where they go next (exit points).                                                                                   |
| 5    | Fill Section 3: Visual Layout / Wireframe                          | Create an ASCII wireframe showing approximate element positions. Use box-drawing characters. Mark safe areas for notched devices.                                                                            |
| 6    | Fill Section 4: State Diagram                                      | Map all possible states of the screen (loading, empty, populated, error, etc.) and transitions between them. Use ASCII flow diagrams.                                                                        |
| 7    | Fill Section 5: UI Elements Inventory                              | List every UI element with: ID, name, type (badge), position/anchoring, size, and visual description. Be exhaustive.                                                                                         |
| 8    | Fill Section 5B: Interactive Element Details                        | For each interactive element, create an element-spec-card documenting all states (default, pressed, disabled, hover, selected) with colors, scale, and feedback.                                              |
| 9    | Fill Section 6: Interactions & Gestures                            | Document every user interaction: tap, swipe, long-press, drag, etc. Include the trigger, action, feedback, and result for each.                                                                              |
| 10   | Fill Section 7: Data Requirements                                  | List all data the screen needs: field names, types, sources, update frequency, and fallback values for offline/error states.                                                                                 |
| 11   | Fill Section 8: Business Rules & Validation                        | Define rules (RULE-NNN format) covering visibility conditions, validation logic, edge cases, and error handling.                                                                                             |
| 12   | Fill Section 9-12: Responsive, Accessibility, Animation, Technical | Define breakpoints, scaling behavior, accessibility requirements (WCAG targets), animation specs (duration, easing, properties), and technical implementation notes (Canvas hierarchy, performance targets).  |
| 13   | Fill Section 13: Acceptance Criteria                               | Write testable criteria (AC-NNN format) that QA can verify. Cover functional requirements, edge cases, and performance targets.                                                                              |
| 14   | Fill Section 14: Notes & Open Questions                            | Document unresolved decisions, assumptions, known limitations, and questions for stakeholders. Use warning blocks for questions and info blocks for informational notes.                                      |
| 15   | Review Against Examples                                            | Compare your completed spec against Examples A-D above to ensure completeness and consistency. Verify all sections are filled and no placeholders remain.                                                    |

### Interactive Element Checklist

| Element Type | Badge Class      | Required States                                 | Key Properties to Document                                                                  |
| ------------ | ---------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Button       | `badge-button`   | Default, Pressed, Disabled, (Hover for desktop) | Background color, text color, scale on press, shadow, corner radius, min tap target (44pt)  |
| Toggle       | `badge-toggle`   | On, Off, Disabled                               | Track color (on/off), thumb position, transition duration, label text change                |
| Slider       | `badge-slider`   | Default, Dragging, Disabled                     | Track fill color, thumb size, value range, step increments, value label format              |
| Dropdown     | `badge-dropdown` | Closed, Open, Disabled                          | Arrow rotation, options list max height, scroll behavior, selected item highlight           |
| Tab          | `badge-tab`      | Active, Inactive, Disabled                      | Active indicator (underline/background), text weight/color change, content switch animation |
| Progress Bar | `badge-progress` | Empty, Filling, Full, Animated                  | Fill color gradient, animation duration, label format (% or value), milestone markers       |
| Timer        | `badge-timer`    | Running, Paused, Expired, Warning               | Format (HH:MM:SS), warning threshold, color change on warning, pulse animation              |
| Text Display | `badge-label`    | Default, Loading, Error, Empty                  | Font family, size, weight, color, max lines, truncation behavior, placeholder text          |
| Input Field  | `badge-input`    | Empty, Focused, Filled, Error, Disabled         | Border color per state, placeholder text, character limit, validation rules, keyboard type  |

### Best Practices

| ID     | Practice                        | Details                                                                                                                                                                                                       |
| ------ | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| BP-001 | Use Consistent IDs              | Follow the format `SCR-[FEATURE]-[NNN]` for screen IDs and `RULE-[NNN]` / `AC-[NNN]` for rules and acceptance criteria. This enables cross-referencing across specs.                                         |
| BP-002 | Document All States             | Every screen has at minimum: Loading, Empty/No Data, Populated, Error, and Offline states. Missing state documentation leads to undefined behavior in production.                                             |
| BP-003 | Specify Exact Values            | Avoid vague terms like "large" or "bright." Use exact pixel sizes (pt for iOS), hex colors (#RRGGBB or #RRGGBBAA), and precise timing (ms). Example: "width: 280pt, color: #FF6B35, duration: 300ms."        |
| BP-004 | Design for Minimum Tap Targets  | All interactive elements must have a minimum tap target of 44x44pt (Apple HIG) or 48x48dp (Material Design). Document the visual size AND the tap target size if they differ.                                 |
| BP-005 | Include Fallback Values         | Every data-driven field should have a documented fallback: placeholder text for loading, default image for failed loads, "N/A" for missing data. Never leave a UI element undefined for any data state.       |
| BP-006 | Test on Target Devices          | Document which physical devices and OS versions the spec was validated against. At minimum: iPhone SE (smallest), iPhone 15 Pro Max (largest phone), iPad Air (tablet). Note any device-specific adjustments. |
| BP-007 | Version Your Specs              | Use semantic versioning (v1.0, v1.1, v2.0) in Section 1. Track changes in Section 14 with dates. Major version bumps indicate layout or flow changes; minor versions are for copy or color tweaks.           |
| BP-008 | Cross-Reference Related Screens | In Section 2 (User Flow Context), explicitly reference the Screen IDs of connected screens. This builds a navigable map of the entire app flow. Example: "Tapping Settings opens SCR-SETTINGS-001."          |

### Performance Notes for Unity UI

| Topic                 | Guideline                                                                                                                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Canvas Splitting      | Separate static elements (backgrounds, labels) from dynamic elements (timers, progress bars, animations) into different Canvases. Each Canvas rebuild is O(n) where n = all elements on that Canvas. |
| Raycast Targets       | Disable `Raycast Target` on non-interactive elements (labels, decorative images, backgrounds). Every active raycast target is checked on every touch/click event.                                    |
| Layout Groups         | Use Layout Groups for initial setup, then disable them at runtime if the layout is static. Layout recalculations are expensive and propagate up the hierarchy.                                       |
| Object Pooling        | Pool scrollable list items, popup dialogs, and frequently spawned/despawned UI elements. Instantiate/Destroy causes GC allocation spikes.                                                           |
| Atlas Usage           | Group UI sprites into sprite atlases by screen. Elements on the same Canvas using sprites from different atlases cause additional draw calls (batch breaks).                                         |
| TextMeshPro           | Use TextMeshPro (not legacy Text). Pre-generate font atlases for expected character sets. Dynamic font atlas generation causes frame spikes.                                                         |
| Transparency Overdraw | Minimize overlapping transparent elements. Each transparent pixel is rendered in every overlapping layer. Use opaque backgrounds where possible.                                                     |
| Animation             | Prefer DOTween or custom tweens over Animator/Animation components for simple UI animations (fade, scale, move). Animator overhead is significant for simple state changes.                          |

> **Target frame budget** for UI rendering: less than 2ms per frame on mid-range devices. Profile with Unity Frame Debugger and Profiler to verify Canvas rebuild costs.

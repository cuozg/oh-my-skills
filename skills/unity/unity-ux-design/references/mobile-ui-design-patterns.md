# Mobile Game UI Design Patterns

> Authoritative reference derived from Layer Lab GUI Pro-SuperCasual analysis.
> Reference: `Assets/Layer Lab/GUI Pro-SuperCasual/`

## 1. Lobby / Main Menu Screen

The central hub from which all game systems are accessible.

### Structure
```
Canvas
  SafeArea
    Top
      ResourceBar          (Horizontal: Energy | Coins | Gems with "+" buttons)
      PlayerInfoBar        (Avatar, Username, Level badge, Trophy count)
    Middle
      ProgressSection      (Chest progress bar, Battle Pass bar)
      SideButtons_Left     (Friends, Gift - vertical stack)
      SideButtons_Right    (Ranking, Clan, Quest - vertical stack)
      HeroDisplay          (Character model, Name, Level, XP bar)
      PlayButton           (Large yellow CTA - full width)
    Bottom
      BottomBar_Menu       (5-tab navigation: Shop, Cards, Battle, Inventory, Maps)
      ChatBubble           (Floating chat icon, bottom-left)
```

### Key Patterns
- **Resource Bar**: Always visible at top; each resource has icon + value + blue "+" add button
- **Notification Badges**: Red circles with "!" or count ("7") on buttons requiring attention
- **Hero-Centric Layout**: Character occupies center screen with stats below
- **Primary CTA**: Large, full-width yellow button with 3D bevel effect
- **Side Floating Buttons**: Vertically stacked icon buttons for secondary features
- **Bottom Tab Bar**: 5 tabs with enlarged center tab for primary action (Battle)

### Layer Lab Example
- DemoScene sections: `Top`, `Middle`, `Bottom`
- Resource bar: `Group_ResourceBar` with coin/gem icons
- Bottom nav: `BottomBar_Menu` with `Button_01` through `Button_05`
- Player info: avatar in `BorderFrame_Circle78_Role`

---

## 2. Popup / Modal Dialog

Overlay panels for confirmations, rewards, purchases.

### Structure
```
PopupRoot (covers full screen)
  Dimed                    (Dark overlay, blocks input behind)
  PopupPanel               (Centered rounded rectangle)
    TopSection             (Blue/themed background)
      Title                (Centered header text)
      CloseButton          (Top-right, red square with white X)
      FeaturedIcon         (Large item/chest icon)
      ItemName             (White text below icon)
    BottomSection          (White/light background)
      RewardsList          (Horizontal slots: icon + quantity)
      ActionButton         (Yellow/gold pill button with price)
```

### Key Patterns
- **Dimmed Background**: High-opacity dark overlay (`Dimed` GameObject with black Image, alpha ~0.82)
- **Two-Tone Panel**: Upper colored section (blue/purple) + lower white section
- **Close Button**: Always top-right, red background, white "X", thick black border
- **Reward Slots**: Horizontal list items with icon + text in rounded grey containers
- **Action Button**: Large pill-shaped button at bottom, yellow/gold gradient
- **Panel Border**: Thick black outline (4-6px stroke) around entire panel

### Variants (from Layer Lab)
| Variant | Naming Pattern | Description |
|---------|---------------|-------------|
| Centered small | `Popup_Chest` | Compact purchase confirmation |
| Full-width dimmed | `PopupDimmed_*` | Reward/skin reveal with dim BG |
| Full-screen | `PopupFullScreen_*` | Level up, character upgrades |
| Toast | `Popup_Toast` | Brief notification, auto-dismiss |
| Network error | `Popup_NetworkError` | System error with retry button |

---

## 3. Scrollable List Screen

Used for leaderboards, friends lists, inventories, mail.

### Structure
```
Canvas
  SafeArea
    Header
      ResourceBar
      TitleBar             (Screen name + timer/info + decorative icon)
    Content
      FeaturedSection      (Top 3 podium cards for leaderboards)
      ScrollView
        Viewport
          Content          (Vertical list of items)
            ListItem_01    (Rank badge | Avatar | Name | Score)
            ListItem_02
            ...
      PlayerHighlight      (Sticky bottom row showing player's own rank)
    Footer
      BackButton           (Left-aligned, curved arrow icon)
      TabToggle            (Global/Local filter pills)
```

### Key Patterns
- **Featured Top Section**: Top 3 items displayed as large banner cards (not in scroll)
- **List Item Layout**: Horizontal pill-shaped rows with consistent column spacing:
  - Column 1: Rank badge (hexagonal or numbered)
  - Column 2: Avatar (square, rounded corners)
  - Column 3: Username (bold, left-aligned)
  - Column 4: Score/value (right-aligned with icon)
- **Player Row Highlight**: Current player's row in distinct yellow/gold background
- **Tab Filters**: Pill-shaped toggle buttons in footer (e.g., Global/Local)
- **Consistent Row Height**: All list items same height for uniform scrolling

### Layer Lab Naming
- List frames: `ListFrame01_Blue`, `ListFrame02_Blue`, `ListFrame03_White`
- Item frames: `ItemFrame01_Basic_Navy`, `ItemFrame02_Basic_Orange`
- Scroll content: `Viewport` > `Content` hierarchy

---

## 4. Stage Selection / Map Screen

Level/stage picker with progression path.

### Structure
```
Canvas
  SafeArea
    Header
      ResourceBar
      StageInfo            (Chapter name, progress)
    Content
      MapScroll            (Horizontal or grid scroll)
        StageNode_01       (Circle/card: number, stars, lock state)
        StageNode_02
        ...
        CurrentIndicator   (Highlight on current stage)
    Footer
      NavigationButtons    (Prev/Next chapter arrows)
      BottomBar
```

### Key Patterns
- **Stage Nodes**: Circular icons with stage number, connected by path lines
- **Lock States**: Locked stages show grey/dim with lock icon overlay
- **Star Rating**: 0-3 stars below completed stages
- **Current Stage**: Glow/highlight effect, enlarged node
- **Chapter Navigation**: Left/right arrow buttons for chapter browsing

### Layer Lab Naming
- Stage icons: `StageIcon_Gray` (locked), colored variants (unlocked)
- Navigation: `Button_Prev`, `Button_Next`

---

## 5. Shop / Store Screen

In-app purchase and virtual currency store.

### Structure
```
Canvas
  SafeArea
    Header
      ResourceBar
      ShopTitle
    Content
      TabBar               (Categories: Featured, Skins, Currency, Bundles)
      ScrollView
        Viewport
          Content
            ShopCard_01    (Item image, name, price button)
            ShopCard_02
            ...
    Footer
      BottomBar
```

### Key Patterns
- **Category Tabs**: Horizontal tab bar below header for filtering
- **Shop Cards**: Vertical cards with:
  - Large item preview image (top 60%)
  - Item name and description (middle)
  - Price button with currency icon (bottom)
- **Value Tags**: Star-burst badges ("BEST", "HOT", "x15 Value") overlaid on cards
- **Currency Display**: Price shown with icon (coin/gem) + amount
- **Bundle Cards**: Wider cards showing multiple items grouped together

### Layer Lab Naming
- Price groups: `Group_Price`, `Button_Price`
- Value badges: `Flag_Green`, marketing tag overlays

---

## 6. Player Profile Screen

User stats, equipment, and customization.

### Structure
```
Canvas
  SafeArea
    Header
      BackButton
      ProfileTitle
    Content
      AvatarSection        (Large avatar frame, username, level)
      StatsGrid            (Win rate, trophies, matches played)
      EquipmentSlots       (Helmet, Weapon, Armor, Boots, Ring, Shield)
      AchievementBar       (Progress toward next milestone)
    Footer
      ActionButtons        (Edit Profile, Share)
```

### Key Patterns
- **Large Avatar**: Circular/rounded frame, 2x larger than list avatars
- **Stats Grid**: 2x3 or 3x2 grid of stat cards with icon + label + value
- **Equipment Slots**: 6 icon slots in a grid or ring layout around character
- **Level Badge**: Prominent level number with XP progress bar

### Layer Lab Naming
- Avatar frames: `BorderFrame_Circle78_Role`, `ProfileFrmae_R16`
- Equipment: `6_Equipment` screen pattern

---

## 7. Collection / Inventory Detail

Item inspection with stats, rarity, and upgrade options.

### Structure
```
Canvas
  SafeArea
    Header
      BackButton
      ItemName
    Content
      ItemPreview          (Large centered item image with glow)
      RarityBadge          (Color-coded: Common/Rare/Epic/Legendary/Mythic)
      StatsPanel           (ATK, DEF, HP values with bars)
      DescriptionText
      UpgradeButton        (If upgradeable)
    Footer
      EquipButton          (Primary action)
      SellButton           (Secondary action)
```

### Key Patterns
- **Rarity Color Coding**: Consistent across all UI:
  - Common: Grey
  - Rare: Blue
  - Epic: Purple
  - Legendary: Gold/Orange
  - Mythic: Red/Pink
- **Large Preview**: Item centered with glow/particle effect matching rarity
- **Stat Bars**: Horizontal bars showing stat values relative to max
- **Dual Action Footer**: Equip (primary, colored) + Sell (secondary, grey)

### Layer Lab Naming
- Collection screens: `6_Collection_Detail_3_Rare` through `6_Mythic`
- Item info popups: `7_Equipment_ItemInfoPopup_01` through `07`
- Item icons: `ItemIcon` with rarity frames

---

## 8. Gameplay HUD

In-game overlay during active gameplay.

### Structure
```
Canvas
  SafeArea
    HUD_Top
      Left                 (HP bar, MP bar, player level)
      Center               (Timer, wave counter)
      Right                (Pause button, score)
    HUD_Center             (Combo counter, floating damage numbers)
    HUD_Bottom
      Left                 (Mini-map or character portrait)
      Right                (Ability buttons in grid, Ultimate button)
```

### Key Patterns
- **Minimal Obstruction**: HUD hugs edges, center is clear for gameplay
- **HP/MP Bars**: Top-left, horizontal with gradient fills (green/blue)
- **Timer**: Top-center, dark background with high contrast text
- **Ability Buttons**: Circular, bottom-right, 4 abilities + 1 larger ultimate
- **Cooldown Overlay**: Semi-transparent dark overlay with countdown text on ability buttons
- **Pause Button**: Top-right, small circular button

### Layer Lab Naming
- Play UI: `4_Play_UI_Idle`, `4_Play_UI_Action`
- Timer: `BorderFrame_Oval46_Timer`
- Indicators: `Indicator`, `Slider`

---

## 9. Daily Login / Calendar Screen

Reward calendar showing daily login bonuses.

### Structure
```
Canvas
  SafeArea
    Header
      Title                ("Daily Bonus")
      DayCounter           ("Day 5 of 30")
    Content
      CalendarGrid         (5x6 or 7x5 grid of day cells)
        DayCell_01         (Day number, reward icon, claimed state)
        DayCell_02
        ...
        DayCell_Today      (Highlighted, "Claim" button)
    Footer
      ClaimButton          (Primary action for today's reward)
```

### Key Patterns
- **Grid Layout**: Calendar grid with consistent cell sizing
- **State Indicators**: Claimed (checkmark/grey), Available (highlighted), Locked (dim)
- **Today Highlight**: Current day has glow/border highlight and "Claim" button
- **Milestone Rewards**: Every 7th day has larger/premium reward icon
- **Progress Bar**: Top bar showing overall monthly progress

---

## 10. Result / Victory Screen

Post-match results display.

### Structure
```
Canvas
  FullScreenBg             (Celebratory gradient/particle background)
  Content
    ResultTitle            ("VICTORY!" or "STAGE CLEAR")
    StarRating             (1-3 stars with animation)
    RewardsSection
      RewardItem_01        (Icon + quantity)
      RewardItem_02
      RewardItem_03
    StatsSection           (Score, time, kills, etc.)
  Footer
    ContinueButton         (Primary: "Continue" or "Next Stage")
    ReplayButton           (Secondary: "Replay")
    HomeButton             (Tertiary: "Home")
```

### Key Patterns
- **Full-Screen Celebration**: Particles, glow effects, gradient background
- **Star Rating**: Large animated stars with fill/empty states
- **Reward Cards**: Horizontal row of reward items with animations
- **Three-Tier Buttons**: Primary (colored), Secondary (outline), Tertiary (text)
- **Auto-Continue Timer**: Optional countdown to next action

### Layer Lab Naming
- Victory: `9_Play_Result_Victory`
- Stage clear: `9_Play_StageClear`
- Reward spin: `9_Reward_LuckSpin`

---

## Cross-Pattern Design Rules

### 1. Consistent Navigation
- **Back Button**: Always top-left or bottom-left, curved arrow icon
- **Close Button**: Always top-right on popups, red with white X
- **Bottom Tab Bar**: Present on main screens, hidden during gameplay/popups

### 2. Visual Feedback
- **Button Press**: Scale down to 0.9-0.95 on press
- **Notification**: Red badge with count or "!" for unread/claimable items
- **Selection**: Green checkmark or blue highlight border
- **Locked Content**: Grey/dim overlay with lock icon

### 3. Information Density
- **Mobile First**: Touch targets minimum 44x44pt
- **Visual Hierarchy**: Primary action largest and most colorful
- **Text Readability**: Bold fonts with shadows/outlines on busy backgrounds
- **Whitespace**: Consistent padding (8-16px between elements)

### 4. Color Semantics
| Color | Meaning | Example |
|-------|---------|---------|
| Yellow/Gold | Primary CTA, Premium currency | Play button, Coins |
| Blue | Secondary action, Free currency | Gems, XP, Info |
| Red | Alert, Close, Urgent | Notifications, Close button |
| Green | Success, Health, Confirm | Checkmarks, HP bar |
| Purple | Premium, Rare | Gems, Epic rarity |
| Grey | Disabled, Locked, Inactive | Locked stages, inactive tabs |

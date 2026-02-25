# Mobile Game UI Design Patterns

> Derived from Layer Lab GUI Pro-SuperCasual analysis.

## 1. Lobby / Main Menu
```
Canvas > SafeArea
  Top:    ResourceBar (Energy|Coins|Gems + "+" buttons), PlayerInfoBar
  Middle: ProgressSection, SideButtons_Left/Right, HeroDisplay, PlayButton (large yellow CTA)
  Bottom: BottomBar_Menu (5 tabs, enlarged center), ChatBubble
```
- Resource bar always visible, icon + value + blue "+" add
- Badges: red circles with "!" or count
- Primary CTA: large full-width yellow button

## 2. Popup / Modal
```
PopupRoot (full screen)
  Dimed (dark overlay, alpha ~0.82)
  PopupPanel (centered rounded rect)
    TopSection (blue/themed bg): Title, CloseButton (top-right red X), FeaturedIcon
    BottomSection (white bg): RewardsList (horizontal), ActionButton (yellow pill)
```
| Variant | Description |
|---|---|
| Centered small | Compact purchase confirmation |
| Full-width dimmed | Reward/skin reveal |
| Full-screen | Level up, upgrades |
| Toast | Brief auto-dismiss notification |

## 3. Scrollable List Screen
```
Header: ResourceBar, TitleBar
Content: FeaturedSection (top 3 podium), ScrollView → ListItems
         PlayerHighlight (sticky own rank at bottom)
Footer: BackButton, TabToggle (Global/Local pills)
```
- List item columns: Rank badge | Avatar | Username | Score
- Player row: distinct yellow/gold background
- Consistent row height for uniform scrolling

## 4. Stage Selection
```
Header: ResourceBar, StageInfo (chapter, progress)
Content: MapScroll → StageNodes (circle: number, stars, lock state)
Footer: NavigationButtons (Prev/Next), BottomBar
```
- Locked: grey/dim + lock icon, Completed: 0-3 stars, Current: glow/highlight

## 5. Shop / Store
```
Header: ResourceBar, ShopTitle
Content: TabBar (Featured|Skins|Currency|Bundles), ScrollView → ShopCards
Footer: BottomBar
```
- Cards: large preview (60%), name, price button with currency icon
- Value tags: star-burst badges ("BEST", "x15 Value")

## 6. Player Profile
```
Header: BackButton, ProfileTitle
Content: AvatarSection (large frame), StatsGrid (2×3), EquipmentSlots (6), AchievementBar
Footer: Edit Profile, Share buttons
```

## 7. Collection / Inventory Detail
```
Header: BackButton, ItemName
Content: ItemPreview (centered + glow), RarityBadge, StatsPanel (bars), Description
Footer: EquipButton (primary) + SellButton (secondary)
```
Rarity colors: Common=Grey, Rare=Blue, Epic=Purple, Legendary=Gold, Mythic=Red

## 8. Gameplay HUD
```
HUD_Top:    Left (HP/MP bars) | Center (Timer) | Right (Pause, Score)
HUD_Bottom: Left (Mini-map) | Right (4 abilities + Ultimate)
```
- Minimal center obstruction, HUD hugs edges
- Cooldown: semi-transparent overlay + countdown on ability buttons

## 9. Daily Login / Calendar
```
Header: Title, DayCounter
Content: CalendarGrid (day cells: number, reward icon, claimed state)
Footer: ClaimButton
```
States: Claimed (checkmark/grey), Available (highlighted), Locked (dim). Milestones every 7th day.

## 10. Result / Victory
```
FullScreenBg (particles, gradient)
Content: ResultTitle, StarRating (animated), RewardsSection, StatsSection
Footer: ContinueButton (primary), ReplayButton (secondary), HomeButton (tertiary)
```

# Example: Item List / Leaderboard Screen

Complete Unity hierarchy for a scrollable list screen with tabs, search, and item rows.
Demonstrates ScrollRect configuration, row prefab pattern, and tab navigation.

## Scene Hierarchy

```
Screen_Leaderboard                        [stretch all, child of SafeArea]
│
├── Background                            [stretch all, sibling index 0]
│   Image                                 sprite=BgDark, type=Sliced, color=#1A1A2E
│
├── Panel_Header                          [top-stretch, height=180]
│   RectTransform                         anchorMin=(0,1) anchorMax=(1,1) pivot=(0.5,1) sizeDelta=(0,180)
│   Image                                 sprite=HeaderBar, type=Sliced, color=#16213E
│
│   ├── Button_Back                       [left-center, 56×56]
│   │   RectTransform                     anchorMin=(0,0.5) anchorMax=(0,0.5) pivot=(0,0.5) pos=(24,0) size=(56,56)
│   │   Image                             sprite=IconArrowLeft, preserveAspect=true, color=#FFFFFF
│   │   Button                            transition=ColorTint
│   │
│   ├── Text_ScreenTitle                  [center]
│   │   RectTransform                     anchorMin=(0.5,0.5) anchorMax=(0.5,0.5) pivot=(0.5,0.5)
│   │   TextMeshProUGUI                   text="Leaderboard", fontSize=32, color=#FFFFFF, font=Bold
│   │   Shadow                            effectColor=(0,0,0,0.5), effectDistance=(2,-2)
│   │
│   └── Group_Tabs                        [bottom of header, stretch-width]
│       RectTransform                     anchorMin=(0,0) anchorMax=(1,0) pivot=(0.5,0) sizeDelta=(0,56)
│       HorizontalLayoutGroup            spacing=0, childAlignment=MiddleCenter
│                                         childForceExpandWidth=true, childForceExpandHeight=true
│
│       ├── Button_TabGlobal              [flexible]
│       │   Image                         sprite=TabActive, type=Sliced, color=#FF6D00
│       │   Button                        transition=ColorTint
│       │   └── Text_TabGlobal            TMP "Global", size=22, color=#FFFFFF, font=Bold
│       │
│       ├── Button_TabFriends             [flexible]
│       │   Image                         sprite=TabInactive, type=Sliced, color=#2A2A4A
│       │   Button                        transition=ColorTint
│       │   └── Text_TabFriends           TMP "Friends", size=22, color=#757575
│       │
│       └── Button_TabGuild               [flexible]
│           Image                         sprite=TabInactive, type=Sliced, color=#2A2A4A
│           Button                        transition=ColorTint
│           └── Text_TabGuild             TMP "Guild", size=22, color=#757575
│
├── Panel_PlayerRank                      [below header, height=120]
│   RectTransform                         anchorMin=(0,1) anchorMax=(1,1) pivot=(0.5,1)
│                                         offsetMin=(16,-300) offsetMax=(-16,-180)
│   Image                                 sprite=PanelRounded, type=Sliced, color=#0F3460
│   HorizontalLayoutGroup                spacing=16, padding={16,16,12,12}, childAlignment=MiddleLeft
│
│   ├── Text_MyRank                       TMP "#247", size=28, color=#FFD700, font=Bold
│   │   LayoutElement                     minWidth=80
│   │
│   ├── Image_MyAvatar                    [56×56]
│   │   Image                             sprite=AvatarFrame, preserveAspect=true
│   │   Mask                              showMaskGraphic=true
│   │   └── Image_MyAvatarPic             [stretch all] Image sprite=DefaultAvatar
│   │
│   ├── Group_MyInfo                      [flexible, VerticalLayoutGroup]
│   │   VerticalLayoutGroup               spacing=2, childAlignment=MiddleLeft
│   │   LayoutElement                     flexibleWidth=1
│   │   ├── Text_MyName                   TMP "You", size=24, color=#FFFFFF, font=Bold
│   │   └── Text_MyScore                  TMP "Score: 14,320", size=18, color=#B0BEC5
│   │
│   └── Icon_MyTrend                      [32×32]
│       Image                             sprite=IconTrendUp, preserveAspect=true, color=#4CAF50
│
├── Panel_ListArea                        [stretch between player rank and bottom]
│   RectTransform                         anchorMin=(0,0) anchorMax=(1,1) offsetMin=(0,0) offsetMax=(0,-300)
│
│   └── ScrollView                        [stretch all]
│       ScrollRect                        vertical=true, horizontal=false
│                                         movementType=Elastic, elasticity=0.1
│                                         scrollSensitivity=20, inertia=true
│                                         decelerationRate=0.135
│       Image                             sprite=none (transparent container)
│
│       ├── Viewport                      [stretch all, Mask]
│       │   RectTransform                 anchorMin=(0,0) anchorMax=(1,1) offsets=0
│       │   Mask                          showMaskGraphic=false
│       │   Image                         sprite=none (required by Mask)
│       │
│       │   └── Content                   [top-stretch, VerticalLayoutGroup]
│       │       RectTransform             anchorMin=(0,1) anchorMax=(1,1) pivot=(0.5,1) sizeDelta=(0,0)
│       │       VerticalLayoutGroup       spacing=8, padding={16,16,8,8}
│       │                                 childAlignment=UpperCenter
│       │                                 childForceExpandWidth=true, childForceExpandHeight=false
│       │       ContentSizeFitter         verticalFit=PreferredSize
│       │
│       │       ├── Item_Row_1            [height=88, stretch-width] — PREFAB INSTANCE
│       │       │   (see Row Prefab below)
│       │       ├── Item_Row_2
│       │       ├── Item_Row_3
│       │       │   ... (repeated for each leaderboard entry)
│       │       └── Item_Row_N
│       │
│       └── Scrollbar_Vertical            [right edge]
│           RectTransform                 anchorMin=(1,0) anchorMax=(1,1) pivot=(1,0.5) sizeDelta=(8,0)
│           Scrollbar                     direction=BottomToTop
│           Image                         sprite=ScrollTrack, color=#1A1A2E_88
│           └── SlidingArea               [stretch all]
│               └── Handle                Image sprite=ScrollHandle, color=#757575
│
└── Panel_LoadingOverlay                  [stretch all, initially inactive]
    Image                                 color=(0,0,0,0.5)
    └── Icon_Spinner                      [64×64, center]
        Image                             sprite=IconSpinner, preserveAspect=true
```

## Row Prefab: `Item_LeaderboardRow`

```
Item_LeaderboardRow                       [height=88, stretch-width]
│   LayoutElement                         minHeight=88, preferredHeight=88
│   Image                                 sprite=RowBg, type=Sliced, color=#16213E
│   HorizontalLayoutGroup                spacing=12, padding={16,16,8,8}, childAlignment=MiddleLeft
│                                         childForceExpandWidth=false, childForceExpandHeight=false
│
├── Text_Rank                             [width=56]
│   LayoutElement                         minWidth=56, preferredWidth=56
│   TextMeshProUGUI                       text="#1", fontSize=26, color=#FFD700, font=Bold, alignment=Center
│
├── Image_RankBadge                       [48×48, only for top 3]
│   Image                                 sprite=Badge_Gold/Silver/Bronze, preserveAspect=true
│   (conditionally active: rank <= 3)
│
├── Image_Avatar                          [56×56]
│   Image                                 sprite=AvatarFrame, preserveAspect=true
│   Mask                                  showMaskGraphic=true
│   └── Image_AvatarPic                   [stretch all]
│       Image                             sprite=PlayerAvatar, preserveAspect=true
│
├── Group_PlayerInfo                      [flexible width, VerticalLayoutGroup]
│   LayoutElement                         flexibleWidth=1
│   VerticalLayoutGroup                   spacing=2, childAlignment=MiddleLeft
│   ├── Text_PlayerName                   TMP "PlayerName", size=22, color=#FFFFFF
│   └── Text_GuildName                    TMP "Guild Tag", size=16, color=#757575
│
├── Text_Score                            [width=120, right-aligned]
│   LayoutElement                         minWidth=120
│   TextMeshProUGUI                       text="25,430", fontSize=24, color=#4FC3F7, font=Bold, alignment=Right
│
└── Icon_Trend                            [24×24]
    Image                                 sprite=IconTrendUp/Down, preserveAspect=true, color=#4CAF50/#F44336
```

## Visual Variants

### Top 3 Rows
- `Image_RankBadge` active with Gold (#FFD700), Silver (#C0C0C0), or Bronze (#CD7F32) badge
- `Text_Rank` uses matching color for rank number
- Row background has subtle gradient or highlight color

### Self Row (highlighted)
- Row background: `color=#0F3460` (brighter than normal rows)
- Left border accent: 4px strip in `#FFD700`

### Normal Rows
- Alternating backgrounds: `#16213E` / `#1A1A2E` for visual separation

## Component Summary

| Component | Count (screen) | Count (per row) |
|-----------|---------------|-----------------|
| Image | 12 + N×5 | 5 |
| TextMeshProUGUI | 5 + N×4 | 4 |
| Button | 4 | 0 |
| HorizontalLayoutGroup | 2 + N×1 | 1 |
| VerticalLayoutGroup | 1 + N×1 | 1 |
| LayoutElement | 1 + N×3 | 3 |
| ScrollRect | 1 | — |
| Mask | 1 + N×1 | 1 |
| ContentSizeFitter | 1 | — |

## ScrollRect Configuration

| Property | Value | Reason |
|----------|-------|--------|
| vertical | true | Vertical list |
| horizontal | false | No horizontal scroll |
| movementType | Elastic | Bouncy overscroll feel |
| elasticity | 0.1 | Quick snap-back |
| inertia | true | Momentum scrolling |
| decelerationRate | 0.135 | Standard deceleration |
| scrollSensitivity | 20 | Responsive to touch |
| Content.ContentSizeFitter | verticalFit=PreferredSize | Auto-sizes to fit all rows |

## Navigation Flow

- **Button_Back** → deactivates `Screen_Leaderboard`, activates previous screen
- **Button_TabGlobal/Friends/Guild** → swaps Content children, updates tab visual states
- **Item_Row tap** → opens `Popup_PlayerProfile` in PopupLayer
- **Scroll** → vertical scroll with elastic bounce at top/bottom

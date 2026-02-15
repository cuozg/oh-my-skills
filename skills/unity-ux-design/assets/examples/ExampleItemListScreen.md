# Example: Item List / Leaderboard Screen

Scrollable list with tabs, row prefab pattern. ScrollRect + ContentSizeFitter.

## Scene Hierarchy

```
Screen_Leaderboard [stretch all, child of SafeArea]
├── Background [stretch all] Image sprite=BgDark,color=#1A1A2E
├── Panel_Header [top-stretch h=180] Image color=#16213E
│   ├── Button_Back [left-center 56×56] Image IconArrowLeft | Button
│   ├── Text_ScreenTitle [center] TMP "Leaderboard" 32 Bold | Shadow
│   └── Group_Tabs [bottom-stretch h=56, HLG expandW=true]
│       ├── Button_TabGlobal Image TabActive #FF6D00 → TMP "Global" 22 Bold
│       ├── Button_TabFriends Image TabInactive #2A2A4A → TMP "Friends" 22 #757575
│       └── Button_TabGuild Image TabInactive → TMP "Guild" 22 #757575
├── Panel_PlayerRank [h=120, HLG spacing=16 pad=16] Image #0F3460
│   Text_MyRank "#247" 28 Bold #FFD700 | Image_MyAvatar[56×56]+Mask
│   Group_MyInfo[VLG flex=1] Name+Score | Icon_MyTrend[32×32] #4CAF50
├── Panel_ListArea [stretch, offsetMax=(0,-300)]
│   └── ScrollView [ScrollRect vert=true horiz=false elastic=0.1 inertia decel=0.135]
│       ├── Viewport [stretch, Mask showGraphic=false]
│       │   └── Content [top-stretch, VLG spacing=8 pad=16, ContentSizeFitter vertFit=Preferred]
│       │       ├── Item_Row_1..N — PREFAB (see below)
│       └── Scrollbar_Vertical [right w=8] dir=BottomToTop
└── Panel_LoadingOverlay [stretch, inactive] Image(0,0,0,0.5) → Spinner[64×64]
```

## Row Prefab: `Item_LeaderboardRow`

```
Item_LeaderboardRow [h=88, LayoutElement minH=88]
│ Image RowBg #16213E | HLG spacing=12 pad=16 MiddleLeft
├── Text_Rank [w=56] TMP "#1" 26 Bold #FFD700 Center
├── Image_RankBadge [48×48, top 3 only] Gold/Silver/Bronze
├── Image_Avatar [56×56] Image+Mask → AvatarPic
├── Group_PlayerInfo [flex=1, VLG spacing=2] Name 22 + Guild 16 #757575
├── Text_Score [w=120] TMP "25,430" 24 Bold #4FC3F7 Right
└── Icon_Trend [24×24] Up=#4CAF50 / Down=#F44336
```

## Visual Variants

- **Top 3**: RankBadge active, matching rank color, highlight bg
- **Self Row**: bg=#0F3460, left border 4px #FFD700
- **Normal**: Alternating #16213E / #1A1A2E

## Navigation

- Back → previous screen | Tabs → swap content | Row tap → Popup_PlayerProfile

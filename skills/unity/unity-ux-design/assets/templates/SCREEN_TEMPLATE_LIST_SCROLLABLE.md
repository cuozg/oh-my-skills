# Scrollable List Screen Template

> Layer Lab pattern for leaderboard/friends/collection screens.

## Hierarchy
```
Screen_ListExample [stretch, CanvasGroup]
├── Background [stretch] Image raycast=false
├── Top [top-stretch h=160]
│   ├── Topbar [top-stretch h=80] Image dark
│   │   ├── Text_Title [center] TMP "LEADERBOARD" 40 Bold white+outline
│   │   └── Button_Back [mid-left 60×60] → Icon_Back
│   └── Group_Tabs [bottom-stretch h=60, HLG spacing=8 pad=40,40,0,0 expandW=true]
│       ├── Button_TabAll [flexW=1] Image tab_active → TMP "All" Bold White
│       ├── Button_TabGlobal [flexW=1] Image tab_inactive → TMP "Global" Bold Gray
│       └── Button_TabFriends [flexW=1] Image tab_inactive → TMP "Friends" Bold Gray
├── Middle [stretch, top=-160 bottom=100]
│   ├── Group_Featured [top-stretch h=200, HLG spacing=16 pad=40] // optional top-3
│   │   ├── Card_Rank2 [180×180] Image rank_card_blue → Avatar+Medal+Name+Score
│   │   ├── Card_Rank1 [200×200] Image rank_card_gold → Crown+Avatar+Name+Score
│   │   └── Card_Rank3 [180×180] Image rank_card_green → Avatar+Medal+Name+Score
│   └── ScrollView_List [stretch top=-200, ScrollRect vert elastic=0.1 decel=0.135]
│       ├── Viewport [stretch, RectMask2D]
│       │   └── Content [top-stretch pivot=(0.5,1), VLG spacing=8 pad=20,20,8,8 ctrlW=true, CSF vertFit=Preferred]
│       │       ├── Row_Player_N [h=80, Image row_bg, Button, LE prefH=80, HLG spacing=12 pad=16 MiddleLeft]
│       │       │   ├── Text_Rank [w=50] TMP "#4" 24 bold
│       │       │   ├── Image_Avatar [48×48] Image+Mask circular
│       │       │   ├── Text_PlayerName [flexW=1] TMP 22 bold
│       │       │   └── Text_Score [w=120] TMP "12,345" 24 bold #FFD700 right
│       │       └── Row_Player_Self — same structure, Image row_bg_highlight (yellow)
│       └── Scrollbar_Vertical [right w=8] dir=BottomToTop
└── Bottom [bottom-stretch h=100, HLG spacing=20 pad=40 center]
    ├── Button_Refresh [60×60] → Icon_Refresh
    └── Text_UpdateTime TMP "Updated 2m ago" 16 gray
```

## Row Prefab: `Row_PlayerRank`
```
[h=80, Image row_bg sliced, Button ColorTint, LE prefH=80, HLG spacing=12 pad=16 MiddleLeft]
├── Text_Rank [w=50] "#0" 24 bold
├── Image_Avatar [48×48] Image+Mask circular
├── Text_PlayerName [flexW=1] 22 bold
└── Text_Score [w=120] "0" 24 bold yellow right
```

## Grid Variant (replace VLG on Content)
```
Content [GridLayoutGroup cell=(200,240) spacing=(16,16) UpperLeft Horiz FixedCol=3, CSF vertFit=Preferred]
├── Card_Item [Image card_bg, Button] → Icon_Item[80×80] + Text_Name[18] + Text_Level[14] + Image_RarityBorder + Badge_New
```

## Customization
- Remove `Group_Featured` for simple lists. Adjust tab count (2-4). Swap VLG→GLG for grid.
- Add TMP_InputField above ScrollView for search. Add pull-to-refresh on scroll overextension.

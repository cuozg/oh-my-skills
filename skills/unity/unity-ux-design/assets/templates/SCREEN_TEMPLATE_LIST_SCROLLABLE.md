# Scrollable List Screen Template

> Complete GameObject hierarchy for a scrollable list screen (Leaderboard, Friends, Collection) based on Layer Lab GUI Pro-SuperCasual patterns

## Full Hierarchy

```
Screen_ListExample                                // Root screen container
│ [RectTransform] Anchor: Stretch {0,0}→{1,1}
│ [CanvasGroup] alpha=1, interactable=true
│
├── Background                                    // Screen background
│   [RectTransform] Anchor: Stretch {0,0}→{1,1}
│   [Image] sprite=list_bg, Raycast Target=false
│
├── Top                                           // Fixed header
│   │ [RectTransform]
│   │   Anchor: TopStretch {0,1}→{1,1}
│   │   Height: 160
│   │   Pivot: (0.5, 1)
│   │
│   ├── Topbar                                    // Title bar
│   │   │ [RectTransform]
│   │   │   Anchor: TopStretch {0,1}→{1,1}
│   │   │   Height: 80
│   │   │ [Image] sprite=topbar_bg dark
│   │   │
│   │   ├── Text_Title [TextMeshProUGUI]
│   │   │   Text: "LEADERBOARD"
│   │   │   Anchor: Center {0.5,0.5}
│   │   │   Font Size: 40, Bold
│   │   │   Color: White with outline
│   │   │
│   │   └── Button_Back [Button+Image]
│   │       [RectTransform] Anchor: MiddleLeft {0,0.5}
│   │       Position: (40, 0)
│   │       Size: 60×60
│   │       └── Icon_Back [Image] white arrow
│   │
│   └── Group_Tabs                                // Tab filter
│       │ [RectTransform]
│       │   Anchor: BottomStretch {0,0}→{1,0}
│       │   Height: 60
│       │ [HorizontalLayoutGroup]
│       │   Spacing: 8
│       │   Padding: 40,40,0,0
│       │   Child Force Expand Width: true
│       │
│       ├── Button_TabAll [Button+Image]          // Active tab
│       │   │ [Image] sprite=tab_active (bright)
│       │   │ [LayoutElement] flexibleWidth=1
│       │   └── Text_TabAll [TextMeshProUGUI] "All" Bold, White
│       │
│       ├── Button_TabGlobal [Button+Image]       // Inactive tab
│       │   │ [Image] sprite=tab_inactive (dim)
│       │   │ [LayoutElement] flexibleWidth=1
│       │   └── Text_TabGlobal [TextMeshProUGUI] "Global" Bold, Gray
│       │
│       └── Button_TabFriends [Button+Image]
│           │ [Image] sprite=tab_inactive
│           │ [LayoutElement] flexibleWidth=1
│           └── Text_TabFriends [TextMeshProUGUI] "Friends" Bold, Gray
│
├── Middle                                        // Scrollable content
│   │ [RectTransform]
│   │   Anchor: Stretch {0,0}→{1,1}
│   │   Top: -160 (below header)
│   │   Bottom: 100 (above footer)
│   │
│   ├── Group_Featured                            // Optional: top 3 / featured section
│   │   │ [RectTransform]
│   │   │   Anchor: TopStretch {0,1}→{1,1}
│   │   │   Height: 200
│   │   │ [HorizontalLayoutGroup]
│   │   │   Spacing: 16
│   │   │   Child Alignment: MiddleCenter
│   │   │   Padding: 40,40,0,0
│   │   │
│   │   ├── Card_Rank2                            // 2nd place (left)
│   │   │   │ [Image] sprite=rank_card_blue, sliced
│   │   │   │ [Shadow]
│   │   │   │ Size: 180×180
│   │   │   ├── Image_Avatar [Image+Mask] circular 60×60
│   │   │   ├── Image_Medal [Image] silver medal 32×32
│   │   │   ├── Text_Name [TextMeshProUGUI] size=18 bold
│   │   │   └── Text_Score [TextMeshProUGUI] size=22 bold yellow
│   │   │
│   │   ├── Card_Rank1                            // 1st place (center, larger)
│   │   │   │ [Image] sprite=rank_card_gold, sliced
│   │   │   │ [Shadow]
│   │   │   │ Size: 200×200
│   │   │   ├── Image_Crown [Image] crown icon 40×40
│   │   │   ├── Image_Avatar [Image+Mask] circular 72×72
│   │   │   ├── Text_Name [TextMeshProUGUI] size=20 bold
│   │   │   └── Text_Score [TextMeshProUGUI] size=26 bold yellow
│   │   │
│   │   └── Card_Rank3                            // 3rd place (right)
│   │       │ [Image] sprite=rank_card_green, sliced
│   │       │ Size: 180×180
│   │       ├── Image_Avatar [Image+Mask] circular 60×60
│   │       ├── Image_Medal [Image] bronze medal 32×32
│   │       ├── Text_Name [TextMeshProUGUI] size=18 bold
│   │       └── Text_Score [TextMeshProUGUI] size=22 bold yellow
│   │
│   └── ScrollView_List                           // Scrollable list
│       │ [RectTransform]
│       │   Anchor: Stretch {0,0}→{1,1}
│       │   Top: -200 (below featured section)
│       │ [ScrollRect]
│       │   Horizontal: false
│       │   Vertical: true
│       │   Movement Type: Elastic
│       │   Elasticity: 0.1
│       │   Inertia: true
│       │   Deceleration Rate: 0.135
│       │ [Image] Raycast Target=true (scroll bg)
│       │
│       ├── Viewport                              // Clipping container
│       │   │ [RectTransform] Anchor: Stretch {0,0}→{1,1}
│       │   │ [RectMask2D]                        // Rectangular clip
│       │   │
│       │   └── Content                           // Dynamic content container
│       │       │ [RectTransform]
│       │       │   Anchor: Top {0,1}→{1,1}
│       │       │   Pivot: (0.5, 1)
│       │       │ [VerticalLayoutGroup]
│       │       │   Spacing: 8
│       │       │   Padding: 20,20,8,8
│       │       │   Control Child Size: Width=true, Height=false
│       │       │   Child Force Expand: Width=false, Height=false
│       │       │ [ContentSizeFitter]
│       │       │   Vertical Fit: PreferredSize
│       │       │
│       │       ├── Row_Player_4                  // List row (prefab instance)
│       │       │   │ [RectTransform] Height: 80
│       │       │   │ [Image] sprite=row_bg (sliced, rounded)
│       │       │   │ [Button] ColorTint
│       │       │   │ [LayoutElement] preferredHeight=80
│       │       │   │ [HorizontalLayoutGroup]
│       │       │   │   Spacing: 12
│       │       │   │   Padding: 16,16,0,0
│       │       │   │   Child Alignment: MiddleLeft
│       │       │   │
│       │       │   ├── Text_Rank [TextMeshProUGUI]
│       │       │   │   Text: "#4"
│       │       │   │   Size: 24 bold
│       │       │   │   [LayoutElement] preferredWidth=50
│       │       │   │
│       │       │   ├── Image_Avatar [Image+Mask]
│       │       │   │   Size: 48×48, circular mask
│       │       │   │   [LayoutElement] preferredWidth=48
│       │       │   │
│       │       │   ├── Text_PlayerName [TextMeshProUGUI]
│       │       │   │   Text: "PlayerName"
│       │       │   │   Size: 22 bold
│       │       │   │   [LayoutElement] flexibleWidth=1
│       │       │   │
│       │       │   └── Text_Score [TextMeshProUGUI]
│       │       │       Text: "12,345"
│       │       │       Size: 24 bold
│       │       │       Color: Yellow (#FFD700)
│       │       │       [LayoutElement] preferredWidth=120
│       │       │       Alignment: Right
│       │       │
│       │       ├── Row_Player_5                  // More rows...
│       │       ├── Row_Player_6
│       │       ├── ... (instantiated at runtime)
│       │       │
│       │       └── Row_Player_Self               // Highlighted player row
│       │           │ [Image] sprite=row_bg_highlight (yellow tinted)
│       │           │ [Button]
│       │           │ ... (same child structure as other rows)
│       │
│       └── Scrollbar_Vertical                    // Optional scrollbar
│           [RectTransform] Anchor: RightStretch {1,0}→{1,1}, Width=8
│           [Scrollbar] direction=BottomToTop
│           └── Sliding_Area > Handle [Image]
│
└── Bottom                                        // Fixed footer
    │ [RectTransform]
    │   Anchor: BottomStretch {0,0}→{1,0}
    │   Height: 100
    │   Pivot: (0.5, 0)
    │ [Image] sprite=footer_bg
    │ [HorizontalLayoutGroup]
    │   Spacing: 20
    │   Padding: 40,40,0,0
    │   Child Alignment: MiddleCenter
    │
    ├── Button_Refresh [Button+Image]             // Refresh data
    │   Size: 60×60
    │   └── Icon_Refresh [Image]
    │
    └── Text_UpdateTime [TextMeshProUGUI]         // Last update time
        Text: "Updated 2m ago"
        Size: 16
        Color: Light gray
```

## Row Prefab (for runtime instantiation)

```
Prefab: Row_PlayerRank
│ [RectTransform] Height: 80
│ [Image] sprite=row_bg (sliced)
│ [Button] ColorTint transition
│ [LayoutElement] preferredHeight=80
│ [HorizontalLayoutGroup] Spacing=12, Padding=16,16,0,0, MiddleLeft
│
├── Text_Rank [TextMeshProUGUI] "#0" size=24 bold, width=50
├── Image_Avatar [Image+Mask] 48×48 circular
├── Text_PlayerName [TextMeshProUGUI] "Name" size=22 bold, flexWidth=1
└── Text_Score [TextMeshProUGUI] "0" size=24 bold yellow, width=120, align=right
```

## Variant: Collection Grid (instead of list)

Replace `VerticalLayoutGroup` on Content with:
```
Content
│ [GridLayoutGroup]
│   Cell Size: (200, 240)
│   Spacing: (16, 16)
│   Start Corner: UpperLeft
│   Start Axis: Horizontal
│   Child Alignment: UpperCenter
│   Constraint: FixedColumnCount
│   Constraint Count: 3          // 3 columns for collection grid
│ [ContentSizeFitter]
│   Vertical Fit: PreferredSize
│
├── Card_Item_1 (prefab instance)
│   │ [Image] sprite=card_bg (sliced, rarity border)
│   │ [Button] ColorTint
│   ├── Icon_Item [Image] 80×80
│   ├── Text_Name [TextMeshProUGUI] size=18 bold
│   ├── Text_Level [TextMeshProUGUI] size=14
│   ├── Image_RarityBorder [Image] rarity colored
│   └── Badge_New [Image+Text] conditional visibility
```

## Customization Points

1. **Featured section**: Remove `Group_Featured` for simple lists (friends, settings)
2. **Row content**: Adjust HLG children based on data (add action buttons, status icons)
3. **Tab count**: 2-4 tabs typical, adjust Group_Tabs children
4. **Grid vs List**: Swap VerticalLayoutGroup for GridLayoutGroup (see variant above)
5. **Search bar**: Add TMP_InputField above ScrollView for searchable lists
6. **Pull-to-refresh**: Add script trigger on scroll overextension

---

*Based on Layer Lab GUI Pro-SuperCasual: Leaderboard_list_01, Friends_List, Collection_List — vertical ScrollRect with elastic bounce, consistent row heights, featured top-3 cards*

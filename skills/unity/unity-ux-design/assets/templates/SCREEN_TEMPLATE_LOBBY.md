# Lobby Screen Template

> Complete GameObject hierarchy for a mobile game lobby screen based on Layer Lab GUI Pro-SuperCasual Lobby pattern

## Full Hierarchy

```
Screen_Lobby                                      // Root screen container
│ [RectTransform] Anchor: Stretch {0,0}→{1,1}
│ [CanvasGroup] alpha=1, interactable=true
│
├── Background                                    // Full-bleed background art
│   [RectTransform] Anchor: Stretch {0,0}→{1,1}
│   [Image] sprite=lobby_bg, Raycast Target=false
│
├── Top                                           // Fixed header section
│   │ [RectTransform]
│   │   Anchor: TopStretch {0,1}→{1,1}
│   │   Height: 200
│   │   Pivot: (0.5, 1)
│   │
│   ├── Topbar                                    // Top status strip
│   │   │ [RectTransform]
│   │   │   Anchor: TopStretch {0,1}→{1,1}
│   │   │   Height: 80
│   │   │ [Image] sprite=topbar_bg, Color=(0.1,0.12,0.25,0.9)
│   │   │
│   │   └── Group_ResourceBar                     // Currency displays
│   │       │ [RectTransform] Stretch {0,0}→{1,1}
│   │       │ [HorizontalLayoutGroup]
│   │       │   Spacing: 60
│   │       │   Child Alignment: MiddleCenter
│   │       │   Padding: 40,40,0,0
│   │       │   Child Force Expand Width: true
│   │       │
│   │       ├── Item_Energy                       // Energy display
│   │       │   │ [HorizontalLayoutGroup] Spacing=8
│   │       │   ├── Icon_Energy [Image] 40×40
│   │       │   ├── Text_Energy [TextMeshProUGUI] "25/30" size=24 bold
│   │       │   └── Button_AddEnergy [Button+Image] 36×36 blue "+"
│   │       │
│   │       ├── Item_Coins                        // Coin display
│   │       │   │ [HorizontalLayoutGroup] Spacing=8
│   │       │   ├── Icon_Coin [Image] 40×40
│   │       │   ├── Text_Coins [TextMeshProUGUI] "12,345" size=24 bold
│   │       │   └── Button_AddCoins [Button+Image] 36×36 blue "+"
│   │       │
│   │       └── Item_Gems                         // Gem display
│   │           │ [HorizontalLayoutGroup] Spacing=8
│   │           ├── Icon_Gem [Image] 40×40
│   │           ├── Text_Gems [TextMeshProUGUI] "500" size=24 bold
│   │           └── Button_AddGems [Button+Image] 36×36 blue "+"
│   │
│   └── Group_UserInfo                            // Player identity
│       │ [RectTransform]
│       │   Anchor: TopStretch {0,1}→{1,1}
│       │   Top: 80, Height: 60
│       │ [HorizontalLayoutGroup] Spacing=12, Padding=40,40,0,0
│       │
│       ├── Image_Avatar [Image+Mask] 48×48 circular
│       ├── Text_Username [TextMeshProUGUI] "PlayerName" size=28 bold
│       └── Group_Trophy
│           │ [HorizontalLayoutGroup] Spacing=4
│           ├── Icon_Trophy [Image] 24×24
│           └── Text_TrophyCount [TextMeshProUGUI] "2,456" size=20
│
├── Middle                                        // Main content area
│   │ [RectTransform]
│   │   Anchor: Stretch {0,0}→{1,1}
│   │   Top: -200 (below Top section)
│   │   Bottom: 140 (above Bottom section)
│   │
│   ├── Group_Progress                            // Progress rails
│   │   │ [RectTransform] Anchor: TopStretch {0,1}→{1,1}, Height=80
│   │   │ [HorizontalLayoutGroup] Spacing=20, Padding=40,40,0,0
│   │   │
│   │   ├── Button_ChestProgress                  // Chest progress bar
│   │   │   [Button+Image] sliced panel bg
│   │   │   ├── Icon_Chest [Image] 40×40
│   │   │   ├── Slider_ChestBar [Slider] interactable=false
│   │   │   │   ├── Background [Image]
│   │   │   │   └── Fill_Area > Fill [Image] green
│   │   │   └── Text_ChestCount [TextMeshProUGUI] "3/10"
│   │   │
│   │   └── Button_BattlePass                     // Battle pass progress
│   │       [Button+Image] sliced panel bg
│   │       ├── Icon_BattlePass [Image] 40×40
│   │       ├── Slider_PassBar [Slider] interactable=false
│   │       └── Text_PassLevel [TextMeshProUGUI] "Lv.15"
│   │
│   ├── Group_Hero                                // Central hero display
│   │   │ [RectTransform] Anchor: Center {0.5,0.5}, Size=400×500
│   │   │
│   │   ├── Image_Character [Image] 300×400       // Hero art
│   │   ├── Text_CharacterName [TextMeshProUGUI] "KNIGHT" size=36 bold
│   │   ├── Text_CharacterLevel [TextMeshProUGUI] "Lv.25" size=20
│   │   └── Slider_XPBar [Slider] interactable=false, width=280
│   │       ├── Background [Image]
│   │       └── Fill_Area > Fill [Image] cyan
│   │
│   ├── Group_SideButtons_Left                    // Left floating buttons
│   │   │ [RectTransform] Anchor: MiddleLeft {0,0.5}, Offset=(20,0)
│   │   │ [VerticalLayoutGroup] Spacing=16
│   │   │
│   │   ├── Button_Friends [Button+Image] 70×70
│   │   │   ├── Icon_Friends [Image]
│   │   │   └── Badge_Notification [Image+TextMeshProUGUI] (conditional)
│   │   │
│   │   └── Button_Gift [Button+Image] 70×70
│   │       ├── Icon_Gift [Image]
│   │       └── Badge_Notification [Image+TextMeshProUGUI]
│   │
│   └── Group_SideButtons_Right                   // Right floating buttons
│       │ [RectTransform] Anchor: MiddleRight {1,0.5}, Offset=(-20,0)
│       │ [VerticalLayoutGroup] Spacing=16
│       │
│       ├── Button_Ranking [Button+Image] 70×70
│       │   └── Icon_Ranking [Image]
│       ├── Button_Clan [Button+Image] 70×70
│       │   └── Icon_Clan [Image]
│       └── Button_Quest [Button+Image] 70×70
│           ├── Icon_Quest [Image]
│           └── Badge_Notification [Image+TextMeshProUGUI]
│
├── Bottom                                        // Fixed footer section
│   │ [RectTransform]
│   │   Anchor: BottomStretch {0,0}→{1,0}
│   │   Height: 140
│   │   Pivot: (0.5, 0)
│   │
│   ├── Button_Play                               // Primary CTA
│   │   │ [RectTransform] Anchor: Center {0.5,0.7}
│   │   │   Size: 360×100
│   │   │ [Image] sprite=btn_play_bg (yellow/gold, sliced)
│   │   │ [Button] ColorTint transition
│   │   │ [Shadow] effectDistance=(3,-3)
│   │   │
│   │   └── Text_Play [TextMeshProUGUI]
│   │       Text: "PLAY"
│   │       Font Size: 48
│   │       Font Style: Bold
│   │       Color: White with dark outline
│   │
│   └── BottomBar_Menu                            // Tab navigation
│       │ [RectTransform]
│       │   Anchor: BottomStretch {0,0}→{1,0}
│       │   Height: 80
│       │ [Image] sprite=bottombar_bg (dark navy)
│       │ [HorizontalLayoutGroup]
│       │   Spacing: 0
│       │   Child Force Expand Width: true
│       │
│       ├── Tab_Home [Button+Image]               // Active tab
│       │   ├── Icon_Home [Image] tinted=active color
│       │   └── Text_Home [TextMeshProUGUI] "Home" size=14
│       │
│       ├── Tab_Shop [Button+Image]               // Inactive tab
│       │   └── Icon_Shop [Image] tinted=gray
│       │
│       ├── Tab_Play [Button+Image]               // Center tab (larger)
│       │   │ [LayoutElement] preferredWidth=1.5x
│       │   └── Icon_Play [Image] tinted=active
│       │
│       ├── Tab_Social [Button+Image]
│       │   ├── Icon_Social [Image] tinted=gray
│       │   └── Badge_Social [Image] red dot
│       │
│       └── Tab_Profile [Button+Image]
│           └── Icon_Profile [Image] tinted=gray
│
└── Overlay_Dim                                   // For popup dimming (hidden by default)
    [RectTransform] Anchor: Stretch {0,0}→{1,1}
    [Image] Color=(0,0,0,0.7)
    [CanvasGroup] alpha=0, blocksRaycasts=false
    active: false
```

## Key Configuration Notes

| Element | Config | Value |
|---------|--------|-------|
| All `[Button]` | Transition | ColorTint: Normal(1,1,1,1), Pressed(0.78,0.78,0.78,1) |
| All decorative `[Image]` | Raycast Target | false |
| All `[TextMeshProUGUI]` | Raycast Target | false |
| Screen root | [CanvasGroup] | For fade transitions |
| Panel backgrounds | Image Type | Sliced (9-slice) |
| Icon images | Image Type | Simple, Preserve Aspect |

## Customization Points

1. **Resource types**: Add/remove currency items in Group_ResourceBar
2. **Side buttons**: Adjust based on game features (remove Clan if no clan system)
3. **Progress rails**: Replace with relevant progression systems
4. **Hero display**: Adapt for your game's character presentation
5. **Tab count**: 4-5 tabs in bottom bar (adjust LayoutElement weights)
6. **Play button**: Position and size based on game emphasis

---

*Based on Layer Lab GUI Pro-SuperCasual: Lobby screen — resource bar, hero display, side shortcuts, bottom tab navigation*

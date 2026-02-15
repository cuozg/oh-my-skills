# Lobby Screen Template

> GameObject hierarchy for mobile game lobby (Layer Lab GUI Pro-SuperCasual pattern)

## Full Hierarchy

```
Screen_Lobby                                      // Root
│ [RectTransform] Stretch {0,0}→{1,1}
│ [CanvasGroup] alpha=1
│
├── Background [Image] sprite=lobby_bg, Raycast Target=false
│
├── Top                                           // Fixed header, h=200
│   │ [RectTransform] TopStretch, Height=200, Pivot=(0.5,1)
│   │
│   ├── Topbar                                    // h=80, status strip
│   │   │ [Image] sprite=topbar_bg (0.1,0.12,0.25,0.9)
│   │   └── Group_ResourceBar                     // Currency displays
│   │       │ [HorizontalLayoutGroup] Spacing=60, Padding=40,40,0,0
│   │       ├── Item_Energy {Icon 40×40 + "25/30" + Button_Add 36×36}
│   │       ├── Item_Coins {Icon 40×40 + "12,345" + Button_Add 36×36}
│   │       └── Item_Gems {Icon 40×40 + "500" + Button_Add 36×36}
│   │
│   └── Group_UserInfo                            // Player identity
│       │ [HorizontalLayoutGroup] Spacing=12, Padding=40,40,0,0
│       ├── Image_Avatar [Image+Mask] 48×48 circular
│       ├── Text_Username [TMP] "PlayerName" size=28 bold
│       └── Group_Trophy {Icon 24×24 + "2,456"}
│
├── Middle                                        // Main content
│   │ [RectTransform] Stretch, Top=-200, Bottom=140
│   │
│   ├── Group_Progress                            // Progress rails, h=80
│   │   │ [HorizontalLayoutGroup] Spacing=20, Padding=40,40,0,0
│   │   ├── Button_ChestProgress {Icon + Slider + "3/10"}
│   │   └── Button_BattlePass {Icon + Slider + "Lv.15"}
│   │
│   ├── Group_Hero                                // Center, 400×500
│   │   ├── Image_Character [Image] 300×400
│   │   ├── Text_CharacterName [TMP] "KNIGHT" size=36 bold
│   │   ├── Text_CharacterLevel [TMP] "Lv.25" size=20
│   │   └── Slider_XPBar width=280
│   │
│   ├── Group_SideButtons_Left                    // MiddleLeft, offset=(20,0)
│   │   │ [VerticalLayoutGroup] Spacing=16
│   │   ├── Button_Friends 70×70 {Icon + Badge}
│   │   └── Button_Gift 70×70 {Icon + Badge}
│   │
│   └── Group_SideButtons_Right                   // MiddleRight, offset=(-20,0)
│       │ [VerticalLayoutGroup] Spacing=16
│       ├── Button_Ranking 70×70
│       ├── Button_Clan 70×70
│       └── Button_Quest 70×70 {Icon + Badge}
│
├── Bottom                                        // Fixed footer, h=140
│   │ [RectTransform] BottomStretch, Height=140, Pivot=(0.5,0)
│   │
│   ├── Button_Play                               // Primary CTA, 360×100
│   │   │ [Image] sprite=btn_play_bg (yellow/gold, sliced)
│   │   │ [Button] [Shadow]
│   │   └── Text_Play [TMP] "PLAY" size=48 Bold White
│   │
│   └── BottomBar_Menu                            // Tab nav, h=80
│       │ [Image] sprite=bottombar_bg (dark navy)
│       │ [HorizontalLayoutGroup] ChildForceExpandWidth=true
│       ├── Tab_Home {Icon + "Home"} (active)
│       ├── Tab_Shop {Icon} (inactive/gray)
│       ├── Tab_Play {Icon} (center, 1.5x width)
│       ├── Tab_Social {Icon + Badge}
│       └── Tab_Profile {Icon}
│
└── Overlay_Dim                                   // Popup dimming, hidden
    [RectTransform] Stretch, [Image] (0,0,0,0.7)
    [CanvasGroup] alpha=0, blocksRaycasts=false, active=false
```

## Key Config

| Element | Config | Value |
|---------|--------|-------|
| All [Button] | Transition | ColorTint: Normal(1,1,1,1), Pressed(0.78,0.78,0.78,1) |
| Decorative [Image] | Raycast Target | false |
| Panel backgrounds | Image Type | Sliced (9-slice) |

## Customization Points

1. **Resources**: Add/remove currency items in Group_ResourceBar
2. **Side buttons**: Adjust based on game features
3. **Hero display**: Adapt for your character presentation
4. **Tab count**: 4-5 tabs (adjust LayoutElement weights)

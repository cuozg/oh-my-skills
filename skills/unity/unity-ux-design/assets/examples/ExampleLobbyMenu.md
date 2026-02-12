# Example: Lobby Menu Screen

Complete Unity hierarchy for a mobile game lobby/main menu screen.
Demonstrates Canvas setup, SafeArea, header with resources, content area, and bottom navigation.

## Scene Hierarchy

```
Canvas                                    [Screen Space - Camera]
│   CanvasScaler                          ScaleWithScreenSize, ref=1080×1920, match=0.5
│   GraphicRaycaster
│
└── SafeArea                              [stretch all edges, SafeAreaFitter script]
    │   RectTransform                     anchorMin=(0,0) anchorMax=(1,1) offsets=0
    │
    └── Screen_Lobby                      [active, stretch all]
        │
        ├── Background                    [stretch all, sibling index 0]
        │   Image                         sprite=BgLobby, type=Sliced, color=#2A1B4E
        │
        ├── Panel_Header                  [top-stretch, height=220]
        │   RectTransform                 anchorMin=(0,1) anchorMax=(1,1) pivot=(0.5,1) sizeDelta=(0,220)
        │   Image                         sprite=HeaderBar, type=Sliced, color=#1A0F33
        │
        │   ├── Group_PlayerInfo          [left-anchored, HorizontalLayoutGroup]
        │   │   RectTransform             anchorMin=(0,0.5) anchorMax=(0,0.5) pivot=(0,0.5) pos=(24,0) size=(400,80)
        │   │   HorizontalLayoutGroup     spacing=12, childAlignment=MiddleLeft
        │   │                             childForceExpandWidth=false, childForceExpandHeight=false
        │   │
        │   │   ├── Image_Avatar          [80×80]
        │   │   │   Image                 sprite=AvatarFrame, preserveAspect=true
        │   │   │   Mask                  showMaskGraphic=true
        │   │   │   └── Image_AvatarPic   [stretch all]
        │   │   │       Image             sprite=DefaultAvatar, preserveAspect=true
        │   │   │
        │   │   ├── Group_NameLevel       [VerticalLayoutGroup]
        │   │   │   VerticalLayoutGroup   spacing=2, childAlignment=MiddleLeft
        │   │   │   ├── Text_PlayerName   TMP "Player Name", size=28, color=#FFFFFF, font=Bold
        │   │   │   └── Text_Level        TMP "Lv. 42", size=22, color=#FFD700
        │   │   │
        │   │   └── Button_EditProfile    [44×44, min touch target]
        │   │       Image                 sprite=IconEdit, preserveAspect=true
        │   │       Button                transition=ColorTint, normal=(1,1,1,1), pressed=(0.78,0.78,0.78,1)
        │   │
        │   └── Group_ResourceBar         [right-anchored, HorizontalLayoutGroup]
        │       RectTransform             anchorMin=(1,0.5) anchorMax=(1,0.5) pivot=(1,0.5) pos=(-24,0) size=(360,60)
        │       HorizontalLayoutGroup     spacing=20, childAlignment=MiddleRight
        │
        │       ├── Group_Coins           [HorizontalLayoutGroup, spacing=6]
        │       │   ├── Icon_Coin         [40×40] Image sprite=IconCoin, preserveAspect=true
        │       │   └── Text_CoinCount    TMP "12,450", size=24, color=#FFD700, font=Bold
        │       │
        │       ├── Group_Gems            [HorizontalLayoutGroup, spacing=6]
        │       │   ├── Icon_Gem          [40×40] Image sprite=IconGem, preserveAspect=true
        │       │   └── Text_GemCount     TMP "385", size=24, color=#E040FB, font=Bold
        │       │
        │       └── Group_Energy          [HorizontalLayoutGroup, spacing=6]
        │           ├── Icon_Energy       [40×40] Image sprite=IconEnergy, preserveAspect=true
        │           └── Text_EnergyCount  TMP "28/30", size=24, color=#4FC3F7, font=Bold
        │
        ├── Panel_Content                 [middle-stretch, VerticalLayoutGroup]
        │   RectTransform                 anchorMin=(0,0) anchorMax=(1,1) offsetMin=(0,160) offsetMax=(0,-220)
        │   VerticalLayoutGroup           spacing=24, padding={left=32,right=32,top=24,bottom=24}
        │                                childAlignment=UpperCenter
        │                                childForceExpandWidth=true, childForceExpandHeight=false
        │
        │   ├── Group_FeaturedBanner      [height=280, stretch-width]
        │   │   LayoutElement             minHeight=280, preferredHeight=280
        │   │   Image                     sprite=BannerFrame, type=Sliced
        │   │   ├── Image_BannerArt       [stretch all] Image sprite=EventBanner, preserveAspect=true
        │   │   ├── Text_BannerTitle      TMP "Summer Event!", size=36, color=#FFFFFF, font=Bold
        │   │   │   RectTransform         anchorMin=(0,0) anchorMax=(0.6,0.5) pivot=(0,0)
        │   │   │   Shadow               effectColor=(0,0,0,0.5), effectDistance=(2,-2)
        │   │   └── Button_BannerCTA      [200×56]
        │   │       RectTransform         anchorMin=(0.5,0) anchorMax=(0.5,0) pivot=(0.5,0) pos=(0,20)
        │   │       Image                 sprite=ButtonPrimary, type=Sliced, color=#FF6D00
        │   │       Button                transition=ColorTint
        │   │       └── Text_CTA          TMP "GO!", size=28, color=#FFFFFF, font=Bold
        │   │
        │   ├── Group_QuickPlay           [height=120, stretch-width]
        │   │   LayoutElement             minHeight=120
        │   │   HorizontalLayoutGroup     spacing=16, childAlignment=MiddleCenter
        │   │                             childForceExpandWidth=true, childForceExpandHeight=true
        │   │
        │   │   ├── Button_Adventure      [flexible]
        │   │   │   Image                 sprite=ButtonLarge, type=Sliced, color=#4CAF50
        │   │   │   Button                transition=ColorTint
        │   │   │   ├── Icon_Adventure    [48×48] Image sprite=IconSword
        │   │   │   └── Text_Adventure    TMP "Adventure", size=22, color=#FFFFFF
        │   │   │
        │   │   ├── Button_Arena          [flexible]
        │   │   │   Image                 sprite=ButtonLarge, type=Sliced, color=#F44336
        │   │   │   Button                transition=ColorTint
        │   │   │   ├── Icon_Arena        [48×48] Image sprite=IconShield
        │   │   │   └── Text_Arena        TMP "Arena", size=22, color=#FFFFFF
        │   │   │
        │   │   └── Button_Events         [flexible]
        │   │       Image                 sprite=ButtonLarge, type=Sliced, color=#9C27B0
        │   │       Button                transition=ColorTint
        │   │       ├── Icon_Events       [48×48] Image sprite=IconCalendar
        │   │       └── Text_Events       TMP "Events", size=22, color=#FFFFFF
        │   │
        │   └── Group_DailyRewards        [height=100, stretch-width]
        │       LayoutElement             minHeight=100
        │       Image                     sprite=PanelRounded, type=Sliced, color=#1A237E_AA
        │       HorizontalLayoutGroup     spacing=8, padding={16,16,8,8}, childAlignment=MiddleLeft
        │       ├── Icon_Gift             [64×64] Image sprite=IconGiftBox
        │       ├── Group_DailyText        [VerticalLayoutGroup, spacing=2]
        │       │   ├── Text_DailyTitle   TMP "Daily Reward", size=24, color=#FFD700, font=Bold
        │       │   └── Text_DailyDesc    TMP "Claim your free reward!", size=18, color=#B0BEC5
        │       └── Button_Claim          [140×56, right-anchored]
        │           Image                 sprite=ButtonPrimary, type=Sliced, color=#FFD700
        │           Button                transition=ColorTint
        │           └── Text_Claim        TMP "CLAIM", size=22, color=#1A0F33, font=Bold
        │
        └── Panel_BottomNav               [bottom-stretch, height=160]
            RectTransform                 anchorMin=(0,0) anchorMax=(1,0) pivot=(0.5,0) sizeDelta=(0,160)
            Image                         sprite=BottomBarBg, type=Sliced, color=#0D0D1A
            HorizontalLayoutGroup         spacing=0, childAlignment=MiddleCenter
                                          childForceExpandWidth=true, childForceExpandHeight=false
                                          padding={16,16,8,8}

            ├── Button_NavHome            [flexible, VerticalLayoutGroup]
            │   Button                    transition=ColorTint
            │   ├── Icon_NavHome          [48×48] Image sprite=IconHome, color=#FFD700 (selected)
            │   └── Text_NavHome          TMP "Home", size=16, color=#FFD700
            │
            ├── Button_NavShop            [flexible, VerticalLayoutGroup]
            │   Button                    transition=ColorTint
            │   ├── Icon_NavShop          [48×48] Image sprite=IconShop, color=#757575 (unselected)
            │   └── Text_NavShop          TMP "Shop", size=16, color=#757575
            │
            ├── Button_NavCollection      [flexible, VerticalLayoutGroup]
            │   Button                    transition=ColorTint
            │   ├── Icon_NavCollection    [48×48] Image sprite=IconCollection, color=#757575
            │   └── Text_NavCollection    TMP "Collection", size=16, color=#757575
            │
            ├── Button_NavSocial          [flexible, VerticalLayoutGroup]
            │   Button                    transition=ColorTint
            │   ├── Icon_NavSocial        [48×48] Image sprite=IconFriends, color=#757575
            │   └── Text_NavSocial        TMP "Social", size=16, color=#757575
            │
            └── Button_NavProfile         [flexible, VerticalLayoutGroup]
                Button                    transition=ColorTint
                ├── Icon_NavProfile       [48×48] Image sprite=IconProfile, color=#757575
                └── Text_NavProfile       TMP "Profile", size=16, color=#757575
```

## Component Summary

| Component | Count |
|-----------|-------|
| Image | 32 |
| TextMeshProUGUI | 19 |
| Button | 12 |
| HorizontalLayoutGroup | 9 |
| VerticalLayoutGroup | 4 |
| LayoutElement | 4 |
| Shadow | 1 |
| Mask | 1 |
| CanvasScaler | 1 |
| GraphicRaycaster | 1 |

## Anchor Strategy

| Section | Anchor Pattern | Reason |
|---------|---------------|--------|
| Background | Stretch all (0,0)→(1,1) | Always fills screen |
| Panel_Header | Top-stretch, fixed height | Stays at top edge |
| Panel_Content | Middle-stretch with offsets | Fills between header and bottom nav |
| Panel_BottomNav | Bottom-stretch, fixed height | Stays at bottom edge |
| Group_PlayerInfo | Left-center | Aligns to safe left edge |
| Group_ResourceBar | Right-center | Aligns to safe right edge |

## Navigation Flow

- **Button_NavShop** → activates `Screen_Shop`, deactivates `Screen_Lobby`
- **Button_NavCollection** → activates `Screen_Collection`
- **Button_NavSocial** → activates `Screen_Social`
- **Button_NavProfile** → activates `Screen_Profile`
- **Button_BannerCTA** → navigates to event screen
- **Button_Adventure/Arena/Events** → navigates to respective game mode
- **Button_Claim** → triggers reward claim animation, then refreshes daily reward state
- **Button_EditProfile** → opens `Popup_EditProfile` in PopupLayer

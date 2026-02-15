# Example: Lobby Menu

## Hierarchy
```
Canvas [ScreenSpace-Camera] CanvasScaler=ScaleWithScreenSize,ref=1080×1920,match=0.5 | GraphicRaycaster
└── SafeArea [stretch, SafeAreaFitter]
    └── Screen_Lobby [stretch]
        ├── Background [stretch] Image BgLobby sliced #2A1B4E
        ├── Panel_Header [top-stretch h=220] Image HeaderBar #1A0F33
        │   ├── Group_PlayerInfo [left-center, HLG spacing=12]
        │   │   ├── Image_Avatar [80×80] Image+Mask → Image_AvatarPic
        │   │   ├── Group_NameLevel [VLG spacing=2]
        │   │   │   ├── Text_PlayerName TMP "Player Name" 28 Bold #FFF
        │   │   │   └── Text_Level TMP "Lv. 42" 22 #FFD700
        │   │   └── Button_EditProfile [44×44] Image IconEdit | Button
        │   └── Group_ResourceBar [right-center, HLG spacing=20]
        │       ├── Group_Coins [HLG] Icon[40×40] + "12,450" 24 Bold #FFD700
        │       ├── Group_Gems [HLG] Icon[40×40] + "385" 24 Bold #E040FB
        │       └── Group_Energy [HLG] Icon[40×40] + "28/30" 24 Bold #4FC3F7
        ├── Panel_Content [middle-stretch, VLG spacing=24 pad=32]
        │   ├── Group_FeaturedBanner [h=280] Image_BannerArt + TMP "Summer Event!" 36 Bold
        │   │   └── Button_BannerCTA [200×56] #FF6D00 → "GO!" 28 Bold
        │   ├── Group_QuickPlay [h=120, HLG spacing=16]
        │   │   ├── Button_Adventure #4CAF50 → Icon+"Adventure"
        │   │   ├── Button_Arena #F44336 → Icon+"Arena"
        │   │   └── Button_Events #9C27B0 → Icon+"Events"
        │   └── Group_DailyRewards [h=100, HLG spacing=8 pad=16]
        │       Icon_Gift[64×64] + DailyText(VLG) + Button_Claim[140×56] #FFD700
        └── Panel_BottomNav [bottom-stretch h=160, HLG expandW]
            ├── Button_NavHome Icon+Text "Home" 16 #FFD700 (selected)
            ├── Button_NavShop "Shop" #757575
            ├── Button_NavCollection "Collection" #757575
            ├── Button_NavSocial "Social" #757575
            └── Button_NavProfile "Profile" #757575
```

## Anchors
Background=stretch | Header=top-stretch fixed h | Content=middle w/offsets | BottomNav=bottom-stretch fixed h | PlayerInfo=left-center | ResourceBar=right-center

## Navigation
NavButtons → respective screens | BannerCTA → event | Adventure/Arena/Events → game modes | Claim → reward anim | EditProfile → popup

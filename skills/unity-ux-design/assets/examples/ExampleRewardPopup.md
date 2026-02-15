# Example: Reward Popup Modal

Modal overlay with GridLayoutGroup item grid, sequential reveal animation, rarity system.

## Scene Hierarchy

```
Popup_Reward [stretch all, inactive] CanvasGroup alpha=0
├── Dimmer [stretch] Image(0,0,0,0.6) | Button transition=None (tap to close)
├── Panel_Modal [center 680×920] Image PanelRounded #1A237E | Shadow(0,-6)
│   ├── Image_HeaderGlow [top decorative] Image GlowBurst #FFD700_88
│   ├── Panel_Title [top h=100]
│   │   ├── Text_Title [center] TMP "REWARDS!" 42 Bold #FFD700 | Shadow
│   │   └── Button_Close [top-right 48×48] Image IconClose | Button ColorTint
│   ├── Panel_RewardGrid [middle, offset=(24,140)→(-24,-100)]
│   │   └── ScrollView [ScrollRect vert=true elastic=0.1]
│   │       └── Viewport [Mask] → Content [top-stretch]
│   │           GridLayoutGroup cell=(180,200) spacing=(20,20) cols=3
│   │           ContentSizeFitter vertFit=Preferred
│   │           ├── Item_Reward_1..6 — PREFAB (see below)
│   └── Panel_Actions [bottom h=120, VLG spacing=8 pad=24]
│       ├── Button_ClaimAll [h=64] Image #FFD700 → TMP "CLAIM ALL" 28 Bold #1A0F33
│       └── Button_ClaimDouble [h=44, HLG] Image #4CAF50 → Icon_Ad + TMP "CLAIM ×2" 20
└── Panel_Particles [stretch, raycast=false] celebration effects
```

## Reward Card Prefab: `Item_RewardCard`

```
Item_RewardCard [180×200] CanvasGroup alpha=0 (sequential reveal)
├── BgCard [stretch] Image CardFrame color=rarity | Shadow
├── Image_ItemIcon [center 100×100] preserveAspect
├── Badge_Quantity [top-right 44×44] Image #F44336 → TMP "×5" 18 Bold
├── Image_RarityStrip [bottom h=4] color=rarity
├── Text_ItemName [bottom] TMP "Iron Sword" 16 Center Ellipsis
└── Image_NewBadge [top-left 40×20, conditional] #FF5722 → TMP "NEW" 12 Bold
```

## Rarity Colors

| Rarity | Card BG | Strip | Text |
|--------|---------|-------|------|
| Common | #616161 | #757575 | #BDBDBD |
| Uncommon | #2E7D32 | #4CAF50 | #A5D6A7 |
| Rare | #1565C0 | #2196F3 | #90CAF9 |
| Epic | #6A1B9A | #9C27B0 | #CE93D8 |
| Legendary | #F57F17 | #FFD700 | #FFF176 |

## Animation

**Open (0.4s)**: Dimmer 0→0.6 (0.2s) → Modal scale 0.8→1.0 (0.3s ease-out-back) → Cards reveal (delay=0.3+N×0.08s) → Particles at 0.5s
**Close (0.25s)**: Modal→0.9/0 (0.2s) → Dimmer→0 (0.15s) → SetActive(false)

## Navigation

- Close/Dimmer → close anim | ClaimAll → claim+close | ClaimDouble → ad+2×claim+close

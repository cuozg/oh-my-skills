# Example: Reward Popup Modal

Complete Unity hierarchy for a reward claim popup with item grid and celebration effects.
Demonstrates modal overlay pattern, GridLayoutGroup, and sequential reveal animation.

## Scene Hierarchy

This popup lives inside the `PopupLayer` child of SafeArea (see Canvas Setup template).

```
Popup_Reward                              [stretch all, initially inactive]
│   CanvasGroup                           alpha=0 (animated to 1 on open)
│
├── Dimmer                                [stretch all, sibling index 0]
│   RectTransform                         anchorMin=(0,0) anchorMax=(1,1) offsets=0
│   Image                                 color=(0,0,0,0.6)
│   Button                               transition=None (tap dimmer to close — optional)
│
├── Panel_Modal                           [center, fixed size]
│   RectTransform                         anchorMin=(0.5,0.5) anchorMax=(0.5,0.5)
│                                         pivot=(0.5,0.5) sizeDelta=(680,920)
│   Image                                 sprite=PanelRounded, type=Sliced, color=#1A237E
│   Shadow                                effectColor=(0,0,0,0.4), effectDistance=(0,-6)
│
│   ├── Image_HeaderGlow                  [top of panel, decorative]
│   │   RectTransform                     anchorMin=(0,1) anchorMax=(1,1) pivot=(0.5,1)
│   │                                     sizeDelta=(0,120) offsetMin=(-40,0) offsetMax=(40,60)
│   │   Image                             sprite=GlowBurst, preserveAspect=true, color=#FFD700_88
│   │
│   ├── Panel_Title                       [top of panel, height=100]
│   │   RectTransform                     anchorMin=(0,1) anchorMax=(1,1) pivot=(0.5,1) sizeDelta=(0,100)
│   │
│   │   ├── Text_Title                    [center]
│   │   │   TextMeshProUGUI               text="REWARDS!", fontSize=42, color=#FFD700
│   │   │                                 font=Bold, alignment=Center
│   │   │   Shadow                        effectColor=(0,0,0,0.6), effectDistance=(2,-3)
│   │   │
│   │   └── Button_Close                  [top-right, 48×48]
│   │       RectTransform                 anchorMin=(1,1) anchorMax=(1,1) pivot=(1,1) pos=(-12,-12) size=(48,48)
│   │       Image                         sprite=IconClose, preserveAspect=true, color=#FFFFFF
│   │       Button                        transition=ColorTint
│   │                                     normal=(1,1,1,1), pressed=(0.78,0.78,0.78,1)
│   │
│   ├── Panel_RewardGrid                  [middle content area]
│   │   RectTransform                     anchorMin=(0,0) anchorMax=(1,1)
│   │                                     offsetMin=(24,140) offsetMax=(-24,-100)
│   │
│   │   └── ScrollView                    [stretch all — for many rewards]
│   │       ScrollRect                    vertical=true, horizontal=false
│   │                                     movementType=Elastic, elasticity=0.1
│   │       Image                         color=(0,0,0,0) (transparent)
│   │
│   │       └── Viewport                  [stretch all]
│   │           Mask                      showMaskGraphic=false
│   │           Image                     color=(1,1,1,1) (required by Mask)
│   │
│   │           └── Content               [top-stretch]
│   │               RectTransform         anchorMin=(0,1) anchorMax=(1,1) pivot=(0.5,1) sizeDelta=(0,0)
│   │               GridLayoutGroup       cellSize=(180,200), spacing=(20,20)
│   │                                     startCorner=UpperLeft, startAxis=Horizontal
│   │                                     childAlignment=UpperCenter
│   │                                     constraint=FixedColumnCount, constraintCount=3
│   │               ContentSizeFitter     verticalFit=PreferredSize
│   │
│   │               ├── Item_Reward_1     (see Reward Card Prefab below)
│   │               ├── Item_Reward_2
│   │               ├── Item_Reward_3
│   │               ├── Item_Reward_4
│   │               ├── Item_Reward_5
│   │               └── Item_Reward_6
│   │
│   └── Panel_Actions                     [bottom of panel, height=120]
│       RectTransform                     anchorMin=(0,0) anchorMax=(1,0) pivot=(0.5,0)
│                                         sizeDelta=(0,120)
│       VerticalLayoutGroup               spacing=8, padding={24,24,12,12}
│                                         childAlignment=MiddleCenter
│
│       ├── Button_ClaimAll               [stretch-width, height=64]
│       │   LayoutElement                 minHeight=64, preferredHeight=64
│       │   Image                         sprite=ButtonPrimary, type=Sliced, color=#FFD700
│       │   Button                        transition=ColorTint
│       │   Shadow                        effectColor=(0,0,0,0.3), effectDistance=(0,-3)
│       │   └── Text_ClaimAll             TMP "CLAIM ALL", size=28, color=#1A0F33, font=Bold
│       │
│       └── Button_ClaimDouble            [stretch-width, height=44]
│           LayoutElement                 minHeight=44, preferredHeight=44
│           HorizontalLayoutGroup        spacing=8, childAlignment=MiddleCenter
│           Image                         sprite=ButtonSecondary, type=Sliced, color=#4CAF50
│           Button                        transition=ColorTint
│           ├── Icon_Ad                   [24×24] Image sprite=IconPlayAd, color=#FFFFFF
│           └── Text_ClaimDouble          TMP "CLAIM ×2 (Watch Ad)", size=20, color=#FFFFFF
│
└── Panel_Particles                       [stretch all, raycastTarget=false, on top]
    RectTransform                         anchorMin=(0,0) anchorMax=(1,1) offsets=0
    (Optional: ParticleSystem or animated sparkle images for celebration)
```

## Reward Card Prefab: `Item_RewardCard`

```
Item_RewardCard                           [180×200, from GridLayoutGroup]
│   CanvasGroup                           alpha=0 (animated to 1 sequentially on reveal)
│
├── BgCard                                [stretch all]
│   Image                                 sprite=CardFrame, type=Sliced, color varies by rarity
│   │                                     Common=#616161, Uncommon=#4CAF50, Rare=#2196F3
│   │                                     Epic=#9C27B0, Legendary=#FFD700
│   Shadow                                effectColor=(0,0,0,0.3), effectDistance=(2,-2)
│
├── Image_ItemIcon                        [center, 100×100]
│   RectTransform                         anchorMin=(0.5,0.6) anchorMax=(0.5,0.6) pivot=(0.5,0.5)
│                                         sizeDelta=(100,100)
│   Image                                 sprite=ItemIcon, preserveAspect=true
│
├── Badge_Quantity                        [top-right corner, 44×44]
│   RectTransform                         anchorMin=(1,1) anchorMax=(1,1) pivot=(1,1) pos=(-4,-4) size=(44,44)
│   Image                                 sprite=BadgeCircle, color=#F44336
│   └── Text_Quantity                     TMP "×5", size=18, color=#FFFFFF, font=Bold, alignment=Center
│
├── Image_RarityStrip                     [bottom strip, height=4]
│   RectTransform                         anchorMin=(0,0) anchorMax=(1,0) pivot=(0.5,0) sizeDelta=(0,4)
│   Image                                 color matches rarity (same as BgCard)
│
├── Text_ItemName                         [bottom area]
│   RectTransform                         anchorMin=(0,0) anchorMax=(1,0) pivot=(0.5,0)
│                                         offsetMin=(8,8) offsetMax=(-8,48)
│   TextMeshProUGUI                       text="Iron Sword", fontSize=16, color=#FFFFFF
│                                         alignment=Center, overflowMode=Ellipsis
│
└── Image_NewBadge                        [top-left, 40×20, conditionally active]
    RectTransform                         anchorMin=(0,1) anchorMax=(0,1) pivot=(0,1) pos=(4,-4) size=(40,20)
    Image                                 sprite=BadgeNew, color=#FF5722
    └── Text_New                          TMP "NEW", size=12, color=#FFFFFF, font=Bold
```

## Rarity Color System

| Rarity | Card BG | Strip | Text Color | Badge |
|--------|---------|-------|------------|-------|
| Common | #616161 | #757575 | #BDBDBD | — |
| Uncommon | #2E7D32 | #4CAF50 | #A5D6A7 | — |
| Rare | #1565C0 | #2196F3 | #90CAF9 | — |
| Epic | #6A1B9A | #9C27B0 | #CE93D8 | ✦ |
| Legendary | #F57F17 | #FFD700 | #FFF176 | ✦✦ |

## Animation Sequence

### Open Animation (0.4s total)
1. `Popup_Reward.SetActive(true)`
2. `Dimmer` alpha: 0 → 0.6 over 0.2s (ease-out)
3. `Panel_Modal` scale: 0.8 → 1.0 over 0.3s (ease-out-back), alpha: 0 → 1 over 0.2s
4. Each `Item_RewardCard` reveals sequentially:
   - Card N starts at delay = 0.3 + (N × 0.08)s
   - Scale: 0.5 → 1.0 over 0.2s (ease-out-back)
   - Alpha: 0 → 1 over 0.15s
5. `Panel_Particles` burst effect at 0.5s

### Close Animation (0.25s)
1. `Panel_Modal` scale: 1.0 → 0.9, alpha: 1 → 0 over 0.2s (ease-in)
2. `Dimmer` alpha: 0.6 → 0 over 0.15s
3. `Popup_Reward.SetActive(false)` on complete

## Component Summary

| Component | Count (popup) | Count (per card) |
|-----------|--------------|------------------|
| Image | 10 + N×5 | 5 |
| TextMeshProUGUI | 4 + N×3 | 3 |
| Button | 3 | 0 |
| CanvasGroup | 1 + N×1 | 1 |
| GridLayoutGroup | 1 | — |
| VerticalLayoutGroup | 1 | — |
| HorizontalLayoutGroup | 1 | — |
| Shadow | 2 + N×1 | 1 |
| ScrollRect | 1 | — |
| Mask | 1 | — |
| ContentSizeFitter | 1 | — |
| LayoutElement | 2 | — |

## Navigation Flow

- **Button_Close** → plays close animation, deactivates `Popup_Reward`
- **Dimmer tap** → same as Button_Close (optional — can be disabled for forced claim)
- **Button_ClaimAll** → triggers claim logic, plays close animation
- **Button_ClaimDouble** → shows rewarded ad, then claims ×2, plays close animation
- **After close** → returns to the screen that triggered the popup

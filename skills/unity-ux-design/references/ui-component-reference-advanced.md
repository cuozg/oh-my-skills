# UI Component Reference — Advanced

## 5. ScrollRect

Vertical-only, elastic 0.1, inertia, deceleration 0.135. See responsive-design-implementation.md for full config and hierarchy.

## 6. Slider

**Progress bar** (non-interactive): `Interactable: false`, hide Handle. Fill = colored, Background = dark.
**Settings slider**: `Interactable: true`, visible Handle 40×40.

## 7. Mask vs RectMask2D

| Scenario | Use |
|----------|-----|
| Scroll view / rectangular clip | RectMask2D (better perf) |
| Rounded avatar / shaped clip | Mask + Image |

## 8. LayoutElement

```
[LayoutElement]
  Min/Preferred Width/Height: -1 = ignored
  Flexible Width: 1    // Like CSS flex-grow
  Layout Priority: 1   // Higher = stronger override
```

## 9. TMP_InputField

```
InputField_Username
  [Image]                    // Background (sliced)
  [TMP_InputField]
    Content Type: Standard   // or Alphanumeric, EmailAddress, Password
    Line Type: Single Line
    Character Limit: 20
  +-- Text_Placeholder       // Color: (1,1,1,0.5)
  +-- Text_Input             // Color: (1,1,1,1)
```

## 10. Toggle

Size: 80×40. Transition: ColorTint. Use ToggleGroup for radio/tab behavior.

## 11. Component Combinations

**Resource Display**: HLG → Icon_Coin + Text_Amount + Button_Add
**Item Card**: Image(bg) + Button + Shadow → Icon_Item + Text_Name + Text_Qty + RarityBorder + Badge_New
**Leaderboard Row**: HLG → Text_Rank + Image_Avatar(Mask) + Text_Name(flex=1) + Text_Score

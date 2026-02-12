# Popup Modal Component Template

> Complete GameObject hierarchy for a centered popup modal based on Layer Lab GUI Pro-SuperCasual Popup patterns

## Full Hierarchy

```
Popup_Example                                     // Root popup container
│ [RectTransform] Anchor: Stretch {0,0}→{1,1}
│ [CanvasGroup] alpha=1, interactable=true
│ active: false                                   // Hidden by default
│
├── Dim                                           // Dark overlay blocking parent
│   [RectTransform] Anchor: Stretch {0,0}→{1,1}
│   [Image]
│     Color: (0, 0, 0, 0.7)                     // 70% black overlay
│     Raycast Target: true                        // Blocks touches to parent
│   [Button]                                      // Optional: tap dim to close
│     onClick → ClosePopup()
│
└── Panel                                         // Centered content panel
    │ [RectTransform]
    │   Anchor: Center {0.5, 0.5}
    │   Pivot: (0.5, 0.5)
    │   Size: 800 × 900                          // Fixed size, centered
    │ [Image]
    │   Sprite: popup_panel_bg (sliced, rounded corners)
    │   Color: (1, 1, 1, 1)
    │   Image Type: Sliced
    │ [Shadow]
    │   Effect Color: (0, 0, 0, 0.4)
    │   Effect Distance: (4, -4)
    │ [VerticalLayoutGroup]
    │   Spacing: 0
    │   Padding: 0, 0, 0, 0
    │   Control Child Size: Width=true, Height=false
    │   Child Force Expand: Width=true, Height=false
    │
    ├── Header                                    // Popup header section
    │   │ [RectTransform] Height: 120
    │   │ [Image] sprite=popup_header_bg (blue/themed color)
    │   │ [LayoutElement] preferredHeight=120
    │   │
    │   ├── Text_Title [TextMeshProUGUI]
    │   │   [RectTransform] Anchor: Center {0.5, 0.5}
    │   │   Text: "POPUP TITLE"
    │   │   Font Size: 40
    │   │   Font Style: Bold
    │   │   Color: White with outline
    │   │   Alignment: Center
    │   │   Raycast Target: false
    │   │
    │   └── Button_Close                          // Close button (top-right)
    │       │ [RectTransform]
    │       │   Anchor: TopRight {1, 1}
    │       │   Pivot: (1, 1)
    │       │   Position: (-8, -8)
    │       │   Size: 64 × 64
    │       │ [Image] sprite=btn_close_bg (red square, rounded)
    │       │ [Button] ColorTint transition
    │       │   Normal: (1,1,1,1)
    │       │   Pressed: (0.78,0.78,0.78,1)
    │       │ onClick → ClosePopup()
    │       │
    │       └── Icon_Close [Image]
    │           [RectTransform] Anchor: Center, Size: 32×32
    │           Sprite: icon_x_white
    │           Raycast Target: false
    │
    ├── Body                                      // Main content area
    │   │ [RectTransform] 
    │   │ [LayoutElement]
    │   │   preferredHeight: 520
    │   │   flexibleHeight: 1
    │   │ [VerticalLayoutGroup]
    │   │   Spacing: 16
    │   │   Padding: 32, 32, 24, 24
    │   │   Control Child Size: Width=true, Height=false
    │   │
    │   ├── Image_Featured                        // Featured content (icon/art)
    │   │   [RectTransform] Size: 200 × 200
    │   │   [Image] sprite=featured_item
    │   │   [LayoutElement] preferredHeight=200
    │   │   Raycast Target: false
    │   │
    │   ├── Text_Description [TextMeshProUGUI]    // Description text
    │   │   Text: "Description of the popup content goes here."
    │   │   Font Size: 24
    │   │   Color: Dark gray
    │   │   Alignment: Center
    │   │   Wrapping: Enabled
    │   │   Overflow: Ellipsis
    │   │   [LayoutElement] minHeight=60
    │   │
    │   ├── Divider [Image]                       // Visual separator
    │   │   [LayoutElement] preferredHeight=2
    │   │   Color: (1,1,1,0.2)
    │   │   Raycast Target: false
    │   │
    │   └── Group_RewardList                      // Reward/info items
    │       │ [HorizontalLayoutGroup]
    │       │   Spacing: 24
    │       │   Child Alignment: MiddleCenter
    │       │ [LayoutElement] preferredHeight=100
    │       │
    │       ├── Item_Reward_1                     // Reward item
    │       │   │ [VerticalLayoutGroup] Spacing=4, MiddleCenter
    │       │   ├── Icon_Reward [Image] 48×48
    │       │   └── Text_Quantity [TextMeshProUGUI] "x100" size=18 bold
    │       │
    │       ├── Item_Reward_2
    │       │   │ [VerticalLayoutGroup] Spacing=4
    │       │   ├── Icon_Reward [Image] 48×48
    │       │   └── Text_Quantity [TextMeshProUGUI] "x50" size=18 bold
    │       │
    │       └── Item_Reward_3
    │           │ [VerticalLayoutGroup] Spacing=4
    │           ├── Icon_Reward [Image] 48×48
    │           └── Text_Quantity [TextMeshProUGUI] "x25" size=18 bold
    │
    └── Footer                                    // Action buttons
        │ [RectTransform]
        │ [LayoutElement] preferredHeight=120
        │ [HorizontalLayoutGroup]
        │   Spacing: 24
        │   Padding: 32, 32, 16, 24
        │   Child Alignment: MiddleCenter
        │   Child Force Expand Width: true
        │
        ├── Button_Cancel                         // Secondary action
        │   │ [Image] sprite=btn_gray (sliced)
        │   │ [Button] ColorTint
        │   │ [LayoutElement] flexibleWidth=1, preferredHeight=70
        │   │ [Shadow]
        │   │
        │   └── Text_Cancel [TextMeshProUGUI]
        │       Text: "CANCEL"
        │       Font Size: 28, Bold
        │       Color: White
        │
        └── Button_Confirm                        // Primary action
            │ [Image] sprite=btn_yellow (sliced, gold)
            │ [Button] ColorTint
            │ [LayoutElement] flexibleWidth=1.5, preferredHeight=70
            │ [Shadow]
            │
            ├── Text_Confirm [TextMeshProUGUI]
            │   Text: "CONFIRM"
            │   Font Size: 28, Bold
            │   Color: White with dark outline
            │
            └── Group_Price                       // Optional: price display
                │ [HorizontalLayoutGroup] Spacing=8
                ├── Icon_Currency [Image] 24×24
                └── Text_Price [TextMeshProUGUI] "500" size=24 bold
```

## Popup Open/Close Animation (Script Reference)

```csharp
using UnityEngine;
using System.Collections;

public class PopupController : MonoBehaviour
{
    [SerializeField] private CanvasGroup _canvasGroup;
    [SerializeField] private RectTransform _panel;
    [SerializeField] private float _animDuration = 0.2f;
    
    public void Open()
    {
        gameObject.SetActive(true);
        StartCoroutine(AnimateOpen());
    }
    
    public void Close()
    {
        StartCoroutine(AnimateClose());
    }
    
    private IEnumerator AnimateOpen()
    {
        _canvasGroup.alpha = 0f;
        _panel.localScale = Vector3.one * 0.8f;
        
        float t = 0f;
        while (t < _animDuration)
        {
            t += Time.unscaledDeltaTime;
            float progress = t / _animDuration;
            float eased = 1f - Mathf.Pow(1f - progress, 3f); // EaseOutCubic
            
            _canvasGroup.alpha = eased;
            _panel.localScale = Vector3.one * Mathf.LerpUnclamped(0.8f, 1f, eased);
            yield return null;
        }
        
        _canvasGroup.alpha = 1f;
        _panel.localScale = Vector3.one;
    }
    
    private IEnumerator AnimateClose()
    {
        float t = 0f;
        while (t < _animDuration * 0.75f) // Close faster than open
        {
            t += Time.unscaledDeltaTime;
            float progress = t / (_animDuration * 0.75f);
            
            _canvasGroup.alpha = 1f - progress;
            _panel.localScale = Vector3.one * Mathf.Lerp(1f, 0.8f, progress);
            yield return null;
        }
        
        gameObject.SetActive(false);
    }
}
```

## Popup Variants

### Reward Popup (single item focus)
- Remove Group_RewardList, enlarge Image_Featured
- Footer: single "CLAIM" button (yellow, full width)

### Purchase Confirmation
- Body: Item preview + price breakdown
- Footer: "BUY" (yellow) with currency icon + amount

### Info/Detail Popup
- Body: ScrollView for long text content
- Footer: single "OK" button

### Equipment Info (Layer Lab: 7 rarity variants)
- Header color changes by rarity
- Body: item icon + stat list
- Footer: "EQUIP" + "LEVEL UP" dual buttons

## Checklist

- [ ] Dim blocks touches to parent screen
- [ ] Close button is ≥60×60 touch target at top-right
- [ ] Panel uses sliced sprite for proper scaling
- [ ] Body content doesn't overflow panel bounds
- [ ] Primary button is visually dominant (yellow, larger flex width)
- [ ] All decorative Images have Raycast Target=false
- [ ] CanvasGroup on root for fade animation
- [ ] Popup starts with active=false

---

*Based on Layer Lab GUI Pro-SuperCasual: Popup_Chest, Popup_Settings, Popup_Player_Profile, Equipment_ItemInfoPopup_01-07 — centered panel over dim background with close at top-right*

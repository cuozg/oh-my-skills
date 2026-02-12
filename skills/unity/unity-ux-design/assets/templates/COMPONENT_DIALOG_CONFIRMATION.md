# Confirmation Dialog Component Template

> Minimal confirmation dialog for destructive/important actions based on Layer Lab GUI Pro-SuperCasual popup patterns

## Full Hierarchy

```
Dialog_Confirmation                               // Root dialog container
│ [RectTransform] Anchor: Stretch {0,0}→{1,1}
│ [CanvasGroup] alpha=1
│ active: false                                   // Hidden by default
│
├── Dim                                           // Dark blocking overlay
│   [RectTransform] Anchor: Stretch {0,0}→{1,1}
│   [Image] Color=(0, 0, 0, 0.7)
│   Raycast Target: true
│
└── Panel                                         // Compact centered dialog
    │ [RectTransform]
    │   Anchor: Center {0.5, 0.5}
    │   Pivot: (0.5, 0.5)
    │   Size: 700 × 400                          // Compact size
    │ [Image]
    │   Sprite: dialog_panel_bg (sliced, rounded)
    │   Image Type: Sliced
    │ [Shadow]
    │   Effect Color: (0, 0, 0, 0.3)
    │   Effect Distance: (3, -3)
    │ [VerticalLayoutGroup]
    │   Spacing: 0
    │   Padding: 0, 0, 0, 0
    │   Control Child Size: Width=true, Height=false
    │
    ├── Header                                    // Dialog header
    │   │ [RectTransform]
    │   │ [Image] sprite=dialog_header_bg (themed color)
    │   │ [LayoutElement] preferredHeight=80
    │   │
    │   ├── Text_Title [TextMeshProUGUI]
    │   │   [RectTransform] Anchor: Center
    │   │   Text: "ARE YOU SURE?"
    │   │   Font Size: 32, Bold
    │   │   Color: White with outline
    │   │   Alignment: Center
    │   │   Raycast Target: false
    │   │
    │   └── Button_Close                          // Close button
    │       │ [RectTransform]
    │       │   Anchor: TopRight {1,1}
    │       │   Pivot: (1,1)
    │       │   Position: (-4, -4)
    │       │   Size: 56×56
    │       │ [Image] sprite=btn_close_red (red, rounded)
    │       │ [Button] ColorTint
    │       │
    │       └── Icon_Close [Image]
    │           Size: 28×28
    │           Sprite: icon_x_white
    │           Raycast Target: false
    │
    ├── Body                                      // Message content
    │   │ [LayoutElement] preferredHeight=160, flexibleHeight=1
    │   │ [VerticalLayoutGroup]
    │   │   Spacing: 12
    │   │   Padding: 32, 32, 24, 16
    │   │   Child Alignment: MiddleCenter
    │   │
    │   ├── Icon_Warning [Image]                  // Optional warning icon
    │   │   Size: 64×64
    │   │   Sprite: icon_warning (yellow triangle)
    │   │   Raycast Target: false
    │   │   [LayoutElement] preferredHeight=64
    │   │
    │   └── Text_Message [TextMeshProUGUI]
    │       Text: "This action cannot be undone. Are you sure you want to proceed?"
    │       Font Size: 22
    │       Color: (0.8, 0.8, 0.8, 1)
    │       Alignment: Center
    │       Wrapping: Enabled
    │       Overflow: Ellipsis
    │       Raycast Target: false
    │       [LayoutElement] minHeight=40
    │
    └── Footer                                    // Action buttons
        │ [LayoutElement] preferredHeight=100
        │ [HorizontalLayoutGroup]
        │   Spacing: 20
        │   Padding: 24, 24, 12, 20
        │   Child Alignment: MiddleCenter
        │   Child Force Expand Width: true
        │
        ├── Button_No                             // Cancel / No
        │   │ [Image] sprite=btn_gray (sliced)
        │   │ [Button] ColorTint
        │   │ [LayoutElement] flexibleWidth=1, preferredHeight=60
        │   │ [Shadow]
        │   │
        │   └── Text_No [TextMeshProUGUI]
        │       Text: "NO"
        │       Font Size: 26, Bold
        │       Color: White
        │       Alignment: Center
        │
        └── Button_Yes                            // Confirm / Yes
            │ [Image] sprite=btn_yellow (sliced, gold) OR sprite=btn_red (destructive)
            │ [Button] ColorTint
            │ [LayoutElement] flexibleWidth=1, preferredHeight=60
            │ [Shadow]
            │
            └── Text_Yes [TextMeshProUGUI]
                Text: "YES"
                Font Size: 26, Bold
                Color: White with dark outline
                Alignment: Center
```

## Dialog Variants

### Delete Confirmation (Destructive)
```
Header color: Red
Icon: Warning triangle (yellow)
Message: "Delete [item name]? This cannot be undone."
Button_No: Gray "CANCEL"
Button_Yes: Red "DELETE"
```

### Purchase Confirmation
```
Header color: Blue
Icon: Currency icon
Message: "Buy [item name] for 500 gems?"
Button_No: Gray "CANCEL"
Button_Yes: Yellow "BUY" + Icon_Gem + "500"
```

### Exit Confirmation
```
Header color: Blue
Icon: None
Message: "Are you sure you want to quit?"
Button_No: Gray "STAY"
Button_Yes: Yellow "QUIT"
```

### Single-Button Acknowledgment
```
Header color: Blue
Icon: Info icon
Message: "Your reward has been sent to your inbox."
Footer: Single "OK" button (yellow, full width)
(Remove Button_No, set Button_Yes flexWidth to full)
```

## Controller Script

```csharp
using UnityEngine;
using UnityEngine.Events;
using TMPro;

public class ConfirmationDialog : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI _textTitle;
    [SerializeField] private TextMeshProUGUI _textMessage;
    [SerializeField] private TextMeshProUGUI _textYes;
    [SerializeField] private TextMeshProUGUI _textNo;
    [SerializeField] private GameObject _iconWarning;
    
    private UnityAction _onConfirm;
    private UnityAction _onCancel;
    
    public void Show(string title, string message, 
                     UnityAction onConfirm, UnityAction onCancel = null,
                     string yesText = "YES", string noText = "NO",
                     bool showWarning = false)
    {
        _textTitle.text = title;
        _textMessage.text = message;
        _textYes.text = yesText;
        _textNo.text = noText;
        _iconWarning.SetActive(showWarning);
        
        _onConfirm = onConfirm;
        _onCancel = onCancel;
        
        gameObject.SetActive(true);
    }
    
    public void OnConfirmClicked()
    {
        _onConfirm?.Invoke();
        gameObject.SetActive(false);
    }
    
    public void OnCancelClicked()
    {
        _onCancel?.Invoke();
        gameObject.SetActive(false);
    }
}
```

## Sizing Guidelines

| Aspect | Value | Notes |
|--------|-------|-------|
| Panel width | 600-800 px | ~70-80% of screen width |
| Panel height | 300-500 px | Content-dependent |
| Button height | 60 px | Minimum touch-friendly |
| Button gap | 20 px | Between No and Yes |
| Body padding | 32 px sides, 24 px top/bottom | Readable margins |
| Close button | 56×56 px | Top-right, always accessible |

## Checklist

- [ ] Dialog fits within safe area on smallest supported device
- [ ] Primary action (Yes) is visually dominant (yellow/themed color)
- [ ] Secondary action (No/Cancel) is visually subdued (gray)
- [ ] Destructive confirmations use red for the confirm button
- [ ] Text wraps properly for long messages
- [ ] Close button provides alternative dismiss path
- [ ] Dialog blocks all background interaction via Dim

---

*Based on Layer Lab GUI Pro-SuperCasual: 99_Popup_Close, 99_Popup_DownloadUpdate — compact centered dialogs with clear yes/no actions*

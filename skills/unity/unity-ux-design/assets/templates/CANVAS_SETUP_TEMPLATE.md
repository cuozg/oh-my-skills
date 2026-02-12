# Canvas Setup Template

> Production-ready mobile game Canvas configuration based on Layer Lab GUI Pro-SuperCasual standards

## Complete Hierarchy

```
Canvas                                    // Root UI container
│ [Canvas]
│   Render Mode: Screen Space - Camera
│   Pixel Perfect: false
│   Sort Order: 0
│ [CanvasScaler]
│   UI Scale Mode: Scale With Screen Size
│   Reference Resolution: 1048 x 2048
│   Screen Match Mode: Match Width Or Height
│   Match: 0                             // Match width
│   Reference Pixels Per Unit: 100
│ [GraphicRaycaster]
│   Ignore Reversed Graphics: true
│
├── SafeAreaPanel                         // Insets content from notch/home indicator
│   │ [RectTransform]
│   │   Anchor: Full Stretch {0,0}→{1,1}
│   │   Left/Right/Top/Bottom: 0
│   │ [SafeArea]                         // Custom script (see below)
│   │
│   └── Panel                            // All screens container
│       │ [RectTransform]
│       │   Anchor: Full Stretch {0,0}→{1,1}
│       │   Left/Right/Top/Bottom: 0
│       │
│       ├── Screen_Loading               // Initial loading screen
│       │   [RectTransform] Stretch {0,0}→{1,1}
│       │   [CanvasGroup] alpha=1        // For fade transitions
│       │
│       ├── Screen_Lobby                 // Main lobby
│       │   [RectTransform] Stretch {0,0}→{1,1}
│       │   [CanvasGroup] alpha=1
│       │   active: false                // Toggle via screen manager
│       │
│       ├── Popup_Settings               // Settings popup
│       │   [RectTransform] Stretch {0,0}→{1,1}
│       │   [CanvasGroup] alpha=1
│       │   active: false
│       │
│       └── ... (additional screens)
│
├── PanelControl                         // Persistent overlay controls
│   │ [RectTransform]
│   │   Anchor: Full Stretch {0,0}→{1,1}
│   │
│   ├── Button_Back                      // Persistent back button
│   │   [RectTransform] Anchor: BottomLeft {0,0}
│   │   [Button]
│   │   [Image]
│   │
│   └── Text_ScreenTitle                 // Dynamic screen title
│       [RectTransform] Anchor: TopCenter {0.5,1}
│       [TextMeshProUGUI]
│
└── UnsafeContent                        // Full-bleed content (outside safe area)
    │ [RectTransform]
    │   Anchor: Full Stretch {0,0}→{1,1}
    │
    └── Background_Global                // Full-screen background
        [RectTransform] Stretch {0,0}→{1,1}
        [Image]
        Raycast Target: false
```

## Component Configuration Details

### Canvas Component
```
Property                    Value                   Notes
──────────────────────────────────────────────────────────
Render Mode                 Screen Space - Camera   Supports post-processing
Pixel Perfect               false                   Better scaling on mobile
Sort Order                  0                       Base layer
Additional Shader Channels  TexCoord1               For TMP rendering
```

### CanvasScaler Component
```
Property                    Value                   Notes
──────────────────────────────────────────────────────────
UI Scale Mode               Scale With Screen Size  Adapts to all devices
Reference Resolution        1048 x 2048             Portrait mobile standard
Screen Match Mode           Match Width Or Height
Match                       0                       Width priority (prevents horizontal overflow)
Reference Pixels Per Unit   100                     Standard for sprite imports
```

### SafeArea Script
```csharp
using UnityEngine;

[RequireComponent(typeof(RectTransform))]
public class SafeArea : MonoBehaviour
{
    private RectTransform _rect;
    private Rect _lastSafeArea;

    private void Awake()
    {
        _rect = GetComponent<RectTransform>();
        ApplySafeArea();
    }

    private void Update()
    {
        if (_lastSafeArea != Screen.safeArea)
            ApplySafeArea();
    }

    private void ApplySafeArea()
    {
        Rect safeArea = Screen.safeArea;
        Canvas rootCanvas = GetComponentInParent<Canvas>().rootCanvas;
        
        Vector2 anchorMin = safeArea.position;
        Vector2 anchorMax = safeArea.position + safeArea.size;
        
        anchorMin.x /= rootCanvas.pixelRect.width;
        anchorMin.y /= rootCanvas.pixelRect.height;
        anchorMax.x /= rootCanvas.pixelRect.width;
        anchorMax.y /= rootCanvas.pixelRect.height;
        
        _rect.anchorMin = anchorMin;
        _rect.anchorMax = anchorMax;
        
        _lastSafeArea = safeArea;
    }
}
```

### Screen Manager Script (minimal)
```csharp
using UnityEngine;

public class ScreenManager : MonoBehaviour
{
    [SerializeField] private Transform _panelContainer;
    
    public void ShowScreen(string screenName)
    {
        foreach (Transform child in _panelContainer)
            child.gameObject.SetActive(child.name == screenName);
    }
    
    public void ShowPopup(string popupName)
    {
        Transform popup = _panelContainer.Find(popupName);
        if (popup != null)
            popup.gameObject.SetActive(true);
    }
    
    public void HidePopup(string popupName)
    {
        Transform popup = _panelContainer.Find(popupName);
        if (popup != null)
            popup.gameObject.SetActive(false);
    }
}
```

## Setup Checklist

- [ ] Create Canvas with Screen Space - Camera render mode
- [ ] Assign main camera to Canvas
- [ ] Configure CanvasScaler: Scale With Screen Size, 1048×2048, match width=0
- [ ] Add SafeAreaPanel with SafeArea script
- [ ] Add Panel container inside SafeAreaPanel
- [ ] Add UnsafeContent for full-bleed backgrounds
- [ ] Add PanelControl for persistent UI elements
- [ ] Verify in Game view at multiple resolutions (see responsive-design-implementation.md)

## Resolution Test Matrix

| Device | Resolution | Expected Behavior |
|--------|-----------|-------------------|
| iPhone SE | 750×1334 | Content fits width, scrolls vertically |
| iPhone 15 | 1179×2556 | Safe area insets from notch/home bar |
| iPhone 15 Pro Max | 1290×2796 | Widest phone — verify no cutoff |
| Samsung S24 | 1080×2340 | Standard Android — test safe area |
| iPad Mini | 1488×2266 | Wider aspect — check horizontal padding |
| iPad Pro 12.9 | 2048×2732 | Tablet — may need adaptive layout |

---

*Based on Layer Lab GUI Pro-SuperCasual Canvas configuration: Screen Space - Camera, 1048×2048, Scale With Screen Size, match width=0*

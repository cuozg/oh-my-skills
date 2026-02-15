# Canvas Setup Template

## Hierarchy
```
Canvas [ScreenSpace-Camera, sortOrder=0]
│ CanvasScaler: ScaleWithScreenSize, ref=1048×2048, matchWidthOrHeight=0
│ GraphicRaycaster: ignoreReversed=true
├── SafeAreaPanel [stretch all, SafeArea script]
│   └── Panel [stretch all] // All screens
│       ├── Screen_Loading [CanvasGroup]
│       ├── Screen_Lobby [CanvasGroup] active=false
│       └── Popup_Settings [CanvasGroup] active=false
├── PanelControl // Persistent overlay
│   ├── Button_Back (BottomLeft)
│   └── Text_ScreenTitle (TopCenter)
└── UnsafeContent // Full-bleed outside safe area
    └── Background_Global [Image] raycast=false
```

## SafeArea Script
```csharp
[RequireComponent(typeof(RectTransform))]
public class SafeArea : MonoBehaviour
{
    private RectTransform _rect; private Rect _last;
    private void Awake() { _rect = GetComponent<RectTransform>(); Apply(); }
    private void Update() { if (_last != Screen.safeArea) Apply(); }
    private void Apply()
    {
        var sa = Screen.safeArea;
        var c = GetComponentInParent<Canvas>().rootCanvas;
        _rect.anchorMin = new Vector2(sa.x / c.pixelRect.width, sa.y / c.pixelRect.height);
        _rect.anchorMax = new Vector2((sa.x + sa.width) / c.pixelRect.width, (sa.y + sa.height) / c.pixelRect.height);
        _last = sa;
    }
}
```

## Screen Manager
```csharp
public class ScreenManager : MonoBehaviour
{
    [SerializeField] private Transform _container;
    public void ShowScreen(string name) { foreach (Transform c in _container) c.gameObject.SetActive(c.name == name); }
    public void ShowPopup(string name) => _container.Find(name)?.gameObject.SetActive(true);
    public void HidePopup(string name) => _container.Find(name)?.gameObject.SetActive(false);
}
```

## Checklist
- [ ] Canvas: Screen Space - Camera, assign main camera
- [ ] CanvasScaler: ScaleWithScreenSize, 1048×2048, match=0
- [ ] SafeAreaPanel with SafeArea script
- [ ] UnsafeContent for full-bleed backgrounds
- [ ] Test: iPhone SE 750×1334, iPhone 15 1179×2556, Samsung S24 1080×2340, iPad Pro 2048×2732

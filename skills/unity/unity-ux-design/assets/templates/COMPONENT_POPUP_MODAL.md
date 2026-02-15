# Popup Modal Template

## Hierarchy
```
Popup_Example [stretch all, CanvasGroup, active=false]
├── Dim [stretch all] Image color=(0,0,0,0.7) raycast=true | Button→ClosePopup()
└── Panel [center 800×900] Image sliced popup_panel_bg | Shadow | VLG spacing=0
    ├── Header [h=120] Image popup_header_bg | LayoutElement prefH=120
    │   ├── Text_Title TMP "POPUP TITLE" 40 Bold Center White
    │   └── Button_Close [topright(-8,-8) 64×64] Image btn_close_bg(red) | Button→ClosePopup()
    │       └── Icon_Close [32×32] Image icon_x_white
    ├── Body [prefH=520 flexH=1] VLG spacing=16 pad=32,32,24,24
    │   ├── Image_Featured [200×200]
    │   ├── Text_Description TMP 24 Center Wrap
    │   ├── Divider [h=2] Image color=(1,1,1,0.2)
    │   └── Group_RewardList [HLG spacing=24 MiddleCenter]
    │       ├─── Item_Reward {Icon 48×48 + Text "x100"} (×3)
    └── Footer [h=120] HLG spacing=24 pad=32,32,16,24 MiddleCenter
        ├── Button_Cancel [flexW=1 h=70] Image btn_gray → Text "CANCEL" 28 Bold
        └── Button_Confirm [flexW=1.5 h=70] Image btn_yellow → Text "CONFIRM" 28 Bold
            └── Group_Price {Icon_Currency 24×24 + Text "500"}
```

## Animation
```csharp
public class PopupController : MonoBehaviour
{
    [SerializeField] private CanvasGroup _cg;
    [SerializeField] private RectTransform _panel;
    [SerializeField] private float _dur = 0.2f;
    public void Open() { gameObject.SetActive(true); StartCoroutine(AnimOpen()); }
    public void Close() { StartCoroutine(AnimClose()); }
    private IEnumerator AnimOpen()
    {
        _cg.alpha = 0f; _panel.localScale = Vector3.one * 0.8f;
        float t = 0f;
        while (t < _dur) { t += Time.unscaledDeltaTime; float e = 1f - Mathf.Pow(1f - t/_dur, 3f);
            _cg.alpha = e; _panel.localScale = Vector3.one * Mathf.LerpUnclamped(0.8f, 1f, e); yield return null; }
        _cg.alpha = 1f; _panel.localScale = Vector3.one;
    }
    private IEnumerator AnimClose()
    {
        float t = 0f, d = _dur * 0.75f;
        while (t < d) { t += Time.unscaledDeltaTime; float p = t/d;
            _cg.alpha = 1f-p; _panel.localScale = Vector3.one * Mathf.Lerp(1f, 0.8f, p); yield return null; }
        gameObject.SetActive(false);
    }
}
```

## Variants
- **Reward**: No RewardList, enlarged Image, single "CLAIM" button
- **Purchase**: Item preview + price, "BUY" with currency icon
- **Info**: ScrollView body, single "OK"
- **Equipment**: Header color by rarity, stat list, "EQUIP" + "LEVEL UP"

## Checklist
- [ ] Dim blocks parent touches
- [ ] Close ≥60×60 touch target
- [ ] Sliced sprite on Panel
- [ ] Primary button dominant (yellow, larger flex)
- [ ] Decorative Images raycast=false
- [ ] CanvasGroup on root, starts active=false

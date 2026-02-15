# Confirmation Dialog Template

## Hierarchy
```
Dialog_Confirmation [stretch all, CanvasGroup, active=false]
├── Dim [stretch all] Image color=(0,0,0,0.7) raycast=true
└── Panel [center 700×400] Image sliced dialog_panel_bg | Shadow | VLG spacing=0
    ├── Header [h=80] Image dialog_header_bg | LayoutElement prefH=80
    │   ├── Text_Title TMP "ARE YOU SURE?" 32 Bold Center White
    │   └── Button_Close [topright(-4,-4) 56×56] → Icon_Close 28×28
    ├── Body [prefH=160 flexH=1] VLG spacing=12 pad=32,32,24,16 MiddleCenter
    │   ├── Icon_Warning [64×64] icon_warning (optional)
    │   └── Text_Message TMP 22 Center Wrap
    └── Footer [h=100] HLG spacing=20 pad=24,24,12,20 MiddleCenter
        ├── Button_No [flexW=1 h=60] Image btn_gray → Text "NO" 26 Bold
        └── Button_Yes [flexW=1 h=60] Image btn_yellow|btn_red → Text "YES" 26 Bold
```

## Variants
- **Delete**: Red header, warning icon, red "DELETE" button
- **Purchase**: Blue header, currency icon, yellow "BUY" + gem amount
- **Exit**: Blue header, "STAY" / "QUIT"
- **Ack**: Info icon, single full-width "OK"

## Controller
```csharp
public class ConfirmationDialog : MonoBehaviour
{
    [SerializeField] private TMP_Text _title, _message, _yesText, _noText;
    [SerializeField] private GameObject _iconWarning;
    private UnityAction _onConfirm, _onCancel;
    public void Show(string title, string msg, UnityAction onConfirm, UnityAction onCancel = null,
        string yes = "YES", string no = "NO", bool warn = false)
    {
        _title.text = title; _message.text = msg; _yesText.text = yes; _noText.text = no;
        _iconWarning.SetActive(warn); _onConfirm = onConfirm; _onCancel = onCancel;
        gameObject.SetActive(true);
    }
    public void OnConfirm() { _onConfirm?.Invoke(); gameObject.SetActive(false); }
    public void OnCancel() { _onCancel?.Invoke(); gameObject.SetActive(false); }
}
```

## Checklist
- [ ] Fits safe area on smallest device
- [ ] Primary action visually dominant
- [ ] Destructive = red confirm
- [ ] Dim blocks background interaction
- [ ] Close button as alternative dismiss

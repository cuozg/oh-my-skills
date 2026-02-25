# Data Binding — HUDScreenController Example

## Complete Example — HUDScreenController

```csharp
[RequireComponent(typeof(UIDocument))]
public class HUDScreenController : MonoBehaviour {
    [SerializeField] PlayerData _data;
    void OnEnable() {
        var root = GetComponent<UIDocument>().rootVisualElement;
        root.dataSource = _data;
        Bind(root, "player-name", "text", "PlayerName", BindingMode.OneWay);
        Bind(root, "health-bar", "value", "Health", BindingMode.OneWay);
        Bind(root, "gold-label", "text", "Gold", BindingMode.OneWay, "GameUI");
    }
    static void Bind(VisualElement root, string elemName, string prop,
                     string path, BindingMode mode, string converter = null) {
        var binding = new DataBinding { dataSourcePath = new PropertyPath(path), bindingMode = mode };
        if (converter != null) binding.converterGroup = converter;
        root.Q(elemName).SetBinding(prop, binding);
    }
}
```

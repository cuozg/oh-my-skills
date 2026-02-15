# WebGL Interop Patterns

## 1. C# calling JavaScript (DLLImport)

### JavaScript Plugin (.jslib)
Place in `Assets/Plugins/WebGL/MyPlugin.jslib`:
```javascript
mergeInto(LibraryManager.library, {
  HelloString: function (str) { window.alert(Pointer_stringify(str)); },
  AddNumbers: function (x, y) { return x + y; },
  StringReturnValueFunction: function () {
    var returnStr = "bla";
    var bufferSize = lengthBytesUTF8(returnStr) + 1;
    var buffer = _malloc(bufferSize);
    stringToUTF8(returnStr, buffer, bufferSize);
    return buffer;
  },
  BindCallback: function (callbackName) {
    var name = Pointer_stringify(callbackName);
    window[name] = function(data) {
      unityInstance.SendMessage('JSInteropManager', 'OnJSCallback', JSON.stringify({ name: name, data: data }));
    };
  }
});
```

### C# Wrapper
```csharp
using System.Runtime.InteropServices;

public class JSBinding : MonoBehaviour {
    [DllImport("__Internal")] private static extern void HelloString(string str);
    [DllImport("__Internal")] private static extern int AddNumbers(int x, int y);
    [DllImport("__Internal")] private static extern string StringReturnValueFunction();
}
```

## 2. JavaScript calling C# (SendMessage)

`unityInstance.SendMessage(gameObject, methodName, value);` — value is string, int, or float.

```csharp
public class JSInteropManager : MonoBehaviour {
    public void OnJSCallback(string json) {
        var callback = JsonUtility.FromJson<JSCallbackData>(json);
    }
}
```

## 3. Best Practices
- **Minimize interop calls**: Boundary crossing is expensive, avoid per-frame calls
- **String handling**: Use `Pointer_stringify` (legacy) or modern Emscripten helpers
- **Memory safety**: Careful with `_malloc`, ensure returned strings are managed correctly

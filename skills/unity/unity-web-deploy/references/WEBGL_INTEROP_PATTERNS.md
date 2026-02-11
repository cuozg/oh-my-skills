# WebGL Interop Patterns

This guide covers communication between Unity (C#) and the Web Browser (JavaScript).

## 1. C# calling JavaScript (DLLImport)

### JavaScript Plugin (.jslib)
Place this in `Assets/Plugins/WebGL/MyPlugin.jslib`.

```javascript
mergeInto(LibraryManager.library, {
  Hello: function () {
    window.alert("Hello, world!");
  },

  HelloString: function (str) {
    window.alert(Pointer_stringify(str));
  },

  PrintFloatArray: function (array, size) {
    for(var i = 0; i < size; i++)
      console.log(HEAPF32[(array >> 2) + i]);
  },

  AddNumbers: function (x, y) {
    return x + y;
  },

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
      unityInstance.SendMessage('JSInteropManager', 'OnJSCallback', JSON.stringify({
        name: name,
        data: data
      }));
    };
  }
});
```

### C# Wrapper
```csharp
using System.Runtime.InteropServices;

public class JSBinding : MonoBehaviour {
    [DllImport("__Internal")]
    private static extern void Hello();

    [DllImport("__Internal")]
    private static extern void HelloString(string str);

    [DllImport("__Internal")]
    private static extern void PrintFloatArray(float[] array, int size);

    [DllImport("__Internal")]
    private static extern int AddNumbers(int x, int y);

    [DllImport("__Internal")]
    private static extern string StringReturnValueFunction();

    void Start() {
        Hello();
        HelloString("This is a string.");
        float[] myArray = new float[10];
        PrintFloatArray(myArray, myArray.Length);
        int result = AddNumbers(5, 7);
        Debug.Log(StringReturnValueFunction());
    }
}
```

## 2. JavaScript calling C# (SendMessage)

JavaScript can call a method on a GameObject in Unity using:
`unityInstance.SendMessage(gameObject, methodName, value);`

- **gameObject**: Name of the object in your scene.
- **methodName**: Name of the method to call.
- **value**: A single string, integer, or float.

### Example callback listener
```csharp
public class JSInteropManager : MonoBehaviour {
    public void OnJSCallback(string json) {
        var callback = JsonUtility.FromJson<JSCallbackData>(json);
        // Dispatch to internal listeners...
    }
}
```

## 3. Best Practices
- **Minimize Interop Calls**: Crossing the boundary is expensive. Frequent updates (per frame) should be avoided.
- **String Handling**: Use `Pointer_stringify` (Legacy) or modern Emscripten string helpers.
- **Memory Safety**: Be careful with `_malloc` and Ensure strings returned to C# are managed correctly by the bridge.

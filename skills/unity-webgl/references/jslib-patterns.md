# JSLib Interop Patterns

## File Location & Structure

Place `.jslib` files in `Assets/Plugins/WebGL/`. Unity only includes them in WebGL builds.

```
Assets/
  Plugins/
    WebGL/
      BrowserBridge.jslib      // browser API wrappers
      ClipboardPlugin.jslib    // clipboard access
      StoragePlugin.jslib      // localStorage/sessionStorage
```

## Basic Pattern

### JavaScript Side (.jslib)

```javascript
mergeInto(LibraryManager.library, {

  ShowAlert: function (messagePtr) {
    window.alert(UTF8ToString(messagePtr));
  },

  GetWindowWidth: function () {
    return window.innerWidth;
  }

});
```

### C# Side

```csharp
using System.Runtime.InteropServices;
using UnityEngine;

public static class BrowserBridge
{
#if UNITY_WEBGL && !UNITY_EDITOR
    [DllImport("__Internal")]
    private static extern void ShowAlert(string message);

    [DllImport("__Internal")]
    private static extern int GetWindowWidth();
#endif

    public static void Alert(string message)
    {
#if UNITY_WEBGL && !UNITY_EDITOR
        ShowAlert(message);
#else
        Debug.Log($"[BrowserBridge] Alert: {message}");
#endif
    }

    public static int WindowWidth
    {
        get
        {
#if UNITY_WEBGL && !UNITY_EDITOR
            return GetWindowWidth();
#else
            return Screen.width;
#endif
        }
    }
}
```

## String Marshalling

### C# → JS (incoming strings)

Unity auto-marshals C# strings to UTF-8 pointers. In JS, decode with `UTF8ToString()`:

```javascript
PrintName: function (namePtr) {
  var name = UTF8ToString(namePtr);
  console.log("Hello, " + name);
}
```

### JS → C# (returning strings)

You must allocate a buffer in Emscripten's heap and copy the string into it:

```javascript
GetBrowserLanguage: function () {
  var lang = navigator.language || "en";
  var bufferSize = lengthBytesUTF8(lang) + 1;
  var buffer = _malloc(bufferSize);
  stringToUTF8(lang, buffer, bufferSize);
  return buffer;
}
```

C# side receives it as a `string` automatically:

```csharp
[DllImport("__Internal")]
private static extern string GetBrowserLanguage();
```

### Passing byte arrays

```javascript
ProcessData: function (dataPtr, length) {
  var data = new Uint8Array(HEAPU8.buffer, dataPtr, length);
  // work with data...
}
```

```csharp
[DllImport("__Internal")]
private static extern void ProcessData(byte[] data, int length);

// Call: ProcessData(myBytes, myBytes.Length);
```

## Common Browser API Wrappers

### URL Parameters

```javascript
GetURLParam: function (keyPtr) {
  var key = UTF8ToString(keyPtr);
  var value = new URLSearchParams(window.location.search).get(key) || "";
  var bufferSize = lengthBytesUTF8(value) + 1;
  var buffer = _malloc(bufferSize);
  stringToUTF8(value, buffer, bufferSize);
  return buffer;
}
```

### LocalStorage

```javascript
SetLocalStorage: function (keyPtr, valuePtr) {
  localStorage.setItem(UTF8ToString(keyPtr), UTF8ToString(valuePtr));
},

GetLocalStorage: function (keyPtr) {
  var value = localStorage.getItem(UTF8ToString(keyPtr)) || "";
  var bufferSize = lengthBytesUTF8(value) + 1;
  var buffer = _malloc(bufferSize);
  stringToUTF8(value, buffer, bufferSize);
  return buffer;
},

RemoveLocalStorage: function (keyPtr) {
  localStorage.removeItem(UTF8ToString(keyPtr));
}
```

### Clipboard (requires user gesture)

```javascript
CopyToClipboard: function (textPtr) {
  var text = UTF8ToString(textPtr);
  navigator.clipboard.writeText(text).catch(function(err) {
    // Fallback for older browsers
    var textarea = document.createElement("textarea");
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
  });
}
```

Note: clipboard read requires explicit browser permission and must be triggered by a user interaction (click/key). Schedule clipboard access from a UI callback, not from Update().

### Fullscreen Toggle

```javascript
ToggleFullscreen: function () {
  var canvas = document.getElementById("unity-canvas");
  if (!document.fullscreenElement) {
    canvas.requestFullscreen().catch(function(err) {
      console.warn("Fullscreen request failed: " + err.message);
    });
  } else {
    document.exitFullscreen();
  }
}
```

### Open URL in New Tab

```javascript
OpenURL: function (urlPtr) {
  window.open(UTF8ToString(urlPtr), "_blank");
}
```

## JS → C# Communication

When JS needs to call back into Unity, use `SendMessage` (the only built-in option):

```javascript
// From any JS context:
myUnityInstance.SendMessage("GameManager", "OnAuthComplete", jsonDataString);
```

- First arg: GameObject name in scene
- Second arg: method name (must be `public void MethodName(string param)`)
- Third arg: single string parameter

For complex data, serialize to JSON in JS and deserialize in C#.

## Naming Conventions

- File: `{Purpose}Plugin.jslib` (e.g., `ClipboardPlugin.jslib`, `AnalyticsPlugin.jslib`)
- C# bridge: `{Purpose}Bridge.cs` or `WebGL{Purpose}.cs`
- JS functions: PascalCase to match C# extern declarations
- Guard all call sites: `#if UNITY_WEBGL && !UNITY_EDITOR`

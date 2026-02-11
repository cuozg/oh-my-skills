# Mobile Native Interop Patterns

Guide for communication between Unity (C#) and native iOS (Objective-C/Swift) and Android (Java/Kotlin).

## 1. Android Interop (JNI)

### Calling Java from C#
```csharp
using UnityEngine;

public class AndroidNative {
    public void Vibrate(long milliseconds) {
        #if UNITY_ANDROID && !UNITY_EDITOR
        using (AndroidJavaClass unityPlayer = new AndroidJavaClass("com.unity3d.player.UnityPlayer"))
        using (AndroidJavaObject currentActivity = unityPlayer.GetStatic<AndroidJavaObject>("currentActivity"))
        using (AndroidJavaObject vibrator = currentActivity.Call<AndroidJavaObject>("getSystemService", "vibrator")) {
            vibrator.Call("vibrate", milliseconds);
        }
        #endif
    }
}
```

### Calling C# from Java
In your Java/Kotlin code:
```java
com.unity3d.player.UnityPlayer.UnitySendMessage("NativeManager", "OnNativeCallback", "DataString");
```
- **NativeManager**: Name of the GameObject in Unity.
- **OnNativeCallback**: Name of the public method in C#.
- **DataString**: A single string parameter.

## 2. iOS Interop (Objective-C)

### Calling Objective-C from C#
Place this in `Assets/Plugins/iOS/NativeBridge.mm`:
```objectivec
#import <Foundation/Foundation.h>

extern "C" {
    void _NativeVibrate() {
        // iOS vibration implementation
    }
}
```

In your C# file:
```csharp
using System.Runtime.InteropServices;

public class IOSNative {
    [DllImport("__Internal")]
    private static extern void _NativeVibrate();

    public void Vibrate() {
        #if UNITY_IOS && !UNITY_EDITOR
        _NativeVibrate();
        #endif
    }
}
```

### Calling C# from Objective-C
```objectivec
UnitySendMessage("NativeManager", "OnNativeCallback", "DataString");
```

## 3. Best Practices
- **Conditional Compilation**: Always wrap native calls in `#if UNITY_ANDROID` or `#if UNITY_IOS`.
- **String Handling**: Native strings passed back to Unity are usually copied. Be aware of memory allocations.
- **Async Handling**: Native prompts (like IAP or Permissions) are asynchronous. Use delegates or `TaskCompletionSource` to handle responses in C#.
- **Plugin Management**: Use `Assets/Plugins/` to organize native libraries (`.jar`, `.aar`, `.framework`).

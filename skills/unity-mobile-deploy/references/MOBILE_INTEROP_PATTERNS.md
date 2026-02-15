# Mobile Native Interop Patterns

## 1. Android Interop (JNI)

### C# → Java
```csharp
#if UNITY_ANDROID && !UNITY_EDITOR
using var unityPlayer = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
using var activity = unityPlayer.GetStatic<AndroidJavaObject>("currentActivity");
using var vibrator = activity.Call<AndroidJavaObject>("getSystemService", "vibrator");
vibrator.Call("vibrate", milliseconds);
#endif
```

### Java → C#
```java
UnityPlayer.UnitySendMessage("NativeManager", "OnNativeCallback", "DataString");
```

## 2. iOS Interop (Objective-C)

### C# → Objective-C
`Assets/Plugins/iOS/NativeBridge.mm`:
```objectivec
extern "C" { void _NativeVibrate() { /* iOS impl */ } }
```
C#:
```csharp
[DllImport("__Internal")] private static extern void _NativeVibrate();
#if UNITY_IOS && !UNITY_EDITOR
_NativeVibrate();
#endif
```

### Objective-C → C#
```objectivec
UnitySendMessage("NativeManager", "OnNativeCallback", "DataString");
```

## 3. Best Practices
- Always wrap native calls in `#if UNITY_ANDROID` / `#if UNITY_IOS`
- Native strings passed to Unity are copied — watch allocations
- Native prompts (IAP, Permissions) are async — use delegates or `TaskCompletionSource`
- Organize native libs in `Assets/Plugins/` (`.jar`, `.aar`, `.framework`)

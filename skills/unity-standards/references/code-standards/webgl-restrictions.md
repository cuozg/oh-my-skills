# WebGL Platform Restrictions

## Unsupported APIs

These .NET/Unity APIs are unavailable or severely limited in WebGL builds:

| Category | Restricted | Reason | Workaround |
|----------|-----------|--------|------------|
| **Threading** | `System.Threading`, `Thread`, `Task.Run`, `Parallel.*` | Browser is single-threaded (no pthreads by default) | Use coroutines, `UniTask`, or split work across frames |
| **File System** | `System.IO.File`, `Directory`, `FileStream` | No local filesystem access | Use `PlayerPrefs`, IndexedDB via JSLib, or `Application.persistentDataPath` (mapped to IndexedDB) |
| **Networking** | `System.Net.Sockets`, `TcpClient`, `UdpClient` | No raw socket access in browsers | Use `UnityWebRequest`, WebSocket via JSLib, or WebRTC |
| **Reflection** | Partial — `MakeGenericType`, `Emit`, dynamic codegen | IL2CPP compiles AOT; no JIT | Pre-register types, use `linker.xml` to preserve, avoid `Activator.CreateInstance` on stripped types |
| **Dynamic Loading** | `Assembly.Load`, `AppDomain` | AOT compilation only | Bundle all code at build time; use Addressables for assets |
| **Clipboard** | `GUIUtility.systemCopyBuffer` (limited) | Browser clipboard requires user gesture | Use JSLib wrapper calling `navigator.clipboard` API |
| **Audio** | AudioSource may not play without user gesture | Browser autoplay policy | Start audio from a user-initiated event (button click) |

## Conditional Compilation

Always guard WebGL-specific code:

```csharp
#if UNITY_WEBGL && !UNITY_EDITOR
    // WebGL-only code (runs in browser)
    WebGLBridge.DoSomething();
#elif UNITY_EDITOR
    // Editor fallback for testing
    Debug.Log("WebGL call simulated in editor");
#else
    // Non-WebGL platform fallback
    NativePlatformAlternative();
#endif
```

Guard patterns:
- `#if UNITY_WEBGL` — true in both editor (when WebGL target selected) and builds
- `#if UNITY_WEBGL && !UNITY_EDITOR` — true only in actual WebGL builds
- `#if !UNITY_WEBGL` — exclude code from WebGL builds entirely

## Performance Constraints

### Garbage Collection
GC only runs at **end of frame**. In-frame allocations accumulate without collection.

**Dangerous pattern:**
```csharp
// BAD: OOM risk in WebGL — thousands of string allocations, no GC until frame ends
for (int i = 0; i < 10000; i++)
    result += items[i].ToString() + ", ";
```

**Safe alternative:**
```csharp
// GOOD: Single StringBuilder allocation
var sb = new StringBuilder(10000 * 8);
for (int i = 0; i < 10000; i++)
{
    if (i > 0) sb.Append(", ");
    sb.Append(items[i]);
}
result = sb.ToString();
```

### No Background Threads
All code runs on the main thread. Heavy computation blocks rendering.

**Mitigation:** Split expensive work across frames using coroutines:
```csharp
IEnumerator ProcessInChunks<T>(IList<T> items, int chunkSize, System.Action<T> process)
{
    for (int i = 0; i < items.Count; i++)
    {
        process(items[i]);
        if (i % chunkSize == 0)
            yield return null; // yield to prevent frame stall
    }
}
```

### Memory Budget
Total browser memory = Unity heap + decompressed assets + JS context + DOM.
- Desktop Chrome: ~2-4GB available
- Mobile Safari: ~1-1.5GB before tab crashes
- Mobile Chrome: ~1-2GB

Target 256-512MB Unity heap for broad compatibility.

## Common WebGL Build Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `EntryPointNotFoundException` | Method stripped by IL2CPP | Add type to `linker.xml` |
| `TypeLoadException` | Type stripped or generic not AOT-compiled | Add `[Preserve]` attribute or `linker.xml` entry |
| `NotSupportedException: System.Threading` | Threading API used in WebGL code path | Guard with `#if !UNITY_WEBGL` |
| `Out of memory` | Unity heap exceeded browser limit | Reduce initial memory, enable memory growth, optimize assets |
| MIME type error loading `.wasm` | Server not configured | Set `application/wasm` MIME type |
| `.br` files not decompressing | Missing `Content-Encoding: br` header | Configure server headers |

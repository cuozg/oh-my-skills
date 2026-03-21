# Web Platform Restrictions

## Treat These As Safe Defaults

Web platform behavior shifts across Unity versions, browser versions, and hosting setups. This file captures conservative guidance that is usually safe. For exact support claims, cross-check `references/other/official-source-map.md`.

## Unsupported Or Constrained APIs

| Category | Restricted | Reason | Workaround |
|----------|-----------|--------|------------|
| Threading | Assume no usable gameplay background threads by default | Web builds are heavily constrained by browser and hosting requirements | Split work across frames, coroutines, Awaitable, or UniTask |
| File system | `System.IO.File`, `Directory`, `FileStream` for arbitrary local paths | Browser sandbox | Use `Application.persistentDataPath`, IndexedDB, server-backed saves, or a JSLib bridge |
| Networking | `System.Net.Sockets`, `TcpClient`, `UdpClient` | No raw socket access in browsers | Use `UnityWebRequest`, WebSocket via JSLib, or WebRTC |
| Reflection and codegen | Dynamic code generation, `Emit`, runtime assembly loading | IL2CPP AOT | Pre-register types, preserve with `linker.xml`, avoid runtime codegen assumptions |
| Dynamic loading | `Assembly.Load`, `AppDomain` | Code is compiled ahead of time into Wasm | Bundle code at build time; use Addressables for assets |
| Clipboard and browser APIs | Unity wrappers may be limited | Browser security policies require user gesture or JS interop | Use a JSLib wrapper and a user-initiated flow |
| Audio autoplay | Audio may not start automatically | Browser autoplay policy | Start or unlock audio from user input |

## Conditional Compilation

Always guard Web-specific code explicitly.

```csharp
#if UNITY_WEBGL && !UNITY_EDITOR
    WebGLBridge.DoSomething();
#elif UNITY_EDITOR
    Debug.Log("Web call simulated in editor");
#else
    NativePlatformAlternative();
#endif
```

Guard patterns:
- `#if UNITY_WEBGL` - true when compiling for Web platform
- `#if UNITY_WEBGL && !UNITY_EDITOR` - true only in an actual build, not the editor
- `#if !UNITY_WEBGL` - exclude incompatible code paths entirely

## Performance Constraints

### Allocation Pressure

Per-frame allocation spikes are extra painful on the Web because memory pressure and garbage collection interact with the browser runtime.

```csharp
// Avoid repeated string growth in hot paths
var sb = new StringBuilder(items.Count * 8);
for (int i = 0; i < items.Count; i++)
{
    if (i > 0) sb.Append(", ");
    sb.Append(items[i]);
}
result = sb.ToString();
```

### Heavy Work

Do not assume background threads will save a heavy gameplay algorithm on Web. Design a frame-sliced fallback first.

```csharp
IEnumerator ProcessInChunks<T>(IList<T> items, int chunkSize, System.Action<T> process)
{
    for (int i = 0; i < items.Count; i++)
    {
        process(items[i]);
        if ((i + 1) % chunkSize == 0)
            yield return null;
    }
}
```

### Memory Budget

Browser memory ceilings vary widely by browser, OS, and device class. Profile on the actual target browsers instead of relying on a single hard budget number.

Guidance:
- Keep initial heap modest.
- Prefer streaming and incremental loading.
- Reduce texture and audio memory aggressively for browser builds.
- Test low-memory failure behavior on target hardware.

## Common Web Build Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `EntryPointNotFoundException` | Method stripped by IL2CPP | Add preserve attributes or `linker.xml` |
| `TypeLoadException` | Type stripped or generic not AOT-compiled | Preserve types explicitly |
| `NotSupportedException: System.Threading` | Threading API reached on Web code path | Guard or redesign the code path |
| `Out of memory` | Heap or decompressed assets exceed browser limits | Reduce memory footprint and loading burst size |
| MIME type error loading `.wasm` | Server misconfiguration | Serve the correct MIME type |
| `.br` files not decompressing | Missing `Content-Encoding: br` header | Fix server headers |

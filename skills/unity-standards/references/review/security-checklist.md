# Security Checklist

## Input Validation

- [ ] User text input length-capped before processing
- [ ] Numeric inputs clamped to valid ranges (`Mathf.Clamp`)
- [ ] File paths sanitized — no `..` traversal, whitelist allowed directories
- [ ] Player names stripped of HTML/rich text tags
- [ ] Deserialized data validated before use (don't trust save files)

```csharp
// BAD: Unclamped input
public void SetVolume(float vol) => AudioListener.volume = vol;

// GOOD: Clamped
public void SetVolume(float vol) => AudioListener.volume = Mathf.Clamp01(vol);
```

## Data Storage

| Storage | Security | Use For |
|---------|----------|---------|
| `PlayerPrefs` | Plain text, easily edited | Non-sensitive settings only |
| Local JSON file | Readable on disk | Game progress (with integrity hash) |
| Encrypted file | Tamper-resistant | Purchases, unlocks |
| Server-side | Most secure | Multiplayer state, leaderboards |

- [ ] No secrets in `PlayerPrefs` (tokens, passwords, keys)
- [ ] No API keys in client code — use server proxy
- [ ] Save file integrity: hash or HMAC to detect tampering
- [ ] Sensitive data wiped from memory after use (`Array.Clear`)

## ScriptableObject Exposure

- [ ] SO assets in builds are readable — no secrets in SO fields
- [ ] Runtime SO clones (`Instantiate`) don't persist sensitive data
- [ ] Editor-only SO data stripped from builds via `#if UNITY_EDITOR`

## Debug Code in Builds

- [ ] Debug panels wrapped in `#if UNITY_EDITOR || DEVELOPMENT_BUILD`
- [ ] Cheat commands stripped from release builds
- [ ] `Debug.Log` calls stripped or compiled out in production
- [ ] Test scenes excluded from build settings

```csharp
// Guard debug features
#if UNITY_EDITOR || DEVELOPMENT_BUILD
[SerializeField] private bool enableCheats;
#endif

// Conditional compilation for logs
[System.Diagnostics.Conditional("UNITY_EDITOR")]
private static void DebugLog(string msg) => Debug.Log(msg);
```

## Network / Multiplayer

- [ ] Server authoritative — client sends intent, server validates
- [ ] Rate limiting on client actions (prevent spam/flood)
- [ ] Packet data validated: bounds, types, sequence
- [ ] No client-side trust for damage, currency, position
- [ ] TLS/SSL for all network communication

## Injection Prevention

- [ ] SQL queries parameterized (if using SQLite/backend)
- [ ] No `System.Reflection.Assembly.Load` from user input
- [ ] Rich text tags filtered from user-generated content
- [ ] Asset bundle sources validated (hash check, trusted CDN)

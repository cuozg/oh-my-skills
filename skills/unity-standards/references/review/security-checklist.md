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

## Memory Security

- [ ] Sensitive strings (tokens, passwords) cleared after use: `Array.Clear(charArray, 0, charArray.Length)`
- [ ] Use `SecureString` or `char[]` instead of `string` for passwords (strings are immutable, linger in memory)
- [ ] Crypto keys wiped: `System.Security.Cryptography.CryptographicOperations.ZeroMemory(keySpan)`
- [ ] No sensitive data in `Debug.Log` statements

```csharp
// BAD: password as string — stays in managed heap
string password = inputField.text;

// GOOD: char array — can be zeroed
char[] password = new char[inputField.text.Length];
inputField.text.CopyTo(0, password, 0, password.Length);
try { Authenticate(password); }
finally { Array.Clear(password, 0, password.Length); }
```

## IL2CPP & Code Protection

- [ ] IL2CPP backend enabled for release builds (converts C# to C++ — harder to reverse)
- [ ] `link.xml` preserves types needed via reflection (prevents stripping needed code)
- [ ] `[Preserve]` attribute on reflection-accessed types
- [ ] No business logic in Lua/interpreted scripts (easily readable)

```xml
<!-- link.xml — prevent IL2CPP from stripping -->
<linker>
    <assembly fullname="Game.Core">
        <type fullname="Game.Core.SaveData" preserve="all"/>
    </assembly>
</linker>
```

## Anti-Tamper

- [ ] Build hash/checksum verified on startup (detect modified binaries)
- [ ] Time-based checks for speedhack detection: `Time.realtimeSinceStartup` vs `System.DateTime`
- [ ] Critical calculations server-side (currency, damage, progression)
- [ ] PlayerPrefs integrity: store HMAC alongside values

```csharp
// HMAC integrity for local data
using System.Security.Cryptography;
static string ComputeHMAC(string data, byte[] key)
{
    using var hmac = new HMACSHA256(key);
    var hash = hmac.ComputeHash(System.Text.Encoding.UTF8.GetBytes(data));
    return System.Convert.ToBase64String(hash);
}
```

## Secure Randomness

- [ ] `UnityEngine.Random` for gameplay (deterministic, seedable)
- [ ] `System.Security.Cryptography.RandomNumberGenerator` for tokens, keys, nonces

```csharp
using System.Security.Cryptography;
byte[] token = new byte[32];
RandomNumberGenerator.Fill(token); // cryptographically secure
string tokenStr = Convert.ToBase64String(token);
```

## Certificate Pinning (Network)

- [ ] TLS certificate validated — pin public key hash for sensitive APIs
- [ ] `UnityWebRequest.certificateHandler` implemented for custom validation
- [ ] No HTTP — all communication over HTTPS

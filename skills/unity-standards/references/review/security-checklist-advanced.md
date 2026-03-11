# Security Checklist — Advanced

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

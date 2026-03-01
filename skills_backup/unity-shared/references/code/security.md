## Serialization Safety
- `BinaryFormatter` is BANNED (RCE vulnerability, Microsoft deprecated).
- `JsonUtility`: Safe by design (no type resolution).
- Newtonsoft: ALWAYS use `TypeNameHandling.None`.
- Network: Use MessagePack or MemoryPack (schema-bound, no type injection).

## Data Integrity
- HMAC-SHA256 for save file signing (compute on save, verify on load).
- `CryptographicOperations.FixedTimeEquals` for timing-safe comparison.
- Encrypted PlayerPrefs: AES-128 minimum for sensitive data.
```csharp
public static byte[] ComputeHmac(byte[] data, byte[] key) {
    using var hmac = new System.Security.Cryptography.HMACSHA256(key);
    return hmac.ComputeHash(data);
}
```

## Memory & Anti-Cheat
- SecureInt pattern: XOR with random key, re-randomize on set.
- Server-side canonical for competitive games.
- ACTk (Anti-Cheat Toolkit) for ObscuredInt/ObscuredFloat if needed.

## Input Validation
- Server-authoritative RPC validation (never trust client).
- NGO (Netcode for GameObjects): `SenderClientId` is spoofable (issue #3015).
- Validate ALL RPC parameters: range checks, null checks, rate limiting.

## Network Security
- `CertificateHandler`: pin PUBLIC KEY hash, not certificate (certs rotate).
- HMAC payload signing with ±30s timestamp for replay protection.
- TLS 1.2+ minimum.

## AssetBundle Integrity
- Always load via HTTPS + CRC verification.
- LZMA safe, LZ4 needs careful decompression bounds.
- NEVER accept user-uploaded AssetBundles.

## Build Security
- IL2CPP always for release builds (not protection, but friction).
- Managed Stripping Level: High + `link.xml` for preserved types.
- Obfuscation: Obfuscator Pro / Beebyte / GuardingPear as friction layer.

## Secure Coding
- `CryptographicOperations.FixedTimeEquals`, never `==` for secrets.
- No secrets in client binary (API keys, passwords).
- `RandomNumberGenerator.Fill`, NEVER `System.Random` for crypto.
- Parameterized queries if using SQLite.

## Pre-Release Checklist
- [ ] IL2CPP Enabled
- [ ] Managed Stripping: High
- [ ] No `Debug.Log` in prod
- [ ] HTTPS Enforced
- [ ] Saves Cryptographically Signed
- [ ] Server Validates RPC Input
- [ ] Obfuscation Applied
- [ ] Public Key Pinned
- [ ] No Embedded Secrets
- [ ] Network Rate Limiting
- [ ] Anti-Cheat/Tamper Enabled
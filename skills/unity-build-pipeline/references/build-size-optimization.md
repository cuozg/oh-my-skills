# Build Size Optimization

Strategies for reducing build size across textures, audio, code, and assets.

## Optimization Checklist

| Area | Action | Typical Savings |
|:-----|:-------|:---------------|
| Textures | Max 1024 for mobile, ASTC/ETC2 | 20-40% |
| Audio | Vorbis compression, quality 70% | 10-20% |
| Code stripping | IL2CPP + High stripping level | 5-15% |
| Unused assets | Remove from Resources, use Addressables | 10-30% |
| Shaders | Strip unused variants | 5-20% |

## Detailed Strategies

### Textures

- Compress to ASTC (iOS) or ETC2 (Android)
- Limit max size to 1024×1024 for mobile
- Use MipMaps for static textures
- Disable mipmaps for UI textures

### Audio

- Convert to Vorbis format in import settings
- Set quality to 70% (good tradeoff)
- Remove .wav raw audio files after conversion

### Code Stripping

- Use IL2CPP for release builds
- Set `Managed Stripping Level: High` in PlayerSettings
- Test thoroughly; High may strip needed reflection APIs

### Addressables

- Use Addressables instead of Resources folder
- Load only needed content
- Group by download size/frequency

### Shaders

- Strip unused shader variants via `ShaderVariantCollection`
- Set `Shader Stripping: Aggressive`
- Pre-build variants for your target hardware

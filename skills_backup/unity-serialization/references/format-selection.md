# Format Selection Guide

## Comparison Table

| Format | Best For | Pros | Cons |
|:-------|:---------|:-----|:-----|
| **JsonUtility** | Simple Unity types | Fast, built-in, native Unity types | No polymorphism/Dictionary/null |
| **Newtonsoft.Json** | Complex/polymorphic, APIs | Full JSON, custom converters, LINQ | External dependency, slower |
| **Custom binary** | Large datasets, perf-critical | Smallest files, fastest I/O | Manual implementation |
| **ScriptableObject** | Design-time configs | Inspector-editable, hot-reload | Not for runtime persistence |
| **PlayerPrefs** | Small settings | Simplest API, cross-platform | String keys, limited size |

## Decision Flow

```
Settings/preferences       → PlayerPrefs wrapper
Designer-authored configs  → ScriptableObject containers
Runtime game state         → JSON file (JsonUtility or Newtonsoft)
Large binary data          → Custom binary format
Server communication       → Newtonsoft.Json
```

## JsonUtility vs Newtonsoft.Json

| Feature | JsonUtility | Newtonsoft.Json |
|:--------|:------------|:----------------|
| Speed | Fastest (native C++) | Slower (managed) |
| Dictionary/Polymorphism | No | Yes |
| Custom converters | No | Yes |
| Unity types (Vector3) | Native | Requires converters |
| Dependency | Built-in | `com.unity.nuget.newtonsoft-json` |

**Rule**: Start with JsonUtility. Switch to Newtonsoft when you need Dictionary, polymorphism, or custom conversion.

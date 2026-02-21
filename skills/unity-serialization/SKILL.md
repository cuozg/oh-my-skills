---
name: unity-serialization
description: "(opencode-project - Skill) Unity serialization patterns and data persistence. Covers JSON serialization (JsonUtility, Newtonsoft), binary serialization, ScriptableObject data containers, PlayerPrefs, save/load systems, and asset serialization. Use when: (1) Building save/load systems, (2) Serializing complex data structures, (3) Creating ScriptableObject data containers, (4) Working with JSON/binary data, (5) Managing persistent game data. Triggers: 'save system', 'load data', 'serialize', 'deserialize', 'ScriptableObject data', 'JSON', 'PlayerPrefs', 'persistent data'."
---

# unity-serialization — Data Persistence & Serialization

**Input**: Data persistence requirement (what to save/load, frequency, size), target platforms, schema history
**Output**: Data models with attributes, save/load manager, file I/O with error handling, migration logic

## Workflow

1. **Analyze data requirements** — structure, size, access frequency, security needs
2. **Choose serialization strategy** — JsonUtility (simple), Newtonsoft (complex/polymorphic), binary (large)
3. **Design data models** — `[Serializable]` classes with version tags and defaults
4. **Implement save/load manager** — async I/O, error handling, backup/restore
5. **Platform-specific paths** — `Application.persistentDataPath` with platform-aware subdirs
6. **Versioning and migration** — version tags, stepwise migration chain
7. **Test roundtrip** — serialize-deserialize produces identical data, test corruption recovery

## Format Selection

| Format | Best For | Pros | Cons |
|:-------|:---------|:-----|:-----|
| **JsonUtility** | Simple Unity types | Fast, built-in, native Unity types | No polymorphism/Dictionary/null |
| **Newtonsoft.Json** | Complex/polymorphic, APIs | Full JSON, custom converters, LINQ | External dependency, slower |
| **Custom binary** | Large datasets, perf-critical | Smallest files, fastest I/O | Manual implementation |
| **ScriptableObject** | Design-time configs | Inspector-editable, hot-reload | Not for runtime persistence |
| **PlayerPrefs** | Small settings | Simplest API, cross-platform | String keys, limited size |

### Decision Flow

```
Settings/preferences → PlayerPrefs wrapper
Designer-authored configs → ScriptableObject containers
Runtime game state → JSON file (JsonUtility or Newtonsoft)
Large binary data → Custom binary format
Server communication → Newtonsoft.Json
```

## Key Patterns

### Versioned Save Data

```csharp
[Serializable]
public class SaveData
{
    public int version = SaveManager.CurrentVersion;
    public string lastSaveTimestamp;
    public PlayerSaveData player;
    public List<InventoryItemData> inventory;
}

[Serializable]
public class PlayerSaveData
{
    public string displayName;
    public int level;
    public float[] position; // Use float[] instead of Vector3 for portability

    public void SetPosition(Vector3 pos) => position = new[] { pos.x, pos.y, pos.z };
    public Vector3 GetPosition() =>
        position is { Length: >= 3 } ? new Vector3(position[0], position[1], position[2]) : Vector3.zero;
}
```

### Save Manager with Async I/O

```csharp
public class SaveManager : MonoBehaviour
{
    public const int CurrentVersion = 2;
    private const string SaveFileName = "save.json";
    private string SavePath => Path.Combine(Application.persistentDataPath, SaveFileName);
    private string BackupPath => SavePath + ".backup";

    public async Awaitable SaveAsync(SaveData data)
    {
        data.version = CurrentVersion;
        data.lastSaveTimestamp = DateTime.UtcNow.ToString("o");
        string json = JsonUtility.ToJson(data, prettyPrint: true);
        try
        {
            if (File.Exists(SavePath)) File.Copy(SavePath, BackupPath, overwrite: true);
            await File.WriteAllTextAsync(SavePath, json);
        }
        catch (IOException ex) { Debug.LogError($"[SaveManager] Save failed: {ex.Message}"); }
    }

    public async Awaitable<SaveData> LoadAsync()
    {
        SaveData data = await TryLoadFromPath(SavePath);
        if (data == null && File.Exists(BackupPath)) data = await TryLoadFromPath(BackupPath);
        if (data != null && data.version < CurrentVersion) data = MigrationRunner.Migrate(data);
        return data ?? new SaveData();
    }

    private async Awaitable<SaveData> TryLoadFromPath(string path)
    {
        if (!File.Exists(path)) return null;
        try { return JsonUtility.FromJson<SaveData>(await File.ReadAllTextAsync(path)); }
        catch (Exception ex) { Debug.LogError($"[SaveManager] Load failed: {ex.Message}"); return null; }
    }
}
```

### Migration Runner

```csharp
public static class MigrationRunner
{
    private static readonly Dictionary<int, Func<SaveData, SaveData>> Migrations = new()
    {
        { 1, data => { data.inventory ??= new List<InventoryItemData>(); data.version = 2; return data; } },
    };

    public static SaveData Migrate(SaveData data)
    {
        while (data.version < SaveManager.CurrentVersion)
        {
            if (!Migrations.TryGetValue(data.version, out var migrator)) break;
            data = migrator(data);
        }
        return data;
    }
}
```

### Type-Safe PlayerPrefs Wrapper

```csharp
public static class GameSettings
{
    public static float MusicVolume
    {
        get => PlayerPrefs.GetFloat("settings_music_volume", 0.8f);
        set { PlayerPrefs.SetFloat("settings_music_volume", Mathf.Clamp01(value)); PlayerPrefs.Save(); }
    }
    // Same pattern for SfxVolume, Language, etc.
}
```

## Best Practices

### Do
- Version every save format with integer in root object
- Use `Application.persistentDataPath` — never hardcode paths
- Implement backup rotation before overwriting
- Validate after deserialization (null fields, out-of-range values)
- Use `[Serializable]` POCOs separate from MonoBehaviour
- Handle I/O exceptions (permissions, disk full)
- Use async I/O for large files

### Do Not
- **Never use BinaryFormatter** — security vulnerability, deprecated
- Never store gameplay state in PlayerPrefs (settings only)
- Never serialize MonoBehaviour/GameObject references (use IDs/paths)
- Never modify ScriptableObjects at runtime without cloning
- Never assume save files exist — handle missing gracefully
- Never store sensitive data unencrypted

## JsonUtility vs Newtonsoft.Json

| Feature | JsonUtility | Newtonsoft.Json |
|:--------|:------------|:----------------|
| Speed | Fastest (native C++) | Slower (managed) |
| Dictionary/Polymorphism | No | Yes |
| Custom converters | No | Yes |
| Unity types (Vector3) | Native | Requires converters |
| Dependency | Built-in | `com.unity.nuget.newtonsoft-json` |

**Rule**: Start with JsonUtility. Switch to Newtonsoft when you need Dictionary, polymorphism, or custom conversion.

## Handoff & Boundaries

- **Delegates to**: `unity-code-deep` (general C#), `unity-optimize-performance` (large dataset perf), `flatbuffers-coder` (binary serialization)
- **Does NOT handle**: Networking/multiplayer sync, database systems, Asset Bundle serialization, Editor serialization (SerializedObject)

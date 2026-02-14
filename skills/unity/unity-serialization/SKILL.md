---
name: unity-serialization
description: "(opencode-project - Skill) Unity serialization patterns and data persistence. Covers JSON serialization (JsonUtility, Newtonsoft), binary serialization, ScriptableObject data containers, PlayerPrefs, save/load systems, and asset serialization. Use when: (1) Building save/load systems, (2) Serializing complex data structures, (3) Creating ScriptableObject data containers, (4) Working with JSON/binary data, (5) Managing persistent game data. Triggers: 'save system', 'load data', 'serialize', 'deserialize', 'ScriptableObject data', 'JSON', 'PlayerPrefs', 'persistent data'."
---

# unity-serialization — Data Persistence & Serialization

Implement robust data persistence and serialization systems for Unity projects — covering save/load architecture, data format selection, and cross-platform data storage patterns.

## Purpose

Design and build serialization pipelines that reliably persist game data across sessions, platforms, and schema versions. Choose the right serialization format for each use case, implement versioned save systems with migration support, and handle edge cases (corruption, missing files, platform differences) gracefully.

## Input

- **Required**: Data persistence requirement (what data to save/load, frequency, size constraints)
- **Optional**: Target platforms, existing data models, schema version history, security requirements

## Output

Production-ready serialization code: data models with proper attributes, save/load manager, file I/O with error handling, and migration logic if applicable. All code compiles and follows `unity-code` quality standards.

## Examples

| User Request | Skill Action |
|:---|:---|
| "Build a save system for player progress" | Design versioned save format, implement SaveManager with async file I/O, add corruption recovery |
| "Serialize inventory data to JSON" | Create `[Serializable]` data models, implement JsonUtility or Newtonsoft serialization with type handling |
| "Store settings in PlayerPrefs" | Build type-safe PlayerPrefs wrapper with defaults, validation, and clear separation from game saves |
| "Migrate save files from v1 to v2 schema" | Implement version-tagged save format with stepwise migration chain |

## Workflow

1. **Analyze data requirements** — Identify data structure, size, access frequency, and security needs
2. **Choose serialization strategy** — JsonUtility for simple Unity types, Newtonsoft.Json for complex/polymorphic, binary for large datasets
3. **Design data models** — Create `[Serializable]` classes with proper attributes, version tags, and defaults
4. **Implement save/load manager** — Centralized I/O with async operations, error handling, and backup/restore
5. **Add platform-specific path handling** — Use `Application.persistentDataPath` with platform-aware subdirectories
6. **Implement versioning and migration** — Tag saves with version numbers, build migration chain for schema changes
7. **Test serialization roundtrip** — Verify serialize-deserialize produces identical data, test corruption recovery

---

## Serialization Strategy Selection

### Format Comparison

| Format | Best For | Pros | Cons |
|:-------|:---------|:-----|:-----|
| **JsonUtility** | Simple Unity types, quick prototyping | Fast, no dependency, handles Unity types natively | No polymorphism, no Dictionary, no null support |
| **Newtonsoft.Json** | Complex data, polymorphic types, APIs | Full JSON support, custom converters, LINQ-to-JSON | External dependency, slower than JsonUtility |
| **Binary (BinaryFormatter)** | Legacy only | Compact output | Security risk, deprecated — avoid in new code |
| **Binary (custom)** | Large datasets, performance-critical | Smallest file size, fastest I/O | Manual implementation, no human-readable output |
| **ScriptableObject** | Design-time data, configs, shared assets | Inspector-editable, asset references, hot-reload | Not for runtime-generated data persistence |
| **PlayerPrefs** | Small settings (volume, language) | Simplest API, cross-platform | String-based keys, no structured data, limited size |

### Decision Flow

```
What kind of data?
  Settings/preferences (small, simple)
    -> PlayerPrefs wrapper
  Designer-authored configs (items, levels, abilities)
    -> ScriptableObject containers
  Runtime game state (saves, progress, inventory)
    -> JSON file (JsonUtility or Newtonsoft)
  Large binary data (terrain, mesh, replay)
    -> Custom binary format
  Server communication
    -> Newtonsoft.Json (standard JSON)
```

---

## Key Patterns

### Serializable Data Models

```csharp
/// <summary>
/// Root save data container with version tracking for migration support.
/// </summary>
[Serializable]
public class SaveData
{
    public int version = SaveManager.CurrentVersion;
    public string lastSaveTimestamp;
    public PlayerSaveData player;
    public List<InventoryItemData> inventory;
    public Dictionary<string, bool> flags; // Newtonsoft only
}

[Serializable]
public class PlayerSaveData
{
    public string displayName;
    public int level;
    public float experiencePoints;
    public float[] position; // Use float[] instead of Vector3 for portability

    /// <summary>
    /// Convert Unity Vector3 to serializable array.
    /// </summary>
    public void SetPosition(Vector3 pos)
    {
        position = new float[] { pos.x, pos.y, pos.z };
    }

    /// <summary>
    /// Reconstruct Vector3 from serialized array.
    /// </summary>
    public Vector3 GetPosition()
    {
        if (position == null || position.Length < 3) return Vector3.zero;
        return new Vector3(position[0], position[1], position[2]);
    }
}
```

### Save Manager with Async I/O

```csharp
/// <summary>
/// Centralized save/load manager with async file I/O, versioning, and backup.
/// </summary>
public class SaveManager : MonoBehaviour
{
    public const int CurrentVersion = 2;
    private const string SaveFileName = "save.json";
    private const string BackupSuffix = ".backup";

    private string SavePath => Path.Combine(Application.persistentDataPath, SaveFileName);
    private string BackupPath => SavePath + BackupSuffix;

    /// <summary>
    /// Save game data asynchronously with backup rotation.
    /// </summary>
    public async Awaitable SaveAsync(SaveData data)
    {
        data.version = CurrentVersion;
        data.lastSaveTimestamp = DateTime.UtcNow.ToString("o");

        string json = JsonUtility.ToJson(data, prettyPrint: true);

        try
        {
            // Rotate backup before overwriting
            if (File.Exists(SavePath))
            {
                File.Copy(SavePath, BackupPath, overwrite: true);
            }

            await File.WriteAllTextAsync(SavePath, json);
        }
        catch (IOException ex)
        {
            Debug.LogError($"[SaveManager] Failed to write save: {ex.Message}");
        }
    }

    /// <summary>
    /// Load game data with fallback to backup on corruption.
    /// </summary>
    public async Awaitable<SaveData> LoadAsync()
    {
        SaveData data = await TryLoadFromPath(SavePath);

        // Fallback to backup if primary is missing or corrupt
        if (data == null && File.Exists(BackupPath))
        {
            Debug.LogWarning("[SaveManager] Primary save corrupt, loading backup.");
            data = await TryLoadFromPath(BackupPath);
        }

        // Apply migrations if needed
        if (data != null && data.version < CurrentVersion)
        {
            data = MigrationRunner.Migrate(data);
        }

        return data ?? new SaveData();
    }

    private async Awaitable<SaveData> TryLoadFromPath(string path)
    {
        if (!File.Exists(path)) return null;

        try
        {
            string json = await File.ReadAllTextAsync(path);
            return JsonUtility.FromJson<SaveData>(json);
        }
        catch (Exception ex)
        {
            Debug.LogError($"[SaveManager] Failed to load from {path}: {ex.Message}");
            return null;
        }
    }
}
```

### Save File Versioning and Migration

```csharp
/// <summary>
/// Stepwise migration runner — upgrades save data one version at a time.
/// </summary>
public static class MigrationRunner
{
    private static readonly Dictionary<int, Func<SaveData, SaveData>> Migrations = new()
    {
        { 1, MigrateV1ToV2 },
        // { 2, MigrateV2ToV3 },
    };

    public static SaveData Migrate(SaveData data)
    {
        while (data.version < SaveManager.CurrentVersion)
        {
            if (!Migrations.TryGetValue(data.version, out var migrator))
            {
                Debug.LogError($"[Migration] No migration path from v{data.version}");
                break;
            }
            data = migrator(data);
            Debug.Log($"[Migration] Migrated save to v{data.version}");
        }
        return data;
    }

    private static SaveData MigrateV1ToV2(SaveData data)
    {
        // Example: v2 added inventory system
        data.inventory ??= new List<InventoryItemData>();
        data.version = 2;
        return data;
    }
}
```

### Type-Safe PlayerPrefs Wrapper

```csharp
/// <summary>
/// Type-safe wrapper over PlayerPrefs with default values and clear key management.
/// </summary>
public static class GameSettings
{
    private const string KeyMusicVolume = "settings_music_volume";
    private const string KeySfxVolume = "settings_sfx_volume";
    private const string KeyLanguage = "settings_language";

    public static float MusicVolume
    {
        get => PlayerPrefs.GetFloat(KeyMusicVolume, 0.8f);
        set { PlayerPrefs.SetFloat(KeyMusicVolume, Mathf.Clamp01(value)); PlayerPrefs.Save(); }
    }

    public static float SfxVolume
    {
        get => PlayerPrefs.GetFloat(KeySfxVolume, 1.0f);
        set { PlayerPrefs.SetFloat(KeySfxVolume, Mathf.Clamp01(value)); PlayerPrefs.Save(); }
    }

    public static string Language
    {
        get => PlayerPrefs.GetString(KeyLanguage, "en");
        set { PlayerPrefs.SetString(KeyLanguage, value); PlayerPrefs.Save(); }
    }

    /// <summary>
    /// Reset all settings to defaults.
    /// </summary>
    public static void ResetToDefaults()
    {
        PlayerPrefs.DeleteKey(KeyMusicVolume);
        PlayerPrefs.DeleteKey(KeySfxVolume);
        PlayerPrefs.DeleteKey(KeyLanguage);
        PlayerPrefs.Save();
    }
}
```

---

## Best Practices

### Do

- **Version every save format** — Include a version integer in every serialized root object
- **Use `Application.persistentDataPath`** — Never hardcode paths; this is the only cross-platform safe location
- **Implement backup rotation** — Copy existing save before overwriting to prevent data loss
- **Validate after deserialization** — Check for null fields, out-of-range values, and missing collections
- **Use `[Serializable]` POCOs for data** — Separate data models from MonoBehaviour logic
- **Handle I/O exceptions** — File operations can fail (permissions, disk full, concurrent access)
- **Use async I/O for large files** — Prevent frame hitches during save/load
- **Test on all target platforms** — File system behavior varies (case sensitivity, path separators, sandboxing)

### Do Not

- **Never use BinaryFormatter** — Security vulnerability (arbitrary code execution via crafted payloads), deprecated by Microsoft
- **Never store gameplay state in PlayerPrefs** — PlayerPrefs is for small settings only; it is not encrypted, easily editable, and has size limits
- **Never serialize MonoBehaviour or GameObject references** — Use IDs or paths to reconstruct references after load
- **Never modify ScriptableObjects at runtime without cloning** — Changes persist in Editor and affect all references
- **Never assume save files exist** — Always handle missing file case gracefully
- **Never store sensitive data unencrypted** — Use platform encryption APIs or AES for player-sensitive data

---

## JsonUtility vs Newtonsoft.Json

| Feature | JsonUtility | Newtonsoft.Json |
|:--------|:------------|:----------------|
| Speed | Fastest (native C++) | Slower (managed C#) |
| Dictionary support | No | Yes |
| Polymorphism | No | Yes (`TypeNameHandling`) |
| Null handling | Skips nulls | Configurable |
| Custom converters | No | Yes (`JsonConverter`) |
| Unity types (Vector3, Color) | Native support | Requires custom converters |
| Pretty print | Yes | Yes |
| Dependency | Built-in | Package: `com.unity.nuget.newtonsoft-json` |

**Rule of thumb**: Start with JsonUtility. Switch to Newtonsoft only when you need Dictionary, polymorphism, or custom conversion.

---

## Handoff & Boundaries

### Delegates To

| Skill | When |
|:------|:-----|
| `unity-code` | General C# implementation beyond serialization-specific patterns |
| `unity-optimize-performance` | Large dataset serialization causing frame drops or memory pressure |
| `flatbuffers-coder` | High-performance binary serialization for data tables and network payloads |

### Does Not Handle

- **Networking/multiplayer sync** — Serialization for network transport is handled by networking-specific code
- **Database systems** — SQLite, cloud databases, or server-side persistence are outside scope
- **Asset Bundle serialization** — Build pipeline asset packaging belongs to `unity-build-pipeline`
- **Editor serialization (SerializedObject/SerializedProperty)** — Inspector and Editor tooling belongs to `unity-editor-tools`

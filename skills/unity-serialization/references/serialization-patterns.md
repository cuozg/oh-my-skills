# Serialization Patterns

## Versioned Save Data

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

## Save Manager with Async I/O
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

## Migration Runner
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

## Type-Safe PlayerPrefs Wrapper
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

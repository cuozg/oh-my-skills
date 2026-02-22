---
name: unity-serialization
description: "(opencode-project - Skill) Unity serialization patterns and data persistence. Covers JSON serialization (JsonUtility, Newtonsoft), binary serialization, ScriptableObject data containers, PlayerPrefs, save/load systems, and asset serialization. Use when: (1) Building save/load systems, (2) Serializing complex data structures, (3) Creating ScriptableObject data containers, (4) Working with JSON/binary data, (5) Managing persistent game data. Triggers: 'save system', 'load data', 'serialize', 'deserialize', 'ScriptableObject data', 'JSON', 'PlayerPrefs', 'persistent data'."
---

# unity-serialization — Data Persistence & Serialization

**Input**: Data persistence requirement (what to save/load, frequency, size), target platforms, schema history

## Output
Production-ready C# serialization code following the patterns in `references/`.

## Workflow

1. **Analyze data requirements** — structure, size, access frequency, security needs
2. **Choose serialization strategy** — see `references/format-selection.md` for comparison
3. **Design data models** — `[Serializable]` classes with version tags and defaults
4. **Implement save/load manager** — async I/O, error handling, backup/restore (see `references/serialization-patterns.md`)
5. **Platform-specific paths** — `Application.persistentDataPath` with platform-aware subdirs
6. **Versioning and migration** — version tags, stepwise migration chain
7. **Test roundtrip** — serialize-deserialize produces identical data, test corruption recovery

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

## References

- `references/format-selection.md` — format comparison table, decision flow, JsonUtility vs Newtonsoft
- `references/serialization-patterns.md` — versioned SaveData, SaveManager, MigrationRunner, PlayerPrefs wrapper

## Handoff & Boundaries

- **Delegates to**: `unity-code-deep` (general C#), `unity-optimize-performance` (large dataset perf), `flatbuffers-coder` (binary serialization)
- **Does NOT handle**: Networking/multiplayer sync, database systems, Asset Bundle serialization, Editor serialization (SerializedObject)

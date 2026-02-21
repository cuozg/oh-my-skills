---
name: flatbuffers-coder
description: "FlatBuffers for Unity. Use when: (1) Creating/updating .fbs schemas, (2) Generating C# classes, (3) Converting JSON to binary, (4) Managing FlatBuffers pipeline. Triggers: 'schema', 'binary data', 'serialize', 'fbs file', 'flatbuffers'."
---

# FlatBuffers Specialist

## Input
Schema requirements (table name, fields, types, key). Optional: JSON data, existing `.fbs` for updates.

## Output
`.fbs` schema + generated C# + binary data. Follow [FBS_TEMPLATE.md](assets/templates/FBS_TEMPLATE.md).

## File Locations

| Type | Location |
|------|----------|
| Schemas | `FlatBuffers/New_Fbs/` |
| Generated C# | `FlatBuffers/Gen_Cs/` → `Assets/Scripts/Game/Managers/FlatBuffers/` |
| Input JSON | `FlatBuffers/Input_Json/` |
| Output Binary | `FlatBuffers/Output_Bin/` → `Assets/StreamingAssets/Blueprints/` |

## Schema Pattern

```flatbuffers
table [Name]FlatBuffer {
  items:[[Name]FlatBufferDataRaw];
}
table [Name]FlatBufferDataRaw {
  ID:string (key);
  // ... fields
}
root_type [Name]FlatBuffer;
```

## Workflow

1. Create/update `.fbs` in `FlatBuffers/New_Fbs/`
2. Generate C#: `bash FlatBuffers/generate_cs.sh`
3. Convert data: update + run `bash FlatBuffers/generate_data.sh`
4. Deploy: `python3 FlatBuffers/generateAll.py` or move manually

## Best Practices

- Always `ID:string (key)` for lookup tables
- Provide sensible defaults to save binary space
- Comment fields for purpose/valid ranges
- Pause Unity Editor before generation
- Verify generated C# compiles

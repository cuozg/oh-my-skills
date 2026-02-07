---
name: flatbuffers-coder
description: "FlatBuffers for Unity. Use when: (1) Creating/updating .fbs schemas, (2) Generating C# classes, (3) Converting JSON to binary, (4) Managing FlatBuffers pipeline. Triggers: 'schema', 'binary data', 'serialize', 'fbs file', 'flatbuffers'."
---

# FlatBuffers Specialist

Manage schemas, code generation, and binary data conversion.

## Output Requirement (MANDATORY)

**Every schema MUST follow the template**: [FBS_TEMPLATE.md](assets/templates/FBS_TEMPLATE.md)

Save schemas to: `FlatBuffers/New_Fbs/[Name].fbs`

Read the template first, then populate all sections.

## File Locations

| Type | Location |
|------|----------|
| Schemas (.fbs) | `FlatBuffers/New_Fbs/` |
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

1. **Schema**: Create/update `.fbs` in `FlatBuffers/New_Fbs/`
2. **Generate C#**: `bash FlatBuffers/generate_cs.sh`
3. **Convert Data**: Update `generate_data.sh`, run `bash FlatBuffers/generate_data.sh`
4. **Deploy**: Move files to Unity locations (or use `python3 FlatBuffers/generateAll.py`)

## Best Practices

- **Unique Keys**: Always `ID:string (key);` for lookup tables
- **Defaults**: Provide sensible defaults to save binary space
- **Document**: Comment fields in `.fbs` for purpose/valid ranges
- **Safety**: Ensure Unity Editor paused before running generation
- **Validate**: Verify generated C# compiles in Unity

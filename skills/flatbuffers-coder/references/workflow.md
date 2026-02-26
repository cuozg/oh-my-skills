## Workflow

1. Create/update `.fbs` in `FlatBuffers/New_Fbs/`
2. Generate C#: `bash FlatBuffers/generate_cs.sh`
3. Convert data: update + run `bash FlatBuffers/generate_data.sh`
4. Deploy: `python3 FlatBuffers/generateAll.py` or move manually

## File Locations

| Type | Location |
|------|----------|
| Schemas | `FlatBuffers/New_Fbs/` |
| Generated C# | `FlatBuffers/Gen_Cs/` → `Assets/Scripts/Game/Managers/FlatBuffers/` |
| Input JSON | `FlatBuffers/Input_Json/` |
| Output Binary | `FlatBuffers/Output_Bin/` → `Assets/StreamingAssets/Blueprints/` |

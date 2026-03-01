---
name: flatbuffers-coder
description: "FlatBuffers for Unity. Use when: (1) Creating/updating .fbs schemas, (2) Generating C# classes, (3) Converting JSON to binary, (4) Managing FlatBuffers pipeline. Triggers: 'schema', 'binary data', 'serialize', 'fbs file', 'flatbuffers'."
---

# FlatBuffers Specialist

## Input
Schema requirements (table name, fields, types, key). Optional: JSON data, existing `.fbs` for updates.

## Output
`.fbs` schema + generated C# + binary data. Follow [FBS_TEMPLATE.md](assets/templates/FBS_TEMPLATE.md).

## Key Rules

See flatbuffers-schema-pattern.md (loaded below) for schema design rules and best practices.

## Shared References

Load shared FlatBuffers resources from `unity-shared`:

```python
read_skill_file("unity-shared", "references/flatbuffers-schema-pattern.md")
```

## Reference Files
- [FBS_TEMPLATE.md](assets/templates/FBS_TEMPLATE.md) — Schema template
- workflow.md — FlatBuffers pipeline workflow

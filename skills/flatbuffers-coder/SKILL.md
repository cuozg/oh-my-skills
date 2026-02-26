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

See [schema-pattern.md](references/schema-pattern.md) for schema design rules and best practices.

## Reference Files
- [schema-pattern.md](references/schema-pattern.md) — Schema pattern + best practices
- [workflow.md](references/workflow.md) — Workflow steps + file locations
- [FBS_TEMPLATE.md](assets/templates/FBS_TEMPLATE.md) — Schema template

---
name: flatbuffers-coder
description: FlatBuffers pipeline — define .fbs schema, generate C# via flatc, serialize/deserialize binary data. Triggers — 'flatbuffers', 'fbs schema', 'flatbuffer', 'binary serialization', 'flatc'.
---
# flatbuffers-coder

Define FlatBuffers schemas, generate C# code, and implement binary serialization roundtrips.

## When to Use

- Adding FlatBuffers-based serialization to a Unity project
- Defining or modifying `.fbs` schema files for game data
- Generating C# classes from `.fbs` using `flatc`
- Implementing read/write helpers for FlatBuffers binary data
- Debugging serialization mismatches between schema and runtime code

## Workflow

1. **Define** — Write `.fbs` schema: tables, structs, enums, unions, root_type
2. **Generate** — Run `flatc --csharp` to produce C# builder/accessor files
3. **Implement** — Write serialization helpers using the generated `FlatBufferBuilder`
4. **Deserialize** — Implement `GetRootAs*` accessors for reading binary buffers
5. **Test** — Roundtrip: serialize → write bytes → read bytes → assert field values match

## Rules

- Keep schemas backward-compatible — only add fields, never reorder or remove
- Always set `root_type` in every `.fbs` file used as a top-level buffer
- Namespace C# output with `--gen-namespace` to avoid collisions
- Regenerate C# after every `.fbs` change — never hand-edit generated files
- Use `flatc --json` to inspect binary files during debugging

## Output Format

`.fbs` schema file(s) + generated C# accessor/builder file(s) + serialization helper class.
Binary test file included when a roundtrip test is requested.

## Reference Files

- `references/fbs-schema-patterns.md` — unions, attributes, field patterns (loads `unity-standards/references/other/flatbuffers-guide.md` for basics)
- `references/flatc-workflow.md` — install, generation flags, serialize examples (loads `unity-standards/references/other/flatbuffers-guide.md` for basics)

Load references on demand via `read_skill_file("flatbuffers-coder", "references/{file}")` and `read_skill_file("unity-standards", "references/other/flatbuffers-guide.md")`.

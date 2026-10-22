# FlatBuffers Schema Patterns

> **Shared basics**: `unity-standards/references/other/flatbuffers-guide.md`
> Load via: `read_skill_file("unity-standards", "references/other/flatbuffers-guide.md")`
> Covers: schema syntax, table vs struct, backward compat rules, C# generation, Unity integration.

## File Structure

```fbs
// my_data.fbs
namespace MyGame.Data;

enum ItemType : byte { Weapon = 0, Armor = 1, Consumable = 2 }

struct Vec3 {
  x: float;
  y: float;
  z: float;
}

table Item {
  id: uint32;
  name: string;
  type: ItemType;
  position: Vec3;
  tags: [string];       // vector of strings
  stats: [float];       // vector of scalars
}

table ItemList {
  items: [Item];
}

root_type ItemList;
```

## Common Field Patterns

```fbs
table Player {
  id: uint64;
  name: string;
  health: float = 100.0;      // default value
  alive: bool = true;
  inventory: [Item];          // vector of tables (offsets)
  metadata: [ubyte] (nested_flatbuffer);  // embedded buffer
}
```

## Unions

```fbs
union Payload { TextPayload, ImagePayload }

table Message {
  payload_type: Payload;   // auto-generated discriminant
  payload: Payload;
}
```

## Namespacing

```fbs
namespace MyGame.Serialization;  // maps to C# namespace MyGame.Serialization
```

## Attributes

```fbs
table Config {
  data: [ubyte] (nested_flatbuffer);  // embed another FlatBuffer
  id: uint32 (key);                   // used for binary search in sorted vectors
  name: string (required);            // disallow null
}
```

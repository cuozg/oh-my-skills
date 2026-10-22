# FlatBuffers Guide

## Pipeline

1. Define `.fbs` schema
2. Generate C# with `flatc --csharp`
3. Serialize with `FlatBufferBuilder`
4. Deserialize with `GetRootAs*`

Keep the `flatc` version equal to the FlatBuffers C# runtime in the project (source or
DLL under `Assets/Plugins/`). Current runtimes use `namespace Google.FlatBuffers`;
older ones use `FlatBuffers`.

## Schema Syntax

```fbs
namespace Game.Data;

enum ItemType : byte { Weapon = 0, Armor, Consumable }

struct Vec3 { x:float; y:float; z:float; }

table Item {
  id:int;
  name:string;
  type:ItemType = Weapon;
  position:Vec3;
  tags:[string];
}

root_type Item;
```

## Generate C#

```bash
flatc --csharp -o Assets/Scripts/Generated/ schema.fbs
```

## Serialize

Create strings, vectors, and child tables before `Start*`; structs are written inline.

```csharp
using Google.FlatBuffers;

var builder = new FlatBufferBuilder(256);
var nameOffset = builder.CreateString("Sword");
Item.StartItem(builder);
Item.AddId(builder, 1);
Item.AddName(builder, nameOffset);
Item.AddType(builder, ItemType.Weapon);
Item.AddPosition(builder, Vec3.CreateVec3(builder, 0f, 1f, 0f));
var item = Item.EndItem(builder);
builder.Finish(item.Value);
byte[] bytes = builder.SizedByteArray();
File.WriteAllBytes(Path.Combine(Application.persistentDataPath, "item.bin"), bytes);
```

## Deserialize

```csharp
byte[] bytes = File.ReadAllBytes(Path.Combine(Application.persistentDataPath, "item.bin"));
var buf = new ByteBuffer(bytes);
var item = Item.GetRootAsItem(buf);
Debug.Log($"{item.Name} type={item.Type}");
```

## Schema Evolution Rules

| Safe                        | Unsafe                  |
|-----------------------------|-------------------------|
| Add field at end of table   | Remove any field        |
| Add new enum value at end   | Reorder fields          |
| Add new table               | Change field type       |
| Deprecate field (`(deprecated)`) | Change default value |
| Rename field (binary-safe; breaks code/JSON) | Insert field mid-table without `(id: n)` |

# FlatBuffers Guide

## Pipeline

1. Define `.fbs` schema
2. Generate C# with `flatc --csharp`
3. Serialize with `FlatBufferBuilder`
4. Deserialize with `GetRootAs*`

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

```csharp
var builder = new FlatBufferBuilder(256);
var nameOffset = builder.CreateString("Sword");
var item = Item.CreateItem(builder, 1, nameOffset, ItemType.Weapon);
builder.Finish(item.Value);
byte[] bytes = builder.SizedByteArray();
File.WriteAllBytes(path, bytes);
```

## Deserialize

```csharp
byte[] bytes = File.ReadAllBytes(path);
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
| Deprecate field             | Rename field            |

## Size Comparison (1000 items)

| Format | Size   | Parse Time |
|--------|--------|------------|
| JSON   | ~150KB | ~12ms      |
| FlatBuffers | ~40KB | ~0.1ms |

# flatc Workflow

## Install

```bash
# macOS
brew install flatbuffers

# Or download binary from https://github.com/google/flatbuffers/releases
flatc --version
```

## Generate C# from .fbs

```bash
# Single file
flatc --csharp -o Assets/Generated/ schemas/item.fbs

# Multiple files, shared namespace
flatc --csharp --gen-namespace -o Assets/Generated/ schemas/*.fbs

# With reflection (needed for JSON conversion)
flatc --csharp --reflect-names -o Assets/Generated/ schemas/item.fbs
```

## JSON → Binary

```bash
# Convert JSON test data to binary
flatc --binary schemas/item.fbs testdata/items.json
# outputs: items.bin
```

## Binary → JSON (debug inspect)

```bash
flatc --json --strict-json schemas/item.fbs -- items.bin
```

## C# Serialize Example

```csharp
using FlatBuffers;
using MyGame.Data;

public static byte[] SerializeItems(List<ItemData> items)
{
    var builder = new FlatBufferBuilder(1024);
    var itemOffsets = items.Select(i =>
    {
        var name = builder.CreateString(i.Name);
        Item.StartItem(builder);
        Item.AddId(builder, i.Id);
        Item.AddName(builder, name);
        Item.AddType(builder, (ItemType)i.Type);
        return Item.EndItem(builder);
    }).ToArray();

    var vec = ItemList.CreateItemsVector(builder, itemOffsets);
    ItemList.StartItemList(builder);
    ItemList.AddItems(builder, vec);
    var root = ItemList.EndItemList(builder);
    builder.Finish(root.Value);
    return builder.SizedByteArray();
}
```

## C# Deserialize Example

```csharp
public static ItemList DeserializeItems(byte[] data)
{
    var buf = new ByteBuffer(data);
    return ItemList.GetRootAsItemList(buf);
}
```

## Unity Integration

1. Add `com.google.flatbuffers` via Package Manager (Git URL):
   `https://github.com/google/flatbuffers.git?path=net/FlatBuffers`
2. Place generated C# files in `Assets/Generated/` (exclude from source control)
3. Add a `generate_schemas.sh` script + pre-build step to auto-regenerate on schema change
4. Store binary data in `StreamingAssets/` or `Resources/` depending on load strategy

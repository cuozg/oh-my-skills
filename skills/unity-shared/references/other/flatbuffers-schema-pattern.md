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

## Best Practices

- Always `ID:string (key)` for lookup tables
- Provide sensible defaults to save binary space
- Comment fields for purpose/valid ranges
- Pause Unity Editor before generation
- Verify generated C# compiles

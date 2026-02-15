# FlatBuffers Schema Template

```flatbuffers
// File: NewFeatureFlatBuffer.fbs
// namespace Project.Data;

table NewFeatureFlatBuffer {
  items:[NewFeatureFlatBufferDataRaw];
}

table NewFeatureFlatBufferDataRaw {
  ID:string (key);
  Name:string;
  Value:int = 0;
  IsEnabled:bool = true;
  Tags:[string];
  Values:[int];
}

root_type NewFeatureFlatBuffer;
```

# FlatBuffers Schema Template

Follow this template when creating new schemas for the project.

```flatbuffers
// File: NewFeatureFlatBuffer.fbs

// Define namespaces if required by the project
// namespace Project.Data;

table NewFeatureFlatBuffer {
  items:[NewFeatureFlatBufferDataRaw];
}

table NewFeatureFlatBufferDataRaw {
  ID:string (key);
  
  // Naming convention: a0, b0 etc are used in legacy files, 
  // but descriptive names are preferred for new systems.
  Name:string;
  Value:int = 0;
  IsEnabled:bool = true;
  
  // Arrays
  Tags:[string];
  Values:[int];
}

root_type NewFeatureFlatBuffer;
```

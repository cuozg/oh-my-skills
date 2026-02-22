<!-- PART 2/2 of SYSTEM_DOCUMENT_TEMPLATE.md -->
<!-- Split template chunk: keep order and concatenate parts to reconstruct full template. -->

## 6. How to Implement / Update
<!-- [REQ: How to implement/update new function with it?] Step-by-step extension guide. -->

### 6.1 Adding a New {Feature/Variant}
<!-- Step-by-step guide for the most common extension point (e.g., adding a new enemy type, new item). -->
1. Create a new class/ScriptableObject at `Path/To/Folder`.
2. Implement the `IInterface` or inherit from `BaseClass`.
3. Register the new type in `ConfigurationManager`.
4. (Optional) Add the prefab to the `Resources` folder.

### 6.2 Common Modification Patterns
<!-- Patterns developers follow when modifying this system. -->
<!-- e.g., "To change the speed formula, modify CalculateSpeed() in MovementSystem.cs" -->

## 7. Attention Points
<!-- [REQ: Anything need to be attention?] Gotchas, constraints, performance, thread safety. -->

### 7.1 Critical Constraints
<!-- Things that MUST be true for the system to work (e.g., "Must be initialized after AudioSystem"). -->
- 

### 7.2 Known Limitations
<!-- Current limitations (e.g., "Does not support local multiplayer"). -->
- 

### 7.3 Performance Considerations
<!-- [REQ: Attention points] Memory, CPU, GC implications. -->
- 

### 7.4 Thread Safety
<!-- [REQ: Attention points] Is this system thread-safe? Main-thread only? -->
- 

## 8. Integration Points
<!-- [REQ: Detail about this feature] Dependencies and Dependents. -->

### 8.1 Dependencies (What This System Uses)
| System/Service | How It's Used | Coupling Type (Hard/Soft) |
|---------------|---------------|---------------------------|
| | | |

### 8.2 Dependents (What Uses This System)
| System/Service | How It Uses This | Impact of Changes |
|---------------|-----------------|-------------------|
| | | |

## 9. Error Handling
<!-- [REQ: Detail about this feature] How does this system handle errors? -->

| Error Scenario | How It's Handled | Recovery Strategy |
|---------------|-----------------|-------------------|
| | | |

## 10. Testing Guide
<!-- How to verify changes to this system. -->

### 10.1 Unit Test Coverage
<!-- Existing tests and what they cover. -->

### 10.2 Manual Testing Steps
1. Play scene `Scenes/Main`.
2. Perform action X.
3. Verify result Y.

## 11. Related Documents
<!-- Links to TDDs, plans, other system docs. -->
- 

## 12. Change Log
| Date | Author | Change Description |
|------|--------|-------------------|
| {Date} | AI Assistant | Initial document creation |

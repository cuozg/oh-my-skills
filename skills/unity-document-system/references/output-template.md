```markdown
# {SystemName} — System Document

> **Generated**: {Date}
> **Author**: AI Assistant
> **Status**: Draft | Review | Approved
> **Version**: 1.0

---

## 1. What It Is
<!-- [REQ: What it is?] Clear explanation of what this system is. -->
<!-- Explain the high-level concept clearly for a new developer. -->
<!-- Describe the core functionality in one paragraph. -->

## 2. Purpose & Responsibility
<!-- [REQ: What it is?] Why does this system exist? What problem does it solve? -->
<!-- Define its Single Responsibility. What is in scope vs out of scope? -->

## 3. Data Structures
<!-- [REQ: Data structure] All data models, ScriptableObjects, configs, serialization. -->

### 3.1 Primary Data Models
```csharp
// Key data structures (structs, classes) with field descriptions
// Focus on the data schema, not behavior.
```

### 3.2 Configuration & Assets
<!-- [REQ: Data structure] How is this system configured? -->
<!-- ScriptableObjects, JSON, Prefab variants, or constants? -->

## 4. How It Works
<!-- [REQ: How it works?] Detailed explanation with flow diagrams (Mermaid). -->

### 4.1 Initialization Flow
<!-- [REQ: How it works?] Mermaid sequence diagram for startup/initialization. -->
```mermaid
sequenceDiagram
    %% Show initialization/setup sequence
    %% Example:
    %% GameManager->>System: Initialize()
    %% System->>Config: Load()
    %% System-->>GameManager: Ready
```

### 4.2 Core Execution Flow
<!-- [REQ: How it works?] Mermaid sequence diagram for the main runtime loop/logic. -->
```mermaid
sequenceDiagram
    %% Show the main runtime flow
    %% Example:
    %% Update()->>ProcessInput()
    %% ProcessInput()->>Move()
    %% Move()->>Event: Invoke(OnMoved)
```

## 5. Architecture & Feature Details
<!-- [REQ: Detail about this feature] Deep technical details, architecture context. -->

### 5.1 System Context Diagram
```mermaid
graph TD
    %% Show this system and its relationships to other systems
    %% Example:
    %% PlayerController -->|Input| MovementSystem
    %% MovementSystem -->|Position| Physics
```

### 5.2 Key Classes & Components
<!-- [REQ: Detail about this feature] List the main scripts and their roles. -->
| Class/Component | Role | File Path |
|----------------|------|-----------|
| | | |

### 5.3 Key Methods
<!-- [REQ: Detail about this feature] The most important functions driving the logic. -->
| Method | Purpose | Called By |
|--------|---------|----------|
| | | |

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
```

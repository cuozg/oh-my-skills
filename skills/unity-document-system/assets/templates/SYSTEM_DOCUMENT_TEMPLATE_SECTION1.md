<!-- PART 1/2 of SYSTEM_DOCUMENT_TEMPLATE.md -->
<!-- Split template chunk: keep order and concatenate parts to reconstruct full template. -->

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


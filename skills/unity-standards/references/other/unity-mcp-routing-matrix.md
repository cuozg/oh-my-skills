# Unity MCP Routing Matrix (51 Tools)

AI agent decision tree for selecting the correct Unity MCP tool. Optimized for fast lookup.

**Rule:** When in doubt, check the guard clauses. Wrong tool selection wastes tokens and produces errors.

---

## AI Agent Routing Logic

### Root: What is your Unity task?

```
What is your Unity task?
|
+---> GENERATE or CREATE an asset?          --> Go to [Asset Generation Branch]
+---> EDIT or MODIFY a C# script?           --> Go to [Scripting Branch]
+---> EDIT or MODIFY a shader?              --> Go to [Shader Branch]
+---> READ or INSPECT a file?               --> Go to [Reading Branch]
+---> WORK WITH the scene or GameObjects?   --> Go to [Scene Branch]
+---> CAPTURE a visual/screenshot?          --> Go to [Visual Capture Branch]
+---> DEBUG or read console?                --> Go to [Debugging Branch]
+---> ANALYZE profiler data?                --> Go to [Profiling Branch]
+---> CONTROL the editor (play/pause/etc)?  --> Go to [Editor Control Branch]
+---> MANAGE packages?                      --> Go to [Package Branch]
+---> MANAGE assets (move/rename/delete)?   --> Go to [Asset Management Branch]
+---> GET project info or context?          --> Go to [Project Info Branch]
+---> EDIT audio clips?                     --> Go to [Audio Branch]
+---> RUN arbitrary C# code?                --> Go to [Code Execution Branch]
```

---

### Asset Generation Branch

```
Want to GENERATE or CREATE an asset?
|
+---> Generate NEW asset with AI (sprite, image, mesh, sound, cubemap, material, terrain)?
|     --> Unity_AssetGeneration_GenerateAsset
|         Modes: GenerateSprite, GenerateImage, GenerateSpritesheet,
|                GenerateCubemap, UpscaleCubemap, GenerateMaterial,
|                AddPbrToMaterial, GenerateMesh, GenerateSound,
|                GenerateTerrainLayer, AddPbrToTerrainLayer,
|                GenerateHumanoidAnimation,
|                RemoveSpriteBackground, RemoveImageBackground,
|                EditSpriteWithPrompt, EditImageWithPrompt
|         REQUIRES: Call GetModels first to get modelId
|         TIP: For materials/terrain layers, call GetCompositionPatterns first
|
+---> Need model IDs for generation?
|     --> Unity_AssetGeneration_GetModels
|
+---> Need composition patterns for materials/terrain?
|     --> Unity_AssetGeneration_GetCompositionPatterns
|
+---> Convert EXISTING texture to material? (no AI)
|     --> Unity_AssetGeneration_ConvertToMaterial
|
+---> Convert EXISTING texture to terrain layer? (no AI)
|     --> Unity_AssetGeneration_ConvertToTerrainLayer
|
+---> Convert EXISTING sprite sheet to AnimationClip? (no AI)
|     --> Unity_AssetGeneration_ConvertSpri_dca62520
|
+---> Create AnimatorController from EXISTING AnimationClip?
|     --> Unity_AssetGeneration_CreateAnima_40e1a9ab
|
+---> Edit EXISTING humanoid animation (remove root motion / trim to loop)?
|     --> Unity_AssetGeneration_EditAnimati_47017090
|         Modes: MakeStationary, TrimToBestLoop
|
+---> Resume or discard interrupted generation?
      --> Unity_AssetGeneration_ManageInterrupted
          Modes: List, Resume, Discard
```

**GUARD CLAUSES - Asset Generation:**
- DO NOT use `GenerateAsset` for non-generative conversions -- use the `Convert*` tools
- DO NOT use `Convert*` tools when you need AI generation -- use `GenerateAsset`
- DO NOT use `EditAnimati` for non-humanoid animations -- it only supports humanoid
- ALWAYS call `GetModels` before `GenerateAsset` to get a valid `modelId`

---

### Scripting Branch

```
Want to EDIT or MODIFY a C# script?
|
+---> Create a NEW script from scratch?
|     --> Unity_CreateScript
|         Params: Path, Contents, ScriptType, Namespace
|
+---> Delete a script?
|     --> Unity_DeleteScript
|         Params: Uri
|
+---> Edit at METHOD/CLASS level (replace, insert, delete method)?
|     --> Unity_ScriptApplyEdits  [PREFERRED for structural edits]
|         Ops: replace_method, insert_method, delete_method,
|              anchor_insert, anchor_delete, anchor_replace
|         TIP: Use Preview=true first to verify changes
|
+---> Edit at exact CHARACTER POSITION (line/column ranges)?
|     --> Unity_ApplyTextEdits
|         REQUIRES: Verify content at target lines BEFORE editing
|         REQUIRES: PreconditionSha256 (get via GetSha)
|
+---> Find a pattern/method/variable in a file?
|     --> Unity_FindInFile
|         Params: Uri, Pattern (regex), IgnoreCase
|
+---> Get file hash for precondition check?
|     --> Unity_GetSha
|
+---> Validate a script for errors/diagnostics?
|     --> Unity_ValidateScript
|         Levels: basic (syntax), standard (deeper + perf hints)
|
+---> Legacy operations (create/read/delete)?
      --> Unity_ManageScript
          NOTE: Prefer CreateScript, ReadResource, DeleteScript instead
```

**GUARD CLAUSES - Scripting:**
- DO NOT use `ApplyTextEdits` for method-level changes -- use `ScriptApplyEdits` (safer)
- DO NOT use `ScriptApplyEdits` for character-precise edits -- use `ApplyTextEdits`
- DO NOT use `ManageScript` for reads -- use `ReadResource` instead
- ALWAYS call `GetSha` before `ApplyTextEdits` to get `PreconditionSha256`
- ALWAYS verify content at target lines before `ApplyTextEdits`

---

### Shader Branch

```
Want to EDIT or MODIFY a shader?
|
--> Unity_ManageShader
    Modes: Create, Read, Update, Delete
    Params: Action, Name, Path, Contents
```

**GUARD CLAUSES - Shader:**
- DO NOT use `ManageShader` for C# scripts -- use `ManageScript`/`CreateScript`
- DO NOT use `ManageShader` for material properties -- use `ManageAsset`

---

### Reading Branch

```
Want to READ or INSPECT a file?
|
+---> Read a script/resource with line slicing?
|     --> Unity_ReadResource
|         Params: Uri, StartLine, LineCount, HeadBytes, TailLines, Request
|         TIP: Request accepts natural language ("show 40 lines around MethodName")
|
+---> Get script capabilities info?
      --> Unity_ManageScript_capabilities
          Returns: supported ops, max payload, guard flags
```

**GUARD CLAUSES - Reading:**
- DO NOT use `ManageScript(action=read)` -- use `ReadResource` instead (better slicing)
- DO NOT use `ReadResource` for editing -- it's read-only

---

### Scene Branch

```
Want to WORK WITH the scene or GameObjects?
|
+---> Create, modify, delete, find GameObjects?
|     --> Unity_ManageGameObject
|         Actions: create, modify, delete, find,
|                  add_component, remove_component, set_component_property,
|                  get_components, get_component
|         Search: by_name, by_id, by_path
|         Features: save_as_prefab, set_active, primitive_type
|
+---> Create, load, save scenes or get hierarchy?
      --> Unity_ManageScene
          Actions: Create, Load, Save, GetHierarchy, GetActive, GetBuildSettings
          TIP: Use Depth param to limit hierarchy depth (-1=full, 0=root only)
```

**GUARD CLAUSES - Scene:**
- DO NOT use `ManageGameObject` for asset-level operations -- use `ManageAsset`
- DO NOT use `ManageScene` for individual GameObject operations -- use `ManageGameObject`
- DO NOT use `ManageGameObject` for script content -- use scripting tools

---

### Visual Capture Branch

```
Want to CAPTURE a visual/screenshot?
|
+---> Capture from a specific Camera component?
|     --> Unity_Camera_Capture
|         Params: cameraInstanceID (optional -- omit for scene view)
|         NOTE: Computationally expensive, use sparingly
|
+---> Capture a 2D scene region (orthographic)?
|     --> Unity_SceneView_Capture2DScene
|         Params: worldX, worldY, worldWidth, worldHeight, pixelsPerUnit
|         USE FOR: tilemaps, 2D games, specific 2D regions
|
+---> Capture 3D scene from multiple angles (4-view grid)?
      --> Unity_SceneView_CaptureMultiAngleSceneView
          Params: focusObjectIds (optional -- focuses on specific objects)
          Returns: 2x2 grid (Isometric, Front, Top, Right)
          NOTE: Computationally expensive, use sparingly
```

**GUARD CLAUSES - Visual Capture:**
- DO NOT use `CaptureMultiAngleSceneView` for 2D projects -- use `Capture2DScene`
- DO NOT use `CaptureMultiAngleSceneView` to get editor window info -- it's for 3D scenes
- DO NOT use `Camera_Capture` when you need multi-angle -- use `CaptureMultiAngleSceneView`
- DO NOT use any capture tool for Unity Editor UI screenshots -- use OS screenshot tools

---

### Debugging Branch

```
Want to DEBUG or read the console?
|
+---> Get console logs (errors, warnings, messages)?
|     --> Unity_GetConsoleLogs
|         Params: logTypes, maxEntries, includeStackTrace
|         USE FOR: Quick error check, debugging
|
+---> Get console with filtering, timestamps, or clear it?
      --> Unity_ReadConsole
          Actions: Get, Clear
          Params: Types, Count, FilterText, SinceTimestamp, Format, IncludeStacktrace
          Formats: Plain, Detailed, Json
          USE FOR: Filtered queries, clearing console, timestamp-based retrieval
```

**GUARD CLAUSES - Debugging:**
- DO NOT use `GetConsoleLogs` if you need to filter by text/timestamp -- use `ReadConsole`
- DO NOT use `GetConsoleLogs` to clear console -- use `ReadConsole(Action=Clear)`
- Use `ReadConsole` when you need structured output (Json format)

---

### Profiling Branch

```
Want to ANALYZE profiler data?
|
+---> Overall GC summary (all frames)?
|     --> Unity_Profiler_GetOverallGcAlloca_ac50c101
|
+---> Single frame analysis?
|     |
|     +---> Top samples by TOTAL time?
|     |     --> Unity_Profiler_GetFrameTopTimeSam_ccc85b2d
|     |         Params: frameIndex, targetFrameTime
|     |
|     +---> Top samples by SELF time?
|     |     --> Unity_Profiler_GetFrameSelfTimeSa_e44ee448
|     |         Params: frameIndex
|     |
|     +---> GC allocations in frame?
|           --> Unity_Profiler_GetFrameGcAllocati_a7eb5b61
|               Params: frameIndex
|
+---> Multi-frame range analysis?
|     |
|     +---> Time profiling across frames?
|     |     --> Unity_Profiler_GetFrameRangeTopTimeSummary
|     |         Params: startFrameIndex, lastFrameIndex, targetFrameTime
|     |
|     +---> GC allocations across frames?
|           --> Unity_Profiler_GetFrameRangeGcAll_90f409da
|               Params: startFrameIndex, lastFrameIndex
|
+---> Specific sample drill-down?
|     |
|     +---> Time summary BY INDEX?
|     |     --> Unity_Profiler_GetSampleTimeSummary
|     |         Params: frameIndex, threadName, sampleIndex
|     |
|     +---> Time summary BY MARKER PATH?
|     |     --> Unity_Profiler_GetSampleTimeSumma_a680062a
|     |         Params: frameIndex, threadName, markerIdPath
|     |
|     +---> GC allocations BY INDEX?
|     |     --> Unity_Profiler_GetSampleGcAllocat_4a279ae5
|     |         Params: frameIndex, threadName, sampleIndex
|     |
|     +---> GC allocations BY MARKER PATH?
|     |     --> Unity_Profiler_GetSampleGcAllocat_89f626bb
|     |         Params: frameIndex, threadName, markerIdPath
|     |
|     +---> Bottom-up sample time?
|     |     --> Unity_Profiler_GetBottomUpSampleT_55cc1e4e
|     |         Params: frameIndex, threadName, bottomUpSampleIndex
|     |
|     +---> Related samples on OTHER threads?
|           --> Unity_Profiler_GetRelatedSamplesT_a6086ba0
|               Params: frameIndex, threadName, sampleIndex, relatedThreadName
```

**GUARD CLAUSES - Profiling:**
- DO NOT use single-frame tools for multi-frame analysis -- use `FrameRange*` tools
- DO NOT use index-based lookups when you have a marker name -- use `markerIdPath` variants
- DO NOT use profiling tools to FIX performance -- they're read-only analysis; use skills

---

### Editor Control Branch

```
Want to CONTROL the Unity editor?
|
+---> Play, pause, stop, get state, manage tools/tags/layers?
|     --> Unity_ManageEditor
|         Actions: Play, Pause, Stop, GetState, GetProjectRoot,
|                  GetWindows, GetActiveTool, GetSelection, GetPrefabStage,
|                  SetActiveTool, AddTag, RemoveTag, GetTags,
|                  AddLayer, RemoveLayer, GetLayers
|
+---> Execute a menu command or find menu items?
      --> Unity_ManageMenuItem
          Actions: Execute, List, Exists, Refresh
          TIP: Use List first to find the correct MenuPath
```

**GUARD CLAUSES - Editor Control:**
- DO NOT use `ManageEditor` for scene hierarchy -- use `ManageScene`
- DO NOT use `ManageMenuItem` to create new menu items -- use editor scripts
- ALWAYS use `List` before `Execute` if unsure of exact menu path

---

### Package Branch

```
Want to MANAGE Unity packages?
|
+---> Install, remove, embed, or install samples?
|     --> Unity_PackageManager_ExecuteAction
|         Ops: Add, Remove, Embed, Unembed, Sample
|         Params: operation, package, version, sampleIndex
|
+---> Get package info/description (read-only)?
      --> Unity_PackageManager_GetData
          Params: packageID, installedOnly
```

**GUARD CLAUSES - Package:**
- DO NOT use `GetData` to install -- it's read-only; use `ExecuteAction`
- DO NOT use for NuGet packages -- these are Unity Package Manager only

---

### Asset Management Branch

```
Want to MANAGE assets (move/rename/create/search)?
|
+---> Import, create, modify, delete, duplicate, move, rename, search assets?
|     --> Unity_ManageAsset
|         Actions: Import, Create, Modify, Delete, Duplicate, Move,
|                  Rename, Search, GetInfo, CreateFolder, GetComponents
|         TIP: Set GeneratePreview=true for visual assets
|
+---> Find assets by name or visual similarity?
|     --> Unity_FindProjectAssets
|         Params: query, startIndex
|         NOTE: Includes semantic/visual search, not just name matching
|
+---> Import FBX from URL into scene?
      --> Unity_ImportExternalModel
          Params: Name, FbxUrl, Height, AlbedoTextureUrl
          NOTE: Also creates prefab automatically
```

**GUARD CLAUSES - Asset Management:**
- DO NOT use `ManageAsset` for script operations -- use scripting tools
- DO NOT use `ManageAsset` for scene hierarchy -- use `ManageGameObject`
- DO NOT use `ImportExternalModel` for generated meshes -- use `GenerateAsset(GenerateMesh)`

---

### Project Info Branch

```
Want to GET project info or context?
|
+---> Get project overview, folder structure, taxonomy?
|     --> Unity_GetProjectData
|         Params: maxAssetItems, maxOutputChars, maxTaxonomyDepth
|
+---> Get coding standards, naming conventions, project guidelines?
|     --> Unity_GetUserGuidelines
|         NOTE: Call this BEFORE working on any Unity file
|
+---> List files by glob pattern?
      --> Unity_ListResources
          Params: Pattern (default *.cs), Under (default Assets), Limit
          Returns: unity://path/... URIs for use with other tools
```

**GUARD CLAUSES - Project Info:**
- DO NOT use `ListResources` to read file contents -- it only lists URIs
- DO NOT skip `GetUserGuidelines` before writing code -- it ensures style compliance

---

### Audio Branch

```
Want to EDIT audio clips?
|
--> Unity_AudioClip_Edit
    Commands: TrimSilence, TrimSound, ChangeVolume, LoopSound
    Params: inputAudioClipPath, command, startTime, endTime, factor, crossfadeDurationMs
    TIP: TrimSilence before LoopSound for best results
```

**GUARD CLAUSES - Audio:**
- DO NOT use for generating audio -- use `GenerateAsset(GenerateSound)`
- DO NOT use for non-audio assets

---

### Code Execution Branch

```
Want to RUN arbitrary C# in the editor?
|
--> Unity_RunCommand
    Params: Code, Title
    PATTERN: Must use `internal class CommandScript : IRunCommand`
    Must use `result.RegisterObjectCreation()` / `result.RegisterObjectModification()`
    Must use `result.DestroyObject()` instead of `Object.DestroyImmediate`
```

**GUARD CLAUSES - Code Execution:**
- DO NOT use for persistent scripts -- use `CreateScript`
- DO NOT use for asset generation -- use `GenerateAsset`
- ALWAYS use `internal class CommandScript` (not `public` -- causes compilation error)
- ALWAYS use `result.Log()` for output, not `Debug.Log()`

---

## Quick Tool Lookup

| Problem Type | Primary Tool | Mode/Action | Exclusions |
|:---|:---|:---|:---|
| **Generate sprite/image** (AI) | `GenerateAsset` | `GenerateSprite` / `GenerateImage` | Not for conversions |
| **Generate 3D mesh** (AI) | `GenerateAsset` | `GenerateMesh` | Not for FBX import |
| **Generate sound** (AI) | `GenerateAsset` | `GenerateSound` | Not for audio editing |
| **Generate material** (AI) | `GenerateAsset` | `GenerateMaterial` | Not for simple texture assignment |
| **Generate cubemap** (AI) | `GenerateAsset` | `GenerateCubemap` | -- |
| **Generate spritesheet** (AI) | `GenerateAsset` | `GenerateSpritesheet` | -- |
| **Generate humanoid anim** (AI) | `GenerateAsset` | `GenerateHumanoidAnimation` | -- |
| **Generate terrain layer** (AI) | `GenerateAsset` | `GenerateTerrainLayer` | Not for simple conversions |
| **Remove background** | `GenerateAsset` | `RemoveSpriteBackground` / `RemoveImageBackground` | -- |
| **Edit sprite/image with prompt** | `GenerateAsset` | `EditSpriteWithPrompt` / `EditImageWithPrompt` | -- |
| **Add PBR maps** | `GenerateAsset` | `AddPbrToMaterial` / `AddPbrToTerrainLayer` | -- |
| **Upscale cubemap** | `GenerateAsset` | `UpscaleCubemap` | -- |
| **Texture to material** (no AI) | `ConvertToMaterial` | -- | Not for PBR/generation |
| **Texture to terrain layer** (no AI) | `ConvertToTerrainLayer` | -- | Not for PBR/generation |
| **Sprite sheet to AnimClip** (no AI) | `ConvertSpri_dca62520` | -- | Not for generation |
| **AnimClip to AnimController** | `CreateAnima_40e1a9ab` | -- | Not for clip creation |
| **Remove root motion** | `EditAnimati_47017090` | `MakeStationary` | Humanoid only |
| **Trim anim to best loop** | `EditAnimati_47017090` | `TrimToBestLoop` | Humanoid only |
| **List AI generation models** | `GetModels` | -- | Read-only |
| **List composition patterns** | `GetComposit_832d2c69` | -- | Read-only |
| **Resume stuck generation** | `ManageInterrupted` | `List` / `Resume` / `Discard` | -- |
| **Trim audio silence** | `AudioClip_Edit` | `TrimSilence` | Not for audio generation |
| **Trim audio to range** | `AudioClip_Edit` | `TrimSound` | Not for audio generation |
| **Change audio volume** | `AudioClip_Edit` | `ChangeVolume` | Not for audio generation |
| **Loop audio seamlessly** | `AudioClip_Edit` | `LoopSound` | TrimSilence first |
| **Create new C# script** | `CreateScript` | -- | Not for editing |
| **Delete C# script** | `DeleteScript` | -- | Not for reading |
| **Replace/insert method** | `ScriptApplyEdits` | `replace_method` / `insert_method` / `delete_method` | Not for char-level edits |
| **Pattern-based anchor edit** | `ScriptApplyEdits` | `anchor_insert` / `anchor_replace` / `anchor_delete` | Not for char-level edits |
| **Precise character edit** | `ApplyTextEdits` | -- | Not for method-level; need SHA first |
| **Search in file (regex)** | `FindInFile` | -- | Not for editing |
| **Get file SHA256** | `GetSha` | -- | Not for reading content |
| **Validate script** | `ValidateScript` | `basic` / `standard` | Not for fixing |
| **Read file with slicing** | `ReadResource` | -- | Read-only |
| **Legacy script CRUD** | `ManageScript` | `create` / `read` / `delete` | Prefer dedicated tools |
| **Script capabilities** | `ManageScript_capabilities` | -- | Info only |
| **Create/update/delete shader** | `ManageShader` | `Create` / `Read` / `Update` / `Delete` | Not for C# |
| **Create/modify GameObject** | `ManageGameObject` | `create` / `modify` / `delete` / `find` | Not for assets |
| **Add/remove component** | `ManageGameObject` | `add_component` / `remove_component` | Not for script content |
| **Get components on object** | `ManageGameObject` | `get_components` / `get_component` | -- |
| **Set component property** | `ManageGameObject` | `set_component_property` | -- |
| **Load/save/create scene** | `ManageScene` | `Create` / `Load` / `Save` | Not for GameObjects |
| **Get scene hierarchy** | `ManageScene` | `GetHierarchy` | Not for asset hierarchy |
| **Get build settings** | `ManageScene` | `GetBuildSettings` | -- |
| **Play/Pause/Stop editor** | `ManageEditor` | `Play` / `Pause` / `Stop` | Not for scene ops |
| **Manage tags/layers** | `ManageEditor` | `AddTag` / `AddLayer` / etc. | Not for asset ops |
| **Get editor selection** | `ManageEditor` | `GetSelection` | -- |
| **Execute menu command** | `ManageMenuItem` | `Execute` | Use List first |
| **Find menu items** | `ManageMenuItem` | `List` | -- |
| **Capture camera view** | `Camera_Capture` | -- | Not for multi-angle |
| **Capture 2D region** | `Capture2DScene` | -- | Not for 3D |
| **Capture 3D multi-angle** | `CaptureMultiAngleSceneView` | -- | Not for 2D; expensive |
| **Get console errors** | `GetConsoleLogs` | -- | No filtering by text |
| **Read/clear console** | `ReadConsole` | `Get` / `Clear` | -- |
| **Overall GC summary** | `GetOverallGcAlloca_ac50c101` | -- | All frames aggregate |
| **Frame top time samples** | `GetFrameTopTimeSam_ccc85b2d` | -- | Single frame |
| **Frame self time samples** | `GetFrameSelfTimeSa_e44ee448` | -- | Single frame |
| **Frame GC allocations** | `GetFrameGcAllocati_a7eb5b61` | -- | Single frame |
| **Multi-frame time summary** | `GetFrameRangeTopTimeSummary` | -- | Frame range |
| **Multi-frame GC summary** | `GetFrameRangeGcAll_90f409da` | -- | Frame range |
| **Sample time (by index)** | `GetSampleTimeSummary` | -- | Drill-down |
| **Sample time (by marker)** | `GetSampleTimeSumma_a680062a` | -- | Drill-down |
| **Sample GC (by index)** | `GetSampleGcAllocat_4a279ae5` | -- | Drill-down |
| **Sample GC (by marker)** | `GetSampleGcAllocat_89f626bb` | -- | Drill-down |
| **Bottom-up sample time** | `GetBottomUpSampleT_55cc1e4e` | -- | Drill-down |
| **Cross-thread samples** | `GetRelatedSamplesT_a6086ba0` | -- | Multi-thread |
| **Install/remove package** | `PackageManager_ExecuteAction` | `Add` / `Remove` / `Embed` / `Sample` | Not for info |
| **Package info** | `PackageManager_GetData` | -- | Read-only |
| **Move/rename/delete asset** | `ManageAsset` | `Move` / `Rename` / `Delete` / etc. | Not for scripts |
| **Search assets** | `ManageAsset` | `Search` | By pattern only |
| **Semantic asset search** | `FindProjectAssets` | -- | Name + visual search |
| **Import FBX from URL** | `ImportExternalModel` | -- | Not for generated meshes |
| **Project overview** | `GetProjectData` | -- | Read-only |
| **Project guidelines** | `GetUserGuidelines` | -- | Call before coding |
| **List files by glob** | `ListResources` | -- | URIs only, no content |
| **Run C# in editor** | `RunCommand` | -- | Not for persistent scripts |

---

## Tools by Category

### Asset Generation (9 tools)

| Tool | Description |
|:---|:---|
| `GenerateAsset` | AI-powered generation of sprites, images, meshes, sounds, cubemaps, materials, terrain layers, spritesheets, humanoid animations; also background removal and prompt-based editing |
| `GetModels` | List available AI models with model IDs |
| `GetComposit_832d2c69` | List composition patterns for material/terrain reference |
| `ConvertToMaterial` | Texture to Material (non-generative) |
| `ConvertToTerrainLayer` | Texture to TerrainLayer (non-generative) |
| `ConvertSpri_dca62520` | Sprite sheet to AnimationClip (non-generative) |
| `CreateAnima_40e1a9ab` | AnimationClip to AnimatorController |
| `EditAnimati_47017090` | Edit humanoid animation (MakeStationary / TrimToBestLoop) |
| `ManageInterrupted` | List/resume/discard interrupted generations |

### Audio (1 tool)

| Tool | Description |
|:---|:---|
| `AudioClip_Edit` | TrimSilence, TrimSound, ChangeVolume, LoopSound |

### Scripting (10 tools)

| Tool | Description |
|:---|:---|
| `CreateScript` | Create new C# script at path |
| `DeleteScript` | Delete C# script by URI |
| `ScriptApplyEdits` | Structured method/class edits (replace, insert, delete, anchor) |
| `ApplyTextEdits` | Precise character-position edits with SHA precondition |
| `FindInFile` | Regex pattern search returning line numbers |
| `GetSha` | Get SHA256 hash for precondition checks |
| `ValidateScript` | Script validation and diagnostics (basic/standard) |
| `ReadResource` | Read files with line slicing and natural language requests |
| `ManageScript` | Legacy CRUD router (prefer dedicated tools) |
| `ManageScript_capabilities` | Query supported operations and limits |

### Shader (1 tool)

| Tool | Description |
|:---|:---|
| `ManageShader` | Create, Read, Update, Delete shader files |

### Scene Management (2 tools)

| Tool | Description |
|:---|:---|
| `ManageGameObject` | Create/modify/delete/find GameObjects; component operations |
| `ManageScene` | Create/load/save scenes; get hierarchy and build settings |

### Visual Capture (3 tools)

| Tool | Description |
|:---|:---|
| `Camera_Capture` | Render from specific camera or scene view |
| `Capture2DScene` | Orthographic capture of 2D scene region |
| `CaptureMultiAngleSceneView` | 4-view grid (Iso/Front/Top/Right) for 3D validation |

### Debugging (2 tools)

| Tool | Description |
|:---|:---|
| `GetConsoleLogs` | Get console messages/warnings/errors with stack traces |
| `ReadConsole` | Get/clear console with filtering, timestamps, formats |

### Profiling (12 tools)

| Tool | Description |
|:---|:---|
| `GetOverallGcAlloca_ac50c101` | Overall GC allocation summary (all frames) |
| `GetFrameTopTimeSam_ccc85b2d` | Top samples by total time (single frame) |
| `GetFrameSelfTimeSa_e44ee448` | Top samples by self time (single frame) |
| `GetFrameGcAllocati_a7eb5b61` | GC allocations (single frame) |
| `GetFrameRangeTopTimeSummary` | Time summary (frame range) |
| `GetFrameRangeGcAll_90f409da` | GC summary (frame range) |
| `GetSampleTimeSummary` | Sample time by index |
| `GetSampleTimeSumma_a680062a` | Sample time by marker path |
| `GetSampleGcAllocat_4a279ae5` | Sample GC by index |
| `GetSampleGcAllocat_89f626bb` | Sample GC by marker path |
| `GetBottomUpSampleT_55cc1e4e` | Bottom-up sample time analysis |
| `GetRelatedSamplesT_a6086ba0` | Related samples on other threads |

### Editor Control (2 tools)

| Tool | Description |
|:---|:---|
| `ManageEditor` | Play/Pause/Stop, tags, layers, selection, tools, windows |
| `ManageMenuItem` | Execute/list/check menu items |

### Asset Management (3 tools)

| Tool | Description |
|:---|:---|
| `ManageAsset` | Import/Create/Modify/Delete/Duplicate/Move/Rename/Search/GetInfo/CreateFolder |
| `FindProjectAssets` | Name + semantic/visual asset search |
| `ImportExternalModel` | Import FBX from URL, instantiate, save as prefab |

### Package Management (2 tools)

| Tool | Description |
|:---|:---|
| `PackageManager_ExecuteAction` | Add/Remove/Embed/Unembed packages, install samples |
| `PackageManager_GetData` | Get package description and metadata (read-only) |

### Project Info (3 tools)

| Tool | Description |
|:---|:---|
| `GetProjectData` | Project overview, taxonomy, folder structure |
| `GetUserGuidelines` | Coding standards, naming, project conventions |
| `ListResources` | List file URIs by glob pattern |

### Code Execution (1 tool)

| Tool | Description |
|:---|:---|
| `RunCommand` | Compile and execute arbitrary C# in the editor |

---

## Find Tool by Keyword

| Keyword / Phrase | Tool |
|:---|:---|
| add component | `ManageGameObject` (add_component) |
| add layer | `ManageEditor` (AddLayer) |
| add package | `PackageManager_ExecuteAction` (Add) |
| add PBR | `GenerateAsset` (AddPbrToMaterial / AddPbrToTerrainLayer) |
| add tag | `ManageEditor` (AddTag) |
| anchor edit | `ScriptApplyEdits` (anchor_insert / anchor_replace) |
| animation controller | `CreateAnima_40e1a9ab` |
| animator from clip | `CreateAnima_40e1a9ab` |
| asset info | `ManageAsset` (GetInfo) |
| audio trim | `AudioClip_Edit` (TrimSilence / TrimSound) |
| bottom-up profiling | `GetBottomUpSampleT_55cc1e4e` |
| build settings | `ManageScene` (GetBuildSettings) |
| camera capture | `Camera_Capture` |
| change volume | `AudioClip_Edit` (ChangeVolume) |
| check for errors | `GetConsoleLogs` or `ReadConsole` |
| clear console | `ReadConsole` (Clear) |
| coding standards | `GetUserGuidelines` |
| composition patterns | `GetComposit_832d2c69` |
| console errors | `GetConsoleLogs` |
| console messages | `ReadConsole` (Get) |
| create folder | `ManageAsset` (CreateFolder) |
| create GameObject | `ManageGameObject` (create) |
| create material (no AI) | `ConvertToMaterial` |
| create scene | `ManageScene` (Create) |
| create script | `CreateScript` |
| create shader | `ManageShader` (Create) |
| cross-thread samples | `GetRelatedSamplesT_a6086ba0` |
| delete asset | `ManageAsset` (Delete) |
| delete method | `ScriptApplyEdits` (delete_method) |
| delete script | `DeleteScript` |
| duplicate asset | `ManageAsset` (Duplicate) |
| edit animation | `EditAnimati_47017090` |
| edit image with prompt | `GenerateAsset` (EditImageWithPrompt) |
| edit sprite with prompt | `GenerateAsset` (EditSpriteWithPrompt) |
| editor state | `ManageEditor` (GetState) |
| embed package | `PackageManager_ExecuteAction` (Embed) |
| execute menu | `ManageMenuItem` (Execute) |
| FBX import | `ImportExternalModel` |
| file hash | `GetSha` |
| find asset | `FindProjectAssets` |
| find GameObject | `ManageGameObject` (find) |
| find in file | `FindInFile` |
| find menu item | `ManageMenuItem` (List) |
| frame GC allocations | `GetFrameGcAllocati_a7eb5b61` |
| frame time breakdown | `GetFrameTopTimeSam_ccc85b2d` |
| GC allocations | `GetOverallGcAlloca_ac50c101` (overall) |
| GC by marker | `GetSampleGcAllocat_89f626bb` |
| GC spikes | `GetFrameGcAllocati_a7eb5b61` (per frame) |
| generate cubemap | `GenerateAsset` (GenerateCubemap) |
| generate image | `GenerateAsset` (GenerateImage) |
| generate material (AI) | `GenerateAsset` (GenerateMaterial) |
| generate mesh | `GenerateAsset` (GenerateMesh) |
| generate sound | `GenerateAsset` (GenerateSound) |
| generate sprite | `GenerateAsset` (GenerateSprite) |
| generate spritesheet | `GenerateAsset` (GenerateSpritesheet) |
| generate terrain layer (AI) | `GenerateAsset` (GenerateTerrainLayer) |
| get components | `ManageGameObject` (get_components) |
| get hierarchy | `ManageScene` (GetHierarchy) |
| get selection | `ManageEditor` (GetSelection) |
| guidelines | `GetUserGuidelines` |
| humanoid animation | `GenerateAsset` (GenerateHumanoidAnimation) |
| import asset | `ManageAsset` (Import) |
| insert method | `ScriptApplyEdits` (insert_method) |
| install package | `PackageManager_ExecuteAction` (Add) |
| install sample | `PackageManager_ExecuteAction` (Sample) |
| interrupted generation | `ManageInterrupted` |
| list files | `ListResources` |
| list models | `GetModels` |
| load scene | `ManageScene` (Load) |
| loop audio | `AudioClip_Edit` (LoopSound) |
| make stationary | `EditAnimati_47017090` (MakeStationary) |
| marker path lookup | `GetSampleTimeSumma_a680062a` / `GetSampleGcAllocat_89f626bb` |
| modify asset | `ManageAsset` (Modify) |
| modify GameObject | `ManageGameObject` (modify) |
| move asset | `ManageAsset` (Move) |
| multi-angle capture | `CaptureMultiAngleSceneView` |
| multi-frame GC | `GetFrameRangeGcAll_90f409da` |
| multi-frame time | `GetFrameRangeTopTimeSummary` |
| naming conventions | `GetUserGuidelines` |
| orthographic capture | `Capture2DScene` |
| package info | `PackageManager_GetData` |
| pause game | `ManageEditor` (Pause) |
| play game | `ManageEditor` (Play) |
| precise edit | `ApplyTextEdits` |
| prefab stage | `ManageEditor` (GetPrefabStage) |
| profiler overall | `GetOverallGcAlloca_ac50c101` |
| project overview | `GetProjectData` |
| project root | `ManageEditor` (GetProjectRoot) |
| read file | `ReadResource` |
| read script | `ReadResource` |
| read shader | `ManageShader` (Read) |
| regex search | `FindInFile` |
| related threads | `GetRelatedSamplesT_a6086ba0` |
| remove background | `GenerateAsset` (RemoveSpriteBackground / RemoveImageBackground) |
| remove component | `ManageGameObject` (remove_component) |
| remove package | `PackageManager_ExecuteAction` (Remove) |
| remove root motion | `EditAnimati_47017090` (MakeStationary) |
| rename asset | `ManageAsset` (Rename) |
| replace method | `ScriptApplyEdits` (replace_method) |
| resume generation | `ManageInterrupted` (Resume) |
| run C# code | `RunCommand` |
| sample time | `GetSampleTimeSummary` |
| save as prefab | `ManageGameObject` (save_as_prefab) |
| save scene | `ManageScene` (Save) |
| scene view capture | `Camera_Capture` (no cameraInstanceID) |
| script capabilities | `ManageScript_capabilities` |
| search assets | `ManageAsset` (Search) or `FindProjectAssets` |
| self time | `GetFrameSelfTimeSa_e44ee448` |
| semantic search | `FindProjectAssets` |
| set component property | `ManageGameObject` (set_component_property) |
| SHA256 | `GetSha` |
| sprite sheet to anim | `ConvertSpri_dca62520` |
| stop game | `ManageEditor` (Stop) |
| texture to material | `ConvertToMaterial` |
| texture to terrain layer | `ConvertToTerrainLayer` |
| tilemap capture | `Capture2DScene` |
| top time samples | `GetFrameTopTimeSam_ccc85b2d` |
| trim to loop | `EditAnimati_47017090` (TrimToBestLoop) |
| upscale cubemap | `GenerateAsset` (UpscaleCubemap) |
| validate script | `ValidateScript` |

---

## Workflow Cheat Sheet

### Before Writing Code
1. `GetUserGuidelines` -- load project conventions
2. `ListResources` -- find relevant files
3. `ReadResource` -- read existing code

### Creating a Script
1. `CreateScript` -- write the file
2. `ValidateScript` -- check for errors
3. `ReadConsole(Get)` -- verify no compile errors

### Editing a Script (Structural)
1. `ReadResource` -- read current state
2. `FindInFile` -- locate target method/pattern
3. `ScriptApplyEdits` -- apply structural edit (Preview=true first)
4. `ValidateScript` -- verify result

### Editing a Script (Precise)
1. `ReadResource` -- read current state
2. `GetSha` -- get precondition hash
3. `ApplyTextEdits` -- apply edit with SHA
4. `ValidateScript` -- verify result

### Generating an Asset
1. `GetModels` -- pick a model ID
2. `GetComposit_832d2c69` -- (optional) pick composition pattern for materials
3. `GenerateAsset` -- generate with prompt + modelId
4. `FindProjectAssets` -- verify it was created

### Profiling Investigation
1. `GetOverallGcAlloca_ac50c101` -- start with overall picture
2. `GetFrameRangeTopTimeSummary` -- identify slow frame range
3. `GetFrameTopTimeSam_ccc85b2d` -- drill into worst frame
4. `GetSampleTimeSummary` / `GetSampleGcAllocat_4a279ae5` -- drill into specific sample
5. `GetRelatedSamplesT_a6086ba0` -- check cross-thread impact

### Scene Setup
1. `ManageScene(GetActive)` -- check current scene
2. `ManageGameObject(create)` -- create objects
3. `ManageGameObject(add_component)` -- add components
4. `ManageGameObject(set_component_property)` -- configure
5. `CaptureMultiAngleSceneView` or `Capture2DScene` -- verify visually

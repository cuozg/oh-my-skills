# Unity MCP Routing Matrix

Use this when Unity Editor automation is available through MCP. Tool names vary
by integration version, so route by capability first, then inspect the exact tool
schema in the current session.

## First Checks

1. Confirm the active Unity project/root before modifying anything.
2. Read user/project guidelines if the Unity MCP exposes them.
3. Prefer read-only inspection before mutation.
4. For script edits, read the target content and use structured edits when
   possible.
5. After modifications, refresh/compile, scan console errors, and run focused
   tests or scene validation.

## Capability Routing

| Need | Use Tool Family | Notes |
| --- | --- | --- |
| Read project guidelines/context | project/user-guideline tools | Do this before project-specific code work. |
| Search files or assets | grep/find/list asset tools | Prefer narrow search terms and paged results. |
| Read a file | read resource/script tools | Use line slicing around the relevant symbol. |
| Create C# script | create script tool | Match namespace/folder/asmdef conventions. |
| Edit C# script structurally | script apply edits | Prefer method/class/anchor edits over raw ranges. |
| Edit exact text ranges | apply text edits | Verify line/column and SHA first. |
| Validate script | validate script / refresh compile | Compile evidence beats static guesses. |
| Scene/GameObject changes | manage scene/gameobject/component tools | Use instance IDs or full paths when possible. |
| Prefab work | prefab tools | Prefer prefab-stage/headless prefab edits over scene instances. |
| UI Toolkit | UI tools | Keep UXML/USS/controller changes together and render when possible. |
| Materials/textures/VFX/audio | domain asset tools | Use non-generative conversion tools for existing assets. |
| Generated assets | asset-generation tools | Use only when the user explicitly asks for generation. |
| Console/debugging | console tools | Pull errors/warnings with stack traces for root cause. |
| Screenshots/visual QA | camera/scene capture tools | Choose 2D, camera, or multi-angle based on project type. |
| Build/package settings | build/package/editor tools | Treat build setting changes as high blast radius. |
| Arbitrary editor C# | run-command/execute-code tools | Use for inspection or batch editor operations; keep code small. |

## Script Edit Standards

- Use structured script edits for method replacement, insertion, and anchor-based
  changes.
- Use precise text edits only after reading the target lines and obtaining a
  precondition hash when available.
- Do not use broad whole-file rewrites for small changes.
- Validate after editing and inspect console errors.

## Scene And Prefab Standards

- Search by path or instance ID when names are ambiguous.
- Read components before setting serialized properties.
- Register or use tool-supported undo/dirty handling when available.
- Save scenes/prefabs only when the requested work requires persistence.
- For visual/layout changes, capture a screenshot or scene view when feasible.

## Asset Generation Guardrails

- Call model-listing tools before generative asset tools when the schema requires
  a model ID.
- Use conversion tools for existing textures, sprite sheets, materials, terrain
  layers, animation clips, or controller creation.
- Do not generate assets as a shortcut for code, scene setup, or explanation
  tasks.
- Place generated assets under the requested or project-standard folder.

## Debugging And QA Loop

1. Read console errors/warnings.
2. Inspect the failing object/script/asset.
3. Reproduce through Play Mode, tests, scene capture, or targeted command when
   practical.
4. Apply the smallest fix.
5. Refresh/compile, rerun the narrow proof, and rescan console.

## When MCP Is Not Enough

Use normal shell/git tools for repository-wide text search, diffs, package files,
and non-Unity assets. Use Unity MCP for editor state, serialized object data,
scene/prefab inspection, compile feedback, and Play Mode proof.

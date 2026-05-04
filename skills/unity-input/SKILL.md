---
name: unity-input
description: "Work on Unity input across gameplay, UI, controllers, rebinding, touch, and debugging. MUST use for Input System action assets, legacy Input Manager checks, PlayerInput components, generated input wrappers, controller support, mobile touch controls, rebinding UX, and input behavior validation. Do not convert input backends or replace bindings without explicit approval."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-input

Guide safe Unity input work across legacy Input Manager, the Input System package, UI input, controllers, and mobile touch.

## When to use

Use for:

- Gameplay input actions, maps, bindings, and control schemes.
- UI input modules and navigation issues.
- Controller/gamepad/keyboard/mouse support.
- Rebinding and generated wrapper validation.
- Touch input, gestures, and mobile control checks.
- Input debugging across platforms.

## Discovery

1. Check `Packages/manifest.json` and `Packages/packages-lock.json` for `com.unity.inputsystem`.
2. Inspect `ProjectSettings/ProjectSettings.asset` for active input handling when needed.
3. Locate `.inputactions` assets, generated wrappers, `PlayerInput`, `InputActionAsset`, and UI input modules.
4. Determine whether the project uses legacy input, the Input System package, or both.
5. Identify platform-specific controls and existing binding conventions before changes.

## MCP tool usage

- Use `ManageAsset(Search/GetInfo)` to find `.inputactions`, settings, prefabs, and scenes using input components.
- Use `ManageGameObject(GetComponents/GetComponent)` to inspect `PlayerInput`, UI modules, and input-related MonoBehaviours.
- Use `ReadConsole` or `GetConsoleLogs` for input package, generated wrapper, or compile errors.
- Use `ManageEditor(GetState)` before entering Play Mode or inspecting scene state.
- Use `RunCommand` only for targeted editor API inspection when MCP tools cannot expose input settings.

## Safety rules

- Do not convert input backends without explicit user approval.
- Preserve existing bindings unless the user asks for changes.
- Prefer additive action maps or bindings over destructive rewrites.
- Do not regenerate wrappers unless the target `.inputactions` asset and generated class path are clear.
- Keep mobile touch work compatible with desktop/controller paths unless the user requests platform-specific behavior.

## Validation

Verify:

- `.inputactions` assets exist and contain expected action maps and bindings.
- Generated wrappers compile and match asset names when used.
- `PlayerInput` components reference the correct action assets and control schemes.
- UI input modules are compatible with the selected input backend.
- Platform-specific controls are represented by bindings or fallback paths.
- Unity console has no input package, compile, serialization, or generated-code errors.

## Boundaries

- Delegate gameplay behavior implementation to `unity-code` when input is only one part of broader runtime logic.
- Delegate UI Toolkit screen work to `unity-uitoolkit`.
- Delegate mobile platform permission/build concerns to `unity-mobile`.
- Delegate package installation/removal to `unity-package-manager`.

## Handoff

Report detected input backend, affected assets/components, binding changes or recommendations, validation evidence, and any required manual controller/device test.

---
name: unity-qa-automation
description: "Automate Unity QA checks with MCP inspection, scene hierarchy review, GameObject/component validation, Play Mode smoke checks, screenshot or scene captures, console log scanning, and regression evidence. MUST use for non-destructive automated verification, smoke checks, scene validation, screenshot validation, and pass/fail reports. Do not replace unit tests, manual QA test cases, debugging, or profiler analysis."
metadata:
  author: kuozg
  version: "1.0"
---
# unity-qa-automation

Run evidence-backed Unity QA automation using MCP tools without destructive project changes.

## When to use

Use for:

- Smoke checks and regression checks.
- Scene validation and hierarchy inspection.
- GameObject/component presence checks.
- Screenshot, camera, or scene-view validation.
- Console-log-based verification.
- Automated pass/fail reports with concrete evidence.

## MCP tool usage

- Use `ManageScene(GetActive/GetHierarchy/Load)` for scene state and hierarchy checks.
- Use `ManageGameObject(find/get_components/get_component)` for object and component assertions.
- Use `ManageEditor(GetState/Play/Stop)` for controlled Play Mode smoke checks when requested.
- Use `ReadConsole` or `GetConsoleLogs` to scan errors and warnings.
- Use `Camera_Capture`, `SceneView_Capture2DScene`, or `SceneView_CaptureMultiAngleSceneView` when visual evidence is relevant.
- Use `ManageAsset(GetInfo/Search)` for required asset existence checks.

## Safety rules

- Avoid destructive scene or project changes during QA validation.
- Do not save scenes, modify assets, or alter settings unless the test explicitly requires setup and the user approves.
- Do not treat screenshots as sufficient when console, hierarchy, or component checks are required.
- Reset Play Mode state after smoke checks.
- Keep checks deterministic and cite exact evidence.

## Pass/fail reporting

For each check, report:

- Check name.
- Expected condition.
- Observed result.
- Evidence from hierarchy, component data, console output, capture, or asset info.
- Verdict: `PASS`, `FAIL`, or `BLOCKED`.

## Validation patterns

- Scene check: hierarchy exists, required objects active, transforms/components match expectations.
- Prefab/asset check: asset exists and has expected type/references.
- Smoke check: enter Play Mode, observe state/logs, exit Play Mode.
- Screenshot check: capture the relevant view and pair it with hierarchy/console evidence.
- Console check: no new errors, warnings classified, stack traces included when relevant.

## Boundaries

- Use `unity-test-unit` for automated Edit Mode or Play Mode unit tests.
- Use `unity-test-case` for manual QA test plan documents.
- Use `unity-debug` for diagnosing a known failure.
- Use `unity-profiler` for performance traces, frame time, GC, or memory analysis.
- Use `unity-scene-builder` for creating or modifying scenes.

## Handoff

Return a pass/fail report with evidence per check, console status, captures if generated, and any follow-up tests needed.

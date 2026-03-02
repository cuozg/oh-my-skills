# Prefab & Scene Review Checklist

## Missing Scripts

- [ ] No `m_Script: {fileID: 0, guid: 00000000..., type: 0}` entries (CRITICAL)
- [ ] All component GUIDs resolve to existing `.cs` files in project
- [ ] No orphaned `MonoBehaviour` blocks without a script reference

## Prefab Variants

- [ ] Base prefab GUID in `m_SourcePrefab` resolves to an existing `.prefab` file (CRITICAL if not)
- [ ] Variant overrides do not duplicate entire base prefab structure (NOTE)
- [ ] Nested prefab references all resolve (check all `m_CorrespondingSourceObject` GUIDs)

## UI & Raycast Blockers

- [ ] `Image` / `RawImage` with `raycastTarget: 1` has a parent `Button`, `Toggle`, or `EventTrigger`
- [ ] Fullscreen overlay panels have `raycastTarget: 0` unless intentionally blocking (WARNING)
- [ ] `GraphicRaycaster` exists on Canvas root — not duplicated on children

## Hierarchy & Transforms

- [ ] Hierarchy depth ≤ 8 levels for runtime-spawned prefabs (NOTE if exceeded)
- [ ] Root transform has position `(0,0,0)`, rotation `(0,0,0)`, scale `(1,1,1)` for prefabs
- [ ] No non-uniform scale on GameObjects with `Rigidbody` or `Collider` (WARNING)
- [ ] No duplicate component types on same GameObject except Colliders (WARNING)

## Scene-Specific

- [ ] No duplicate singleton-manager GameObjects in scene (CRITICAL)
- [ ] `activeSelf: 0` on root prefab instances flagged as NOTE
- [ ] Camera has correct `cullingMask` set — not "Everything" in production scenes (NOTE)
- [ ] EventSystem present in UI scenes; absent in non-UI scenes

## Severity Guide

- CRITICAL: missing script, broken variant GUID, duplicate singleton
- WARNING: raycast blocker leak, non-uniform scale on physics object
- NOTE: hierarchy depth, inactive root, style

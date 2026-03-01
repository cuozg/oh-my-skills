# Unity Best Practices Checklist

> For full-project quality audits. PR-level review → see specialized review files.
> Lifecycle & serialization details → `review/review-prefab-patterns.md`, `review/review-general-checklists.md`

---

## Input System

- Using new Input System (`InputAction`, `InputActionAsset`), not legacy `Input.GetKey`
- Input actions defined in `.inputactions` asset, not hardcoded in scripts
- Control scheme defined for each target platform (Keyboard&Mouse, Gamepad, Touch)
- Input processed in `Update`, physics input applied in `FixedUpdate`
- Rebinding UI provided for player customization

## Data Structures

- `Dictionary` for O(1) lookup by key; `List` only for ordered/indexed access
- `HashSet` for membership checks instead of `List.Contains`
- `Queue`/`Stack` for FIFO/LIFO instead of `List` with insert/remove at index 0
- `NativeArray`/`NativeList` for Jobs/Burst-compatible data (dispose in `OnDestroy`)

## Networking

- Authoritative server model — client sends input, server validates
- Network messages use delta compression (send changes, not full state)
- Lag compensation implemented for real-time gameplay
- Connection timeout and reconnection logic in place
- Server validates all client inputs (never trust client state)

## Accessibility

- Text meets minimum contrast ratio (4.5:1 for body, 3:1 for large text)
- Interactive elements have minimum touch target 44×44dp
- Color is not the sole indicator (use icons, patterns, or labels alongside)
- Subtitles/captions available for dialogue and important audio cues
- Remappable controls and alternative input methods supported

## Scripting Standards

- `[RequireComponent]` used for hard dependencies
- `CompareTag()` instead of `== "tag"` (avoids allocation)
- `TryGetComponent` instead of `GetComponent` + null check
- Coroutines cached: `_waitForSeconds = new WaitForSeconds(1f)` (avoids per-call allocation)
- `StringBuilder` for string construction in loops (not `+=` concatenation)

---

## Lifecycle Quick Reference

> Full lifecycle review → `review/review-general-checklists.md` (Lifecycle section)

| Phase | Use For | Don't |
|-------|---------|-------|
| `Awake` | Self-init, `GetComponent`, field assignment | Reference other objects (not guaranteed initialized) |
| `OnEnable` | Subscribe events, register with managers | Heavy computation (called on every enable) |
| `Start` | Cross-object setup, initial state | Assume other `Start` methods ran already |
| `OnDisable` | Unsubscribe events, pause behavior | Destroy shared resources (other scripts may need them) |
| `OnDestroy` | Final cleanup, dispose native resources | Access other destroyed objects |

## Serialization Quick Reference

> Full serialization review → `review/review-prefab-patterns.md` (Serialization section)

| Rule | Why |
|------|-----|
| `[FormerlySerializedAs]` before field rename | Prevents data loss in existing prefabs/scenes |
| `[field: SerializeField]` on auto-properties | Unity can't serialize auto-properties without it |
| `[System.Serializable]` on nested classes | Required for Inspector visibility |
| Never serialize `Dictionary` directly | Use `List<SerializableKeyValue>` wrapper |
| Validate in `OnValidate()` | Catch invalid Inspector values in editor |

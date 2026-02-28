# Prefab Review — .prefab/.unity Files

Load when PR modifies `.prefab`, `.unity`, or prefab-related `.asset` files.

## :red_circle: Critical

| YAML Pattern | Issue | Fix |
|:-------------|:------|:----|
| `m_Script: {fileID: 0}` | Missing script ref → MissingReferenceException | Restore GUID or remove component |
| `m_Script` GUID changed vs previous | All instances lose component silently | Check .meta regeneration |
| Same MonoBehaviour type twice on one GO | Duplicate callbacks, state conflict | Remove duplicate |
| `m_CorrespondingSourceObject: {fileID: 0}` | Broken variant link | Re-link or convert to standalone |
| Component block with all fields zeroed | Silent data loss (bad merge) | Revert from git |
| `m_RaycastTarget: 1` on Image/Text without Button/Toggle | Blocks touch on elements behind | `m_RaycastTarget: 0` |
| Full-screen Image with `m_RaycastTarget: 1` | Screen unresponsive | `m_RaycastTarget: 0` (unless intentional blocker) |
| Canvas without GraphicRaycaster | No UI input works | Add GraphicRaycaster |
| Scene with Canvas but no EventSystem | All UI non-functional | Add EventSystem |
| Rigidbody on UI hierarchy | Physics on UI = unexpected | Remove |
| `[SerializeField]` renamed without `[FormerlySerializedAs]` | Prefab data silently lost | Add attribute |
| Field type changed on serialized field | Deserialization zeroes data | Migration code |
| Nested Canvas without `overrideSorting` where independent sort is required | Inherited sorting causes draw-order conflict/Z-fighting | Enable `overrideSorting` and assign explicit sorting order |
| `m_LocalEulerAnglesHint` diverges from `m_LocalRotation` after merge | Transform inspector mismatch and unstable edits | Re-save transform from editor to realign quaternion/hint |
| `m_AnchorMin == m_AnchorMax` + non-zero `m_SizeDelta` under LayoutGroup | Manual rect conflicts with layout-driven sizing | Let LayoutGroup drive size or remove layout control |
| Root Canvas missing `CanvasScaler` | Resolution-dependent UI size breaks across devices | Add/configure `CanvasScaler` strategy |
| Nested prefab instance points to missing/deleted source | Broken nested prefab reference and missing content | Re-link nested prefab or replace instance |

## :yellow_circle: Major

| Pattern | Fix |
|:--------|:----|
| `m_Modifications` with 20+ entries (override sprawl) | Apply intentional to base, revert accidental |
| 5+ levels empty parent transforms | Flatten hierarchy |
| `m_IsActive: 0` children not toggled by code | Remove if unused |
| Anchor mismatch for intended layout | Fix anchors |
| LayoutGroup parent + hardcoded position on child | Remove one |
| ContentSizeFitter on LayoutGroup child | Move to separate object |
| Button `m_OnClick` with 0 persistent calls | Wire handler or remove |
| `m_Target: {fileID: 0}` in persistent call | Fix target ref |
| Canvas sort order collision | Unique sort orders |
| `m_PlayOnAwake: 1` unintentional | `m_PlayOnAwake: 0` |
| `m_Controller: {fileID: 0}` | Assign or remove Animator |
| `prewarm: 1` on heavy ParticleSystem | Disable prewarm |
| Small touch target without `m_RaycastPadding` | Add padding to meet minimum tap area (~44px) |
| TextMeshPro `m_enableAutoSizing: 1` inside LayoutGroup | Disable autosize or isolate text from layout-driven size loops |
| UI Animator `updateMode: 0` (Normal) for pause-independent UI | Use UnscaledTime for pause menus/HUD transitions |
| Collider moved at runtime without matching Rigidbody | Add Rigidbody or avoid runtime movement |
| Multiple AudioSource components on one GO without intent | Split by purpose or document clearly |
| ParticleSystem default `maxParticles: 1000` on mobile-target effect | Set platform-appropriate particle cap |

## :large_blue_circle: Minor

Default naming (`GameObject (1)`), empty GameObjects, hardcoded text (localization), added component on variant (confirm variant-specific).

## Grep — Run on changed prefabs

For each changed .prefab/.unity file, run these grep patterns:
- `m_Script: {fileID: 0}` — missing scripts
- `m_CorrespondingSourceObject: {fileID: 0}` — broken variant
- `m_RaycastTarget: 1` — raycast audit (check if GO has Button/Toggle/InputField, if not → :red_circle:)
- `{fileID: 10303}` — default material
- `m_PlayOnAwake: 1` — audio auto-play
- `m_Controller: {fileID: 0}` — empty animator

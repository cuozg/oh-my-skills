# Prefab Review — .prefab/.unity Files

Load when PR modifies `.prefab`, `.unity`, or prefab-related `.asset` files.

## 🔴 Critical

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

## 🟡 Major

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

## 🔵 Minor

Default naming (`GameObject (1)`), empty GameObjects, hardcoded text (localization), added component on variant (confirm variant-specific).

## Grep — Run on changed prefabs

```bash
for f in $(gh pr diff <N> --name-only | grep -E '\.(prefab|unity)$'); do
  grep -n "m_Script: {fileID: 0}" "$f"                    # missing scripts
  grep -n "m_CorrespondingSourceObject: {fileID: 0}" "$f"  # broken variant
  grep -n "m_RaycastTarget: 1" "$f"                        # raycast audit
  grep -n "{fileID: 10303}" "$f"                            # default material
  grep -n "m_PlayOnAwake: 1" "$f"                          # audio auto-play
  grep -n "m_Controller: {fileID: 0}" "$f"                 # empty animator
done
```

For each `m_RaycastTarget: 1` hit → check if GO has Button/Toggle/InputField. If not → 🔴.

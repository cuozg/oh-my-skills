# Prefab & Scene Review — PR Checklist

> Authoritative for: prefab/scene YAML patterns, UI hierarchy, serialization in prefabs, scene management.
> Cross-ref: `review-asset-patterns.md` (materials, textures on prefabs), `review-architecture-patterns.md` (scene architecture)

---

## 🔴 Critical — Prefab YAML Patterns

| Name | Issue | Fix |
|------|-------|-----|
| `m_Script: {fileID: 0}` | Missing script — component shows "Missing (Mono Script)" | Remove broken component or restore the script; check `.meta` GUID matches |
| `m_Father: {fileID: 0}` | Detached child — object has no parent in hierarchy | Re-parent in editor; verify prefab variant didn't break nesting |
| `m_PrefabInstance` with empty `m_Modifications` | Prefab instance lost all overrides — reverted silently | Re-apply overrides; check if prefab source was force-reimported |
| `m_CorrespondingSourceObject: {fileID: 0}` | Broken prefab variant link — variant disconnected from base | Re-create variant from base prefab; don't edit variant's internal YAML |
| `serializedVersion` Mismatch | Different Unity versions produced different serialization — merge conflict risk | Standardize Unity version across team; resolve in editor, not text |
| GUID Collision in `.meta` | Two assets share same GUID — references break unpredictably | Delete one `.meta` and reimport; ensure VCS doesn't merge `.meta` files |
| `m_IsActive: 0` on Root | Root GameObject disabled — entire prefab invisible at runtime | Verify intentional; if not, set `m_IsActive: 1`; check instantiation code |

## 🔴 Critical — Serialization

| Name | Issue | Fix |
|------|-------|-----|
| Missing `[SerializeField]` | Private field intended for Inspector not serialized — value lost on play/build | Add `[SerializeField]` to private fields shown in Inspector |
| Missing `[FormerlySerializedAs]` | Field renamed without migration — existing prefab values silently zeroed | Add `[FormerlySerializedAs("oldName")]` before renaming; remove after one release cycle |
| Serializing Non-Serializable Type | `Dictionary`, `interface`, `abstract class` field in Inspector — always null | Use `List<SerializableKeyValue>` for dicts; use concrete type or SO reference |
| `[HideInInspector]` Masking Required Field | Required field hidden — designers can't configure it | Remove `[HideInInspector]` on required fields; use `[Header]` for organization instead |
| SO Runtime Mutation in Prefab | Prefab references SO that gets modified at runtime — shared state bug | Clone SO in `Awake` for runtime use; keep prefab reference as template |

## 🟡 Major — Prefab Structure

| Name | Issue | Fix |
|------|-------|-----|
| Deep Nesting (5+ Levels) | Deeply nested hierarchy — hard to navigate, expensive `GetComponentInChildren` | Flatten hierarchy; use references instead of nesting |
| Oversized Prefab | Prefab >100KB YAML — slow to load, hard to diff, merge-conflict magnet | Split into nested prefabs; extract reusable parts |
| Missing Raycast Target Toggle | UI Image/Text has `Raycast Target: true` when not interactive | Disable `Raycast Target` on decorative UI elements — reduces event processing |
| Incorrect Canvas Render Mode | Canvas set to `Screen Space - Camera` without camera assigned | Assign camera, or use `Screen Space - Overlay` for HUD |
| Missing Layout Fitter | Text or dynamic content overflows its container | Add `ContentSizeFitter` or `LayoutGroup`; set preferred/min sizes |
| Broken Variant Override | Prefab variant overrides property that base prefab later deleted | Open variant in editor; Unity will show warning — resolve by re-creating property |
| Nested Prefab Instance Unpacked | Nested prefab accidentally unpacked — loses connection to source | Re-add as prefab instance; don't unpack unless intentional |
| Event Listener Pointing to Missing Object | `UnityEvent` in prefab references destroyed/moved GameObject | Fix in Inspector; ensure target exists in same prefab scope or scene |

## 🟡 Major — Scene Patterns

| Name | Issue | Fix |
|------|-------|-----|
| Massive Scene File | Scene >1MB YAML — long load, constant merge conflicts | Split into additive scenes (UI, Gameplay, Environment) |
| Baked Lighting Data Committed | `LightingData.asset` and `LightmapSnapshot` in VCS — huge binary files | Add to `.gitignore`; rebake per machine; store settings, not output |
| Scene Contains Test/Debug Objects | Temporary objects (debug cubes, test spawners) left in scene | Remove before PR; use `[ExecuteInEditMode]` tools instead of scene objects |
| DontDestroyOnLoad Objects in Scene | Persistent objects placed in specific scene — breaks if scene isn't loaded first | Spawn persistent objects from bootstrap scene or programmatic initializer |
| Missing Object References | Serialized field shows `None (Type)` — will NullRef at runtime | Assign in Inspector or add null check in `Awake`/`Start` with descriptive error |
| Incorrect Sorting Layer/Order | UI or 2D sprite renders behind/in front of wrong elements | Set `Sorting Layer` and `Order in Layer`; use named layers for clarity |

## 🟡 Major — Serialization Best Practices

| Name | Issue | Fix |
|------|-------|-----|
| Public Field Without `[field: SerializeField]` | Auto-property `public float Speed { get; set; }` not serialized by Unity | Use `[field: SerializeField] public float Speed { get; private set; }` |
| No `OnValidate` for Constrained Values | Inspector allows invalid values (negative health, speed > max) | Add `OnValidate()` to clamp values and log warnings |
| Missing `[Tooltip]` on Inspector Fields | Team doesn't know what each field does | Add `[Tooltip("Description")]` to all designer-facing fields |
| `[System.Serializable]` Missing on Nested Class | Nested class in MonoBehaviour not serialized — values reset on play | Add `[System.Serializable]` to all classes used as serialized fields |
| Large Array in Prefab | 500+ element array serialized in prefab YAML — slow, unmergeable | Move to external data file (JSON, CSV, SO); load at runtime |

## 🔵 Medium

| Name | Issue | Fix |
|------|-------|-----|
| Inconsistent Prefab Naming | Mix of `PFB_`, `Prefab_`, no prefix across folders | Standardize: `PFB_Category_Name` or `Name.prefab` in typed folders |
| Missing Prefab Variant for Variations | Copy-pasted prefab with 2 property changes instead of variant | Create prefab variant from base; override only differing properties |
| Canvas Scaler Mismatch | Different canvases use different reference resolutions | Standardize `Canvas Scaler` settings: same reference resolution, match mode |
| Unused Components on Prefab | `AudioSource`, `Collider`, or other component present but unused | Remove unused components — reduces memory and confusion |
| Asset Organization | Prefabs scattered in root `Assets/` folder | Organize: `Assets/Prefabs/{Category}/PFB_Name.prefab` |
| Scene Not in Build Settings | Scene exists but not added to build settings — can't load at runtime | Add to `File > Build Settings`; verify build index is correct |

## 🟢 Minor

| Name | Issue | Fix |
|------|-------|-----|
| Missing `[DisallowMultipleComponent]` | Same component added twice by accident | Add attribute to components that must be unique per GameObject |
| No Preview Icon | Custom component has no gizmo icon — hard to find in scene | Add `[AddComponentMenu]` and custom icon via `MonoScript` |
| Inconsistent UI Anchor Setup | UI elements use absolute positioning instead of anchors | Set anchors to match intended responsive behavior |
| Missing `[RequireComponent]` | Component depends on another (e.g., needs `Rigidbody`) but doesn't declare it | Add `[RequireComponent(typeof(Rigidbody))]` — auto-adds dependency |

---

## PR Grep Commands

```bash
# Find missing scripts in prefabs/scenes
grep -rn "m_Script: {fileID: 0}" Assets/ --include="*.prefab" --include="*.unity"

# Find broken prefab variant links
grep -rn "m_CorrespondingSourceObject: {fileID: 0}" Assets/ --include="*.prefab"

# Find disabled root objects
grep -rn "m_IsActive: 0" Assets/ --include="*.prefab" | head -20

# Find UI elements with Raycast Target enabled
grep -rn "m_RaycastTarget: 1" Assets/ --include="*.prefab"

# Find large prefab files (>100KB)
find Assets/ -name "*.prefab" -size +100k

# Find FormerlySerializedAs usage (migration tracking)
grep -rn "FormerlySerializedAs" Assets/Scripts/ --include="*.cs"
```

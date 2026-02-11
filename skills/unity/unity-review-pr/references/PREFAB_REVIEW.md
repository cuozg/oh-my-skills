# Prefab Review Checklist

Load this reference when PR modifies `.prefab`, `.unity`, or prefab-related `.asset` files. Each issue follows: **Issue → Why → Fix → Priority**.

---

## Table of Contents

1. [Script References](#1-script-references)
2. [Prefab Variant Integrity](#2-prefab-variant-integrity)
3. [Hierarchy & Structure](#3-hierarchy--structure)
4. [Serialization Safety](#4-serialization-safety)
5. [UI Prefab Configuration](#5-ui-prefab-configuration)
6. [Component Integrity](#6-component-integrity)
7. [Grep Patterns](#7-grep-patterns)

---

## 1. Script References

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Missing script reference** | `m_Script: {fileID: 0}` | `MissingReferenceException` at runtime; all serialized data on this component is lost | Restore correct script GUID or remove dead component | 🔴 Critical |
| **Script GUID changed** | `m_Script` GUID differs from previous version in diff | All prefab instances referencing old GUID lose the component silently | Verify `.meta` file wasn't regenerated; restore original GUID | 🔴 Critical |
| **Multiple scripts of same type** | Same MonoBehaviour type appears twice on one GameObject | Both receive callbacks; state conflicts; undefined behavior | Remove duplicate; verify which holds correct serialized data | 🔴 Critical |

### Example

```yaml
# BAD — zeroed script GUID
--- !u!114 &7854932106809508124
MonoBehaviour:
  m_Script: {fileID: 0}          # ← class deleted or .meta regenerated
  m_Name:
  m_EditorClassIdentifier:

# FIX: Restore correct GUID from git history, or remove entire component block
```

---

## 2. Prefab Variant Integrity

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Broken variant link** | `m_CorrespondingSourceObject: {fileID: 0}` | Variant loses all parent overrides; visual/behavioral regression | Re-link to source prefab or convert to standalone prefab | 🔴 Critical |
| **Override sprawl** | Large `m_Modifications` block with 20+ entries | Hard to track intentional vs accidental overrides; merge conflict magnet | Apply intentional overrides to base; revert accidental ones | 🟡 Major |
| **Removed override resets to base** | Property removed from `m_Modifications` | Property silently reverts to base prefab value — may be unintended | Verify the revert is intentional; re-apply if not | 🟡 Major |
| **Added component on variant** | New component appears only on variant | May indicate logic that should live in base prefab | Confirm this is variant-specific; push to base if shared | 🔵 Minor |

---

## 3. Hierarchy & Structure

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Excessive nesting** | 5+ levels of empty parent transforms | Each level adds Transform overhead; complicates code access via `Find`/path | Flatten hierarchy; merge transforms where possible | 🟡 Major |
| **Orphaned inactive children** | `m_IsActive: 0` on children not toggled by code | Dead objects inflate prefab size and instantiate cost | Confirm intentional; remove if unused | 🟡 Major |
| **Default naming** | `GameObject`, `GameObject (1)`, `Image (2)` | Unreadable hierarchy; impossible to reference by name | Rename to describe purpose: `HealthBar`, `TitleText` | 🔵 Minor |
| **Empty GameObjects** | GameObject with only Transform, no components, no children | Clutter; potential leftover from iteration | Remove or document purpose | 🔵 Minor |
| **Stripped component data** | Component block present but all fields zeroed unexpectedly | Silent data loss on existing instances | Revert; likely bad merge conflict resolution | 🔴 Critical |

---

## 4. Serialization Safety

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Field renamed without migration** | `[SerializeField]` field name changed in C# diff; no `[FormerlySerializedAs]` | All existing prefab/SO instances lose the value silently | Add `[FormerlySerializedAs("oldName")]` before the field | 🔴 Critical |
| **Field type changed** | Serialized field type changed (e.g., `int` → `float`, `string` → `enum`) | Deserialization fails silently; data zeroed | Add migration code or versioned deserialization | 🔴 Critical |
| **SerializeReference type removed** | `[SerializeReference]` concrete type deleted | Existing data becomes `null`; `ManagedReferenceMissingType` warning | Preserve type or add migration | 🔴 Critical |
| **Visibility flip** | `private` → `public` on `[SerializeField]` field | Can break prefab serialization path; exposes internals | Keep `[SerializeField] private`; add property if external access needed | 🟡 Major |

---

## 5. UI Prefab Configuration

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **RaycastTarget on decoration** | `m_RaycastTarget: 1` on Image/Text without Button/Toggle/InputField sibling | Blocks touch/click on interactive elements underneath; invisible to testers | Set `m_RaycastTarget: 0` | 🔴 Critical |
| **RaycastTarget on full-screen overlay** | Full-screen Image with `m_RaycastTarget: 1` as background | Entire screen becomes unresponsive | `m_RaycastTarget: 0` unless intentional touch blocker | 🔴 Critical |
| **Missing GraphicRaycaster** | Canvas without `GraphicRaycaster` component | No UI element on this Canvas receives input | Add `GraphicRaycaster` | 🔴 Critical |
| **Missing EventSystem** | Scene has Canvas but no EventSystem GameObject | All UI input non-functional | Add EventSystem with InputModule | 🔴 Critical |
| **Missing CanvasRenderer** | UI element has Image/Text but no CanvasRenderer | Element invisible at runtime | Add CanvasRenderer | 🟡 Major |
| **Anchor mismatch** | `m_AnchorMin`/`m_AnchorMax` don't match stretch/fixed intent | UI breaks on different resolutions | Set anchors matching layout intent | 🟡 Major |
| **LayoutGroup + manual position** | LayoutGroup on parent + hardcoded `m_AnchoredPosition` on child | Layout fights manual position; unpredictable | Remove manual position or LayoutGroup | 🟡 Major |
| **ContentSizeFitter conflict** | `ContentSizeFitter` on same object as `LayoutGroup` child | Size oscillation; layout rebuild loops | Move to parent or separate object | 🟡 Major |
| **Empty onClick** | Button `m_OnClick` with 0 persistent calls | Button does nothing when clicked | Wire handler or remove button | 🟡 Major |
| **Missing event target** | `m_Target: {fileID: 0}` in persistent call | `NullReferenceException` on click | Fix target reference | 🟡 Major |
| **Canvas sort order collision** | Multiple Canvases with same `m_SortingOrder` | Undefined render order; flickering | Assign unique sort orders | 🟡 Major |
| **Hardcoded text** | Text component with non-placeholder content | Breaks localization | Use localization key | 🔵 Minor |

### RaycastTarget Investigation Pattern

```bash
# Find all RaycastTarget: 1 in changed prefabs
for f in $CHANGED_PREFABS; do
  echo "=== RaycastTarget audit: $f ==="
  grep -n "m_RaycastTarget: 1" "$f" 2>/dev/null
done
# Then verify each hit: does the object have Button/Toggle/InputField/ScrollRect?
# If not → flag as 🔴 Critical
```

---

## 6. Component Integrity

| Issue | Evidence | Why | Fix | Priority |
|:------|:---------|:----|:----|:---------|
| **Rigidbody on UI** | Rigidbody/Rigidbody2D on UI hierarchy | Physics component on UI; unexpected behavior | Remove unless intentional physics UI | 🔴 Critical |
| **Collider on disabled GO** | Collider enabled on `m_IsActive: 0` object | May still register in physics broadphase | Disable collider component, not just GO | 🟡 Major |
| **AudioSource playOnAwake** | `m_PlayOnAwake: 1` unintentionally | Sound plays immediately on load | Set `m_PlayOnAwake: 0` | 🟡 Major |
| **Animator no controller** | `m_Controller: {fileID: 0}` | Component overhead with no function | Assign controller or remove Animator | 🟡 Major |
| **ParticleSystem prewarm** | `prewarm: 1` on heavy system | Frame spike on first enable | Disable prewarm or reduce emission | 🟡 Major |

---

## 7. Grep Patterns

Run against changed `.prefab` and `.unity` files:

```bash
CHANGED_PREFABS=$(gh pr diff <number> --name-only | grep -E '\.(prefab|unity)$')

for f in $CHANGED_PREFABS; do
  echo "=== $f ==="
  grep -n "m_Script: {fileID: 0}" "$f" 2>/dev/null          # missing scripts
  grep -n "m_CorrespondingSourceObject: {fileID: 0}" "$f" 2>/dev/null  # broken variant
  grep -n "m_RaycastTarget: 1" "$f" 2>/dev/null              # raycast blocking
  grep -n "{fileID: 10303}" "$f" 2>/dev/null                  # default material
  grep -n "m_IsActive: 0" "$f" 2>/dev/null                   # inactive objects
  grep -n "m_PlayOnAwake: 1" "$f" 2>/dev/null                # audio auto-play
  grep -n "m_Controller: {fileID: 0}" "$f" 2>/dev/null       # empty animator
done
```

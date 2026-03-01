# Unity PR Review Checker

Automated static analysis for Unity C# projects. Runs the same rule set in two places:

- **Unity EditorWindow** — IMGUI tool under `Tools › PR Review Checker` for local pre-commit review
- **CI Python script** — headless scanner for GitHub Actions with annotations, SARIF, and JSON output

---

## Quick Start

### 1 — Editor Tool (Local)

Copy the `Editor/` folder into your Unity project's `Assets/` folder:

```
YourProject/
└── Assets/
    └── Editor/
        └── PRReviewChecker/       ← copy this entire folder
            ├── PRReviewFinding.cs
            ├── PRReviewEngine.cs
            ├── PRReviewCheckerWindow.cs
            └── Rules/
                ├── CodeLogicRules.cs
                ├── SerializationRules.cs
                ├── SecurityRules.cs
                ├── PerformanceRules.cs
                ├── PrefabRules.cs
                └── AssetSettingsRules.cs
```

Open the window: **Tools › PR Review Checker** (or `Ctrl+Shift+P`)

The window scans your `Assets/` folder and displays findings grouped by category, with severity badges (🔴 P0 / 🟠 P1 / 🔵 P2), search/filter toolbar, a split detail panel, and a **Copy Report** button.

### 2 — CI Script (GitHub Actions)

1. Copy `Scripts/pr_review_check.py` into your repo (e.g. `Scripts/`)
2. Copy `.github/workflows/pr-review-check.yml` into your repo's `.github/workflows/`
3. Edit the two env vars at the top of the workflow file:

```yaml
env:
  ASSETS_ROOT: Assets                     # path to your Assets/ folder
  SCRIPT_PATH: Scripts/pr_review_check.py # path to the script
  FAIL_ON: P1                             # P0 | P1 | P2 | none
```

The workflow triggers on PRs that touch `.cs`, `.prefab`, `.unity`, `.mat`, `.anim`, `.fbx`, or `.meta` files.

---

## Script Usage

```bash
# Basic terminal report
python Scripts/pr_review_check.py Assets/

# GitHub Actions annotations (used in CI)
python Scripts/pr_review_check.py Assets/ --github-annotations

# All outputs at once
python Scripts/pr_review_check.py Assets/ \
  --github-annotations \
  --sarif report.sarif.json \
  --json  report.json

# Only run Security rules
python Scripts/pr_review_check.py Assets/ --category Security

# Fail only on P0 (block-merge) findings
python Scripts/pr_review_check.py Assets/ --fail-on P0

# Disable colour (e.g. in pipes)
python Scripts/pr_review_check.py Assets/ --no-color
```

**Exit codes:**
| Code | Meaning |
|------|---------|
| `0` | Clean (or only P2 suggestions) |
| `1` | P0 / P1 findings found (configurable via `--fail-on`) |
| `2` | `Assets/` folder not found |

---

## Output Formats

| Flag | Output |
|------|--------|
| _(default)_ | ANSI colour terminal report |
| `--github-annotations` | `::error file=…,line=…::` workflow commands |
| `--sarif output.json` | SARIF v2.1 (uploaded to GitHub Code Scanning) |
| `--json output.json` | Raw findings array |

---

## Rule Reference

### 🔴 P0 — Block Merge

| Rule ID | Category | Description |
|---------|----------|-------------|
| SEC001 | Security | PlayerPrefs stores a secret/password/token key |
| SEC002 | Security | Hard-coded API key or secret string literal |
| SEC003 | Security | `Assembly.Load` — CVE-2025-59489 RCE vector |
| SEC004 | Security | `Application.OpenURL` called with non-literal (open redirect) |
| SEC005 | Security | Deprecated `WWW` class (use `UnityWebRequest`) |
| SEC006 | Security | Plain HTTP endpoint (use HTTPS) |

### 🟠 P1 — Must Fix

| Rule ID | Category | Description |
|---------|----------|-------------|
| CL001 | Code Logic | `== null` on a UnityEngine.Object (use `!obj` instead) |
| CL002 | Code Logic | `Camera.main` called in Update (caches per frame) |
| CL003 | Code Logic | `Find`, `FindObjectOfType`, `FindGameObjectsWithTag` at runtime |
| CL004 | Code Logic | Empty `catch` block swallowing exceptions |
| CL005 | Code Logic | `GetComponent` called inside Update |
| CL006 | Code Logic | `StartCoroutine` called without null-guard |
| CL007 | Code Logic | `Destroy` called without null-guard |
| SR001 | Serialization | `public` field without `[SerializeField]` or `[HideInInspector]` |
| SR002 | Serialization | `Dictionary` in a `[SerializeField]` (not serializable) |
| SR003 | Serialization | Auto-property on `[Serializable]` class (backing field invisible to Unity) |
| SR004 | Serialization | `BinaryFormatter` (obsolete, security risk) |
| SR005 | Serialization | `[SerializeReference]` without null-check on read |
| SR006 | Serialization | `OnValidate` modifies data without `Undo.RecordObject` |
| PERF001 | Performance | String concatenation with `+` inside Update/FixedUpdate/LateUpdate |
| PERF002 | Performance | `new` allocation (List/Array/object) inside Update |
| PERF003 | Performance | LINQ query inside Update |
| PERF004 | Performance | `SendMessage` / `BroadcastMessage` call |
| PERF005 | Performance | Unguarded `Debug.Log` in a production build |
| PERF006 | Performance | Tag comparison via string (`tag == "…"`) instead of `CompareTag` |
| PERF007 | Performance | `RaycastHit` allocated inside a loop |
| PF001 | Prefab | Missing script reference (`fileID: 0`) in prefab YAML |
| PF002 | Prefab | Broken prefab variant (base GUID not found in project) |
| PF003 | Prefab | Canvas without `GraphicRaycaster` component |
| PF004 | Prefab | Non-uniform scale on a GameObject with a collider |

### 🔵 P2 — Suggestions

| Rule ID | Category | Description |
|---------|----------|-------------|
| AS001 | Asset Settings | Texture `Read/Write` enabled (doubles VRAM usage) |
| AS002 | Asset Settings | Sprite with mipmaps enabled (wastes memory) |
| AS003 | Asset Settings | Large texture (>2048px) with no compression |
| AS004 | Asset Settings | Non-power-of-two texture that cannot be compressed on mobile |
| AS005 | Asset Settings | Mesh `Read/Write` enabled outside of Editor |
| AS006 | Asset Settings | Mesh normals disabled but material uses lighting |
| AS007 | Asset Settings | Large audio clip (>200 KB) set to `Decompress On Load` |

---

## Assembly Definition (Optional)

To isolate the Editor scripts from your game assemblies, add an `.asmdef` next to the `PRReviewChecker/` folder:

```json
{
    "name": "PRReviewChecker.Editor",
    "references": [],
    "includePlatforms": ["Editor"],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": false,
    "precompiledReferences": [],
    "autoReferenced": false,
    "defineConstraints": [],
    "versionDefines": [],
    "noEngineReferences": false
}
```

---

## Requirements

| Component | Requirement |
|-----------|-------------|
| Editor C# | Unity 2021.3 LTS+ |
| Python CI | Python 3.9+ (no external dependencies) |
| GitHub Actions | Any GitHub-hosted runner (`ubuntu-latest` recommended) |
| SARIF upload | Repository must have GitHub Advanced Security enabled (or be public) |

---

## License

MIT

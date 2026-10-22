#!/usr/bin/env python3
"""
Generate a Unity project folder structure with assembly definitions and an
agent guide (CLAUDE.md) for any Unity 6 project.

Layout (tiered asmdefs, event-bus feature isolation, MVVM view controllers):
    Assets/
    +-- Scenes/                                 # project-level scenes
    +-- Settings/{Build Profiles,Scenes}/       # build profiles + scene templates
    +-- Tests/{EditMode,PlayMode}/              # test assemblies
    +-- _<Project>/                             # game-specific
    |   +-- Audio, Fonts, Shaders, Sprites, VFXs
    |   +-- Datas/{Events,Levels}               # ScriptableObject data assets
    |   +-- Editor/                             # editor-only scripts
    |   +-- Prefabs/{GamePlay,Services,UI}      # categorized prefabs
    |   +-- Scenes/                             # game scenes
    |   +-- Scripts/
    |   |   +-- Bootstrap/, Core/, Events/, Models/, Systems/
    |   |   +-- Features/<Name>/ ...            # self-contained features
    |   |   +-- ViewControllers/<Name>/ ...     # UI controllers
    |   |   +-- ViewModels/
    +-- _<SDK>/                                 # optional shared SDK
    CLAUDE.md                                   # managed agent-guide block

Usage:
    generate_structure.py [--company <name>] [--project <name>]
        [--features <csv>] [--ui-controllers <csv>] [--sdk <name>]
        [--pipeline auto|URP|URP2D|HDRP|Built-in] [--unity-version <ver>]
        [--gitignore] [--no-claude-md] [--output-dir <path>] [--dry-run]

--company / --project / --pipeline / --unity-version are auto-detected from
--output-dir (ProjectSettings + Packages/manifest.json) when omitted.

Output: JSON manifest of all paths and file contents to stdout.
"""

from __future__ import annotations  # PEP 604 hints on Python 3.7+

import argparse
import json
import re
import sys
from pathlib import Path


GITIGNORE_CONTENT = """# Unity generated
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Bb]uilds/
[Ll]ogs/
[Uu]ser[Ss]ettings/
[Uu]tmp/
[Mm]emoryCaptures/
[Rr]ecordings/

# IDE
.vs/
.idea/
*.csproj
*.sln
*.suo
*.user
*.userprefs
*.pidb
*.booproj

# OS
.DS_Store
Thumbs.db

# Builds
*.apk
*.aab
*.unitypackage
*.app

# Crashlytics
crashlytics-build.properties

# Claude — personal settings only; keep CLAUDE.md and shared .claude/ content tracked
.claude/settings.local.json
CLAUDE.local.md
"""

# Markers delimiting the CLAUDE.md section this script owns. Anything outside
# the markers belongs to the user and is never touched on re-runs.
CLAUDE_BEGIN = "<!-- unity-init:begin (managed by unity-init; edit outside this block) -->"
CLAUDE_END = "<!-- unity-init:end -->"

PIPELINE_CHOICES = ["auto", "URP", "URP2D", "HDRP", "Built-in"]
DEFAULT_UNITY_VERSION = "Unity 6 LTS (6000.x)"


def make_asmdef(
    name: str,
    references: list[str] | None = None,
    *,
    is_test: bool = False,
    editor_only: bool = False,
    auto_referenced: bool = True,
    root_namespace: str = "",
) -> str:
    """Generate .asmdef JSON content."""
    asmdef: dict = {
        "name": name,
        "rootNamespace": root_namespace or name,
        "references": references or [],
        "includePlatforms": ["Editor"] if editor_only else [],
        "excludePlatforms": [],
        "allowUnsafeCode": False,
        "overrideReferences": is_test,
        "precompiledReferences": [],
        "autoReferenced": auto_referenced,
        "defineConstraints": ["UNITY_INCLUDE_TESTS"] if is_test else [],
        "versionDefines": [],
        "noEngineReferences": False,
    }
    if is_test:
        asmdef["precompiledReferences"] = ["nunit.framework.dll"]
    return json.dumps(asmdef, indent=4)


def to_identifier(raw: str) -> str:
    """Turn a display name ("My Cool Game!") into a C# identifier ("MyCoolGame").

    Unity companyName/productName are free text, but they feed asmdef names and
    namespaces, which must be valid C# identifiers.
    """
    words = re.findall(r"[A-Za-z0-9]+", raw or "")
    ident = "".join(w[:1].upper() + w[1:] for w in words)
    if ident and ident[0].isdigit():
        ident = f"_{ident}"  # namespaces cannot start with a digit
    return ident


# ── Project auto-detection ───────────────────────────────────────
def detect_project_info(project_dir: str | Path | None) -> dict:
    """Read company, product, Unity version, and render pipeline from a Unity project.

    Returns only the keys it could detect, so callers can layer CLI overrides on top.
    """
    info: dict = {}
    if not project_dir:
        return info
    root = Path(project_dir)

    settings = root / "ProjectSettings" / "ProjectSettings.asset"
    if settings.is_file():
        text = settings.read_text(errors="ignore")
        for key, field in (("company", "companyName"), ("project", "productName")):
            m = re.search(rf"^\s*{field}:\s*(.+?)\s*$", text, re.MULTILINE)
            if m and to_identifier(m.group(1)):
                info[key] = to_identifier(m.group(1))

    version = root / "ProjectSettings" / "ProjectVersion.txt"
    if version.is_file():
        m = re.search(r"m_EditorVersion:\s*(\S+)", version.read_text(errors="ignore"))
        if m:
            info["unity_version"] = m.group(1)

    manifest = root / "Packages" / "manifest.json"
    if manifest.is_file():
        try:
            deps = json.loads(manifest.read_text()).get("dependencies", {})
        except (json.JSONDecodeError, AttributeError):
            deps = {}
        if "com.unity.render-pipelines.high-definition" in deps:
            info["pipeline"] = "HDRP"
        elif "com.unity.render-pipelines.universal" in deps:
            # URP vs URP 2D lives in the renderer asset, not the manifest; the
            # 2D feature package is the cheap signal for 2D projects.
            info["pipeline"] = "URP2D" if "com.unity.feature.2d" in deps else "URP"
        else:
            info["pipeline"] = "Built-in"

    return info


# ── Docs ─────────────────────────────────────────────────────────
def make_readme(feature: str) -> str:
    return f"# {feature}\n\nWhat this feature does and how to use it.\n"


def make_agents(feature: str, ns_root: str) -> str:
    # Event channel is derived from the namespace root (was hardcoded to one title).
    return (
        f"# {feature} — Agent Rules\n\n"
        f"Feature-specific constraints and gotchas for `{feature}`.\n\n"
        f"- Communicate with other features via `{ns_root}.Events` only.\n"
        f"- Do not reference other features directly.\n"
    )


def make_project_readme(project: str) -> str:
    return (
        f"# {project}\n\nGame-specific root. Add features under `Scripts/Features/` "
        f"and data under `Datas/`.\n"
    )


def make_project_agents(project: str) -> str:
    return (
        f"# {project} — Agent Rules\n\n"
        f"- Follow the root `CLAUDE.md` (unity-init block) before any change.\n"
        f"- Asset-first: create ScriptableObject/prefab before logic.\n"
        f"- Update `README.md` + `AGENTS.md` of any feature you touch.\n"
    )


def make_claude_md(
    *,
    project: str,
    ns_root: str,
    project_root: str,
    pipeline: str,
    unity_version: str,
    features: list[str],
    ui_controllers: list[str],
    sdk_root: str | None,
) -> str:
    """Build the managed CLAUDE.md block: project facts, mandatory rules, how-to.

    Everything is derived from the generation inputs so the guide always matches
    the generated tree.
    """
    feature_list = ", ".join(f"`{f}`" for f in features) or "_none yet_"
    vc_list = ", ".join(f"`{c}`" for c in ui_controllers) or "_none yet_"
    sdk_row = f"| `{sdk_root}/` | Shared SDK (Core, Events, Editor) |\n" if sdk_root else ""

    return f"""{CLAUDE_BEGIN}
# {project} — Agent Guide

## Project Facts

| Key | Value |
|---|---|
| Unity | {unity_version} — source of truth: `ProjectSettings/ProjectVersion.txt` |
| Render pipeline | {pipeline} |
| Namespace root | `{ns_root}` |
| Game root | `{project_root}/` |
| Features | {feature_list} |
| UI view controllers | {vc_list} |

## MANDATORY — Unity CLI

Every Editor interaction goes through the `unity` CLI (`unity:unity-cli` skill). No exceptions.

1. **Preflight before any Editor-dependent step** (compile, console, tests, scene/prefab/asset edits, Play Mode):
   `unity status --format json` → `unity command --format json`. If `unity` is not installed, stop and ask the user to install it (see `unity:unity-cli`).
2. **Never hand-edit `.unity`, `.prefab`, or `.asset` YAML while an Editor is reachable.** Use the Editor's commands (`unity command --query <term>` to find them). With no Editor, say "no live Editor detected — editing the file directly" before touching YAML.
3. **Compile check after every C# change**: `unity command recompile` (name as listed) + console scan for `error CS`. If the CLI cannot connect, check Safe Mode first: `unity pipeline list --format json`, then `grep -E 'error CS[0-9]{{4}}' Logs/Editor.log`.
4. **No "done" without test evidence**: report the `unity test` (or Editor test command) result and exit code (`0` pass, `8` tests failed, `6` no verdict). If tests could not run, say "not run" — never imply they passed.
5. Pass `--caller plugin --skill <skill-in-use>` on every `unity command`; pass `--project-path .` when more than one Editor is open.
6. A sandboxed shell can hide a running Editor: ask the user before concluding none is open. Never suggest disabling the sandbox.

## MANDATORY — Unity Skills

Invoke the matching skill **before** acting; follow its workflow and output template.

| Task | Skill |
|---|---|
| Any runtime C# (write, refactor, review standards) | `unity-standards` |
| Editor tooling — inspectors, windows, drawers, gizmos, menu items | `unity-editor` |
| Unit tests (Edit Mode / Play Mode) | `unity-test-unit` |
| Bug, error, crash, wrong behavior | `unity-debug` (+ `unity-log` for trace logs) |
| Pull request review | `unity-review-pr` |
| Technical design / "how should we build this" | `unity-technical` |
| Estimate — HTML report / CSV sheet | `unity-costing` / `unity-wbs` |
| System documentation | `unity-document` |
| UI Toolkit / uGUI | `unity:ui-uitk` / `unity:ui-ugui` |
| Packages (UPM add/remove/upgrade) | `unity:unity-package-management` |
| Editor, tests, builds, project/version management | `unity:unity-cli` |

If a required skill is not installed, stop and tell the user which one is missing — do not improvise its workflow.

## How to Work With This Project

Run commands from the project root (the folder containing this file).

```bash
unity open .                                   # opens with the version in ProjectVersion.txt
unity status --format json                     # wait for an instance with state "ready"
unity pipeline list                            # com.unity.pipeline present? install only after asking:
#   unity pipeline install --project-path .
unity command --format json                    # discover what this Editor exposes
unity test . --mode EditMode --format json     # headless tests (close the GUI Editor first)
unity test . --mode PlayMode --format json
unity build . --profile "<Build Profile name>" --output-path Builds/<target>/
```

Build profiles live in `Assets/Settings/Build Profiles/`. Logs: `Logs/Editor.log` — always read through `grep`, never dump whole.

## Project Structure

| Path | Purpose |
|---|---|
| `Assets/Scenes/` | Project-level (non-game) scenes |
| `Assets/Settings/Build Profiles/` | Per-platform build profiles |
| `Assets/Tests/EditMode/`, `Assets/Tests/PlayMode/` | Test assemblies |
| `{project_root}/Datas/` | ScriptableObject data assets (`Events/`, `Levels/`) |
| `{project_root}/Prefabs/` | `GamePlay/`, `Services/`, `UI/` prefabs |
| `{project_root}/Scripts/Core/`, `Events/` | Foundation — zero internal deps |
| `{project_root}/Scripts/Models/` | Data layer → Core |
| `{project_root}/Scripts/Systems/` | Cross-cutting services → Core, Events, Models |
| `{project_root}/Scripts/ViewModels/` | MVVM → Core, Events |
| `{project_root}/Scripts/Features/<Name>/` | Isolated features → Core, Events only |
| `{project_root}/Scripts/ViewControllers/<Name>/` | UI controllers → Core, Events, ViewModels |
| `{project_root}/Scripts/Bootstrap/` | Composition root — the only place features are wired |
| `{project_root}/Editor/` | Editor-only assembly |
{sdk_row}
## Architecture Rules

- Features talk only through `{ns_root}.Events`; never reference another feature assembly.
- `Bootstrap` is the only assembly that wires features together.
- Asset-first: create ScriptableObject data and prefabs before logic.
- Every feature folder keeps `README.md` (what + how) and `AGENTS.md` (gotchas) current.
- No `Resources/` folders — load content through Addressables or explicit references.
- New feature = new `Features/<Name>/Scripts/{ns_root}.Features.<Name>.asmdef` referencing Core + Events, then add it to Bootstrap, Editor, and test asmdefs.
{CLAUDE_END}
"""


def merge_managed_block(existing: str | None, block: str) -> str:
    """Insert or replace the unity-init block inside CLAUDE.md content.

    - No file → the block alone.
    - File without markers → user content kept, block appended.
    - File with markers → only the text between markers is replaced.
    """
    if not existing:
        return block
    start = existing.find(CLAUDE_BEGIN)
    end = existing.find(CLAUDE_END, start if start >= 0 else 0)
    if start >= 0 and end >= 0:
        tail = existing[end + len(CLAUDE_END):].lstrip("\n")
        merged = existing[:start] + block
        return merged + ("\n" + tail if tail else "")
    return existing.rstrip("\n") + "\n\n" + block


# ── Assembly topology ─────────────────────────────────────────────
# Foundation tier (no internal deps)
ZERO_DEP_ASMDEFS = ["Core", "Events"]

# Foundation-tier data layer (depends on Core only)
DATA_ASMDEFS = {"Models": ["Core"]}

# Cross-cutting tier (depend on Core+Events)
CROSSCUTTING_DEPS = {"Systems": ["Core", "Events", "Models"]}


def generate_manifest(
    company: str,
    project: str,
    features: list[str] | None = None,
    ui_controllers: list[str] | None = None,
    sdk: str | None = None,
    pipeline: str = "URP",
    include_gitignore: bool = True,
    include_claude_md: bool = True,
    unity_version: str | None = None,
) -> dict:
    """
    Generate a manifest of directories and files for a Unity project.

    Returns dict with:
        - directories: list of directory paths (relative to project root)
        - files: list of {path, content, mode} dicts
          (mode "create" = skip if exists, "managed-block" = merge into CLAUDE.md)
        - tree: human-readable tree string
    """
    company = to_identifier(company)
    project = to_identifier(project)
    if not company or not project:
        raise ValueError("company and project must contain at least one letter or digit")

    # Strip whitespace from feature / UI controller names; no game-specific defaults.
    features = [f.strip() for f in (features or []) if f and f.strip()]
    ui_controllers = [c.strip() for c in (ui_controllers or []) if c and c.strip()]

    ns_root = f"{company}.{project}"
    project_root = f"Assets/_{project}"

    directories: list[str] = []
    files: list[dict] = []

    # ── Root-level project directories ───────────────────────────
    directories.extend([
        "Assets/Scenes",
        "Assets/Settings/Build Profiles",
        "Assets/Settings/Scenes",
        "Assets/Tests/EditMode",
        "Assets/Tests/PlayMode",
    ])

    # ── _<Project> top-level ─────────────────────────────────────
    project_dirs = [
        f"{project_root}/Audio",
        f"{project_root}/Datas/Events",
        f"{project_root}/Datas/Levels",
        f"{project_root}/Editor",
        f"{project_root}/Fonts",
        f"{project_root}/Prefabs/GamePlay",
        f"{project_root}/Prefabs/Services",
        f"{project_root}/Prefabs/UI",
        f"{project_root}/Scenes",
        f"{project_root}/Shaders",
        f"{project_root}/Sprites",
        f"{project_root}/VFXs",
    ]
    directories.extend(project_dirs)

    # Project README + AGENTS
    files.append({"path": f"{project_root}/README.md", "content": make_project_readme(project)})
    files.append({"path": f"{project_root}/AGENTS.md", "content": make_project_agents(project)})

    # ── _<Project>/Scripts ───────────────────────────────────────
    script_dirs = [
        f"{project_root}/Scripts/Bootstrap",
        f"{project_root}/Scripts/Core",
        f"{project_root}/Scripts/Events",
        f"{project_root}/Scripts/Models",
        f"{project_root}/Scripts/Systems",
        f"{project_root}/Scripts/ViewModels",
    ]
    directories.extend(script_dirs)

    foundation_asmdefs: list[str] = []

    # Zero-dep foundation tier: Core, Events
    for asm in ZERO_DEP_ASMDEFS:
        full = f"{ns_root}.{asm}"
        foundation_asmdefs.append(full)
        files.append({
            "path": f"{project_root}/Scripts/{asm}/{full}.asmdef",
            "content": make_asmdef(full),
        })

    # Data layer (Models → Core)
    for asm, deps in DATA_ASMDEFS.items():
        full = f"{ns_root}.{asm}"
        foundation_asmdefs.append(full)
        refs = [f"{ns_root}.{d}" for d in deps]
        files.append({
            "path": f"{project_root}/Scripts/{asm}/{full}.asmdef",
            "content": make_asmdef(full, references=refs),
        })

    # Cross-cutting tier: Systems, etc.
    for asm, deps in CROSSCUTTING_DEPS.items():
        full = f"{ns_root}.{asm}"
        refs = [f"{ns_root}.{d}" for d in deps]
        files.append({
            "path": f"{project_root}/Scripts/{asm}/{full}.asmdef",
            "content": make_asmdef(full, references=refs),
        })

    # ViewModels tier (depends on Core + Events)
    vm_asm = f"{ns_root}.ViewModels"
    files.append({
        "path": f"{project_root}/Scripts/ViewModels/{vm_asm}.asmdef",
        "content": make_asmdef(vm_asm, references=[f"{ns_root}.Core", f"{ns_root}.Events"]),
    })

    # ── Features ─────────────────────────────────────────────────
    feature_asmdefs: list[str] = []
    for feat in features:
        base = f"{project_root}/Scripts/Features/{feat}"
        directories.extend([f"{base}/Scripts", f"{base}/Tests"])
        asm = f"{ns_root}.Features.{feat}"
        feature_asmdefs.append(asm)
        files.append({
            "path": f"{base}/Scripts/{asm}.asmdef",
            "content": make_asmdef(
                asm, references=[f"{ns_root}.Core", f"{ns_root}.Events"]
            ),
        })
        # Feature docs
        files.append({"path": f"{base}/README.md", "content": make_readme(feat)})
        files.append({"path": f"{base}/AGENTS.md", "content": make_agents(feat, ns_root)})

    # ── UI ViewControllers ───────────────────────────────────────
    vc_asmdefs: list[str] = []
    for vc in ui_controllers:
        base = f"{project_root}/Scripts/ViewControllers/{vc}"
        directories.append(f"{base}/Scripts")
        asm = f"{ns_root}.ViewControllers.{vc}"
        vc_asmdefs.append(asm)
        files.append({
            "path": f"{base}/Scripts/{asm}.asmdef",
            "content": make_asmdef(
                asm, references=[f"{ns_root}.Core", f"{ns_root}.Events", vm_asm]
            ),
        })

    # Top-level ViewControllers (composes sub-controllers + ViewModels)
    vc_root_asm = f"{ns_root}.ViewControllers"
    vc_refs = [
        f"{ns_root}.Core",
        f"{ns_root}.Events",
        vm_asm,
        *vc_asmdefs,
    ]
    files.append({
        "path": f"{project_root}/Scripts/ViewControllers/{vc_root_asm}.asmdef",
        "content": make_asmdef(vc_root_asm, references=vc_refs),
    })
    directories.append(f"{project_root}/Scripts/ViewControllers")

    # ── Bootstrap (composition root, refs Core + Events + every generated feature) ──
    # References only features that actually exist; a fixed list caused
    # missing-assembly errors whenever --features differed from it.
    bootstrap_asm = f"{ns_root}.Bootstrap"
    files.append({
        "path": f"{project_root}/Scripts/Bootstrap/{bootstrap_asm}.asmdef",
        "content": make_asmdef(
            bootstrap_asm,
            references=[f"{ns_root}.Core", f"{ns_root}.Events", *feature_asmdefs],
        ),
    })

    # ── Editor (editor-only, refs everything) ────────────────────
    editor_asm = f"{ns_root}.Editor"
    editor_refs = [
        f"{ns_root}.Core",
        f"{ns_root}.Events",
        f"{ns_root}.ViewModels",
        f"{ns_root}.Models",
        *feature_asmdefs,
    ]
    files.append({
        "path": f"{project_root}/Editor/{editor_asm}.asmdef",
        "content": make_asmdef(
            editor_asm, references=editor_refs, editor_only=True
        ),
    })

    # ── Test assemblies (Assets/Tests/{Edit,Play}Mode) ──────────
    edit_tests = f"{ns_root}.EditMode.Tests"
    files.append({
        "path": f"Assets/Tests/EditMode/{edit_tests}.asmdef",
        "content": make_asmdef(
            edit_tests,
            references=[
                f"{ns_root}.Core",
                f"{ns_root}.Events",
                f"{ns_root}.ViewModels",
                *feature_asmdefs,
            ],
            is_test=True,
            auto_referenced=False,
            editor_only=True,
        ),
    })

    play_tests = f"{ns_root}.PlayMode.Tests"
    files.append({
        "path": f"Assets/Tests/PlayMode/{play_tests}.asmdef",
        "content": make_asmdef(
            play_tests,
            references=[
                f"{ns_root}.Core",
                f"{ns_root}.Events",
                f"{ns_root}.ViewModels",
                f"{ns_root}.Bootstrap",
                *feature_asmdefs,
            ],
            is_test=True,
            auto_referenced=False,
        ),
    })

    # ── Optional SDK scaffold (Assets/_<SDK>) ───────────────────
    sdk_info = None
    sdk_root = None
    if sdk:
        sdk = to_identifier(sdk)
        sdk_root = f"Assets/_{sdk}"
        sdk_ns = f"{company}.{sdk}"
        sdk_dirs = [
            f"{sdk_root}/Scripts/Core",
            f"{sdk_root}/Scripts/Events",
            f"{sdk_root}/Editor",
        ]
        directories.extend(sdk_dirs)

        sdk_core = f"{sdk_ns}.Core"
        sdk_events = f"{sdk_ns}.Events"
        sdk_editor = f"{sdk_ns}.Editor"

        files.append({
            "path": f"{sdk_root}/Scripts/Core/{sdk_core}.asmdef",
            "content": make_asmdef(sdk_core),
        })
        files.append({
            "path": f"{sdk_root}/Scripts/Events/{sdk_events}.asmdef",
            "content": make_asmdef(sdk_events),
        })
        files.append({
            "path": f"{sdk_root}/Editor/{sdk_editor}.asmdef",
            "content": make_asmdef(
                sdk_editor, references=[sdk_core, sdk_events], editor_only=True
            ),
        })
        files.append({"path": f"{sdk_root}/README.md", "content": make_project_readme(sdk)})
        sdk_info = {"root": sdk_root, "namespace": sdk_ns}

    # ── .gitignore ──────────────────────────────────────────────
    if include_gitignore:
        files.append({"path": ".gitignore", "content": GITIGNORE_CONTENT.lstrip()})

    # Every file so far is create-only: never overwrite existing project files.
    for f in files:
        f.setdefault("mode", "create")

    # ── CLAUDE.md (managed block, merged into any existing file) ─
    if include_claude_md:
        files.append({
            "path": "CLAUDE.md",
            "mode": "managed-block",
            "content": make_claude_md(
                project=project,
                ns_root=ns_root,
                project_root=project_root,
                pipeline=pipeline,
                unity_version=unity_version or DEFAULT_UNITY_VERSION,
                features=features,
                ui_controllers=ui_controllers,
                sdk_root=sdk_root,
            ),
        })

    # ── Build tree string ───────────────────────────────────────
    tree = build_tree(directories, files)

    return {
        "company": company,
        "project": project,
        "namespace_root": ns_root,
        "pipeline": pipeline,
        "unity_version": unity_version or DEFAULT_UNITY_VERSION,
        "features": features,
        "ui_controllers": ui_controllers,
        "sdk": sdk_info,
        "directories": sorted(set(directories)),
        "files": files,
        "tree": tree,
    }


def build_tree(directories: list[str], files: list[dict]) -> str:
    """Build a human-readable tree representation."""
    all_paths = sorted(set(directories + [f["path"] for f in files]))
    dir_set = set(directories)
    lines = []
    for p in all_paths:
        suffix = "/" if p in dir_set else ""
        lines.append(f"{p}{suffix}")
    return "\n".join(lines)


def apply_manifest(manifest: dict, output_dir: str) -> dict:
    """Apply manifest to disk without clobbering existing work.

    - "create" files are written only when missing (existing ones are reported as skipped).
    - "managed-block" files (CLAUDE.md) get the unity-init block inserted or replaced.

    Returns {"created": [...], "updated": [...], "skipped": [...]} absolute paths.
    """
    root = Path(output_dir)
    result: dict = {"created": [], "updated": [], "skipped": []}

    for d in manifest["directories"]:
        path = root / d
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            result["created"].append(str(path))

    for f in manifest["files"]:
        path = root / f["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        if f.get("mode") == "managed-block":
            existing = path.read_text() if path.is_file() else None
            path.write_text(merge_managed_block(existing, f["content"]))
            result["updated" if existing is not None else "created"].append(str(path))
        elif path.exists():
            result["skipped"].append(str(path))
        else:
            path.write_text(f["content"])
            result["created"].append(str(path))

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate Unity project folder structure, asmdefs, and CLAUDE.md"
    )
    parser.add_argument("--company", default=None,
                        help="Company/studio name (default: ProjectSettings companyName)")
    parser.add_argument("--project", default=None,
                        help="Project name (default: ProjectSettings productName)")
    parser.add_argument("--features", default="", help="Comma-separated feature names")
    parser.add_argument("--ui-controllers", default="",
                        help="Comma-separated UI ViewController names")
    parser.add_argument("--sdk", default=None,
                        help="Generate shared SDK scaffold at Assets/_<sdk>/")
    parser.add_argument("--pipeline", default="auto", choices=PIPELINE_CHOICES,
                        help="Render pipeline (default: auto-detect, else URP)")
    parser.add_argument("--unity-version", default=None,
                        help="Unity version for CLAUDE.md (default: ProjectVersion.txt)")
    parser.add_argument("--gitignore", action="store_true", default=False,
                        help="Include .gitignore file (skipped if one exists)")
    parser.add_argument("--no-claude-md", action="store_true", default=False,
                        help="Do not write the CLAUDE.md managed block")
    parser.add_argument("--output-dir", default=None,
                        help="Unity project root to apply the structure to")
    parser.add_argument("--dry-run", action="store_true", default=False,
                        help="Print manifest JSON without creating files")

    args = parser.parse_args()
    detected = detect_project_info(args.output_dir)

    # CLI flags override detection; detection overrides built-in defaults.
    company = args.company or detected.get("company")
    project = args.project or detected.get("project")
    if not company or not project:
        parser.error("--company and --project are required when they cannot be "
                     "detected from <output-dir>/ProjectSettings/ProjectSettings.asset")
    pipeline = args.pipeline if args.pipeline != "auto" else detected.get("pipeline", "URP")

    manifest = generate_manifest(
        company=company,
        project=project,
        features=[f.strip() for f in args.features.split(",") if f.strip()],
        ui_controllers=[c.strip() for c in args.ui_controllers.split(",") if c.strip()],
        sdk=args.sdk,
        pipeline=pipeline,
        include_gitignore=args.gitignore,
        include_claude_md=not args.no_claude_md,
        unity_version=args.unity_version or detected.get("unity_version"),
    )
    manifest["detected"] = detected

    if args.dry_run or not args.output_dir:
        print(json.dumps(manifest, indent=2))
    else:
        result = apply_manifest(manifest, args.output_dir)
        print(
            json.dumps(
                {
                    "status": "success",
                    "detected": detected,
                    "created_count": len(result["created"]),
                    "updated_count": len(result["updated"]),
                    "skipped_count": len(result["skipped"]),
                    "tree": manifest["tree"],
                    **result,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Generate Unity project folder structure with assembly definitions.

Layout matches the ZenoGames Ten Crush pattern:
    Assets/
    +-- Scenes/                                 # project-level scenes
    +-- Settings/{Build Profiles,Scenes}/       # URP assets + scene templates
    +-- Tests/{EditMode,PlayMode}/              # co-located tests
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

Usage:
    generate_structure.py --company <name> --project <name>
        [--features <csv>] [--ui-controllers <csv>] [--sdk <name>]
        [--pipeline URP|URP2D|HDRP|Built-in]
        [--gitignore] [--output-dir <path>] [--dry-run]

Output: JSON manifest of all paths and file contents to stdout.
"""

import argparse
import json
import sys
from pathlib import Path


GITIGNORE_CONTENT = """# Unity generated
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Bb]uilds/
[Ll]ogs/
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

# Unity MCP / Claude
.claude/
"""


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


def make_readme(feature: str) -> str:
    return f"# {feature}\n\nWhat this feature does and how to use it.\n"


def make_agents(feature: str) -> str:
    return (
        f"# {feature} — Agent Rules\n\n"
        f"Feature-specific constraints and gotchas for `{feature}`.\n\n"
        f"- Communicate with other features via `TenCrush.Events` only.\n"
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
        f"- Follow `unity-standards` skill before any change.\n"
        f"- Asset-first: create ScriptableObject/prefab before logic.\n"
        f"- Update `README.md` + `AGENTS.md` of any feature you touch.\n"
    )


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
) -> dict:
    """
    Generate a manifest of directories and files for a Unity project.

    Returns dict with:
        - directories: list of directory paths (relative to project root)
        - files: list of {path, content} dicts
        - tree: human-readable tree string
    """
    features = features if features is not None else [
        "Board", "Match", "Score", "Goal", "Audio", "Input", "Tile", "VFX"
    ]
    ui_controllers = ui_controllers if ui_controllers is not None else [
        "HUD", "Popups"
    ]
    ui_controllers = [c for c in ui_controllers if c]

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

    # Strip whitespace from feature / UI controller names
    features = [f.strip() for f in (features or []) if f and f.strip()]
    ui_controllers = [c.strip() for c in (ui_controllers or []) if c and c.strip()]

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
        feat = feat.strip()
        if not feat:
            continue
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
        files.append({"path": f"{base}/AGENTS.md", "content": make_agents(feat)})

    # ── UI ViewControllers ───────────────────────────────────────
    vc_asmdefs: list[str] = []
    for vc in ui_controllers:
        vc = vc.strip()
        if not vc:
            continue
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

    # Top-level ViewControllers (composes HUD + Popups + ViewModels)
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

    # ── Bootstrap (composition root, refs Core + Events + features) ──
    bootstrap_asm = f"{ns_root}.Bootstrap"
    files.append({
        "path": f"{project_root}/Scripts/Bootstrap/{bootstrap_asm}.asmdef",
        "content": make_asmdef(
            bootstrap_asm,
            references=[
                f"{ns_root}.Core",
                f"{ns_root}.Events",
                # Common feature wiring; user can add more after generation.
                f"{ns_root}.Features.Board",
                f"{ns_root}.Features.Match",
                f"{ns_root}.Features.Score",
                f"{ns_root}.Features.Goal",
                f"{ns_root}.Features.Audio",
            ],
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

    # ── Optional SDK scaffold (e.g. _ZenoSDK) ───────────────────
    sdk_info = None
    if sdk:
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

    # ── Build tree string ───────────────────────────────────────
    tree = build_tree(directories, files)

    return {
        "company": company,
        "project": project,
        "namespace_root": ns_root,
        "pipeline": pipeline,
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


def apply_manifest(manifest: dict, output_dir: str) -> list[str]:
    """Apply manifest to disk — create directories and write files."""
    root = Path(output_dir)
    created = []

    for d in manifest["directories"]:
        path = root / d
        path.mkdir(parents=True, exist_ok=True)
        created.append(str(path))

    for f in manifest["files"]:
        path = root / f["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f["content"])
        created.append(str(path))

    return created


def main():
    parser = argparse.ArgumentParser(
        description="Generate Unity project folder structure (Ten Crush pattern)"
    )
    parser.add_argument("--company", required=True, help="Company/studio name")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument(
        "--features",
        default="Board,Match,Score,Goal,Audio,Input,Tile,VFX",
        help="Comma-separated feature names",
    )
    parser.add_argument(
        "--ui-controllers",
        default="HUD,Popups",
        help="Comma-separated UI ViewController names",
    )
    parser.add_argument(
        "--sdk",
        default=None,
        help="Generate shared SDK scaffold at Assets/_<sdk>/ (e.g. ZenoSDK)",
    )
    parser.add_argument(
        "--pipeline",
        default="URP",
        choices=["URP", "URP2D", "HDRP", "Built-in"],
        help="Render pipeline (default: URP)",
    )
    parser.add_argument(
        "--gitignore",
        action="store_true",
        default=False,
        help="Include .gitignore file",
    )
    parser.add_argument(
        "--output-dir", default=None, help="Apply structure to this directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print manifest JSON without creating files",
    )

    args = parser.parse_args()
    features = [f.strip() for f in args.features.split(",") if f.strip()]
    ui_controllers = [c.strip() for c in args.ui_controllers.split(",") if c.strip()]

    manifest = generate_manifest(
        company=args.company,
        project=args.project,
        features=features,
        ui_controllers=ui_controllers,
        sdk=args.sdk,
        pipeline=args.pipeline,
        include_gitignore=args.gitignore,
    )

    if args.dry_run or not args.output_dir:
        print(json.dumps(manifest, indent=2))
    else:
        created = apply_manifest(manifest, args.output_dir)
        print(
            json.dumps(
                {
                    "status": "success",
                    "created_count": len(created),
                    "tree": manifest["tree"],
                    "paths": created,
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
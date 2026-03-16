#!/usr/bin/env python3
"""
Generate Unity project folder structure with assembly definitions.

Usage:
    generate_structure.py --company <name> --project <name>
        [--features <comma-separated>] [--pipeline URP|HDRP|Built-in]
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
"""


def make_asmdef(
    name: str,
    references: list[str] | None = None,
    is_test: bool = False,
    root_namespace: str = "",
) -> str:
    """Generate .asmdef JSON content."""
    asmdef = {
        "name": name,
        "rootNamespace": root_namespace or name,
        "references": references or [],
        "includePlatforms": [],
        "excludePlatforms": [],
        "allowUnsafeCode": False,
        "overrideReferences": is_test,
        "precompiledReferences": [],
        "autoReferenced": False,
        "defineConstraints": ["UNITY_INCLUDE_TESTS"] if is_test else [],
        "versionDefines": [],
        "noEngineReferences": False,
    }
    if is_test:
        asmdef["precompiledReferences"] = ["nunit.framework.dll"]
        asmdef["overrideReferences"] = True
    return json.dumps(asmdef, indent=4)


def generate_manifest(
    company: str,
    project: str,
    features: list[str] | None = None,
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
    features = features if features is not None else ["Player"]
    ns_root = f"{company}.{project}"

    directories: list[str] = []
    files: list[dict] = []

    # ── Core directories ────────────────────────────────────────
    core_dirs = [
        "Assets/_Project/Core/Scripts",
        "Assets/_Project/Infrastructure/Scripts",
        "Assets/_Project/UI",
        "Assets/_Project/Settings",
        "Assets/_Project/Art",
        "Assets/_Project/Audio",
        "Assets/_Project/Scenes",
        "Assets/Plugins",
    ]
    directories.extend(core_dirs)

    # Core .asmdef
    core_asm_name = f"{ns_root}.Core"
    files.append(
        {
            "path": f"Assets/_Project/Core/Scripts/{core_asm_name}.asmdef",
            "content": make_asmdef(core_asm_name, root_namespace=core_asm_name),
        }
    )

    # ── Feature directories ─────────────────────────────────────
    feature_asm_names = []
    for feat in features:
        feat_name = feat.strip()
        if not feat_name:
            continue
        base = f"Assets/_Project/Features/{feat_name}"
        feat_dirs = [
            f"{base}/Scripts",
            f"{base}/Prefabs",
            f"{base}/Art",
            f"{base}/Animations",
            f"{base}/Tests",
        ]
        directories.extend(feat_dirs)

        # Feature .asmdef
        feat_asm = f"{ns_root}.{feat_name}"
        feature_asm_names.append(feat_asm)
        files.append(
            {
                "path": f"{base}/Scripts/{feat_asm}.asmdef",
                "content": make_asmdef(
                    feat_asm, references=[core_asm_name], root_namespace=feat_asm
                ),
            }
        )

        # Test .asmdef
        test_asm = f"{ns_root}.{feat_name}.Tests"
        files.append(
            {
                "path": f"{base}/Tests/{test_asm}.asmdef",
                "content": make_asmdef(
                    test_asm,
                    references=[feat_asm, core_asm_name],
                    is_test=True,
                    root_namespace=test_asm,
                ),
            }
        )

    # ── Infrastructure .asmdef ──────────────────────────────────
    infra_asm = f"{ns_root}.Infrastructure"
    infra_refs = [core_asm_name] + feature_asm_names
    files.append(
        {
            "path": f"Assets/_Project/Infrastructure/Scripts/{infra_asm}.asmdef",
            "content": make_asmdef(
                infra_asm, references=infra_refs, root_namespace=infra_asm
            ),
        }
    )

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
        "directories": sorted(directories),
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
    """
    Apply a manifest to disk — create directories and write files.
    Returns list of created paths.
    """
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
        description="Generate Unity project folder structure"
    )
    parser.add_argument("--company", required=True, help="Company/studio name")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument(
        "--features",
        default="Player",
        help="Comma-separated feature names (default: Player)",
    )
    parser.add_argument(
        "--pipeline",
        default="URP",
        choices=["URP", "HDRP", "Built-in"],
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

    manifest = generate_manifest(
        company=args.company,
        project=args.project,
        features=features,
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

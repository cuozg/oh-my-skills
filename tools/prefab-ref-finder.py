#!/usr/bin/env python3
"""
Prefab Reference Finder - Search Unity serialized files for script references.

Given a C# file path, class name, or GUID, searches .prefab, .unity, and
.asset files for references. Reports which assets would break if the script
is modified, renamed, or deleted.

Usage:
  prefab-ref-finder.py <target> <project_root> [--types prefab,scene,asset]
"""

import sys
import os
import re
from pathlib import Path
from collections import defaultdict


ASSET_EXTENSIONS = {
    "prefab": ".prefab",
    "scene": ".unity",
    "asset": ".asset",
}


def find_script_file(class_name, scripts_dir):
    pattern = re.compile(rf"(?:class|struct|interface)\s+{re.escape(class_name)}\b")
    for root, dirs, files in os.walk(scripts_dir):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if not f.endswith(".cs"):
                continue
            filepath = Path(root) / f
            try:
                content = filepath.read_text(encoding="utf-8", errors="replace")
                if pattern.search(content):
                    return filepath
            except Exception:
                continue
    return None


def extract_guid_from_meta(cs_filepath):
    meta_path = Path(str(cs_filepath) + ".meta")
    if not meta_path.exists():
        return None
    try:
        content = meta_path.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"guid:\s*([a-f0-9]+)", content)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def search_assets_for_guid(guid, project_root, extensions):
    results = defaultdict(list)

    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "Library"]
        for f in files:
            ext = Path(f).suffix.lower()
            if ext not in extensions:
                continue
            filepath = Path(root) / f
            try:
                content = filepath.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            if guid not in content:
                continue

            lines = content.splitlines()
            contexts = extract_reference_context(lines, guid)
            rel_path = str(filepath)
            results[rel_path] = contexts

    return results


def extract_reference_context(lines, guid):
    contexts = []
    for i, line in enumerate(lines):
        if guid not in line:
            continue

        game_object_name = find_parent_game_object(lines, i)
        component_type = "MonoBehaviour"

        # m_Script: {fileID: ..., guid: XXXX, ...} pattern
        if "m_Script:" in line:
            component_type = "Script Reference"

        contexts.append(
            {
                "line": i + 1,
                "game_object": game_object_name,
                "component": component_type,
                "raw": line.strip()[:100],
            }
        )

    return contexts


def find_parent_game_object(lines, ref_line_idx):
    for i in range(ref_line_idx, max(ref_line_idx - 50, -1), -1):
        line = lines[i]
        name_match = re.search(r"m_Name:\s*(.+)", line)
        if name_match:
            return name_match.group(1).strip()
    return "(unknown)"


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: prefab-ref-finder.py <target> <project_root> [--types prefab,scene,asset]"
        )
        print("  target:       C# file path, class name, or GUID")
        print("  project_root: Unity project root directory")
        sys.exit(1)

    target = sys.argv[1]
    project_root = Path(sys.argv[2])

    asset_types = ["prefab", "scene"]
    for i, arg in enumerate(sys.argv):
        if arg == "--types" and i + 1 < len(sys.argv):
            asset_types = [t.strip() for t in sys.argv[i + 1].split(",")]

    extensions = set()
    for t in asset_types:
        if t in ASSET_EXTENSIONS:
            extensions.add(ASSET_EXTENSIONS[t])

    if not extensions:
        print(
            f"No valid asset types specified. Valid: {', '.join(ASSET_EXTENSIONS.keys())}"
        )
        sys.exit(1)

    if not project_root.exists():
        print(f"Project root not found: {project_root}")
        sys.exit(1)

    scripts_dir = project_root / "Assets" / "Scripts"
    cs_filepath = None
    class_name = None
    guid = None

    # GUID detection: 32 hex characters
    if re.match(r"^[a-f0-9]{32}$", target):
        guid = target
    elif target.endswith(".cs"):
        cs_filepath = Path(target)
        if not cs_filepath.exists():
            cs_filepath = project_root / target
        if not cs_filepath.exists():
            print(f"File not found: {target}")
            sys.exit(1)
    else:
        class_name = target
        if scripts_dir.exists():
            cs_filepath = find_script_file(class_name, scripts_dir)
        if not cs_filepath:
            print(f"Could not find script for class: {class_name}")
            print("Provide a file path or GUID instead.")
            sys.exit(1)

    if cs_filepath and not guid:
        class_match = None
        try:
            content = cs_filepath.read_text(encoding="utf-8", errors="replace")
            class_match = re.search(r"class\s+(\w+)", content)
        except Exception:
            pass
        if class_match and not class_name:
            class_name = class_match.group(1)
        if not class_name:
            class_name = cs_filepath.stem

        guid = extract_guid_from_meta(cs_filepath)
        if not guid:
            print(f"Could not extract GUID from {cs_filepath}.meta")
            print("The .meta file may not exist or may be in an unexpected format.")
            sys.exit(1)

    report = []
    report.append(f"# Prefab/Scene Reference Report: {class_name or guid}")

    report.append("\n## Target")
    if cs_filepath:
        report.append(f"  Script: {cs_filepath}")
    report.append(f"  GUID: {guid}")
    if class_name:
        report.append(f"  Class: {class_name}")
    report.append(
        f"  Searching: {', '.join(f'.{e}' for e in sorted(t.lstrip('.') for t in extensions))} files"
    )

    results = search_assets_for_guid(guid, project_root / "Assets", extensions)

    if not results:
        report.append(f"\n## No References Found")
        report.append("  This script is not referenced by any searched asset files.")
        report.append("  Safe to modify or delete (from a prefab/scene perspective).")
        print("\n".join(report))
        return

    by_type = defaultdict(dict)
    for filepath, contexts in results.items():
        ext = Path(filepath).suffix.lower()
        type_name = next(
            (k for k, v in ASSET_EXTENSIONS.items() if v == ext),
            "other",
        )
        by_type[type_name][filepath] = contexts

    total_assets = len(results)
    total_refs = sum(len(c) for c in results.values())
    report.append(
        f"\n## References Found ({total_assets} assets, {total_refs} references)"
    )

    for type_name in ["prefab", "scene", "asset"]:
        if type_name not in by_type:
            continue
        assets = by_type[type_name]
        report.append(f"\n### {type_name.capitalize()}s ({len(assets)})")
        for filepath, contexts in sorted(assets.items()):
            report.append(f"  {filepath}")
            for ctx in contexts[:3]:
                report.append(
                    f"    - GameObject: {ctx['game_object']}"
                    f" | {ctx['component']} (line {ctx['line']})"
                )
            if len(contexts) > 3:
                report.append(f"    ... and {len(contexts) - 3} more references")

    report.append(f"\n## Summary")
    report.append(f"  Total references: {total_refs} across {total_assets} assets")
    if total_assets > 0:
        risk = "HIGH" if total_assets > 5 else "MEDIUM" if total_assets > 1 else "LOW"
        report.append(
            f"  Risk if deleted: {risk} — "
            f"{total_assets} asset{'s' if total_assets > 1 else ''} "
            f"would have missing script references"
        )
    else:
        report.append("  Risk if deleted: NONE — no asset references found")

    print("\n".join(report))


if __name__ == "__main__":
    main()

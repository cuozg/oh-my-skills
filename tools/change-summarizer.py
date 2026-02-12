#!/usr/bin/env python3
"""
Change Summarizer - Analyze uncommitted git changes for a Unity project.

Produces a structured summary: files changed, systems affected,
risk assessment, and suggested test areas. Context-aware for
WWE Champions patterns (DataManagers, Singletons, UI Controllers).

Usage:
  change-summarizer.py <project_root> [--staged-only] [--path-filter <path>]
"""

import sys
import os
import re
import subprocess
from pathlib import Path
from collections import defaultdict


FILE_CATEGORY_RULES = [
    (r"DataManager", "Data Manager"),
    (r": Singleton<", "Singleton Manager"),
    (r"Manager\.cs$", "Manager"),
    (r"Controller\.cs$", "UI Controller"),
    (r"Script\.cs$", "Script"),
    (r"Editor/", "Editor Script"),
    (r"\.shader$|\.hlsl$", "Shader"),
    (r"\.prefab$", "Prefab"),
    (r"\.unity$", "Scene"),
    (r"\.asset$", "Asset"),
    (r"\.json$", "JSON Data"),
    (r"\.cs$", "C# Script"),
]

# Paths mapped to system names
SYSTEM_PATHS = {
    "DailyBoss": "Daily Boss",
    "RoadBoss": "Road Boss",
    "GachaV2": "Gacha",
    "AscensionSystem": "Ascension",
    "Multiplayer": "Multiplayer",
    "ChatSocketSystem": "Chat",
    "Mentor": "Mentor",
    "Game/Managers": "Core Managers",
    "Game/UI": "Core UI",
    "Game/Battle": "Battle System",
    "Game/Gameplay": "Core Gameplay",
    "Game/Analytics": "Analytics",
    "Game/IAP": "IAP / Purchases",
    "Game/Audio": "Audio",
    "Game/User": "User Data",
    "KFF": "Core Framework (KFF)",
    "Startup": "Startup Flow",
    "DataDrivenUi": "Data-Driven UI",
    "Util": "Utilities",
    "NewHomeHUD": "Home HUD",
}

# Risk: HIGH for critical systems, MEDIUM for game logic, LOW for peripherals
HIGH_RISK_INDICATORS = [
    "Singleton<",
    "DataManager<",
    "KFF/",
    "Startup/",
    "PlayerInfoScript",
    "SaveData",
    "ICMultiplayerComms",
    "GearDataLoadingManager",
]

MEDIUM_RISK_INDICATORS = [
    "Controller.cs",
    "Manager.cs",
    "Game/Battle/",
    "Game/Gameplay/",
]


def run_git(args, cwd):
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return result.stdout.strip()


def classify_file(filepath, diff_content=""):
    combined = filepath + " " + diff_content
    for pattern, category in FILE_CATEGORY_RULES:
        if re.search(pattern, combined):
            return category
    return "Other"


def detect_system(filepath):
    for path_prefix, system_name in SYSTEM_PATHS.items():
        if path_prefix in filepath:
            return system_name

    # Release-based features: R23/ through R73/
    release_match = re.search(r"/(R\d+)/", filepath)
    if release_match:
        return f"Release {release_match.group(1)}"

    return "Other"


def assess_file_risk(filepath, diff_content=""):
    combined = filepath + "\n" + diff_content
    for indicator in HIGH_RISK_INDICATORS:
        if indicator in combined:
            return "HIGH", f"Contains {indicator}"
    for indicator in MEDIUM_RISK_INDICATORS:
        if indicator in combined:
            return "MEDIUM", f"Contains {indicator}"
    return "LOW", "Standard code"


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: change-summarizer.py <project_root> [--staged-only] [--path-filter <path>]"
        )
        sys.exit(1)

    project_root = Path(sys.argv[1])
    staged_only = "--staged-only" in sys.argv
    path_filter = None
    for i, arg in enumerate(sys.argv):
        if arg == "--path-filter" and i + 1 < len(sys.argv):
            path_filter = sys.argv[i + 1]

    if not project_root.exists():
        print(f"Project root not found: {project_root}")
        sys.exit(1)

    diff_flag = "--cached" if staged_only else ""
    diff_args = ["diff", "--numstat"]
    if staged_only:
        diff_args.append("--cached")
    if path_filter:
        diff_args.extend(["--", path_filter])

    numstat_output = run_git(diff_args, project_root)

    stat_args = ["diff", "--stat"]
    if staged_only:
        stat_args.append("--cached")
    if path_filter:
        stat_args.extend(["--", path_filter])

    diff_content_args = ["diff"]
    if staged_only:
        diff_content_args.append("--cached")
    if path_filter:
        diff_content_args.extend(["--", path_filter])
    full_diff = run_git(diff_content_args, project_root)

    if not numstat_output:
        untracked = run_git(
            ["ls-files", "--others", "--exclude-standard"], project_root
        )
        if untracked:
            print("# Change Summary\n")
            print("## Overview")
            print("  No modified files (staged or unstaged).")
            untracked_files = untracked.splitlines()
            print(f"  Untracked files: {len(untracked_files)}")
            print("\n## Untracked Files")
            for f in untracked_files[:20]:
                print(f"  A {f}")
            if len(untracked_files) > 20:
                print(f"  ... and {len(untracked_files) - 20} more")
        else:
            print("# Change Summary\n")
            print("No changes detected (working tree is clean).")
        return

    total_added = 0
    total_removed = 0
    file_entries = []
    systems = defaultdict(list)
    risk_factors = []
    overall_risk = "LOW"

    per_file_diff = {}
    current_file = None
    current_lines = []
    for line in full_diff.splitlines():
        if line.startswith("diff --git"):
            if current_file:
                per_file_diff[current_file] = "\n".join(current_lines)
            match = re.search(r"b/(.+)$", line)
            current_file = match.group(1) if match else None
            current_lines = [line]
        elif current_file:
            current_lines.append(line)
    if current_file:
        per_file_diff[current_file] = "\n".join(current_lines)

    for line in numstat_output.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        added = int(parts[0]) if parts[0] != "-" else 0
        removed = int(parts[1]) if parts[1] != "-" else 0
        filepath = parts[2]

        total_added += added
        total_removed += removed

        file_diff = per_file_diff.get(filepath, "")
        category = classify_file(filepath, file_diff)
        system = detect_system(filepath)
        risk, risk_reason = assess_file_risk(filepath, file_diff)

        file_entries.append(
            {
                "path": filepath,
                "added": added,
                "removed": removed,
                "category": category,
                "system": system,
                "risk": risk,
                "risk_reason": risk_reason,
            }
        )

        systems[system].append(filepath)

        if risk == "HIGH":
            overall_risk = "HIGH"
            risk_factors.append(f"Modified {category}: {filepath} ({risk_reason})")
        elif risk == "MEDIUM" and overall_risk != "HIGH":
            overall_risk = "MEDIUM"
            risk_factors.append(f"Modified {category}: {filepath}")

    report = []
    report.append("# Change Summary")

    report.append("\n## Overview")
    report.append(f"  Files changed: {len(file_entries)}")
    report.append(f"  Lines added: {total_added}  |  Lines removed: {total_removed}")
    report.append(f"  Risk level: {overall_risk}")

    report.append("\n## Changed Files")
    for entry in sorted(file_entries, key=lambda e: e["path"]):
        status = "M"
        report.append(
            f"  {status} {entry['path']} ({entry['category']}) "
            f"+{entry['added']}/-{entry['removed']}"
        )

    report.append("\n## Systems Affected")
    for system, files in sorted(systems.items()):
        report.append(
            f"  - {system} ({len(files)} file{'s' if len(files) > 1 else ''})"
        )

    if risk_factors:
        report.append("\n## Risk Factors")
        for factor in risk_factors:
            report.append(f"  - {factor}")

    report.append("\n## Suggested Test Areas")
    test_num = 1
    for system, files in sorted(systems.items()):
        has_high_risk = any(
            e["risk"] == "HIGH" for e in file_entries if e["system"] == system
        )
        priority = " [HIGH PRIORITY]" if has_high_risk else ""
        report.append(f"  {test_num}. {system}{priority}")
        test_num += 1

    if any(e["category"] == "Singleton Manager" for e in file_entries):
        report.append(f"  {test_num}. Full regression — singleton manager modified")
        test_num += 1
    if any(e["category"] == "Data Manager" for e in file_entries):
        report.append(f"  {test_num}. Blueprint data loading verification")

    print("\n".join(report))


if __name__ == "__main__":
    main()

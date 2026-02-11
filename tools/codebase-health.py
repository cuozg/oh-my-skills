#!/usr/bin/env python3
"""
Codebase Health Analyzer for Unity C# projects.
Scans Assets/Scripts/ and reports:
  - File counts by extension
  - Top 15 largest C# files (by line count)
  - TODO/FIXME/HACK comment counts
  - Empty Update()/Start()/OnGUI() method detection
  - Singleton<T> usage count
  - Line count distribution (buckets)
"""

import sys
import os
import re
from pathlib import Path
from collections import Counter, defaultdict


def count_lines(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def scan_csharp_file(filepath):
    """Scan a single C# file for health metrics."""
    results = {
        "lines": 0,
        "todos": 0,
        "fixmes": 0,
        "hacks": 0,
        "empty_updates": [],
        "singletons": [],
    }

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
            lines = content.splitlines()
    except Exception:
        return results

    results["lines"] = len(lines)

    # Count TODO/FIXME/HACK
    for line in lines:
        upper = line.upper()
        if "TODO" in upper:
            results["todos"] += 1
        if "FIXME" in upper:
            results["fixmes"] += 1
        if "HACK" in upper:
            results["hacks"] += 1

    # Detect empty Unity callbacks (Update, Start, OnGUI)
    # Pattern: method with empty body or only whitespace/comments
    for callback in ["Update", "Start", "OnGUI", "LateUpdate", "FixedUpdate"]:
        pattern = rf"(?:void\s+{callback}\s*\(\s*\)\s*\{{[\s]*\}})"
        if re.search(pattern, content):
            results["empty_updates"].append(callback)

    # Detect Singleton usage
    singleton_match = re.findall(r":\s*Singleton<(\w+)>", content)
    if singleton_match:
        results["singletons"] = singleton_match

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: codebase-health.py <scripts_directory>")
        sys.exit(1)

    scripts_dir = Path(sys.argv[1])
    if not scripts_dir.exists():
        print(f"Directory not found: {scripts_dir}")
        sys.exit(1)

    # Collect all files
    ext_counts = Counter()
    cs_files = []
    total_files = 0

    for root, dirs, files in os.walk(scripts_dir):
        # Skip hidden dirs and meta files
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if f.endswith(".meta"):
                continue
            total_files += 1
            ext = Path(f).suffix.lower()
            ext_counts[ext] += 1
            if ext == ".cs":
                cs_files.append(Path(root) / f)

    # Analyze C# files
    file_metrics = []
    total_todos = 0
    total_fixmes = 0
    total_hacks = 0
    total_lines = 0
    empty_callbacks = []
    all_singletons = []
    line_buckets = Counter()  # 0-100, 101-300, 301-500, 501-1000, 1000+

    for cs_file in cs_files:
        metrics = scan_csharp_file(cs_file)
        file_metrics.append((cs_file, metrics))
        total_todos += metrics["todos"]
        total_fixmes += metrics["fixmes"]
        total_hacks += metrics["hacks"]
        total_lines += metrics["lines"]

        if metrics["empty_updates"]:
            rel = cs_file.relative_to(scripts_dir)
            for cb in metrics["empty_updates"]:
                empty_callbacks.append(f"  {rel}: {cb}()")

        if metrics["singletons"]:
            rel = cs_file.relative_to(scripts_dir)
            for s in metrics["singletons"]:
                all_singletons.append(f"  {rel}: Singleton<{s}>")

        lc = metrics["lines"]
        if lc <= 100:
            line_buckets["0-100"] += 1
        elif lc <= 300:
            line_buckets["101-300"] += 1
        elif lc <= 500:
            line_buckets["301-500"] += 1
        elif lc <= 1000:
            line_buckets["501-1000"] += 1
        else:
            line_buckets["1000+"] += 1

    # Sort by line count for largest files
    file_metrics.sort(key=lambda x: x[1]["lines"], reverse=True)

    # Build report
    report = []
    report.append("# Codebase Health Report")
    report.append(f"\nScanned: {scripts_dir}")
    report.append(f"Total files (excl .meta): {total_files}")
    report.append(f"C# files: {len(cs_files)}")
    report.append(f"Total C# lines: {total_lines:,}")

    report.append("\n## File Types")
    for ext, count in ext_counts.most_common(15):
        report.append(f"  {ext or '(no ext)'}: {count}")

    report.append("\n## Top 15 Largest C# Files")
    for cs_file, metrics in file_metrics[:15]:
        rel = cs_file.relative_to(scripts_dir)
        report.append(f"  {metrics['lines']:>6} lines  {rel}")

    report.append("\n## Line Count Distribution")
    for bucket in ["0-100", "101-300", "301-500", "501-1000", "1000+"]:
        count = line_buckets.get(bucket, 0)
        pct = (count / len(cs_files) * 100) if cs_files else 0
        bar = "#" * int(pct / 2)
        report.append(f"  {bucket:>8}: {count:>5} ({pct:5.1f}%) {bar}")

    report.append(f"\n## Code Markers")
    report.append(f"  TODO:  {total_todos}")
    report.append(f"  FIXME: {total_fixmes}")
    report.append(f"  HACK:  {total_hacks}")

    report.append(f"\n## Singleton<T> Usage ({len(all_singletons)} classes)")
    if all_singletons:
        for s in all_singletons[:30]:
            report.append(s)
        if len(all_singletons) > 30:
            report.append(f"  ... and {len(all_singletons) - 30} more")

    report.append(f"\n## Empty Unity Callbacks ({len(empty_callbacks)} found)")
    if empty_callbacks:
        for cb in empty_callbacks[:20]:
            report.append(cb)
        if len(empty_callbacks) > 20:
            report.append(f"  ... and {len(empty_callbacks) - 20} more")
    else:
        report.append("  None detected (good!)")

    print("\n".join(report))


if __name__ == "__main__":
    main()

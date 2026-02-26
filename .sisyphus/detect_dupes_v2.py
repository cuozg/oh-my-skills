#!/usr/bin/env python3
"""Detect >3 consecutive similar lines between SKILL.md and reference files.
Uses fuzzy matching: strips markdown formatting chars, normalizes whitespace."""

import os
import re

SKILLS_DIR = "skills"
MIN_CONSECUTIVE_NONBLANK = 4  # >3 non-blank lines


def normalize(line):
    """Normalize for comparison: strip formatting, whitespace, bullets."""
    s = line.strip()
    # Remove leading markdown markers: -, *, >, #, numbers
    s = re.sub(r"^[\-\*\>\#\d\.]+\s*", "", s)
    # Remove trailing markdown
    s = re.sub(r"\s*[\-\*]+\s*$", "", s)
    # Normalize whitespace
    s = re.sub(r"\s+", " ", s)
    # Remove backticks and bold/italic markers
    s = s.replace("`", "").replace("*", "").replace("_", "")
    return s.lower().strip()


def find_consecutive_dupes(lines_a, lines_b):
    """Find all runs of consecutive similar lines."""
    results = []
    norm_a = [normalize(l) for l in lines_a]
    norm_b = [normalize(l) for l in lines_b]

    # Build index of norm_b for fast lookup
    b_index = {}
    for j, nb in enumerate(norm_b):
        if nb and len(nb) > 5:  # Skip very short/empty
            b_index.setdefault(nb, []).append(j)

    visited_a = set()

    for i in range(len(norm_a)):
        if i in visited_a:
            continue
        na = norm_a[i]
        if not na or len(na) <= 5:
            continue
        if na not in b_index:
            continue

        for j in b_index[na]:
            # Count consecutive matches starting from (i, j)
            k = 0
            non_blank = 0
            while i + k < len(norm_a) and j + k < len(norm_b):
                if norm_a[i + k] == norm_b[j + k]:
                    if norm_a[i + k]:
                        non_blank += 1
                    k += 1
                elif not norm_a[i + k] and not norm_b[j + k]:
                    # Both blank - continue
                    k += 1
                else:
                    break

            if non_blank >= MIN_CONSECUTIVE_NONBLANK:
                results.append(
                    {
                        "a_start": i + 1,
                        "a_end": i + k,
                        "b_start": j + 1,
                        "b_end": j + k,
                        "count": k,
                        "non_blank": non_blank,
                        "sample": [lines_a[i + x].rstrip() for x in range(min(k, 6))],
                    }
                )

    # Deduplicate overlapping ranges
    if not results:
        return results
    results.sort(key=lambda r: (-r["non_blank"], r["a_start"]))
    filtered = []
    used_a = set()
    for r in results:
        a_range = set(range(r["a_start"], r["a_end"] + 1))
        if len(a_range & used_a) > len(a_range) * 0.3:
            continue
        filtered.append(r)
        used_a |= a_range
    return filtered


def scan_skill(skill_dir):
    """Scan a single skill directory for duplicates."""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    refs_dir = os.path.join(skill_dir, "references")

    if not os.path.isfile(skill_md) or not os.path.isdir(refs_dir):
        return []

    with open(skill_md, "r") as f:
        skill_lines = f.readlines()

    findings = []
    for root, dirs, files in os.walk(refs_dir):
        for ref_file in sorted(files):
            ref_path = os.path.join(root, ref_file)
            if ref_file.startswith(".") or ref_file.endswith((".py", ".sh", ".pyc")):
                continue

            try:
                with open(ref_path, "r") as f:
                    ref_lines = f.readlines()
            except (UnicodeDecodeError, IsADirectoryError):
                continue

            rel_path = os.path.relpath(ref_path, skill_dir)
            dupes = find_consecutive_dupes(skill_lines, ref_lines)
            for d in dupes:
                findings.append(
                    {
                        "skill": os.path.basename(skill_dir),
                        "ref_file": rel_path,
                        "skill_lines": f"{d['a_start']}-{d['a_end']}",
                        "ref_lines": f"{d['b_start']}-{d['b_end']}",
                        "count": d["count"],
                        "non_blank": d["non_blank"],
                        "sample": d["sample"],
                    }
                )
    return findings


def main():
    all_findings = []
    for skill_name in sorted(os.listdir(SKILLS_DIR)):
        if skill_name == "skill-creator":
            continue
        skill_dir = os.path.join(SKILLS_DIR, skill_name)
        if not os.path.isdir(skill_dir):
            continue
        findings = scan_skill(skill_dir)
        all_findings.extend(findings)

    if not all_findings:
        print("NO DUPLICATES FOUND")
        return

    print(f"FOUND {len(all_findings)} DUPLICATE BLOCKS\n")
    print(f"{'Skill':<30} {'Ref File':<40} {'SKILL.md':<12} {'Ref':<12} {'Lines':<6}")
    print("=" * 104)
    for f in all_findings:
        print(
            f"{f['skill']:<30} {f['ref_file']:<40} {f['skill_lines']:<12} {f['ref_lines']:<12} {f['non_blank']:<6}"
        )
        for s in f["sample"][:3]:
            print(f"    | {s[:90]}")
        print()


if __name__ == "__main__":
    main()

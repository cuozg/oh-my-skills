#!/usr/bin/env python3
"""Detect >3 consecutive identical lines between SKILL.md and reference files."""

import os
import sys

SKILLS_DIR = "skills"
MIN_CONSECUTIVE = 4  # >3 means >=4


def normalize(line):
    """Normalize a line for comparison (strip whitespace, ignore blank)."""
    return line.strip()


def find_consecutive_dupes(lines_a, lines_b, min_count=MIN_CONSECUTIVE):
    """Find all runs of >= min_count consecutive identical lines between two sets."""
    results = []
    norm_a = [normalize(l) for l in lines_a]
    norm_b = [normalize(l) for l in lines_b]

    i = 0
    while i < len(norm_a):
        if not norm_a[i]:  # skip blank lines as start
            i += 1
            continue
        for j in range(len(norm_b)):
            if not norm_b[j]:
                continue
            if norm_a[i] == norm_b[j]:
                # Count consecutive matches
                k = 0
                while (
                    i + k < len(norm_a)
                    and j + k < len(norm_b)
                    and norm_a[i + k] == norm_b[j + k]
                ):
                    k += 1
                # Filter: only count non-blank lines
                non_blank = sum(1 for x in range(k) if norm_a[i + x])
                if non_blank >= min_count:
                    results.append(
                        {
                            "a_start": i + 1,  # 1-indexed
                            "a_end": i + k,
                            "b_start": j + 1,
                            "b_end": j + k,
                            "count": k,
                            "non_blank": non_blank,
                            "sample": [
                                lines_a[i + x].rstrip() for x in range(min(k, 5))
                            ],
                        }
                    )
        i += 1

    # Deduplicate overlapping ranges - keep longest
    if not results:
        return results
    results.sort(key=lambda r: (-r["non_blank"], r["a_start"]))
    filtered = []
    used_a = set()
    used_b = set()
    for r in results:
        a_range = set(range(r["a_start"], r["a_end"] + 1))
        b_range = set(range(r["b_start"], r["b_end"] + 1))
        # Skip if >50% overlap with already found
        if len(a_range & used_a) > len(a_range) * 0.5:
            continue
        if len(b_range & used_b) > len(b_range) * 0.5:
            continue
        filtered.append(r)
        used_a |= a_range
        used_b |= b_range
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
    for ref_file in sorted(os.listdir(refs_dir)):
        ref_path = os.path.join(refs_dir, ref_file)
        if not os.path.isfile(ref_path) or ref_file.startswith("."):
            continue
        # Skip non-text files
        if not ref_file.endswith((".md", ".txt", ".yaml", ".yml")):
            continue

        with open(ref_path, "r") as f:
            ref_lines = f.readlines()

        dupes = find_consecutive_dupes(skill_lines, ref_lines)
        for d in dupes:
            findings.append(
                {
                    "skill": os.path.basename(skill_dir),
                    "ref_file": ref_file,
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
    print(
        f"{'Skill':<30} {'Ref File':<35} {'SKILL.md Lines':<15} {'Ref Lines':<15} {'Count':<6}"
    )
    print("-" * 105)
    for f in all_findings:
        print(
            f"{f['skill']:<30} {f['ref_file']:<35} {f['skill_lines']:<15} {f['ref_lines']:<15} {f['count']:<6}"
        )
        for s in f["sample"][:3]:
            print(f"    | {s[:80]}")
        print()


if __name__ == "__main__":
    main()

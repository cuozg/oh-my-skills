#!/usr/bin/env python3
"""
Unity Log Analyzer - Parse and classify Unity Editor console output.

Features:
  - Classify log entries by severity (Error, Warning, Info)
  - Group duplicate messages
  - Extract stack traces and associate with errors
  - Identify common error patterns and suggest fixes
  - Prioritize actionable errors
"""

import sys
import re
from pathlib import Path
from collections import Counter, defaultdict


# Common Unity error patterns and suggested fixes
ERROR_PATTERNS = {
    r"NullReferenceException": {
        "category": "Null Reference",
        "fix": "Add null check before accessing the object. Check serialized references in Inspector. Verify object isn't destroyed.",
    },
    r"MissingReferenceException": {
        "category": "Missing Reference",
        "fix": "Object was destroyed but still referenced. Add 'if (this == null) return' after await. Check for destroyed references in callbacks.",
    },
    r"IndexOutOfRangeException": {
        "category": "Index Out of Range",
        "fix": "Validate array/list bounds before access. Check Count/Length before indexing.",
    },
    r"InvalidOperationException": {
        "category": "Invalid Operation",
        "fix": "Check collection modification during enumeration. Verify object state before operation.",
    },
    r"KeyNotFoundException": {
        "category": "Key Not Found",
        "fix": "Use TryGetValue() instead of direct dictionary access. Verify key exists with ContainsKey().",
    },
    r"FormatException": {
        "category": "Format Error",
        "fix": "Validate string format before parsing. Use TryParse() instead of Parse().",
    },
    r"StackOverflowException": {
        "category": "Stack Overflow",
        "fix": "Check for infinite recursion. Add base case to recursive methods.",
    },
    r"[Cc]annot (implicitly )?convert type": {
        "category": "Type Mismatch",
        "fix": "Check type compatibility. Use explicit cast or convert. Verify generic type parameters.",
    },
    r"does not contain a definition for": {
        "category": "Missing Member",
        "fix": "Check spelling. Verify correct using directives. Check if the API changed in a Unity update.",
    },
    r"[Ss]hader (error|warning|not supported)": {
        "category": "Shader Issue",
        "fix": "Check shader compatibility with current render pipeline (URP/HDRP). Verify shader variant compilation.",
    },
    r"[Tt]he type or namespace .* could not be found": {
        "category": "Missing Type/Namespace",
        "fix": "Add missing using directive. Check assembly definition references. Verify package is installed.",
    },
    r"[Ss]erializ(ation|ed).*error": {
        "category": "Serialization Error",
        "fix": "Check [Serializable] attribute. Verify field types are serializable. Check for circular references.",
    },
    r"[Aa]sset[Bb]undle.*error|[Bb]undle.*fail": {
        "category": "AssetBundle Error",
        "fix": "Rebuild asset bundles. Check bundle dependencies. Verify CDN availability.",
    },
    r"[Oo]ut of memory|[Mm]emory.*alloc": {
        "category": "Memory Issue",
        "fix": "Profile memory usage. Check for leaks. Reduce texture sizes. Implement object pooling.",
    },
}


def classify_line(line):
    """Classify a log line by severity."""
    upper = line.upper()
    if any(marker in upper for marker in ["ERROR", "EXCEPTION", "[ERROR]"]):
        return "ERROR"
    if any(marker in upper for marker in ["WARNING", "[WARN]", "[WARNING]"]):
        return "WARNING"
    return "INFO"


def parse_stack_trace(lines, start_idx):
    """Extract a stack trace starting from a given index."""
    trace = []
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        # Stack trace lines typically start with "at " or contain file:line
        if (
            re.match(r"^(at\s|.*\.(cs|dll):\d+)", line)
            or line.startswith("UnityEngine.")
            or line.startswith("System.")
        ):
            trace.append(line)
            i += 1
        elif line.startswith("(") or "rethrow" in line.lower():
            trace.append(line)
            i += 1
        else:
            break
    return trace, i


def match_error_pattern(message):
    """Match an error message against known patterns."""
    for pattern, info in ERROR_PATTERNS.items():
        if re.search(pattern, message):
            return info
    return None


def analyze_logs(log_text, severity_filter="all"):
    """Analyze Unity console logs."""
    lines = log_text.splitlines()

    entries = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        severity = classify_line(line)

        # Check if next lines are stack trace
        trace, next_i = parse_stack_trace(lines, i + 1)

        entries.append(
            {
                "message": line,
                "severity": severity,
                "stack_trace": trace,
                "line_num": i + 1,
            }
        )
        i = next_i if next_i > i + 1 else i + 1

    # Filter by severity
    if severity_filter == "errors":
        entries = [e for e in entries if e["severity"] == "ERROR"]
    elif severity_filter == "warnings":
        entries = [e for e in entries if e["severity"] in ("ERROR", "WARNING")]

    # Group duplicates
    message_groups = defaultdict(list)
    for entry in entries:
        # Normalize message for grouping (remove line numbers, timestamps)
        normalized = re.sub(r"(line \d+|:\d+|\[\d+:\d+:\d+\])", "", entry["message"])
        normalized = normalized.strip()
        message_groups[normalized].append(entry)

    # Count by severity
    severity_counts = Counter(e["severity"] for e in entries)

    # Build report
    report = []
    report.append("# Unity Log Analysis")
    report.append(f"\nTotal entries: {len(entries)}")
    report.append(f"  Errors:   {severity_counts.get('ERROR', 0)}")
    report.append(f"  Warnings: {severity_counts.get('WARNING', 0)}")
    report.append(f"  Info:     {severity_counts.get('INFO', 0)}")
    report.append(f"Unique messages: {len(message_groups)}")

    # Errors first (most actionable)
    error_groups = {
        k: v for k, v in message_groups.items() if v[0]["severity"] == "ERROR"
    }
    if error_groups:
        report.append(f"\n## Errors ({len(error_groups)} unique)")
        for normalized, group in sorted(error_groups.items(), key=lambda x: -len(x[1])):
            count = len(group)
            entry = group[0]
            report.append(
                f"\n### {'[x' + str(count) + '] ' if count > 1 else ''}{entry['message'][:120]}"
            )
            if count > 1:
                report.append(f"  Occurrences: {count}")

            # Stack trace
            if entry["stack_trace"]:
                report.append(f"  Stack trace:")
                for t in entry["stack_trace"][:5]:
                    report.append(f"    {t}")
                if len(entry["stack_trace"]) > 5:
                    report.append(
                        f"    ... ({len(entry['stack_trace']) - 5} more frames)"
                    )

            # Pattern match
            pattern_info = match_error_pattern(entry["message"])
            if pattern_info:
                report.append(f"  Category: {pattern_info['category']}")
                report.append(f"  Suggested fix: {pattern_info['fix']}")

    # Warnings
    warning_groups = {
        k: v for k, v in message_groups.items() if v[0]["severity"] == "WARNING"
    }
    if warning_groups:
        report.append(f"\n## Warnings ({len(warning_groups)} unique)")
        # Show top 10 by frequency
        sorted_warnings = sorted(warning_groups.items(), key=lambda x: -len(x[1]))
        for normalized, group in sorted_warnings[:10]:
            count = len(group)
            entry = group[0]
            msg = entry["message"][:100]
            report.append(f"  [{count}x] {msg}")
        if len(warning_groups) > 10:
            report.append(f"  ... and {len(warning_groups) - 10} more unique warnings")

    # Summary
    if error_groups:
        report.append(f"\n## Priority Fix Order")
        sorted_errors = sorted(error_groups.items(), key=lambda x: -len(x[1]))
        for i, (normalized, group) in enumerate(sorted_errors[:5]):
            entry = group[0]
            pattern_info = match_error_pattern(entry["message"])
            cat = pattern_info["category"] if pattern_info else "Unknown"
            report.append(f"  {i + 1}. [{cat}] {entry['message'][:80]} ({len(group)}x)")

    if not entries:
        report.append(
            "\nNo log entries found. Console may be clean or log format is unrecognized."
        )

    print("\n".join(report))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: unity-log-analyzer.py <log_file> [all|errors|warnings]")
        sys.exit(1)

    log_file = Path(sys.argv[1])
    severity = sys.argv[2] if len(sys.argv) > 2 else "all"

    if not log_file.exists():
        print(f"Log file not found: {log_file}")
        sys.exit(1)

    log_text = log_file.read_text(encoding="utf-8", errors="replace")
    analyze_logs(log_text, severity)

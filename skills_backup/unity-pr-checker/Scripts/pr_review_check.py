#!/usr/bin/env python3
"""
pr_review_check.py — Headless Unity PR Review Checker

Runs the same rule set as PRReviewCheckerWindow.cs but purely in Python
with no Unity process required. Outputs:
  - Human-readable terminal report (default)
  - GitHub Actions annotations (--github-annotations)
  - SARIF v2.1 (--sarif <output.sarif.json>)
  - JSON (--json <output.json>)

Usage:
    python pr_review_check.py [assets_root] [options]

    assets_root: path to Unity project's Assets/ folder
                 defaults to ./Assets

GitHub Actions:
    - name: PR Review Checker
      run: python Scripts/pr_review_check.py Assets --github-annotations
      # Will annotate PR lines and set exit code 1 if P0 found

Exit codes:
    0 — no issues (or only P2 suggestions)
    1 — one or more P0/P1 issues found
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Callable, Iterator, Optional


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

SEVERITY_P0 = "P0_BlockMerge"
SEVERITY_P1 = "P1_MustFix"
SEVERITY_P2 = "P2_Suggestion"

CATEGORY_CODE   = "CodeLogic"
CATEGORY_SERIAL = "Serialization"
CATEGORY_SEC    = "Security"
CATEGORY_PERF   = "Performance"
CATEGORY_PREFAB = "PrefabIntegrity"
CATEGORY_ASSET  = "AssetSettings"


@dataclass
class Finding:
    severity:      str
    category:      str
    rule_id:       str
    title:         str
    file_path:     str
    line:          int
    detail:        str
    why:           str
    how_to_fix:    str


# ---------------------------------------------------------------------------
# Base rule helpers
# ---------------------------------------------------------------------------

def _scan_cs_files(assets_root: str) -> Iterator[tuple[str, str, list[str]]]:
    """Yield (file_path, full_text, lines) for every .cs file."""
    for root, dirs, files in os.walk(assets_root):
        # Skip generated / editor-only dirs
        dirs[:] = [d for d in dirs if d not in ("Generated", "Editor")]
        for f in files:
            if f.endswith(".cs"):
                full = os.path.join(root, f)
                try:
                    text = Path(full).read_text(encoding="utf-8", errors="replace")
                    yield full, text, text.splitlines()
                except OSError:
                    pass


def _rel(full_path: str, assets_root: str) -> str:
    try:
        return os.path.relpath(full_path, assets_root)
    except ValueError:
        return full_path


def _line_of(text: str, char_idx: int) -> int:
    return text[:char_idx].count("\n") + 1


def _regex_scan(
    assets_root: str,
    category: str,
    rules: list[tuple],
    extra_filter: Optional[Callable[[str], bool]] = None,
) -> list[Finding]:
    findings: list[Finding] = []
    for file_path, text, _ in _scan_cs_files(assets_root):
        if extra_filter and extra_filter(file_path):
            continue
        rel = _rel(file_path, assets_root)
        for rule_id, title, pattern, severity, why, fix in rules:
            try:
                for m in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
                    findings.append(Finding(
                        severity=severity,
                        category=category,
                        rule_id=rule_id,
                        title=title,
                        file_path=rel,
                        line=_line_of(text, m.start()),
                        detail=m.group(0)[:120].strip(),
                        why=why,
                        how_to_fix=fix,
                    ))
            except re.error:
                pass
    return findings


# ---------------------------------------------------------------------------
# Code Logic Rules  (mirrors CodeLogicRules.cs)
# ---------------------------------------------------------------------------

CODE_RULES = [
    (
        "CL001", "Unity Object null check using == null",
        r"if\s*\(\s*\w+\s*==\s*null\s*\)|if\s*\(\s*null\s*==\s*\w+\s*\)",
        SEVERITY_P1,
        "Unity overloads == for destroyed objects — but 'is null' will NOT catch destroyed objects.",
        "Use 'if (!obj)' for destroyed-object checks on UnityEngine.Object subclasses.",
    ),
    (
        "CL002", "Camera.main accessed in hot path",
        r"(void\s+(?:Update|FixedUpdate|LateUpdate))[^}]*Camera\.main",
        SEVERITY_P1,
        "Camera.main calls FindObjectOfType internally — O(n) scan every frame.",
        "Cache Camera.main in Awake/Start.",
    ),
    (
        "CL003", "GameObject.Find / FindObjectOfType outside Awake/Start",
        r"(?:GameObject\.Find|FindObjectOfType|FindObjectsOfType)\s*[<(]",
        SEVERITY_P1,
        "Find* methods are O(n) scene scans. Called per-frame they spike CPU.",
        "Cache in Awake/Start or use dependency injection.",
    ),
    (
        "CL004", "Empty catch block swallows exceptions",
        r"catch\s*(?:\([^)]*\))?\s*\{\s*\}",
        SEVERITY_P1,
        "Silent failures hide bugs and make debugging extremely difficult.",
        "Add at minimum: catch (Exception e) { Debug.LogException(e); }",
    ),
    (
        "CL005", "GetComponent inside Update loop",
        r"(?:void\s+(?:Update|FixedUpdate|LateUpdate))[^}]*GetComponent\s*[<(]",
        SEVERITY_P1,
        "GetComponent involves a native-to-managed bridge call every frame.",
        "Cache component references in Awake.",
    ),
    (
        "CL006", "SendMessage / BroadcastMessage usage",
        r"\b(?:SendMessage|BroadcastMessage|SendMessageUpwards)\s*\(",
        SEVERITY_P1,
        "SendMessage uses reflection — ~10x slower than a direct call, triggers GC.",
        "Replace with direct calls, C# events, or ScriptableObject event channels.",
    ),
]


def run_code_logic(assets_root: str) -> list[Finding]:
    return _regex_scan(assets_root, CATEGORY_CODE, CODE_RULES)


# ---------------------------------------------------------------------------
# Serialization Rules  (mirrors SerializationRules.cs)
# ---------------------------------------------------------------------------

SERIAL_RULES = [
    (
        "SR001", "Public field without [SerializeField]",
        r"public\s+(?!static|const|readonly|class|struct|enum|interface|override|virtual|abstract)[\w<>\[\]]+\s+\w+\s*;",
        SEVERITY_P2,
        "Public fields expose data externally. Prefer [SerializeField] private fields.",
        "Change to [SerializeField] private and add a public property if needed.",
    ),
    (
        "SR002", "Dictionary/HashSet used as serialized field",
        r"\[SerializeField\][^;]*(?:Dictionary|HashSet)\s*<",
        SEVERITY_P0,
        "Unity cannot serialize Dictionary or HashSet — always null at runtime.",
        "Use a List<KVPair> or a custom [Serializable] class instead.",
    ),
    (
        "SR003", "Auto-property on [System.Serializable] class",
        r"\[System\.Serializable\][^{]*\{[^}]*\{\s*get;\s*(?:set;)?\s*\}",
        SEVERITY_P1,
        "Unity serializes fields, not properties. Auto-properties are silently ignored.",
        "Replace with [SerializeField] private fields.",
    ),
    (
        "SR004", "BinaryFormatter usage",
        r"BinaryFormatter\s*(?:\(\)|\.)",
        SEVERITY_P0,
        "BinaryFormatter is deprecated and has deserialization RCE vulnerabilities.",
        "Replace with JsonUtility, Newtonsoft.Json, or a proper binary format.",
    ),
]


def run_serialization(assets_root: str) -> list[Finding]:
    return _regex_scan(assets_root, CATEGORY_SERIAL, SERIAL_RULES)


# ---------------------------------------------------------------------------
# Security Rules  (mirrors SecurityRules.cs)
# ---------------------------------------------------------------------------

SEC_RULES = [
    (
        "SEC001", "PlayerPrefs storing sensitive data",
        r'PlayerPrefs\.Set(?:String|Int|Float)\s*\(\s*"[^"]*(?:password|token|secret|apikey|api_key|auth)[^"]*"',
        SEVERITY_P0,
        "PlayerPrefs is plaintext on disk — readable by other apps or from device backups.",
        "Use OS Keychain APIs or server-side token exchange. Never store credentials in PlayerPrefs.",
    ),
    (
        "SEC002", "Hardcoded secret/API key",
        r'(?:api[_-]?key|secret|password|token|bearer|apiSecret)\s*=\s*"[A-Za-z0-9+/=_\-]{8,}"',
        SEVERITY_P0,
        "Hardcoded secrets are trivially extracted from built apps.",
        "Use environment variables or a secrets manager. Rotate any exposed secrets immediately.",
    ),
    (
        "SEC003", "Assembly.Load / LoadFrom with runtime path",
        r"Assembly\.(?:Load|LoadFrom|LoadFile)\s*\(",
        SEVERITY_P0,
        "Dynamic assembly loading is the vector for CVE-2025-59489 (Unity Android ACE, CVSS 8.4).",
        "Remove dynamic assembly loading. Validate signatures if plugin architecture is required.",
    ),
    (
        "SEC004", "Application.OpenURL with variable input",
        r'Application\.OpenURL\s*\(\s*(?!"http)',
        SEVERITY_P1,
        "OpenURL with unsanitized input enables URL injection attacks.",
        "Validate URLs against an allowlist before calling OpenURL.",
    ),
    (
        "SEC005", "WWW class usage (deprecated, no TLS enforcement)",
        r"\bnew\s+WWW\s*\(",
        SEVERITY_P1,
        "WWW is deprecated since Unity 2018.2 and doesn't enforce TLS certificate validation.",
        "Replace with UnityWebRequest.",
    ),
    (
        "SEC006", "Insecure HTTP endpoint",
        r'"http://(?!localhost|127\.0\.0\.1)',
        SEVERITY_P1,
        "Plain HTTP transmits data unencrypted, including auth tokens.",
        "Use HTTPS for all production endpoints.",
    ),
]


def run_security(assets_root: str) -> list[Finding]:
    return _regex_scan(assets_root, CATEGORY_SEC, SEC_RULES)


# ---------------------------------------------------------------------------
# Performance Rules  (mirrors PerformanceRules.cs)
# ---------------------------------------------------------------------------

PERF_RULES = [
    (
        "PERF001", "String concatenation (+) in Update — GC alloc per frame",
        r'(?:void\s+(?:Update|FixedUpdate|LateUpdate)[^{]*\{[^}]*)\+\s*"|\+\s*[a-zA-Z_]\w*\s*\+',
        SEVERITY_P1,
        "String + string creates a new heap allocation every call at 60fps.",
        "Use StringBuilder or string.Format with cached format strings.",
    ),
    (
        "PERF002", "new() allocation inside Update/FixedUpdate/LateUpdate",
        r'(?:void\s+(?:Update|FixedUpdate|LateUpdate)[^{]*\{[^}]*)\bnew\s+(?!List|Dictionary|HashSet)\w+\s*[(<]',
        SEVERITY_P1,
        "Object allocation in a hot path forces GC collection.",
        "Cache reusable objects as fields. Use object pools.",
    ),
    (
        "PERF003", "LINQ in Update hot path",
        r'(?:void\s+(?:Update|FixedUpdate|LateUpdate)[^{]*\{[^}]*)(?:\.Where\(|\.Select\(|\.FirstOrDefault\(|\.Any\(|\.ToList\(|\.ToArray\()',
        SEVERITY_P1,
        "LINQ allocates IEnumerator objects and intermediate collections on the heap.",
        "Pre-compute and cache LINQ results. Use manual for loops in hot paths.",
    ),
    (
        "PERF004", "SendMessage / BroadcastMessage",
        r"\b(?:SendMessage|BroadcastMessage|SendMessageUpwards)\s*\(",
        SEVERITY_P1,
        "SendMessage uses reflection — ~10x slower than a direct call.",
        "Replace with direct calls, C# events, or UnityEvent.",
    ),
    (
        "PERF005", "tag comparison with string literal",
        r"\.tag\s*==\s*\"",
        SEVERITY_P2,
        "gameObject.tag == \"string\" allocates a new string each comparison.",
        "Use gameObject.CompareTag(\"TagName\") — it's allocation-free.",
    ),
]


def run_performance(assets_root: str) -> list[Finding]:
    return _regex_scan(assets_root, CATEGORY_PERF, PERF_RULES)


# ---------------------------------------------------------------------------
# Prefab Rules  (YAML-only — no AssetDatabase available headlessly)
# ---------------------------------------------------------------------------

def run_prefab(assets_root: str) -> list[Finding]:
    findings: list[Finding] = []
    exts = ("*.prefab", "*.unity")

    for ext in exts:
        for filepath in Path(assets_root).rglob(ext):
            try:
                text = filepath.read_text(encoding="utf-8", errors="replace")
                rel = _rel(str(filepath), assets_root)

                # PF001: Missing script references
                for m in re.finditer(r"m_Script:\s*\{fileID:\s*0\}", text):
                    findings.append(Finding(
                        severity=SEVERITY_P0,
                        category=CATEGORY_PREFAB,
                        rule_id="PF001",
                        title="Missing script reference (fileID: 0)",
                        file_path=rel,
                        line=_line_of(text, m.start()),
                        detail=m.group(0).strip(),
                        why="Missing scripts cause NullReferenceExceptions and broken prefab behavior at runtime.",
                        how_to_fix="Locate the original script or remove the component. Never commit with missing scripts.",
                    ))

                # PF002: Canvas without GraphicRaycaster (YAML heuristic)
                if "Canvas:" in text and "GraphicRaycaster:" not in text:
                    findings.append(Finding(
                        severity=SEVERITY_P1,
                        category=CATEGORY_PREFAB,
                        rule_id="PF003",
                        title="Canvas prefab likely missing GraphicRaycaster",
                        file_path=rel,
                        line=0,
                        detail="Canvas found, GraphicRaycaster not found in YAML",
                        why="A Canvas without GraphicRaycaster won't process any UI input events.",
                        how_to_fix="Add GraphicRaycaster component to the Canvas GameObject.",
                    ))

            except OSError:
                pass

    return findings


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def run_all(assets_root: str) -> list[Finding]:
    runners = [
        run_code_logic,
        run_serialization,
        run_security,
        run_performance,
        run_prefab,
    ]
    findings: list[Finding] = []
    for runner in runners:
        findings.extend(runner(assets_root))

    findings.sort(key=lambda f: (
        {"P0_BlockMerge": 0, "P1_MustFix": 1, "P2_Suggestion": 2}.get(f.severity, 9),
        f.category,
        f.file_path,
        f.line,
    ))
    return findings


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

SEVERITY_EMOJI = {
    SEVERITY_P0: "⛔",
    SEVERITY_P1: "⚠️ ",
    SEVERITY_P2: "💡",
}

ANSI = {
    "reset":  "\033[0m",
    "bold":   "\033[1m",
    "red":    "\033[31m",
    "yellow": "\033[33m",
    "blue":   "\033[34m",
    "grey":   "\033[90m",
    "green":  "\033[32m",
}


def _c(text: str, *codes: str, no_color: bool = False) -> str:
    if no_color or not sys.stdout.isatty():
        return text
    return "".join(ANSI.get(c, "") for c in codes) + text + ANSI["reset"]


def format_terminal(findings: list[Finding], no_color: bool = False) -> str:
    if not findings:
        return _c("✅  No issues found.", "green", no_color=no_color)

    lines = []
    lines.append(_c("\n╔══════════════════════════════════════════════╗", "bold", no_color=no_color))
    lines.append(_c("║         PR Review Checker Results            ║", "bold", no_color=no_color))
    lines.append(_c("╚══════════════════════════════════════════════╝\n", "bold", no_color=no_color))

    p0 = [f for f in findings if f.severity == SEVERITY_P0]
    p1 = [f for f in findings if f.severity == SEVERITY_P1]
    p2 = [f for f in findings if f.severity == SEVERITY_P2]

    lines.append(
        f"  Total: {len(findings)}  |  "
        f"{_c(f'⛔ P0: {len(p0)}', 'red', 'bold', no_color=no_color)}  |  "
        f"{_c(f'⚠️  P1: {len(p1)}', 'yellow', 'bold', no_color=no_color)}  |  "
        f"{_c(f'💡 P2: {len(p2)}', 'blue', no_color=no_color)}\n"
    )

    current_cat = None
    for f in findings:
        if f.category != current_cat:
            current_cat = f.category
            lines.append(_c(f"\n── {f.category} ────────────────────────────", "bold", no_color=no_color))

        sev_color = {"P0_BlockMerge": "red", "P1_MustFix": "yellow", "P2_Suggestion": "blue"}.get(f.severity, "grey")
        sev_label = f"[{f.severity}]"
        emoji = SEVERITY_EMOJI.get(f.severity, "  ")

        lines.append(
            f"  {emoji} {_c(sev_label, sev_color, 'bold', no_color=no_color)} "
            f"{_c(f.rule_id, 'bold', no_color=no_color)} {f.title}"
        )
        lines.append(f"     {_c(f.file_path, 'grey', no_color=no_color)}:{f.line}")
        if f.detail:
            snippet = f.detail[:80] + ("…" if len(f.detail) > 80 else "")
            lines.append(f"     {_c(snippet, 'grey', no_color=no_color)}")
        lines.append(f"     → {_c(f.how_to_fix[:100], 'green', no_color=no_color)}")
        lines.append("")

    return "\n".join(lines)


def format_github_annotations(findings: list[Finding]) -> str:
    """
    GitHub Actions workflow command format.
    https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
    """
    lines = []
    for f in findings:
        level = {"P0_BlockMerge": "error", "P1_MustFix": "warning", "P2_Suggestion": "notice"}.get(f.severity, "notice")
        file_path = f.file_path.replace("\\", "/")
        title = f"{f.rule_id}: {f.title}"
        msg = f"{f.why} FIX: {f.how_to_fix}"
        line_part = f",line={f.line}" if f.line > 0 else ""
        lines.append(f"::{level} file={file_path}{line_part},title={title}::{msg}")
    return "\n".join(lines)


def format_sarif(findings: list[Finding], assets_root: str) -> dict:
    """SARIF v2.1 — compatible with GitHub Code Scanning, VS Code SARIF viewer."""
    rules_map: dict[str, dict] = {}
    results = []

    for f in findings:
        if f.rule_id not in rules_map:
            rules_map[f.rule_id] = {
                "id": f.rule_id,
                "name": f.title.replace(" ", ""),
                "shortDescription": {"text": f.title},
                "fullDescription": {"text": f.why},
                "help": {"text": f.how_to_fix, "markdown": f"**Fix:** {f.how_to_fix}"},
                "defaultConfiguration": {
                    "level": {
                        SEVERITY_P0: "error",
                        SEVERITY_P1: "warning",
                        SEVERITY_P2: "note",
                    }.get(f.severity, "note"),
                },
            }

        uri = f.file_path.replace("\\", "/")
        result = {
            "ruleId": f.rule_id,
            "level": {"P0_BlockMerge": "error", "P1_MustFix": "warning", "P2_Suggestion": "note"}.get(f.severity, "note"),
            "message": {"text": f.title},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": uri, "uriBaseId": "SRCROOT"},
                        "region": {"startLine": max(1, f.line)},
                    }
                }
            ],
        }
        results.append(result)

    return {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "PRReviewChecker",
                        "version": "1.0.0",
                        "informationUri": "https://github.com/your-org/your-repo",
                        "rules": list(rules_map.values()),
                    }
                },
                "results": results,
                "originalUriBaseIds": {
                    "SRCROOT": {"uri": Path(assets_root).parent.as_uri() + "/"}
                },
            }
        ],
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Unity PR Review Checker — headless static analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("assets_root", nargs="?", default="Assets",
                        help="Path to Unity project Assets/ folder (default: ./Assets)")
    parser.add_argument("--github-annotations", action="store_true",
                        help="Output GitHub Actions workflow commands")
    parser.add_argument("--sarif", metavar="OUTPUT.json",
                        help="Write SARIF v2.1 report to file")
    parser.add_argument("--json", metavar="OUTPUT.json",
                        help="Write JSON report to file")
    parser.add_argument("--no-color", action="store_true",
                        help="Disable ANSI color output")
    parser.add_argument("--fail-on", choices=["P0", "P1", "P2", "none"], default="P1",
                        help="Exit code 1 if findings at or above this severity exist (default: P1)")
    parser.add_argument("--category", choices=[
        CATEGORY_CODE, CATEGORY_SERIAL, CATEGORY_SEC,
        CATEGORY_PERF, CATEGORY_PREFAB, CATEGORY_ASSET,
    ], help="Run only a specific category")

    args = parser.parse_args()
    assets_root = os.path.abspath(args.assets_root)

    if not os.path.isdir(assets_root):
        print(f"ERROR: Assets root not found: {assets_root}", file=sys.stderr)
        return 2

    print(f"Scanning: {assets_root}", file=sys.stderr)
    findings = run_all(assets_root)

    if args.category:
        findings = [f for f in findings if f.category == args.category]

    # Terminal output
    if not args.github_annotations:
        print(format_terminal(findings, no_color=args.no_color))

    # GitHub Actions annotations
    if args.github_annotations:
        print(format_github_annotations(findings))

    # SARIF
    if args.sarif:
        sarif = format_sarif(findings, assets_root)
        with open(args.sarif, "w") as fp:
            json.dump(sarif, fp, indent=2)
        print(f"SARIF written to: {args.sarif}", file=sys.stderr)

    # JSON
    if args.json:
        with open(args.json, "w") as fp:
            json.dump([asdict(f) for f in findings], fp, indent=2)
        print(f"JSON written to: {args.json}", file=sys.stderr)

    # Exit code
    fail_levels = {
        "P0": {SEVERITY_P0},
        "P1": {SEVERITY_P0, SEVERITY_P1},
        "P2": {SEVERITY_P0, SEVERITY_P1, SEVERITY_P2},
        "none": set(),
    }
    fail_severities = fail_levels.get(args.fail_on, {SEVERITY_P0, SEVERITY_P1})
    if any(f.severity in fail_severities for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

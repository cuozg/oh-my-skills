#!/usr/bin/env python3
"""
verify_implementation.py — Verify acceptance criteria against the codebase.

For each acceptance criterion, runs lightweight heuristic checks:
  - extracts candidate keywords, file paths, and identifiers
  - searches via ripgrep (falls back to grep) for evidence
  - checks for matching test files
  - returns a verdict (met / partial / unmet) with file:line evidence

Usage:
    python verify_implementation.py <path_to_goal.md> [--root <repo_root>]
    from verify_implementation import verify_criteria

Stdlib only. Ripgrep optional (graceful grep fallback).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


# --- Keyword extraction ------------------------------------------------------

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has",
    "have", "in", "is", "it", "its", "of", "on", "or", "that", "the", "to",
    "was", "were", "will", "with", "must", "should", "shall", "can", "may",
    "this", "these", "those", "when", "then", "than", "into", "out", "all",
    "any", "each", "every", "some", "no", "not", "if", "else", "user", "users",
    "via", "using", "after", "before", "over", "under", "new", "old", "also",
    "given", "so", "but", "do", "does", "done",
}

IDENT_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]{2,}\b")
PATH_RE = re.compile(r"(?:[\w./-]+/)+[\w./-]+\.\w+")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
QUOTED_RE = re.compile(r'"([^"]+)"|\'([^\']+)\'')


def extract_terms(criterion: str) -> dict[str, list[str]]:
    """Extract searchable terms from a criterion string."""
    paths = PATH_RE.findall(criterion)
    code_spans = CODE_SPAN_RE.findall(criterion)
    quoted = [q for pair in QUOTED_RE.findall(criterion) for q in pair if q]

    idents = [
        tok for tok in IDENT_RE.findall(criterion)
        if tok.lower() not in STOPWORDS and not tok.isdigit()
    ]
    # Prefer multi-case or underscore identifiers (likely code symbols)
    symbols = [t for t in idents if any(c.isupper() for c in t) or "_" in t]
    keywords = [t for t in idents if t not in symbols][:6]

    return {
        "paths": list(dict.fromkeys(paths)),
        "code_spans": list(dict.fromkeys(code_spans)),
        "quoted": list(dict.fromkeys(quoted)),
        "symbols": list(dict.fromkeys(symbols))[:6],
        "keywords": list(dict.fromkeys(keywords)),
    }


# --- Search ------------------------------------------------------------------

def _run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True, timeout=20, check=False
        )
        return proc.returncode, proc.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return 124, ""


def _rg_available() -> bool:
    return shutil.which("rg") is not None


def search_code(term: str, root: Path, max_hits: int = 5) -> list[dict[str, Any]]:
    """Search repo for term. Returns [{file, line_no, text}, ...]."""
    if not term or len(term) < 2:
        return []

    excludes = [
        ".git", "node_modules", "__pycache__", ".venv", "venv",
        "dist", "build", "target", ".next", ".nuxt",
        "Docs/Goals", "*-workspace",
    ]
    if _rg_available():
        cmd = ["rg", "--no-heading", "--line-number", "--color", "never",
               "--max-count", str(max_hits), "-F", term]
        for pat in excludes:
            cmd.extend(["-g", f"!{pat}"])
    else:
        cmd = ["grep", "-rn", "--max-count", str(max_hits)]
        for pat in excludes:
            cmd.extend(["--exclude-dir", pat.split("/")[-1]])
        cmd.extend(["-F", term, "."])

    rc, out = _run(cmd, root)
    if rc not in (0, 1):
        return []

    hits: list[dict[str, Any]] = []
    for line in out.splitlines()[: max_hits * 3]:
        # format: path:line:content
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue
        file_, lineno, content = parts
        try:
            lineno_int = int(lineno)
        except ValueError:
            continue
        hits.append({
            "file": file_.lstrip("./"),
            "line_no": lineno_int,
            "text": content.strip()[:160],
        })
        if len(hits) >= max_hits:
            break
    return hits


def check_path(path_str: str, root: Path) -> dict[str, Any]:
    """Check whether a referenced path exists."""
    candidate = (root / path_str).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return {"path": path_str, "exists": False, "kind": "outside-repo"}
    exists = candidate.exists()
    kind = "missing"
    if exists:
        kind = "dir" if candidate.is_dir() else "file"
    return {"path": path_str, "exists": exists, "kind": kind}


def find_tests(symbols: list[str], root: Path) -> list[str]:
    """Look for test files that mention any of the given symbols."""
    if not symbols:
        return []
    candidate_dirs = [root / "tests", root / "test", root / "__tests__"]
    test_files: set[str] = set()
    for d in candidate_dirs:
        if not d.exists() or not d.is_dir():
            continue
        for p in d.rglob("*"):
            if not p.is_file():
                continue
            name = p.name.lower()
            if not (name.startswith("test_") or name.endswith("_test.py")
                    or ".test." in name or ".spec." in name):
                continue
            try:
                blob = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if any(sym in blob for sym in symbols):
                test_files.add(str(p.relative_to(root)))
    return sorted(test_files)


# --- Verdict -----------------------------------------------------------------

def verdict_for(
    criterion: dict[str, Any],
    terms: dict[str, list[str]],
    path_checks: list[dict[str, Any]],
    code_hits: list[dict[str, Any]],
    test_files: list[str],
) -> tuple[str, str]:
    """Decide met / partial / unmet. Returns (status, reasoning)."""
    if criterion["checked"]:
        return "met", "criterion marked complete in goal file"

    missing_paths = [p for p in path_checks if not p["exists"]]
    present_paths = [p for p in path_checks if p["exists"]]

    if path_checks and not present_paths:
        return "unmet", f"referenced path(s) missing: {[p['path'] for p in missing_paths]}"

    if not code_hits and not present_paths and not test_files:
        return "unmet", "no code, file, or test evidence found"

    if code_hits and test_files:
        return "met", f"{len(code_hits)} code hit(s) and {len(test_files)} test file(s)"

    if code_hits or present_paths:
        reason = []
        if code_hits:
            reason.append(f"{len(code_hits)} code hit(s)")
        if present_paths:
            reason.append(f"{len(present_paths)} path(s) present")
        if not test_files and terms["symbols"]:
            reason.append("no matching tests")
        return "partial", "; ".join(reason)

    return "unmet", "weak evidence"


# --- Public API --------------------------------------------------------------

def verify_criterion(
    criterion: dict[str, Any], root: Path
) -> dict[str, Any]:
    terms = extract_terms(criterion["text"])
    path_checks = [check_path(p, root) for p in terms["paths"]]

    search_terms: list[str] = []
    search_terms.extend(terms["symbols"])
    search_terms.extend(terms["code_spans"])
    search_terms.extend(terms["quoted"])
    # seed with keywords if nothing stronger was found
    if not search_terms:
        search_terms.extend(terms["keywords"][:3])

    code_hits: list[dict[str, Any]] = []
    seen = set()
    for term in search_terms[:5]:
        for hit in search_code(term, root):
            key = (hit["file"], hit["line_no"])
            if key in seen:
                continue
            seen.add(key)
            code_hits.append({**hit, "matched": term})
            if len(code_hits) >= 8:
                break
        if len(code_hits) >= 8:
            break

    test_files = find_tests(terms["symbols"], root)
    status, reasoning = verdict_for(criterion, terms, path_checks, code_hits, test_files)

    return {
        "text": criterion["text"],
        "checked": criterion["checked"],
        "line_no": criterion["line_no"],
        "status": status,
        "reasoning": reasoning,
        "terms": terms,
        "path_checks": path_checks,
        "code_hits": code_hits[:5],
        "test_files": test_files,
    }


def verify_criteria(
    criteria: list[dict[str, Any]], root: str | Path
) -> list[dict[str, Any]]:
    root_path = Path(root).resolve()
    if not root_path.exists():
        raise FileNotFoundError(f"repo root not found: {root_path}")
    return [verify_criterion(c, root_path) for c in criteria]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Verify acceptance criteria.")
    parser.add_argument("goal", help="path to goal .md file")
    parser.add_argument("--root", default=".", help="repo root (default: .)")
    args = parser.parse_args(argv[1:])

    # Lazy import so this script runs independently
    sys.path.insert(0, str(Path(__file__).parent))
    from parse_goal import parse_goal  # type: ignore

    try:
        goal = parse_goal(args.goal)
        results = verify_criteria(goal["acceptance_criteria"], args.root)
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"goal": goal["title"], "results": results}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
import sys
import os
import re
import subprocess
from pathlib import Path


class RefactoringValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def validate_file(self, filepath: str) -> None:
        if not filepath.endswith(".cs"):
            return
        path = Path(filepath)
        if not path.exists():
            self.errors.append(f"File not found: {filepath}")
            return
        content = path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        self._check_update_antipatterns(filepath, lines)
        self._check_dead_code(filepath, lines)
        self._check_todo_markers(filepath, lines)
        self._check_type_safety(filepath, lines)
        self._check_empty_handlers(filepath, lines)
        self._check_gc_pressure(filepath, lines)

    def _check_update_antipatterns(self, filepath: str, lines: list) -> None:
        update_pattern = re.compile(
            r"^\s*(void|async\s+void|private\s+void|protected\s+void|public\s+void)\s+"
            r"(Update|FixedUpdate|LateUpdate)\s*\("
        )
        antipatterns = [
            (r"GameObject\.Find\s*\(", "GameObject.Find in Update loop"),
            (r"FindObjectOfType\s*[<(]", "FindObjectOfType in Update loop"),
            (r"GetComponent\s*[<(]", "GetComponent in Update loop (cache in Start/Awake)"),
            (r"GetComponentInChildren\s*[<(]", "GetComponentInChildren in Update loop"),
            (r"new\s+List\s*[<(]", "List allocation in Update loop (pre-allocate)"),
            (r"\.ToString\s*\(\)", "ToString in Update loop (GC pressure)"),
            (r"string\s*\+\s*=|string\.Format|string\.Concat|\$\"", "String concatenation in Update loop"),
        ]
        in_update = False
        brace_depth = 0
        for i, line in enumerate(lines, 1):
            if update_pattern.search(line):
                in_update = True
                brace_depth = 0
            if in_update:
                brace_depth += line.count("{") - line.count("}")
                if brace_depth <= 0 and "{" not in line and i > 1:
                    in_update = False
                    continue
                for pattern, message in antipatterns:
                    if re.search(pattern, line):
                        self.errors.append(f"{filepath}:{i}: {message}")

    def _check_dead_code(self, filepath: str, lines: list) -> None:
        content = "\n".join(lines)
        empty_update = re.compile(r"void\s+(Update|FixedUpdate|LateUpdate)\s*\(\s*\)\s*\{\s*\}", re.MULTILINE)
        for m in empty_update.finditer(content):
            line_num = content[: m.start()].count("\n") + 1
            self.warnings.append(f"{filepath}:{line_num}: Empty {m.group(1)}() method — remove to save CPU")
        usings = []
        for i, line in enumerate(lines, 1):
            um = re.match(r"^\s*using\s+(\S+)\s*;", line)
            if um and not um.group(1).startswith("("):
                ns = um.group(1).split(".")[-1]
                usings.append((i, ns, um.group(1)))
        for line_num, short_name, full_ns in usings:
            if full_ns in ("System", "UnityEngine", "System.Collections", "System.Collections.Generic"):
                continue
            body = "\n".join(lines[line_num:])
            if short_name not in body:
                self.info.append(f"{filepath}:{line_num}: Possibly unused using: {full_ns}")

    def _check_todo_markers(self, filepath: str, lines: list) -> None:
        pattern = re.compile(r"//\s*(TODO|HACK|FIXME|XXX)\b", re.IGNORECASE)
        for i, line in enumerate(lines, 1):
            m = pattern.search(line)
            if m:
                marker = m.group(1).upper()
                rest = line[m.end() :].strip()
                if len(rest) < 10:
                    self.warnings.append(f"{filepath}:{i}: {marker} without sufficient context")

    def _check_type_safety(self, filepath: str, lines: list) -> None:
        for i, line in enumerate(lines, 1):
            if re.search(r"\bas\s+any\b", line):
                self.errors.append(f"{filepath}:{i}: 'as any' type cast")
            if re.search(r"#pragma\s+warning\s+disable", line):
                self.warnings.append(f"{filepath}:{i}: Warning suppression — verify it's intentional")

    def _check_empty_handlers(self, filepath: str, lines: list) -> None:
        content = "\n".join(lines)
        empty_catch = re.compile(r"catch\s*\([^)]*\)\s*\{\s*\}", re.MULTILINE)
        for m in empty_catch.finditer(content):
            line_num = content[: m.start()].count("\n") + 1
            self.errors.append(f"{filepath}:{line_num}: Empty catch block — handle or log the exception")

    def _check_gc_pressure(self, filepath: str, lines: list) -> None:
        for i, line in enumerate(lines, 1):
            if re.search(r"\.ToArray\(\)|\.ToList\(\)", line):
                self.info.append(f"{filepath}:{i}: ToArray()/ToList() creates allocation — consider if avoidable")

    def validate_paths(self, paths: list) -> None:
        for p in paths:
            path = Path(p)
            if path.is_file():
                self.validate_file(str(path))
            elif path.is_dir():
                for cs_file in path.rglob("*.cs"):
                    self.validate_file(str(cs_file))
            else:
                self.errors.append(f"Path not found: {p}")

    def validate_git_diff(self) -> None:
        try:
            result = subprocess.run(["git", "diff", "--name-only", "HEAD"], capture_output=True, text=True, check=True)
            staged = subprocess.run(["git", "diff", "--name-only", "--cached"], capture_output=True, text=True, check=True)
            files = set(result.stdout.strip().splitlines() + staged.stdout.strip().splitlines())
            cs_files = [f for f in files if f.endswith(".cs") and Path(f).exists()]
            if not cs_files:
                self.info.append("No C# files changed in git diff.")
                return
            for f in cs_files:
                self.validate_file(f)
        except subprocess.CalledProcessError:
            self.errors.append("Failed to run git diff — not a git repository?")

    def report(self) -> int:
        total = len(self.errors) + len(self.warnings) + len(self.info)
        if total == 0:
            print("✅ Refactoring validation passed — no issues found.")
            return 0
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for e in self.errors:
                print(f"  {e}")
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                print(f"  {w}")
        if self.info:
            print(f"\nℹ️  INFO ({len(self.info)}):")
            for i in self.info:
                print(f"  {i}")
        print(f"\nSummary: {len(self.errors)} errors, {len(self.warnings)} warnings, {len(self.info)} info")
        return 1 if self.errors else 0


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_refactoring.py <path> | --git-diff")
        sys.exit(1)
    validator = RefactoringValidator()
    if sys.argv[1] == "--git-diff":
        validator.validate_git_diff()
    else:
        validator.validate_paths(sys.argv[1:])
    sys.exit(validator.report())


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Parse Unity Editor log files and extract compile errors/warnings in structured format.

Usage:
    parse_unity_log.py <log-file-path> [--ci] [--json] [--warnings-as-errors]

Arguments:
    log-file-path         Path to Unity Editor log file
    --ci                  Exit with code 1 if any errors found (for CI pipelines)
    --json                Output as JSON instead of markdown table
    --warnings-as-errors  Treat warnings as errors (exit 1 if warnings found)

The regex used here matches Unity's own production parser from:
  MicrosoftCSharpCompilerOutputParser.cs (UnityCsReference)
"""

import re
import sys
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

UNITY_LOG_PATTERN = re.compile(
    r"(?P<filename>.+)\((?P<line>\d+),(?P<column>\d+)\):\s*"
    r"(?P<type>warning|error|info)\s*(?P<id>[^:]*):\s*(?P<message>.*)"
)

SCRIPT_IMPORT_PATTERN = re.compile(r"Failed to import script\s+(.+)")
ASSEMBLY_REF_PATTERN = re.compile(
    r"Assembly\s+(.+?)\s+has reference to\s+(.+?)\s+which is not included"
)
SHADER_ERROR_PATTERN = re.compile(r"Shader error in '(.+?)':\s*(.+)")
COMPILE_FAILED_PATTERN = re.compile(
    r"DisplayProgressNotification:\s*Scripts have compiler errors"
)
UNITY_VERSION_PATTERN = re.compile(
    r"^\s*(?:Unity Editor version:|Version:)\s+(\d+\.\d+\.\d+[a-z]\d+)"
)

COMPILER_SECTION_START = re.compile(r"-----CompilerOutput:-stderr-+")
COMPILER_SECTION_END = re.compile(r"-----EndCompilerOutput-+")


@dataclass
class LogEntry:
    filename: str
    line: int
    column: int
    entry_type: str
    code: str
    message: str

    @property
    def is_error(self) -> bool:
        return self.entry_type == "error"

    @property
    def is_warning(self) -> bool:
        return self.entry_type == "warning"


@dataclass
class ParseResult:
    unity_version: Optional[str]
    project_path: Optional[str]
    errors: list
    warnings: list
    infos: list
    script_import_failures: list
    assembly_errors: list
    shader_errors: list
    compilation_failed_marker: bool

    @property
    def total_errors(self) -> int:
        return (
            len(self.errors)
            + len(self.script_import_failures)
            + len(self.assembly_errors)
            + len(self.shader_errors)
        )

    @property
    def has_errors(self) -> bool:
        return self.total_errors > 0 or self.compilation_failed_marker

    @property
    def status(self) -> str:
        return "FAIL" if self.has_errors else "PASS"


def parse_log(log_path: str) -> ParseResult:
    path = Path(log_path)
    if not path.exists():
        print(f"ERROR: Log file not found: {log_path}", file=sys.stderr)
        sys.exit(2)

    result = ParseResult(
        unity_version=None,
        project_path=None,
        errors=[],
        warnings=[],
        infos=[],
        script_import_failures=[],
        assembly_errors=[],
        shader_errors=[],
        compilation_failed_marker=False,
    )

    seen_entries = set()

    with open(path, encoding="utf-8", errors="replace") as f:
        for raw_line in f:
            line = raw_line.strip()

            if not result.unity_version:
                vm = UNITY_VERSION_PATTERN.match(line)
                if vm:
                    result.unity_version = vm.group(1)
                    continue

            if not result.project_path:
                if "Project path:" in line:
                    result.project_path = line.split("Project path:")[-1].strip()
                    continue
                if "project path to:" in line:
                    result.project_path = line.split("project path to:")[-1].strip()
                    continue

            if COMPILE_FAILED_PATTERN.search(line):
                result.compilation_failed_marker = True
                continue

            m = UNITY_LOG_PATTERN.match(line)
            if m:
                entry = LogEntry(
                    filename=m.group("filename").strip(),
                    line=int(m.group("line")),
                    column=int(m.group("column")),
                    entry_type=m.group("type"),
                    code=m.group("id").strip(),
                    message=m.group("message").strip(),
                )
                dedup_key = (entry.filename, entry.line, entry.column, entry.code)
                if dedup_key in seen_entries:
                    continue
                seen_entries.add(dedup_key)

                if entry.is_error:
                    result.errors.append(entry)
                elif entry.is_warning:
                    result.warnings.append(entry)
                else:
                    result.infos.append(entry)
                continue

            m = SCRIPT_IMPORT_PATTERN.search(line)
            if m:
                result.script_import_failures.append(m.group(1).strip())
                continue

            m = ASSEMBLY_REF_PATTERN.search(line)
            if m:
                result.assembly_errors.append(
                    {
                        "assembly": m.group(1).strip(),
                        "missing_ref": m.group(2).strip(),
                    }
                )
                continue

            m = SHADER_ERROR_PATTERN.search(line)
            if m:
                result.shader_errors.append(
                    {
                        "shader": m.group(1).strip(),
                        "message": m.group(2).strip(),
                    }
                )
                continue

    return result


def format_markdown(result: ParseResult) -> str:
    lines = []
    lines.append("## Unity Compile Check Results\n")

    if result.project_path:
        lines.append(f"**Project:** {result.project_path}")
    if result.unity_version:
        lines.append(f"**Unity Version:** {result.unity_version}")
    lines.append(f"**Status:** {result.status}\n")

    if result.errors:
        lines.append(f"### Errors ({len(result.errors)})\n")
        lines.append("| File | Line | Code | Message |")
        lines.append("|------|------|------|---------|")
        for e in result.errors:
            lines.append(f"| {e.filename} | {e.line} | {e.code} | {e.message} |")
        lines.append("")

    if result.script_import_failures:
        lines.append(
            f"### Script Import Failures ({len(result.script_import_failures)})\n"
        )
        for s in result.script_import_failures:
            lines.append(f"- {s}")
        lines.append("")

    if result.assembly_errors:
        lines.append(f"### Assembly Reference Errors ({len(result.assembly_errors)})\n")
        for a in result.assembly_errors:
            lines.append(
                f"- Assembly `{a['assembly']}` missing reference to `{a['missing_ref']}`"
            )
        lines.append("")

    if result.shader_errors:
        lines.append(f"### Shader Errors ({len(result.shader_errors)})\n")
        for s in result.shader_errors:
            lines.append(f"- `{s['shader']}`: {s['message']}")
        lines.append("")

    if result.warnings:
        lines.append(f"### Warnings ({len(result.warnings)})\n")
        lines.append("| File | Line | Code | Message |")
        lines.append("|------|------|------|---------|")
        for w in result.warnings:
            lines.append(f"| {w.filename} | {w.line} | {w.code} | {w.message} |")
        lines.append("")

    total_err = result.total_errors
    total_warn = len(result.warnings)
    lines.append("### Summary\n")
    lines.append(f"- {total_err} error(s), {total_warn} warning(s)")
    if result.errors:
        first = result.errors[0]
        lines.append(f"- First error: {first.filename}:{first.line} — {first.message}")

    return "\n".join(lines)


def format_json(result: ParseResult) -> str:
    data = {
        "status": result.status,
        "unity_version": result.unity_version,
        "project_path": result.project_path,
        "errors": [asdict(e) for e in result.errors],
        "warnings": [asdict(e) for e in result.warnings],
        "script_import_failures": result.script_import_failures,
        "assembly_errors": result.assembly_errors,
        "shader_errors": result.shader_errors,
        "summary": {
            "total_errors": result.total_errors,
            "total_warnings": len(result.warnings),
            "compilation_failed_marker": result.compilation_failed_marker,
        },
    }
    return json.dumps(data, indent=2)


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    log_path = args[0]
    ci_mode = "--ci" in args
    json_mode = "--json" in args
    warnings_as_errors = "--warnings-as-errors" in args

    result = parse_log(log_path)

    if json_mode:
        print(format_json(result))
    else:
        print(format_markdown(result))

    if ci_mode or warnings_as_errors:
        if result.has_errors:
            sys.exit(1)
        if warnings_as_errors and result.warnings:
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import sys
import os
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple


class CoverageChecker:
    def __init__(self):
        self.gaps = []
        self.covered = []
        self.warnings = []
        self.stats = {
            "source_classes": 0, "source_methods": 0,
            "test_classes": 0, "test_methods": 0,
            "covered_methods": 0, "uncovered_methods": 0,
        }

    def extract_public_methods(self, filepath: str) -> List[Tuple[str, str, int]]:
        content = Path(filepath).read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        methods = []
        current_class = None
        class_pattern = re.compile(
            r"^\s*(?:public|internal|private|protected)?\s*(?:abstract|sealed|static|partial)?\s*"
            r"class\s+(\w+)"
        )
        method_pattern = re.compile(
            r"^\s*public\s+(?:static\s+|virtual\s+|override\s+|async\s+)*"
            r"(?:\w+(?:<[^>]+>)?)\s+(\w+)\s*\("
        )
        for i, line in enumerate(lines, 1):
            cm = class_pattern.search(line)
            if cm:
                current_class = cm.group(1)
                self.stats["source_classes"] += 1
            mm = method_pattern.search(line)
            if mm and current_class:
                method_name = mm.group(1)
                if method_name not in (
                    "Awake", "Start", "OnEnable", "OnDisable", "OnDestroy",
                    "OnApplicationPause", "OnApplicationFocus", "OnApplicationQuit",
                    "GetHashCode", "Equals", "ToString",
                ):
                    methods.append((current_class, method_name, i))
                    self.stats["source_methods"] += 1
        return methods

    def extract_test_names(self, filepath: str) -> Set[str]:
        content = Path(filepath).read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        test_names = set()
        test_attr_pattern = re.compile(r"^\s*\[(Test|UnityTest|TestCase)")
        method_pattern = re.compile(r"^\s*public\s+\w+\s+(\w+)\s*\(")
        is_next_test = False
        for line in lines:
            if test_attr_pattern.search(line):
                is_next_test = True
                continue
            if is_next_test:
                mm = method_pattern.search(line)
                if mm:
                    test_names.add(mm.group(1))
                    self.stats["test_methods"] += 1
                    is_next_test = False
        if test_names:
            self.stats["test_classes"] += 1
        return test_names

    def find_test_files(self, test_dir: str, class_name: str) -> List[str]:
        test_path = Path(test_dir)
        if not test_path.exists():
            return []
        candidates = []
        patterns = [
            f"{class_name}Tests.cs", f"{class_name}Test.cs",
            f"{class_name}EventTests.cs", f"{class_name}IntegrationTests.cs",
            f"{class_name}StateTests.cs",
        ]
        for cs_file in test_path.rglob("*.cs"):
            if cs_file.name in patterns or class_name in cs_file.name:
                candidates.append(str(cs_file))
        return candidates

    def check_method_coverage(self, class_name: str, method_name: str, line_num: int, test_names: Set[str], source_file: str) -> bool:
        for test_name in test_names:
            if method_name in test_name:
                self.covered.append(f"{class_name}.{method_name} → covered by {test_name}")
                self.stats["covered_methods"] += 1
                return True
        self.gaps.append(f"{source_file}:{line_num}: {class_name}.{method_name}() — no test found")
        self.stats["uncovered_methods"] += 1
        return False

    def check_critical_patterns(self, filepath: str) -> None:
        content = Path(filepath).read_text(encoding="utf-8", errors="replace")
        critical = [
            (r"event\s+\w+\s+(\w+)", "Event '{}' should have subscription/firing tests"),
            (r"enum\s+(\w+State\w*)", "State enum '{}' transitions should be tested"),
            (r"interface\s+(\w+)", "Interface '{}' implementations should be tested"),
            (r"try\s*\{", "Try/catch blocks should have error-path tests"),
        ]
        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            for pattern, message_tmpl in critical:
                m = re.search(pattern, line)
                if m:
                    name = m.group(1) if m.lastindex else "block"
                    self.warnings.append(f"{filepath}:{i}: {message_tmpl.format(name)}")

    def analyze(self, source_paths: List[str], test_dir: str) -> None:
        for source_path in source_paths:
            path = Path(source_path)
            cs_files = []
            if path.is_file() and path.suffix == ".cs":
                cs_files = [path]
            elif path.is_dir():
                cs_files = list(path.rglob("*.cs"))
            else:
                self.gaps.append(f"Source path not found: {source_path}")
                continue
            for cs_file in cs_files:
                if "Test" in cs_file.parent.name:
                    continue
                methods = self.extract_public_methods(str(cs_file))
                if not methods:
                    continue
                classes: Dict[str, list] = {}
                for cls, method, line in methods:
                    classes.setdefault(cls, []).append((method, line))
                for class_name, class_methods in classes.items():
                    test_files = self.find_test_files(test_dir, class_name)
                    if not test_files:
                        self.gaps.append(f"No test file found for class: {class_name} (source: {cs_file})")
                        self.stats["uncovered_methods"] += len(class_methods)
                        continue
                    all_test_names: Set[str] = set()
                    for tf in test_files:
                        all_test_names.update(self.extract_test_names(tf))
                    for method_name, line_num in class_methods:
                        self.check_method_coverage(class_name, method_name, line_num, all_test_names, str(cs_file))
                self.check_critical_patterns(str(cs_file))

    def report(self) -> int:
        total_methods = self.stats["covered_methods"] + self.stats["uncovered_methods"]
        coverage_pct = (self.stats["covered_methods"] / total_methods * 100) if total_methods > 0 else 0
        print("=" * 60)
        print("REFACTORING TEST COVERAGE REPORT")
        print("=" * 60)
        print(f"\n📊 Statistics:")
        print(f"   Source classes:   {self.stats['source_classes']}")
        print(f"   Source methods:   {self.stats['source_methods']}")
        print(f"   Test classes:     {self.stats['test_classes']}")
        print(f"   Test methods:     {self.stats['test_methods']}")
        print(f"   Coverage:         {coverage_pct:.0f}% ({self.stats['covered_methods']}/{total_methods} methods)")
        if self.covered:
            print(f"\n✅ COVERED ({len(self.covered)}):")
            for c in self.covered[:20]:
                print(f"   {c}")
            if len(self.covered) > 20:
                print(f"   ... and {len(self.covered) - 20} more")
        if self.gaps:
            print(f"\n❌ GAPS ({len(self.gaps)}):")
            for g in self.gaps:
                print(f"   {g}")
        if self.warnings:
            print(f"\n⚠️  REVIEW ({len(self.warnings)}):")
            for w in self.warnings[:15]:
                print(f"   {w}")
            if len(self.warnings) > 15:
                print(f"   ... and {len(self.warnings) - 15} more")
        print(f"\n{'=' * 60}")
        if coverage_pct < 50:
            print("❌ Coverage below 50% — add more tests before proceeding.")
            return 1
        elif coverage_pct < 80:
            print("⚠️  Coverage below 80% — consider adding more tests.")
            return 0
        else:
            print("✅ Coverage looks good.")
            return 0


def main():
    if len(sys.argv) < 3:
        print("Usage: check_test_coverage.py <source-dir> <test-dir>")
        print("       check_test_coverage.py --source <file.cs> --test-dir <dir>")
        sys.exit(1)
    checker = CoverageChecker()
    if sys.argv[1] == "--source":
        if len(sys.argv) < 5 or sys.argv[3] != "--test-dir":
            print("Usage: check_test_coverage.py --source <file.cs> --test-dir <dir>")
            sys.exit(1)
        checker.analyze([sys.argv[2]], sys.argv[4])
    else:
        checker.analyze([sys.argv[1]], sys.argv[2])
    sys.exit(checker.report())


if __name__ == "__main__":
    main()

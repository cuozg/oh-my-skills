#!/usr/bin/env python3
import os
import re
import sys
import json
from collections import defaultdict
from pathlib import Path

SINGLETON_DECL = re.compile(r"class\s+(\w+)\s*:\s*Singleton\s*<\s*(\w+)\s*>")
INSTANCE_ACCESS = re.compile(r"(\w+)\.Instance(?:\.|\s|;|\)|\])")
NULL_CHECK_BEFORE = re.compile(r"(?:if\s*\(\s*\w+\.Instance\s*!=\s*null|if\s*\(\s*\w+\.HasInstance)")
AWAKE_METHOD = re.compile(r"(?:override\s+)?(?:protected|private|public)?\s*(?:override\s+)?void\s+Awake\s*\(")
BASE_AWAKE = re.compile(r"base\.Awake\s*\(")
PUBLIC_FIELD = re.compile(r"^\s*public\s+(?!static|const|readonly|override|virtual|abstract|event|delegate|class|interface|enum|struct)(\w+(?:<[^>]+>)?(?:\[\])?)\s+(\w+)\s*[;={]")


def find_cs_files(root_dir):
    cs_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(".cs") and "/Editor/" not in dirpath:
                cs_files.append(os.path.join(dirpath, f))
    return cs_files


def scan_singleton_declarations(files):
    singletons = {}
    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            for match in SINGLETON_DECL.finditer(content):
                class_name = match.group(1)
                type_param = match.group(2)
                rel_path = os.path.relpath(filepath)
                singletons[class_name] = {
                    "file": rel_path,
                    "type_param": type_param,
                    "self_referencing": class_name == type_param,
                }
        except Exception:
            continue
    return singletons


def scan_instance_access(files, singleton_names):
    access_map = defaultdict(list)
    dep_graph = defaultdict(set)
    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            continue
        rel_path = os.path.relpath(filepath)
        file_singleton = None
        for name, info in singleton_names.items():
            if info["file"] == rel_path:
                file_singleton = name
                break
        in_awake = False
        brace_depth = 0
        awake_brace_start = -1
        for line_num, line in enumerate(lines, 1):
            if AWAKE_METHOD.search(line):
                in_awake = True
                awake_brace_start = brace_depth
            if in_awake:
                brace_depth += line.count("{") - line.count("}")
                if brace_depth <= awake_brace_start and "{" not in line and "}" in line:
                    in_awake = False
            for match in INSTANCE_ACCESS.finditer(line):
                accessed_singleton = match.group(1)
                if accessed_singleton not in singleton_names:
                    continue
                context = lines[max(0, line_num - 3) : line_num]
                context_str = "".join(context)
                has_null_check = bool(NULL_CHECK_BEFORE.search(context_str))
                access_info = {
                    "singleton": accessed_singleton,
                    "line": line_num,
                    "has_null_check": has_null_check,
                    "in_awake": in_awake,
                    "code": line.strip()[:120],
                }
                access_map[rel_path].append(access_info)
                if file_singleton and accessed_singleton != file_singleton:
                    dep_graph[file_singleton].add(accessed_singleton)
    return access_map, dep_graph


def detect_cycles(dep_graph):
    cycles = []
    visited = set()
    rec_stack = set()
    path = []
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        for neighbor in dep_graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)
        path.pop()
        rec_stack.discard(node)
    for node in dep_graph:
        if node not in visited:
            dfs(node)
    return cycles


def check_anti_patterns(files, singleton_names):
    anti_patterns = []
    for class_name, info in singleton_names.items():
        filepath = info["file"]
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.split("\n")
        except Exception:
            continue
        has_awake = bool(AWAKE_METHOD.search(content))
        has_base_awake = bool(BASE_AWAKE.search(content))
        if has_awake and not has_base_awake:
            anti_patterns.append({
                "class": class_name, "file": filepath,
                "issue": "Awake() override without base.Awake() call", "severity": "high",
            })
        public_field_count = 0
        for line in lines:
            if PUBLIC_FIELD.match(line):
                public_field_count += 1
        if public_field_count > 3:
            anti_patterns.append({
                "class": class_name, "file": filepath,
                "issue": f"{public_field_count} public mutable fields — consider encapsulation",
                "severity": "medium",
            })
    return anti_patterns


def compute_stats(singleton_names, dep_graph, access_map, cycles, anti_patterns):
    unsafe_count = 0
    awake_access_count = 0
    for file_accesses in access_map.values():
        for access in file_accesses:
            if not access["has_null_check"]:
                unsafe_count += 1
            if access["in_awake"]:
                awake_access_count += 1
    high_coupling = {k: len(v) for k, v in dep_graph.items() if len(v) >= 5}
    dependents = defaultdict(int)
    for deps in dep_graph.values():
        for d in deps:
            dependents[d] += 1
    top_depended = sorted(dependents.items(), key=lambda x: -x[1])[:10]
    return {
        "total_singletons": len(singleton_names),
        "total_files_with_access": len(access_map),
        "total_instance_accesses": sum(len(v) for v in access_map.values()),
        "unsafe_access_count": unsafe_count,
        "awake_access_count": awake_access_count,
        "circular_dependency_count": len(cycles),
        "anti_pattern_count": len(anti_patterns),
        "high_coupling_singletons": high_coupling,
        "most_depended_on": top_depended,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: audit_singletons.py <root_dir> [--focus all|dependencies|null-checks|init-order]")
        sys.exit(1)
    root_dir = sys.argv[1]
    focus = "all"
    if "--focus" in sys.argv:
        idx = sys.argv.index("--focus")
        if idx + 1 < len(sys.argv):
            focus = sys.argv[idx + 1]
    if not os.path.isdir(root_dir):
        print(json.dumps({"error": f"Directory not found: {root_dir}"}))
        sys.exit(1)
    cs_files = find_cs_files(root_dir)
    singleton_names = scan_singleton_declarations(cs_files)
    access_map, dep_graph = scan_instance_access(cs_files, singleton_names)
    dep_graph_serializable = {k: sorted(list(v)) for k, v in dep_graph.items()}
    cycles = detect_cycles(dep_graph)
    anti_patterns = check_anti_patterns(cs_files, singleton_names)
    stats = compute_stats(singleton_names, dep_graph, access_map, cycles, anti_patterns)
    result = {"stats": stats}
    if focus in ("all", "dependencies"):
        result["singleton_classes"] = singleton_names
        result["dependency_graph"] = dep_graph_serializable
        result["circular_dependencies"] = cycles
    if focus in ("all", "null-checks"):
        unsafe = {}
        for filepath, accesses in access_map.items():
            unsafe_accesses = [a for a in accesses if not a["has_null_check"]]
            if unsafe_accesses:
                unsafe[filepath] = unsafe_accesses
        result["unsafe_access"] = unsafe
    if focus in ("all", "init-order"):
        awake = {}
        for filepath, accesses in access_map.items():
            awake_accesses = [a for a in accesses if a["in_awake"]]
            if awake_accesses:
                awake[filepath] = awake_accesses
        result["awake_time_access"] = awake
    if focus == "all":
        result["anti_patterns"] = anti_patterns
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

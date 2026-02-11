#!/usr/bin/env python3
"""
Blueprint Inspector - Parse and analyze Unity Blueprint JSON data files.

Reports:
  - File metadata (size, record count)
  - Schema: field names, types, nullability
  - Sample records
  - Data quality: missing fields, empty values
"""

import sys
import json
from pathlib import Path
from collections import Counter, defaultdict


def infer_type(value):
    """Infer a human-readable type from a JSON value."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        if len(value) == 0:
            return "string(empty)"
        return "string"
    if isinstance(value, list):
        if len(value) == 0:
            return "array(empty)"
        inner = infer_type(value[0])
        return f"array<{inner}>"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def analyze_blueprint(filepath, sample_count=3):
    """Analyze a Blueprint JSON file."""
    filepath = Path(filepath)

    if not filepath.exists():
        print(f"File not found: {filepath}")
        return

    if not filepath.suffix.lower() == ".json":
        print(f"Warning: File does not have .json extension: {filepath.name}")

    # Read and parse
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    file_size = filepath.stat().st_size
    report = []
    report.append(f"# Blueprint Inspector: {filepath.name}")
    report.append(f"\nFile: {filepath}")
    report.append(f"Size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

    # Determine structure
    records = []
    root_type = type(data).__name__

    if isinstance(data, list):
        records = data
        report.append(f"Root type: array")
        report.append(f"Record count: {len(records)}")
    elif isinstance(data, dict):
        # Common patterns: {"items": [...]} or {"data": [...]} or flat object
        # Try to find the array of records
        array_key = None
        for key, val in data.items():
            if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
                array_key = key
                break

        if array_key:
            records = data[array_key]
            report.append(f"Root type: object")
            report.append(f"Data key: '{array_key}'")
            report.append(f"Record count: {len(records)}")
            # Show top-level keys
            other_keys = [k for k in data.keys() if k != array_key]
            if other_keys:
                report.append(f"Other root keys: {', '.join(other_keys)}")
        else:
            # Flat object or nested structure without obvious array
            report.append(f"Root type: object")
            report.append(
                f"Top-level keys ({len(data)}): {', '.join(list(data.keys())[:20])}"
            )
            if len(data) > 20:
                report.append(f"  ... and {len(data) - 20} more keys")
            # Each value might be a record
            if all(isinstance(v, dict) for v in data.values()):
                records = list(data.values())
                report.append(f"Treating values as records: {len(records)}")
    else:
        report.append(f"Root type: {root_type} (unexpected)")
        print("\n".join(report))
        return

    if not records:
        report.append("\nNo records found to analyze schema.")
        print("\n".join(report))
        return

    # Schema analysis
    field_types = defaultdict(Counter)
    field_nulls = Counter()
    field_presence = Counter()
    all_fields = set()

    for record in records:
        if not isinstance(record, dict):
            continue
        for field in record:
            all_fields.add(field)
            field_presence[field] += 1
            val = record[field]
            t = infer_type(val)
            field_types[field][t] += 1
            if val is None or val == "" or val == []:
                field_nulls[field] += 1

    total = len(records)
    report.append(f"\n## Schema ({len(all_fields)} fields)")
    report.append(f"{'Field':<30} {'Type':<20} {'Present':<10} {'Empty/Null':<10}")
    report.append("-" * 70)

    for field in sorted(all_fields):
        types = field_types[field]
        # Most common type
        main_type = types.most_common(1)[0][0] if types else "unknown"
        if len(types) > 1:
            # Show mixed types
            type_str = " | ".join(f"{t}" for t, _ in types.most_common(3))
        else:
            type_str = main_type
        present = field_presence[field]
        nulls = field_nulls[field]
        present_pct = f"{present}/{total}"
        null_pct = f"{nulls}" if nulls > 0 else "-"
        report.append(f"  {field:<28} {type_str:<20} {present_pct:<10} {null_pct:<10}")

    # Sample records
    report.append(f"\n## Sample Records (first {min(sample_count, len(records))})")
    for i, record in enumerate(records[:sample_count]):
        if not isinstance(record, dict):
            report.append(f"\n### Record {i + 1}: {record}")
            continue
        report.append(f"\n### Record {i + 1}")
        for k, v in record.items():
            val_str = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
            if len(str(val_str)) > 100:
                val_str = str(val_str)[:97] + "..."
            report.append(f"  {k}: {val_str}")

    # Data quality
    report.append(f"\n## Data Quality")
    missing_fields = {f for f in all_fields if field_presence[f] < total}
    if missing_fields:
        report.append(f"Fields not present in all records ({len(missing_fields)}):")
        for f in sorted(missing_fields):
            report.append(f"  {f}: present in {field_presence[f]}/{total}")
    else:
        report.append("All fields present in every record.")

    high_null = {f for f in all_fields if field_nulls[f] > total * 0.5}
    if high_null:
        report.append(f"\nFields with >50% null/empty:")
        for f in sorted(high_null):
            report.append(f"  {f}: {field_nulls[f]}/{total} empty")

    print("\n".join(report))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: blueprint-inspector.py <json_file> [sample_count]")
        sys.exit(1)

    filepath = sys.argv[1]
    samples = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    analyze_blueprint(filepath, samples)

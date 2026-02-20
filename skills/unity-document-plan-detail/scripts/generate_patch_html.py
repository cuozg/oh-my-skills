#!/usr/bin/env python3
"""
generate_patch_html.py — Per-task .patch files → GitHub-style HTML viewer.

Usage:
    python generate_patch_html.py <patches_dir> <output_html> --title TITLE [--tasks-json FILE] [--date DATE]
    python generate_patch_html.py patches/ patch.html --title "Player Health" --tasks-json tasks.json

    Legacy (single patch):
    python generate_patch_html.py changes.patch patch.html --title "Player Health"

Per-task mode: reads patches/<TASK_ID>.patch files + optional tasks.json metadata.
Legacy mode:  reads a single .patch file (backward compatible).
"""

import sys
import json
import re
import html
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR.parent / "assets" / "templates" / "PLAN_PATCH.html"

COST_MAP = {"S": "badge-s", "M": "badge-m", "L": "badge-l", "XL": "badge-xl"}
TYPE_MAP = {
    "Logic": "tag-blue",
    "UI": "tag-purple",
    "Data": "tag-yellow",
    "API": "tag-green",
    "Asset": "tag-yellow",
    "Test": "tag-green",
    "Config": "tag-blue",
}


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def parse_patch(patch_text: str) -> list[dict]:
    files = []
    current_file = None
    current_hunk = None

    lines = patch_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        if line.startswith("--- "):
            old_path = line[4:].strip()
            if i + 1 < len(lines) and lines[i + 1].startswith("+++ "):
                new_path = lines[i + 1][4:].strip()
                if old_path == "/dev/null":
                    status, path = "added", new_path.removeprefix("b/")
                elif new_path == "/dev/null":
                    status, path = "deleted", old_path.removeprefix("a/")
                else:
                    status, path = "modified", new_path.removeprefix("b/")

                current_file = {
                    "path": path,
                    "old_path": old_path.removeprefix("a/"),
                    "status": status,
                    "hunks": [],
                    "additions": 0,
                    "deletions": 0,
                }
                files.append(current_file)
                current_hunk = None
                i += 2
                continue

        hunk_match = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)", line)
        if hunk_match and current_file is not None:
            current_hunk = {
                "header": line,
                "lines": [],
                "old_line": int(hunk_match.group(1)),
                "new_line": int(hunk_match.group(3)),
            }
            current_file["hunks"].append(current_hunk)
            i += 1
            continue

        if current_hunk is not None and current_file is not None:
            if line.startswith("+"):
                current_hunk["lines"].append(
                    ("add", None, current_hunk["new_line"], line[1:])
                )
                current_hunk["new_line"] += 1
                current_file["additions"] += 1
            elif line.startswith("-"):
                current_hunk["lines"].append(
                    ("del", current_hunk["old_line"], None, line[1:])
                )
                current_hunk["old_line"] += 1
                current_file["deletions"] += 1
            elif line.startswith(" "):
                current_hunk["lines"].append(
                    (
                        "ctx",
                        current_hunk["old_line"],
                        current_hunk["new_line"],
                        line[1:],
                    )
                )
                current_hunk["old_line"] += 1
                current_hunk["new_line"] += 1
            elif line.startswith("\\"):
                pass
            else:
                current_hunk = None

        i += 1

    return files


def render_file_row(f: dict) -> str:
    return (
        f'            <div class="fr mono">'
        f'<span class="p">{esc(f["path"])}</span>'
        f'<span class="a">+{f["additions"]}</span>'
        f'<span class="d">-{f["deletions"]}</span>'
        f"</div>"
    )


def render_diff_section(f: dict) -> str:
    status = f["status"]
    label = {"added": "Added", "modified": "Modified", "deleted": "Deleted"}[status]

    rows = []
    for hunk in f["hunks"]:
        rows.append(f'<tr class="h"><td colspan="4">{esc(hunk["header"])}</td></tr>')
        for line_type, old_num, new_num, text in hunk["lines"]:
            old_s = str(old_num) if old_num is not None else ""
            new_s = str(new_num) if new_num is not None else ""
            cls = {"add": "a", "del": "r"}.get(line_type, "c")
            sign = {"add": "+", "del": "-"}.get(line_type, "")
            rows.append(
                f'<tr class="{cls}">'
                f'<td class="ln o">{old_s}</td>'
                f'<td class="ln">{new_s}</td>'
                f'<td class="sg">{sign}</td>'
                f'<td class="cd">{esc(text)}</td>'
                f"</tr>"
            )

    return (
        f'        <div class="df">\n'
        f'            <div class="dh mono">\n'
        f'                <span class="p">{esc(f["path"])}</span>\n'
        f'                <span class="bg-status {status}">{label}</span>\n'
        f"            </div>\n"
        f'            <div style="overflow-x:auto">\n'
        f'                <table class="mono">\n'
        + "\n".join(rows)
        + "\n                </table>\n"
        f"            </div>\n"
        f"        </div>"
    )


def render_task_section(
    task_id: str, files: list[dict], meta: dict | None, patch_rel: str
) -> str:
    adds = sum(f["additions"] for f in files)
    dels = sum(f["deletions"] for f in files)
    subject = meta.get("subject", task_id) if meta else task_id
    task_type = meta.get("type", "Logic") if meta else "Logic"
    cost = meta.get("cost", "M") if meta else "M"
    wave = meta.get("wave", 1) if meta else 1

    type_cls = TYPE_MAP.get(task_type, "tag-blue")
    cost_cls = COST_MAP.get(cost, "badge-m")

    file_rows = "\n".join(render_file_row(f) for f in files)
    diff_html = "\n".join(render_diff_section(f) for f in files)

    return (
        f'        <div class="task-patch" id="{esc(task_id)}">\n'
        f'            <div class="tp-header">\n'
        f'                <div class="tp-title"><code>{esc(task_id)}</code> {esc(subject)}</div>\n'
        f'                <div class="tp-meta">\n'
        f'                    <span class="tag {type_cls}">{esc(task_type)}</span>\n'
        f'                    <span class="badge {cost_cls}">{esc(cost)}</span>\n'
        f'                    <span class="wave-badge">W{wave}</span>\n'
        f'                    <a href="{esc(patch_rel)}" class="tp-dl">Download .patch</a>\n'
        f"                </div>\n"
        f"            </div>\n"
        f'            <div class="tp-info">\n'
        f"                <span>Files: {len(files)}</span>\n"
        f'                <span class="a">+{adds}</span>\n'
        f'                <span class="d">-{dels}</span>\n'
        f"            </div>\n"
        f'            <div class="tp-files">\n'
        f"{file_rows}\n"
        f"            </div>\n"
        f"{diff_html}\n"
        f"        </div>"
    )


def load_tasks_meta(tasks_json_path: Path | None) -> dict[str, dict]:
    if tasks_json_path is None or not tasks_json_path.exists():
        return {}
    data = json.loads(tasks_json_path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {t["id"]: t for t in data if "id" in t}
    return data


def generate_per_task_html(
    task_patches: list[tuple[str, list[dict], str]],
    tasks_meta: dict[str, dict],
    title: str,
    plan_date: str,
    template: str,
) -> str:
    all_files = []
    for _, files, _ in task_patches:
        all_files.extend(files)

    total_adds = sum(f["additions"] for f in all_files)
    total_dels = sum(f["deletions"] for f in all_files)
    unique_paths = {f["path"] for f in all_files}

    sections = []
    for task_id, files, patch_rel in task_patches:
        meta = tasks_meta.get(task_id)
        sections.append(render_task_section(task_id, files, meta, patch_rel))

    result = template
    result = result.replace("{{FEATURE_TITLE}}", esc(title))
    result = result.replace("{{FEATURE_NAME}}", esc(title))
    result = result.replace("{{PLAN_DATE}}", esc(plan_date))
    result = result.replace("{{TASK_COUNT}}", str(len(task_patches)))
    result = result.replace("{{FILE_COUNT}}", str(len(unique_paths)))
    result = result.replace("{{ADDITIONS}}", str(total_adds))
    result = result.replace("{{DELETIONS}}", str(total_dels))
    result = result.replace("{{TASK_SECTIONS}}", "\n".join(sections))

    return result


def generate_legacy_html(
    files: list[dict], title: str, plan_date: str, template: str
) -> str:
    task_patches = [("all", files, "./changes.patch")]
    return generate_per_task_html(task_patches, {}, title, plan_date, template)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Per-task .patch files → GitHub-style HTML viewer"
    )
    parser.add_argument(
        "patch_source",
        help="Directory of per-task .patch files OR single .patch file (legacy)",
    )
    parser.add_argument("output_html", help="Output HTML file path")
    parser.add_argument(
        "--title", default="Code Changes", help="Feature title for the header"
    )
    parser.add_argument(
        "--date", default=date.today().isoformat(), help="Plan date (default: today)"
    )
    parser.add_argument(
        "--tasks-json",
        default=None,
        help="JSON file with task metadata [{id, subject, type, cost, wave}, ...]",
    )
    parser.add_argument(
        "--template",
        default=str(TEMPLATE_PATH),
        help="Path to HTML template (default: assets/templates/PLAN_PATCH.html)",
    )

    args = parser.parse_args()

    template_path = Path(args.template)
    if not template_path.exists():
        print(f"Error: template not found: {template_path}", file=sys.stderr)
        sys.exit(1)
    template = template_path.read_text(encoding="utf-8")

    source = Path(args.patch_source)

    if source.is_dir():
        patch_files = sorted(source.glob("*.patch"))
        if not patch_files:
            print(f"Error: no .patch files in {source}", file=sys.stderr)
            sys.exit(1)

        tasks_meta = load_tasks_meta(Path(args.tasks_json) if args.tasks_json else None)

        task_patches = []
        for pf in patch_files:
            task_id = pf.stem
            files = parse_patch(pf.read_text(encoding="utf-8"))
            patch_rel = f"./patches/{pf.name}"
            task_patches.append((task_id, files, patch_rel))

        output = generate_per_task_html(
            task_patches, tasks_meta, args.title, args.date, template
        )
    elif source.is_file():
        files = parse_patch(source.read_text(encoding="utf-8"))
        output = generate_legacy_html(files, args.title, args.date, template)
    else:
        print(f"Error: patch source not found: {source}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output_html)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()

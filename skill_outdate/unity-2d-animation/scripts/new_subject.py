"""
Scaffold one animated subject folder in a Unity project from the unity-2d-animation templates.

  python3 -I <skill>/scripts/new_subject.py --name Pony --kind character [--image path/to/pony.png] [--project .]

Creates (nothing is overwritten unless --force; the copies are the subject's own and get edited per subject):
  Assets/<Name>/Source/<name>.png                      exported source image (when --image is given)
  Assets/<Name>/Tools~/split_<name>.py, <name>.json    splitter copy + starter config (Unity ignores "~" folders)
  Assets/<Name>/Art/Parts/                             split output lands here
  Assets/<Name>/Scripts/Editor/<Name>RigBuilder.cs, <Name>ClipFactory.cs
  Assets/<Name>/Scripts/Runtime/<Name>DebugHUD.cs, CameraFollow2D.cs, [<Name>Controller.cs  (character only)]
--kind character -> Rigidbody2D + collider + move/run/jump controller; --kind object -> static, clip preview only.
"""
import argparse
import json
import os
import re
import shutil
import sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(SKILL, "templates")

# Starter config: every required key with a placeholder value; fill it from `inspect` measurements.
STARTER_CONFIG = {
    "name": None, "ppu": 500, "origin": [0, 0], "dark_lum": 150, "stroke_reach": 16, "grid": 20,
    "parts": [], "cuts": [], "assign": [], "dark_parts": [], "exclusive": [], "extend": {},
    "anchor_part": None, "glued": {}, "glue_start": 8, "bones": [], "part_bones": {},
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="PascalCase C# identifier, e.g. Pony, TreasureChest")
    ap.add_argument("--kind", required=True, choices=["character", "object"])
    ap.add_argument("--image", help="exported source PNG to copy into Assets/<Name>/Source/")
    ap.add_argument("--project", default=".", help="Unity project root (contains Assets/)")
    ap.add_argument("--force", action="store_true", help="overwrite existing scaffold files")
    a = ap.parse_args()

    if not re.fullmatch(r"[A-Z][A-Za-z0-9]*", a.name):
        sys.exit("--name must be PascalCase letters/digits (it becomes a C# namespace and class prefix)")
    if not os.path.isdir(os.path.join(a.project, "Assets")):
        sys.exit(f"{a.project} has no Assets/ folder - pass --project <Unity project root>")
    lower = a.name[0].lower() + a.name[1:]
    root = os.path.join(a.project, "Assets", a.name)
    subs = {"__NAME__": a.name, "__LOWER__": lower,
            "__HAS_LOCOMOTION__": "true" if a.kind == "character" else "false"}

    # (template, destination) pairs; the controller only exists for characters.
    plan = [
        ("Tools~/split_subject.py", f"Tools~/split_{lower}.py"),
        ("Editor/__NAME__RigBuilder.cs", f"Scripts/Editor/{a.name}RigBuilder.cs"),
        ("Editor/__NAME__ClipFactory.cs", f"Scripts/Editor/{a.name}ClipFactory.cs"),
        ("Runtime/__NAME__DebugHUD.cs", f"Scripts/Runtime/{a.name}DebugHUD.cs"),
        ("Runtime/CameraFollow2D.cs", "Scripts/Runtime/CameraFollow2D.cs"),
    ]
    if a.kind == "character":
        plan.append(("Runtime/__NAME__Controller.cs", f"Scripts/Runtime/{a.name}Controller.cs"))

    existing = [d for _, d in plan if os.path.exists(os.path.join(root, d))]
    if existing and not a.force:
        sys.exit("refusing to overwrite (pass --force): " + ", ".join(existing))

    for d in ("Source", "Tools~", "Art/Parts", "Scripts/Editor", "Scripts/Runtime"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    for src, dst in plan:
        text = open(os.path.join(TEMPLATES, src), encoding="utf-8").read()
        for k, v in subs.items():
            text = text.replace(k, v)
        with open(os.path.join(root, dst), "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote", os.path.join(root, dst))

    cfg_path = os.path.join(root, "Tools~", f"{lower}.json")
    if not os.path.exists(cfg_path) or a.force:
        with open(cfg_path, "w") as f:
            json.dump(dict(STARTER_CONFIG, name=a.name), f, indent=2)
        print("wrote", cfg_path)
    if a.image:
        dst = os.path.join(root, "Source", f"{lower}.png")
        shutil.copyfile(a.image, dst)
        print("wrote", dst)


if __name__ == "__main__":
    main()

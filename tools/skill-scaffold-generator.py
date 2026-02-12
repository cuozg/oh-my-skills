#!/usr/bin/env python3
"""
Skill Scaffold Generator - Domain-aware template scaffolding.

Unlike init_skill.py which creates one generic template, this generates
domain-tailored scaffolds with pre-populated structure based on skill type.

Usage:
    python skill-scaffold-generator.py <skill-name> --type <type> --path <path>

Types:
    workflow    - Sequential multi-step processes (e.g., build, deploy, review)
    tool        - Single-purpose tools/utilities (e.g., pdf-editor, mermaid)
    reference   - Knowledge/guidelines skills (e.g., brand-guidelines, coding-standards)
    integration - External service/API skills (e.g., bigquery, slack-notifier)
"""

import sys
import json
from pathlib import Path

SKILL_TYPES = {
    "workflow": {
        "sections": [
            "## Purpose\n\n[TODO: What process does this skill automate?]",
            "## Input\n\n- **Required**: [TODO: primary input]\n- **Optional**: [TODO: secondary inputs]",
            "## Output\n\n[TODO: What is produced at the end?]",
            "## Workflow\n\n1. [TODO: First step]\n2. [TODO: Second step]\n3. [TODO: Verification step]",
            "## Error Handling\n\n[TODO: What to do when steps fail]",
        ],
        "resources": {"scripts": True, "references": False, "assets": False},
        "description_hint": "Sequential workflow for [domain]. Use when: (1) [trigger1], (2) [trigger2]. Triggers: '[phrase1]', '[phrase2]'.",
    },
    "tool": {
        "sections": [
            "## Purpose\n\n[TODO: What operation does this tool perform?]",
            "## Input\n\n- **Required**: [TODO: primary input]\n- **Optional**: [TODO: secondary inputs]",
            "## Output\n\n[TODO: What is produced?]",
            "## Examples\n\n| Task | Input | Output |\n|:---|:---|:---|\n| [TODO] | [TODO] | [TODO] |",
            "## Quick Start\n\n[TODO: Simplest usage example]",
        ],
        "resources": {"scripts": True, "references": False, "assets": False},
        "description_hint": "[Tool purpose]. Use when: (1) [trigger1], (2) [trigger2]. Triggers: '[phrase1]', '[phrase2]'.",
    },
    "reference": {
        "sections": [
            "## Purpose\n\n[TODO: What knowledge does this skill provide?]",
            "## When to Use\n\n[TODO: Scenarios where this skill applies]",
            "## Guidelines\n\n[TODO: Core guidelines or standards]",
            "## Resources\n\nDetailed reference documentation is available in:\n- `references/[TODO].md` — [TODO: description]",
        ],
        "resources": {"scripts": False, "references": True, "assets": False},
        "description_hint": "[Domain] guidelines and standards. Use when: (1) [trigger1], (2) [trigger2]. Triggers: '[phrase1]', '[phrase2]'.",
    },
    "integration": {
        "sections": [
            "## Purpose\n\n[TODO: What service/API does this integrate with?]",
            "## Prerequisites\n\n- [TODO: Required credentials or setup]",
            "## Configuration\n\n[TODO: Environment variables, config files]",
            "## Operations\n\n### [TODO: Operation 1]\n\n[TODO: How to perform this operation]",
            "## Error Handling\n\n[TODO: Common API errors and recovery]",
        ],
        "resources": {"scripts": True, "references": True, "assets": False},
        "description_hint": "[Service] integration for [purpose]. Use when: (1) [trigger1], (2) [trigger2]. Triggers: '[phrase1]', '[phrase2]'.",
    },
}


def title_case(name):
    return " ".join(word.capitalize() for word in name.split("-"))


def generate_scaffold(skill_name, skill_type, output_path):
    if skill_type not in SKILL_TYPES:
        print(
            f"Unknown type '{skill_type}'. Available: {', '.join(SKILL_TYPES.keys())}"
        )
        return None

    config = SKILL_TYPES[skill_type]
    skill_dir = Path(output_path).resolve() / skill_name

    if skill_dir.exists():
        print(f"Directory already exists: {skill_dir}")
        return None

    skill_dir.mkdir(parents=True, exist_ok=False)

    frontmatter = (
        f'---\nname: {skill_name}\ndescription: "{config["description_hint"]}"\n---\n\n'
    )

    body = f"# {title_case(skill_name)}\n\n"
    body += "\n\n".join(config["sections"])

    (skill_dir / "SKILL.md").write_text(frontmatter + body)
    print(f"Created SKILL.md ({skill_type} template)")

    for rdir, should_create in config["resources"].items():
        if should_create:
            dir_path = skill_dir / rdir
            dir_path.mkdir(exist_ok=True)
            (dir_path / ".gitkeep").write_text("")
            print(f"Created {rdir}/")

    report = {
        "skill_name": skill_name,
        "type": skill_type,
        "path": str(skill_dir),
        "resources_created": [k for k, v in config["resources"].items() if v],
        "sections": len(config["sections"]),
    }

    print(f"\nScaffold created at: {skill_dir}")
    print(f"Type: {skill_type} ({len(config['sections'])} sections)")
    print(f"Resources: {', '.join(report['resources_created']) or 'none'}")
    print("\nNext: Fill [TODO] placeholders in SKILL.md")

    return report


def list_types():
    print("Available scaffold types:\n")
    for name, config in SKILL_TYPES.items():
        section_names = [
            s.split("\n")[0].replace("## ", "") for s in config["sections"]
        ]
        resources = [k for k, v in config["resources"].items() if v]
        print(f"  {name}")
        print(f"    Sections: {' → '.join(section_names)}")
        print(f"    Resources: {', '.join(resources) or 'none'}")
        print()


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--list":
        if "--list" in sys.argv:
            list_types()
            sys.exit(0)
        print(
            "Usage: skill-scaffold-generator.py <skill-name> --type <type> --path <path>"
        )
        print("       skill-scaffold-generator.py --list")
        print(f"\nTypes: {', '.join(SKILL_TYPES.keys())}")
        sys.exit(1)

    skill_name = sys.argv[1]

    skill_type = "tool"
    output_path = "."
    for i, arg in enumerate(sys.argv):
        if arg == "--type" and i + 1 < len(sys.argv):
            skill_type = sys.argv[i + 1]
        if arg == "--path" and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]

    result = generate_scaffold(skill_name, skill_type, output_path)

    if "--json" in sys.argv and result:
        print(json.dumps(result, indent=2))

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()

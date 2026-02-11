#!/usr/bin/env python3
"""
Skill Finder - Match a task description to the best available skill.

Reads all SKILL.md frontmatter (name + description), tokenizes and scores
against the input query using keyword overlap + trigger phrase matching.
"""

import sys
import os
import re
import yaml
from pathlib import Path
from collections import defaultdict


def extract_frontmatter(skill_md_path):
    """Extract name and description from SKILL.md frontmatter."""
    try:
        content = skill_md_path.read_text(encoding="utf-8")
    except Exception:
        return None, None

    if not content.startswith("---"):
        return None, None

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, None

    try:
        fm = yaml.safe_load(match.group(1))
        if isinstance(fm, dict):
            return fm.get("name", ""), fm.get("description", "")
    except yaml.YAMLError:
        pass
    return None, None


def tokenize(text):
    """Simple tokenization: lowercase, split on non-alphanumeric."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def score_skill(query_tokens, query_lower, name, description):
    """Score a skill against a query. Higher = better match."""
    score = 0
    desc_lower = description.lower()
    name_lower = name.lower()

    # Exact name match in query
    if name_lower in query_lower or name_lower.replace("-", " ") in query_lower:
        score += 50

    # Token overlap with description
    desc_tokens = tokenize(description)
    overlap = query_tokens & desc_tokens
    score += len(overlap) * 3

    # Trigger phrase matching (skills use "Triggers:" in description)
    trigger_match = re.search(r"Triggers?:\s*(.+?)(?:\.|$)", description, re.IGNORECASE)
    if trigger_match:
        triggers = trigger_match.group(1).lower()
        trigger_phrases = [t.strip().strip("'\"") for t in triggers.split(",")]
        for phrase in trigger_phrases:
            if phrase in query_lower:
                score += 30

    # "Use when:" matching
    use_when_match = re.search(
        r"Use when:\s*(.+?)(?:\.\s|$)", description, re.IGNORECASE
    )
    if use_when_match:
        use_cases = use_when_match.group(1).lower()
        use_tokens = tokenize(use_cases)
        use_overlap = query_tokens & use_tokens
        score += len(use_overlap) * 5

    # Keyword boosters for common domains
    domain_keywords = {
        "error": ["fix", "error", "debug", "compiler", "exception", "crash"],
        "test": ["test", "unit", "coverage", "tdd", "editmode", "playmode"],
        "review": ["review", "pr", "pull", "request", "check", "changes"],
        "plan": ["plan", "estimate", "breakdown", "architecture", "design"],
        "refactor": [
            "refactor",
            "restructure",
            "extract",
            "rename",
            "simplify",
            "decouple",
        ],
        "performance": ["performance", "optimize", "fps", "memory", "profiler", "gc"],
        "diagram": ["diagram", "flowchart", "sequence", "visualize", "mermaid"],
        "deploy": ["deploy", "build", "ios", "android", "webgl", "mobile"],
        "investigate": ["investigate", "trace", "how", "flow", "analyze", "understand"],
        "ui": ["ui", "ux", "design", "screen", "prefab", "canvas", "layout"],
        "docs": ["document", "readme", "docs", "documentation", "guide"],
        "shader": ["shader", "hlsl", "material", "rendering", "vfx", "art"],
        "commit": ["commit", "git", "stage", "message"],
        "schema": ["schema", "flatbuffer", "fbs", "binary", "serialize"],
    }

    for domain, keywords in domain_keywords.items():
        if any(k in query_lower for k in keywords):
            if any(k in desc_lower for k in keywords):
                score += 10

    return score


def main():
    if len(sys.argv) < 3:
        print("Usage: skill-finder.py <skills_directory> <task_description>")
        sys.exit(1)

    skills_dir = Path(sys.argv[1])
    query = " ".join(sys.argv[2:])
    query_lower = query.lower()
    query_tokens = tokenize(query)

    if not skills_dir.exists():
        print(f"Skills directory not found: {skills_dir}")
        sys.exit(1)

    # Discover all skills
    skills = []
    for skill_md in skills_dir.rglob("SKILL.md"):
        name, description = extract_frontmatter(skill_md)
        if name and description:
            # Calculate category from path
            rel = skill_md.parent.relative_to(skills_dir)
            category = str(rel.parts[0]) if len(rel.parts) > 1 else "other"
            skill_path = f"{category}/{name}"
            skills.append(
                {
                    "name": name,
                    "path": skill_path,
                    "description": description,
                    "score": score_skill(query_tokens, query_lower, name, description),
                }
            )

    # Sort by score descending
    skills.sort(key=lambda s: s["score"], reverse=True)

    # Output
    print(f"# Skill Finder Results")
    print(f'\nQuery: "{query}"')
    print(f"Skills scanned: {len(skills)}")

    # Top matches
    top = [s for s in skills if s["score"] > 0]
    if not top:
        print("\nNo matching skills found.")
        print("Available skills:")
        for s in skills[:10]:
            print(f"  {s['path']}: {s['description'][:80]}...")
        return

    print(f"\n## Best Matches")
    print(f"{'Rank':<5} {'Score':<7} {'Skill':<35} {'Description'}")
    print("-" * 100)

    for i, s in enumerate(top[:8]):
        desc_short = (
            s["description"][:60] + "..."
            if len(s["description"]) > 60
            else s["description"]
        )
        print(f"  {i + 1:<3} {s['score']:<7} {s['path']:<35} {desc_short}")

    # Recommendation
    best = top[0]
    print(f"\n## Recommendation")
    print(f"Use skill: `{best['path']}`")
    print(f'Load with: load_skills=["{best["path"]}"]')

    if len(top) > 1 and top[1]["score"] > best["score"] * 0.7:
        print(f"\nAlso consider: `{top[1]['path']}` (close match)")


if __name__ == "__main__":
    main()

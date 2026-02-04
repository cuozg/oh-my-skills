---
description: Workflow for creating and maintaining technical documentation for Unity projects.
---

# Workflow: Unity Project Documentation

Create and update high-quality technical documentation for scripts, systems, and assets.

1.  **Analyze Source**:
    - Use `grep_search` and Unity MCP to identify public APIs, `ScriptableObject` types, and serialized fields.
    - Identify key dependencies and system interactions.
2.  **Select Template**:
    - Choose a template from `.claude/skills/unity-write-docs/assets/templates/` (e.g., `README_TEMPLATE.md`, `API_TEMPLATE.md`).
3.  **Draft Content**:
    - Write clear, technical descriptions of the logic and intent.
    - Use code snippets and Mermaid diagrams to visualize hierarchies or execution flows.
4.  **Validate**:
    - Cross-reference the documentation with the latest code signatures.
    - Ensure all mentioned links, paths, and prerequisites are accurate.
5.  **Submit**:
    - Save the documentation in the appropriate project location (e.g., project root, feature folder, or `Documents/`).
    - Inform the user of the new/updated documentation.

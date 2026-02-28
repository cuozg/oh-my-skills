# Review Engine
Load shared review logic from `unity-shared` before starting any review:
```python
read_skill_file("unity-shared", "references/review-deep-workflow.md")
read_skill_file("unity-shared", "references/review-gates.md")
read_skill_file("unity-shared", "references/review-logic-data.md")
read_skill_file("unity-shared", "references/review-csharp.md")
read_skill_file("unity-shared", "references/review-perf.md")
read_skill_file("unity-shared", "references/review-unity.md")
read_skill_file("unity-shared", "references/review-architecture.md")
```
These provide the review focus areas, verification gates, and checklists that both PR and local reviews use.
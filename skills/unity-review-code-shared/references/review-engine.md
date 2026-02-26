# Review Engine

Load shared review logic from `unity-code-shared` before starting any review:

```python
read_skill_file("unity-code-shared", "references/review/deep-review-workflow.md")
read_skill_file("unity-code-shared", "references/review/VERIFICATION_GATES.md")
read_skill_file("unity-code-shared", "references/review/logic-review-patterns.md")
read_skill_file("unity-code-shared", "references/review/csharp-quality.md")
read_skill_file("unity-code-shared", "references/review/performance-review.md")
read_skill_file("unity-code-shared", "references/review/unity-specifics.md")
read_skill_file("unity-code-shared", "references/review/architecture-review.md")
```

These provide the review focus areas, verification gates, and checklists that both PR and local reviews use.

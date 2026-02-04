---
description: Workflow for reviewing a Unity Pull Request using GitHub CLI and posting comments.
---

# Workflow: Review PR

Follow these steps to conduct a professional code review using the **unity-review-pr** skill expertise.

1.  **Select & Fetch**: 
    - Use `gh pr list` to identify the PR.
    // turbo
    - Run `gh pr diff --patch <number> > pr_diff.patch`.
2.  **Structural & Asset Analysis**:
    - Load the `unity-review-pr` skill context.
    - Analyze the diff against `.claude/rules/unity-csharp-conventions.md` and `.claude/rules/unity-asset-rules.md`.
    - Evaluate method/class lengths and tech debt markers (TODO/FIXME) as per skill targets.
3.  **Risk & Performance Audit**:
    - Identify memory leaks, missing null guards, and high-allocation patterns in `Update()`.
    - Check for pattern consistency (e.g., Singleton usage, Event architectures).
4.  **Draft findings**:
    - Categorize issues using skill severity levels: 🔴 **Critical**, 🟡 **Major**, 🔵 **Minor**, 💚 **Suggestion**.
    - Provide commit-ready code fixes using `suggestion` blocks.
    - Generate `review.json` following the [REVIEW_JSON_SPEC.md](../skills/unity-review-pr/references/REVIEW_JSON_SPEC.md).
5.  **Submit & Cleanup**:
    // turbo
    - Run `bash .claude/skills/unity-review-pr/scripts/post_review.sh <number> review.json`.
    - Delete `pr_diff.patch` and `review.json`.
6.  **Confirmation**: Provide the PR URL and a high-level summary of the findings to the user.

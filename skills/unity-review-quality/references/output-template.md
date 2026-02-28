# Summary Output Template

After saving the HTML report, present to the user using this exact format:

```
## Quality Review: [ProjectName]

**Grade: [A/B/C/D/F]** — [one-sentence justification]
**Report**: `Documents/Reviews/QUALITY_REVIEW_[ProjectName]_[YYYYMMDD].html`

### Findings Summary
| Severity | Count |
|:---------|------:|
| :red_circle: Critical | [N] |
| :orange_circle: High | [N] |
| :yellow_circle: Medium | [N] |
| :white_circle: Low | [N] |
| **Total** | **[N]** |

### Top Critical Issues
1. **[Issue Title]** — `[File.cs:line]` — [one-sentence description + impact]
2. **[Issue Title]** — `[File.cs:line]` — [one-sentence description + impact]
3. **[Issue Title]** — `[File.cs:line]` — [one-sentence description + impact]
(list up to 5; omit section if 0 critical)

### Top High Issues
1. **[Issue Title]** — `[File.cs:line]` — [one-sentence description]
2. **[Issue Title]** — `[File.cs:line]` — [one-sentence description]
(list up to 5; omit section if 0 high)

### What's Done Well
- [positive observation 1]
- [positive observation 2]
- [positive observation 3]
```

## Severity Classification

| Severity | Icon | Meaning | Examples |
|:---------|:-----|:--------|:---------|
| Critical | :red_circle: | Crash, data loss, security vulnerability, memory leak | NullRef in production path, unsanitized input, undisposed resources |
| High | :orange_circle: | Performance degradation, architectural violation, logic bugs | GetComponent in Update, God class, missing error handling |
| Medium | :yellow_circle: | Code quality, maintainability, conventions | Magic numbers, deep nesting, missing XML docs |
| Low | :white_circle: | Style, minor improvements, nice-to-have | Naming inconsistencies, unused usings, minor refactoring |

## Grading Criteria

| Grade | Criteria |
|:------|:---------|
| A | 0 Critical, <=3 High, clean architecture, good test coverage, follows conventions |
| B | 0 Critical, <=8 High, mostly clean architecture, some tests, minor debt |
| C | <=2 Critical, <=15 High, architectural concerns, limited tests, moderate debt |
| D | <=5 Critical, >15 High, significant architectural issues, no tests, heavy debt |
| F | >5 Critical, project stability at risk, major architectural failures |

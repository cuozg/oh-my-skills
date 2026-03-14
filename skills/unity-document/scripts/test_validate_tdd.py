"""
Tests for validate_tdd.py

Uses tmp_path (pytest fixture) to write temp markdown files so the validator's
file-based API is exercised without touching the real docs folder.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(__file__))
from validate_tdd import validate_tdd

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_TDD_TEMPLATE = """\
# TDD: TestSystem

**Date**: 2026-03-14
**Status**: Draft

---

## Problem

We need a system that handles X efficiently.

---

## Goals

- Achieve sub-10ms response times
- Support 100 concurrent users

## Non-Goals

- Mobile platform support
- Offline mode

---

## Design

### Components

| Component | Responsibility | File |
|-----------|----------------|------|
| Manager | Coordinates lifecycle | `Manager.cs` |
| Handler | Processes events | `Handler.cs` |

### Interfaces

```csharp
public interface IHandler
{{
    void Handle(Event e);
}}
```

### Data Flow

```mermaid
flowchart LR
    A[Input] --> B[Manager] --> C[Handler] --> D[Output]
```

---

## Alternatives Considered

| Option | Pros | Cons | Rejected Because |
|--------|------|------|-----------------|
| Polling | Simple | High CPU | Wastes cycles |
| Observer | Efficient | Complex | N/A - selected |

---

## Dependencies

| System | Coupling | Evidence |
|--------|----------|----------|
| EventBus | Loose | `EventBus.cs:42` |
| SaveSystem | Tight | `SaveManager.cs:15` |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Memory leaks | M | H | Object pooling |
| Race conditions | L | H | Main-thread enforcement |

---

## Open Questions

- Should we support async operations?
"""


def _make_doc(tmp_path, content, filename="tdd.md"):
    path = tmp_path / filename
    path.write_text(content, encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# 1. Valid document passes all checks
# ---------------------------------------------------------------------------


def test_valid_document_passes(tmp_path):
    doc = _make_doc(tmp_path, VALID_TDD_TEMPLATE)
    assert validate_tdd(doc) is True


# ---------------------------------------------------------------------------
# 2. Section presence detection
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "section_header",
    [
        "## Problem",
        "## Goals",
        "## Non-Goals",
        "## Design",
        "## Alternatives Considered",
        "## Dependencies",
        "## Risks",
        "## Open Questions",
    ],
)
def test_missing_section_fails(tmp_path, section_header):
    content = VALID_TDD_TEMPLATE.replace(section_header, "## X-Replaced")
    doc = _make_doc(tmp_path, content)
    assert validate_tdd(doc) is False


# ---------------------------------------------------------------------------
# 3. Mermaid diagram detection
# ---------------------------------------------------------------------------


def test_missing_mermaid_fails(tmp_path):
    content = VALID_TDD_TEMPLATE.replace("```mermaid", "```text")
    doc = _make_doc(tmp_path, content)
    assert validate_tdd(doc) is False


def test_mermaid_missing_diagram_type_fails(tmp_path):
    content = VALID_TDD_TEMPLATE.replace("flowchart LR", "unknownType")
    doc = _make_doc(tmp_path, content)
    assert validate_tdd(doc) is False


# ---------------------------------------------------------------------------
# 4. Alternatives table validation
# ---------------------------------------------------------------------------


def test_alternatives_less_than_2_fails(tmp_path):
    # Remove one alternative row
    content = VALID_TDD_TEMPLATE.replace(
        "| Observer | Efficient | Complex | N/A - selected |", ""
    )
    doc = _make_doc(tmp_path, content)
    assert validate_tdd(doc) is False


# ---------------------------------------------------------------------------
# 5. TODO / TBD / FIXME rejection
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("tag", ["TODO", "TBD", "FIXME"])
def test_forbidden_tag_fails(tmp_path, tag):
    content = VALID_TDD_TEMPLATE + f"\n{tag}: fix later\n"
    doc = _make_doc(tmp_path, content)
    assert validate_tdd(doc) is False


# ---------------------------------------------------------------------------
# 6. Dependencies evidence
# ---------------------------------------------------------------------------


def test_missing_dependency_evidence_fails(tmp_path):
    content = VALID_TDD_TEMPLATE.replace("`EventBus.cs:42`", "somewhere").replace(
        "`SaveManager.cs:15`", "somewhere"
    )
    doc = _make_doc(tmp_path, content)
    assert validate_tdd(doc) is False


# ---------------------------------------------------------------------------
# 7. Metadata validation
# ---------------------------------------------------------------------------


def test_missing_date_fails(tmp_path):
    content = VALID_TDD_TEMPLATE.replace("**Date**: 2026-03-14", "")
    doc = _make_doc(tmp_path, content)
    assert validate_tdd(doc) is False


def test_missing_status_fails(tmp_path):
    content = VALID_TDD_TEMPLATE.replace("**Status**: Draft", "")
    doc = _make_doc(tmp_path, content)
    assert validate_tdd(doc) is False


# ---------------------------------------------------------------------------
# 8. Components table validation
# ---------------------------------------------------------------------------


def test_missing_components_table_fails(tmp_path):
    content = VALID_TDD_TEMPLATE.replace(
        "| Component | Responsibility | File |", "| Name | Role |"
    )
    doc = _make_doc(tmp_path, content)
    assert validate_tdd(doc) is False


# ---------------------------------------------------------------------------
# 9. File not found
# ---------------------------------------------------------------------------


def test_nonexistent_file_returns_false():
    assert validate_tdd("/nonexistent/path/tdd.md") is False


# ---------------------------------------------------------------------------
# 10. Multiple errors accumulate
# ---------------------------------------------------------------------------


def test_multiple_errors_all_reported(tmp_path, capsys):
    content = VALID_TDD_TEMPLATE.replace("## Problem", "## X-Replaced")
    content = content.replace("**Status**: Draft", "")
    doc = _make_doc(tmp_path, content)
    result = validate_tdd(doc)
    captured = capsys.readouterr()
    assert result is False
    assert "Missing section: Problem" in captured.out
    assert "Missing Status" in captured.out

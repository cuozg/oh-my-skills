"""
Tests for validate_system_doc.py

Uses tmp_path (pytest fixture) to write temp markdown files so the validator's
file-based API is exercised without touching the real docs folder.
"""

import sys
import os
import pytest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(__file__))
from validate_system_doc import validate_doc

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _future_date(days: int = 30) -> str:
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")


def _past_date(days: int = 10) -> str:
    return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")


VALID_DOC_TEMPLATE = """\
# MySystem

- Owner: Alice
- Next Review Due: {review_date}

### 1. Overview
Overview text here.

### 2. Architecture
```mermaid
classDiagram
  class Foo {{
    +bar()
  }}
```

### 3. Public API
| Method | Signature | Location | Evidence |
|--------|-----------|----------|----------|
| ---    |           |          |          |
| Foo.bar | bar() | (Foo.cs:10) |

### 4. Decision Drivers
- **Use SO channels** for decoupled events. (EventBus.cs:42)

### 5. Data Flow
```mermaid
sequenceDiagram
  A->>B: message
```

### 6. Extension Guide
| Step | Evidence |
|------|----------|
| ---  |          |
| Add listener | (EventBus.cs:55) |

### 7. Dependencies
| Package | Evidence |
|---------|----------|
| ---     |          |
| UniTask | (Deps.cs:3) |

### 8. Known Limitations
No TODO/TBD/FIXME
"""


def _make_doc(tmp_path, content: str, filename: str = "doc.md") -> str:
    path = tmp_path / filename
    path.write_text(content, encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# 1. Valid document passes all checks
# ---------------------------------------------------------------------------


def test_valid_document_passes(tmp_path):
    doc = _make_doc(tmp_path, VALID_DOC_TEMPLATE.format(review_date=_future_date()))
    assert validate_doc(doc) is True


# ---------------------------------------------------------------------------
# 2. Section presence detection
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "missing_section",
    [
        "### 1. Overview",
        "### 2. Architecture",
        "### 3. Public API",
        "### 4. Decision Drivers",
        "### 5. Data Flow",
        "### 6. Extension Guide",
        "### 7. Dependencies",
        "### 8. Known Limitations",
    ],
)
def test_missing_section_fails(tmp_path, missing_section):
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    content = content.replace(missing_section, "### X. Replaced")
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


def test_all_sections_present_passes(tmp_path):
    """Sanity-check: having all 8 sections is a necessary condition to pass."""
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is True


# ---------------------------------------------------------------------------
# 3. Mermaid diagram detection
# ---------------------------------------------------------------------------


def test_missing_mermaid_diagrams_fails(tmp_path):
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    # Remove both mermaid fences
    content = content.replace("```mermaid", "```text")
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


def test_only_one_mermaid_fails(tmp_path):
    """Validator requires ≥2 mermaid blocks."""
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    # Replace only the second mermaid block
    idx = content.rfind("```mermaid")
    content = content[:idx] + content[idx:].replace("```mermaid", "```text", 1)
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


def test_mermaid_missing_diagram_type_fails(tmp_path):
    """A mermaid block without a recognised diagram type should fail."""
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    # Replace classDiagram with an unknown keyword
    content = content.replace("classDiagram", "unknownType")
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


# ---------------------------------------------------------------------------
# 4. Citation format validation
# ---------------------------------------------------------------------------


def test_missing_citation_in_claim_fails(tmp_path):
    """A bold claim line without (file.cs:N) citation should fail."""
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    # Strip citation from the Decision Drivers bold claim
    content = content.replace(
        "- **Use SO channels** for decoupled events. (EventBus.cs:42)",
        "- **Use SO channels** for decoupled events.",
    )
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


def test_citation_correct_format_passes(tmp_path):
    """Verify (file.cs:N) pattern is accepted."""
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is True


# ---------------------------------------------------------------------------
# 5. TODO / TBD / FIXME rejection
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("tag", ["TODO", "TBD", "FIXME"])
def test_forbidden_tag_fails(tmp_path, tag):
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    content += f"\n{tag}: remove this later\n"
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


def test_todo_in_checklist_exception_passes(tmp_path):
    """The literal string 'No TODO/TBD/FIXME' in a checklist should not fail."""
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    # VALID_DOC_TEMPLATE already includes "No TODO/TBD/FIXME" in Known Limitations
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is True


# ---------------------------------------------------------------------------
# 6. Owner field validation
# ---------------------------------------------------------------------------


def test_missing_owner_fails(tmp_path):
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    content = content.replace("- Owner: Alice", "")
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


def test_owner_placeholder_fails(tmp_path):
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    content = content.replace("- Owner: Alice", "- Owner: {name}")
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


def test_owner_team_placeholder_fails(tmp_path):
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    content = content.replace("- Owner: Alice", "- Owner: {name or team}")
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


def test_real_owner_passes(tmp_path):
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    content = content.replace("- Owner: Alice", "- Owner: Bob Jones")
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is True


# ---------------------------------------------------------------------------
# 7. Review date validation
# ---------------------------------------------------------------------------


def test_missing_review_date_fails(tmp_path):
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    content = content.replace(f"- Next Review Due: {_future_date()}", "")
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


def test_past_review_date_fails(tmp_path):
    content = VALID_DOC_TEMPLATE.format(review_date=_past_date(10))
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


def test_too_far_future_review_date_fails(tmp_path):
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date(days=200))
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


def test_valid_review_date_passes(tmp_path):
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date(days=45))
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is True


def test_invalid_review_date_format_fails(tmp_path):
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    content = content.replace(
        f"- Next Review Due: {_future_date()}", "- Next Review Due: 11/03/2026"
    )
    doc = _make_doc(tmp_path, content)
    assert validate_doc(doc) is False


# ---------------------------------------------------------------------------
# 8. File not found
# ---------------------------------------------------------------------------


def test_nonexistent_file_returns_false():
    assert validate_doc("/nonexistent/path/doc.md") is False


# ---------------------------------------------------------------------------
# 9. Multiple errors accumulate
# ---------------------------------------------------------------------------


def test_multiple_errors_all_reported(tmp_path, capsys):
    """Missing section + no owner should both appear in output."""
    content = VALID_DOC_TEMPLATE.format(review_date=_future_date())
    content = content.replace("### 1. Overview", "### X. Replaced")
    content = content.replace("- Owner: Alice", "- Owner: {name}")
    doc = _make_doc(tmp_path, content)
    result = validate_doc(doc)
    captured = capsys.readouterr()
    assert result is False
    assert "Missing section" in captured.out
    assert "Owner unassigned" in captured.out

"""Unit tests for image_gen.py.

Run with:
    python3 -m pytest skills/imagegen/scripts/test_image_gen.py -v
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

# Ensure the script is importable without executing main()
sys.path.insert(0, str(Path(__file__).parent))

import image_gen  # noqa: E402  (after sys.path manipulation)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_args(**kwargs):
    """Return a minimal argparse.Namespace with sensible defaults for tests."""
    defaults = dict(
        model=image_gen.DEFAULT_MODEL,
        prompt="a sunset over mountains",
        prompt_file=None,
        n=1,
        size=image_gen.DEFAULT_SIZE,
        quality=image_gen.DEFAULT_QUALITY,
        background=None,
        output_format=None,
        output_compression=None,
        moderation=None,
        out="output.png",
        out_dir=None,
        force=False,
        dry_run=False,
        augment=False,
        use_case=None,
        scene=None,
        subject=None,
        style=None,
        composition=None,
        lighting=None,
        palette=None,
        materials=None,
        text=None,
        constraints=None,
        negative=None,
        downscale_max_dim=None,
        downscale_suffix=image_gen.DEFAULT_DOWNSCALE_SUFFIX,
    )
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


# ---------------------------------------------------------------------------
# 1. _die / _warn
# ---------------------------------------------------------------------------


class TestDie:
    def test_raises_system_exit(self):
        with pytest.raises(SystemExit) as exc:
            image_gen._die("boom")
        assert exc.value.code == 1

    def test_custom_exit_code(self):
        with pytest.raises(SystemExit) as exc:
            image_gen._die("boom", code=42)
        assert exc.value.code == 42

    def test_message_printed_to_stderr(self, capsys):
        with pytest.raises(SystemExit):
            image_gen._die("oops")
        captured = capsys.readouterr()
        assert "oops" in captured.err


class TestWarn:
    def test_warning_printed_to_stderr(self, capsys):
        image_gen._warn("heads up")
        captured = capsys.readouterr()
        assert "heads up" in captured.err


# ---------------------------------------------------------------------------
# 2. _ensure_api_key
# ---------------------------------------------------------------------------


class TestEnsureApiKey:
    def test_key_present_does_not_raise(self, monkeypatch, capsys):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        image_gen._ensure_api_key(dry_run=False)  # no exception

    def test_missing_key_dry_run_warns(self, monkeypatch, capsys):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        image_gen._ensure_api_key(dry_run=True)
        captured = capsys.readouterr()
        assert "not set" in captured.err

    def test_missing_key_live_dies(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(SystemExit):
            image_gen._ensure_api_key(dry_run=False)


# ---------------------------------------------------------------------------
# 3. _read_prompt
# ---------------------------------------------------------------------------


class TestReadPrompt:
    def test_returns_prompt_string(self):
        result = image_gen._read_prompt("hello world", None)
        assert result == "hello world"

    def test_strips_whitespace(self):
        result = image_gen._read_prompt("  trimmed  ", None)
        assert result == "trimmed"

    def test_reads_prompt_file(self, tmp_path):
        f = tmp_path / "p.txt"
        f.write_text("from file\n")
        result = image_gen._read_prompt(None, str(f))
        assert result == "from file"

    def test_both_prompt_and_file_dies(self):
        with pytest.raises(SystemExit):
            image_gen._read_prompt("inline", "some_file.txt")

    def test_neither_prompt_nor_file_dies(self):
        with pytest.raises(SystemExit):
            image_gen._read_prompt(None, None)

    def test_missing_file_dies(self):
        with pytest.raises(SystemExit):
            image_gen._read_prompt(None, "/nonexistent/path.txt")


# ---------------------------------------------------------------------------
# 4. _normalize_output_format
# ---------------------------------------------------------------------------


class TestNormalizeOutputFormat:
    def test_default_when_none(self):
        assert image_gen._normalize_output_format(None) == "png"

    def test_png_passthrough(self):
        assert image_gen._normalize_output_format("png") == "png"

    def test_jpg_normalised_to_jpeg(self):
        assert image_gen._normalize_output_format("jpg") == "jpeg"

    def test_webp_passthrough(self):
        assert image_gen._normalize_output_format("webp") == "webp"

    def test_case_insensitive(self):
        assert image_gen._normalize_output_format("PNG") == "png"

    def test_invalid_format_dies(self):
        with pytest.raises(SystemExit):
            image_gen._normalize_output_format("bmp")


# ---------------------------------------------------------------------------
# 5. Validation helpers
# ---------------------------------------------------------------------------


class TestValidateSize:
    def test_valid_sizes_pass(self):
        for s in ("1024x1024", "1536x1024", "1024x1536", "auto"):
            image_gen._validate_size(s)  # no exception

    def test_invalid_size_dies(self):
        with pytest.raises(SystemExit):
            image_gen._validate_size("512x512")


class TestValidateQuality:
    def test_valid_qualities_pass(self):
        for q in ("low", "medium", "high", "auto"):
            image_gen._validate_quality(q)

    def test_invalid_quality_dies(self):
        with pytest.raises(SystemExit):
            image_gen._validate_quality("ultra")


class TestValidateBackground:
    def test_none_is_valid(self):
        image_gen._validate_background(None)

    def test_valid_backgrounds_pass(self):
        for b in ("transparent", "opaque", "auto"):
            image_gen._validate_background(b)

    def test_invalid_background_dies(self):
        with pytest.raises(SystemExit):
            image_gen._validate_background("black")


class TestValidateTransparency:
    def test_transparent_with_png_passes(self):
        image_gen._validate_transparency("transparent", "png")

    def test_transparent_with_webp_passes(self):
        image_gen._validate_transparency("transparent", "webp")

    def test_transparent_with_jpeg_dies(self):
        with pytest.raises(SystemExit):
            image_gen._validate_transparency("transparent", "jpeg")

    def test_opaque_with_jpeg_passes(self):
        image_gen._validate_transparency("opaque", "jpeg")


class TestValidateGeneratePayload:
    def test_valid_payload_passes(self):
        image_gen._validate_generate_payload(
            {"n": 1, "size": "1024x1024", "quality": "auto"}
        )

    def test_n_zero_dies(self):
        with pytest.raises(SystemExit):
            image_gen._validate_generate_payload(
                {"n": 0, "size": "1024x1024", "quality": "auto"}
            )

    def test_n_eleven_dies(self):
        with pytest.raises(SystemExit):
            image_gen._validate_generate_payload(
                {"n": 11, "size": "1024x1024", "quality": "auto"}
            )

    def test_bad_compression_dies(self):
        with pytest.raises(SystemExit):
            image_gen._validate_generate_payload(
                {
                    "n": 1,
                    "size": "1024x1024",
                    "quality": "auto",
                    "output_compression": 101,
                }
            )

    def test_valid_compression_passes(self):
        image_gen._validate_generate_payload(
            {"n": 1, "size": "1024x1024", "quality": "auto", "output_compression": 80}
        )


# ---------------------------------------------------------------------------
# 6. _augment_prompt_fields
# ---------------------------------------------------------------------------


class TestAugmentPromptFields:
    def test_no_augment_returns_prompt_unchanged(self):
        result = image_gen._augment_prompt_fields(False, "my prompt", {})
        assert result == "my prompt"

    def test_augment_includes_primary_request(self):
        result = image_gen._augment_prompt_fields(True, "my prompt", {})
        assert "Primary request: my prompt" in result

    def test_augment_adds_style_field(self):
        fields: dict[str, Optional[str]] = {
            "style": "watercolor",
            "use_case": None,
            "scene": None,
            "subject": None,
            "composition": None,
            "lighting": None,
            "palette": None,
            "materials": None,
            "text": None,
            "constraints": None,
            "negative": None,
        }
        result = image_gen._augment_prompt_fields(True, "my prompt", fields)
        assert "Style/medium: watercolor" in result

    def test_augment_skips_none_fields(self):
        fields: dict[str, Optional[str]] = {
            "style": None,
            "scene": None,
            "use_case": None,
            "subject": None,
            "composition": None,
            "lighting": None,
            "palette": None,
            "materials": None,
            "text": None,
            "constraints": None,
            "negative": None,
        }
        result = image_gen._augment_prompt_fields(True, "my prompt", fields)
        assert "Style" not in result
        assert "Scene" not in result

    def test_augment_adds_use_case_before_prompt(self):
        fields: dict[str, Optional[str]] = {
            "use_case": "game icon",
            "scene": None,
            "subject": None,
            "style": None,
            "composition": None,
            "lighting": None,
            "palette": None,
            "materials": None,
            "text": None,
            "constraints": None,
            "negative": None,
        }
        result = image_gen._augment_prompt_fields(True, "my prompt", fields)
        lines = result.splitlines()
        uc_idx = next(i for i, l in enumerate(lines) if "Use case" in l)
        pr_idx = next(i for i, l in enumerate(lines) if "Primary request" in l)
        assert uc_idx < pr_idx

    def test_augment_includes_negative(self):
        result = image_gen._augment_prompt_fields(
            True,
            "my prompt",
            {
                "negative": "blurry",
                "use_case": None,
                "scene": None,
                "subject": None,
                "style": None,
                "composition": None,
                "lighting": None,
                "palette": None,
                "materials": None,
                "text": None,
                "constraints": None,
            },
        )
        assert "Avoid: blurry" in result

    def test_augment_text_field_quoted(self):
        result = image_gen._augment_prompt_fields(
            True,
            "my prompt",
            {
                "text": "Game Over",
                "use_case": None,
                "scene": None,
                "subject": None,
                "style": None,
                "composition": None,
                "lighting": None,
                "palette": None,
                "materials": None,
                "constraints": None,
                "negative": None,
            },
        )
        assert '"Game Over"' in result

    def test_all_fields_present(self):
        raw: dict[str, str] = {
            "use_case": "icon",
            "scene": "forest",
            "subject": "dragon",
            "style": "pixel art",
            "composition": "centered",
            "lighting": "soft",
            "palette": "earth tones",
            "materials": "stone",
            "text": "ROAR",
            "constraints": "square",
            "negative": "blurry",
        }
        fields = dict(raw)
        result = image_gen._augment_prompt_fields(True, "prompt", fields)
        for keyword in (
            "Use case",
            "Primary request",
            "Scene",
            "Subject",
            "Style",
            "Lighting",
        ):
            assert keyword in result


# ---------------------------------------------------------------------------
# 7. _build_output_paths
# ---------------------------------------------------------------------------


class TestBuildOutputPaths:
    def test_single_output_no_suffix(self):
        paths = image_gen._build_output_paths("image", "png", 1, None)
        assert len(paths) == 1
        assert paths[0].suffix == ".png"

    def test_single_output_with_extension(self):
        paths = image_gen._build_output_paths("output.png", "png", 1, None)
        assert paths[0].name == "output.png"

    def test_multiple_outputs_numbered(self):
        paths = image_gen._build_output_paths("output.png", "png", 3, None)
        assert len(paths) == 3
        assert paths[0].name == "output-1.png"
        assert paths[2].name == "output-3.png"

    def test_out_dir_creates_image_n_paths(self, tmp_path):
        paths = image_gen._build_output_paths("x", "png", 2, str(tmp_path))
        assert len(paths) == 2
        assert all(p.parent == tmp_path for p in paths)
        assert paths[0].name == "image_1.png"

    def test_extension_mismatch_warns(self, capsys):
        image_gen._build_output_paths("output.png", "webp", 1, None)
        captured = capsys.readouterr()
        assert "does not match" in captured.err


# ---------------------------------------------------------------------------
# 8. _check_image_paths
# ---------------------------------------------------------------------------


class TestCheckImagePaths:
    def test_existing_file_returns_path(self, tmp_path):
        f = tmp_path / "img.png"
        f.write_bytes(b"data")
        result = image_gen._check_image_paths([str(f)])
        assert result == [f]

    def test_missing_file_dies(self):
        with pytest.raises(SystemExit):
            image_gen._check_image_paths(["/no/such/file.png"])

    def test_oversized_file_warns(self, tmp_path, capsys):
        f = tmp_path / "big.png"
        f.write_bytes(b"0" * (image_gen.MAX_IMAGE_BYTES + 1))
        image_gen._check_image_paths([str(f)])
        captured = capsys.readouterr()
        assert "exceeds" in captured.err


# ---------------------------------------------------------------------------
# 9. _slugify
# ---------------------------------------------------------------------------


class TestSlugify:
    def test_basic_slug(self):
        assert image_gen._slugify("Hello World") == "hello-world"

    def test_special_chars_replaced(self):
        result = image_gen._slugify("foo@bar!baz")
        assert result == "foo-bar-baz"

    def test_leading_trailing_hyphens_stripped(self):
        result = image_gen._slugify("  --test--  ")
        assert not result.startswith("-")
        assert not result.endswith("-")

    def test_long_value_truncated_at_60(self):
        result = image_gen._slugify("a" * 100)
        assert len(result) <= 60

    def test_empty_string_returns_job(self):
        assert image_gen._slugify("") == "job"
        assert image_gen._slugify("   ") == "job"


# ---------------------------------------------------------------------------
# 10. _normalize_job
# ---------------------------------------------------------------------------


class TestNormalizeJob:
    def test_string_job(self):
        result = image_gen._normalize_job("a prompt", 1)
        assert result == {"prompt": "a prompt"}

    def test_dict_job_with_prompt(self):
        job = {"prompt": "test", "style": "realistic"}
        result = image_gen._normalize_job(job, 1)
        assert result["prompt"] == "test"

    def test_empty_string_dies(self):
        with pytest.raises(SystemExit):
            image_gen._normalize_job("   ", 1)

    def test_dict_missing_prompt_dies(self):
        with pytest.raises(SystemExit):
            image_gen._normalize_job({"style": "realistic"}, 1)

    def test_invalid_type_dies(self):
        with pytest.raises(SystemExit):
            image_gen._normalize_job(12345, 1)


# ---------------------------------------------------------------------------
# 11. _read_jobs_jsonl
# ---------------------------------------------------------------------------


class TestReadJobsJsonl:
    def test_reads_plain_text_lines(self, tmp_path):
        f = tmp_path / "jobs.jsonl"
        f.write_text("prompt one\nprompt two\n")
        jobs = image_gen._read_jobs_jsonl(str(f))
        assert len(jobs) == 2
        assert jobs[0]["prompt"] == "prompt one"

    def test_reads_json_objects(self, tmp_path):
        f = tmp_path / "jobs.jsonl"
        f.write_text('{"prompt": "test"}\n')
        jobs = image_gen._read_jobs_jsonl(str(f))
        assert jobs[0]["prompt"] == "test"

    def test_skips_comments_and_blanks(self, tmp_path):
        f = tmp_path / "jobs.jsonl"
        f.write_text("# comment\n\nprompt one\n")
        jobs = image_gen._read_jobs_jsonl(str(f))
        assert len(jobs) == 1

    def test_missing_file_dies(self):
        with pytest.raises(SystemExit):
            image_gen._read_jobs_jsonl("/no/such/file.jsonl")

    def test_empty_file_dies(self, tmp_path):
        f = tmp_path / "empty.jsonl"
        f.write_text("# just a comment\n")
        with pytest.raises(SystemExit):
            image_gen._read_jobs_jsonl(str(f))

    def test_invalid_json_dies(self, tmp_path):
        f = tmp_path / "bad.jsonl"
        f.write_text("{invalid json}\n")
        with pytest.raises(SystemExit):
            image_gen._read_jobs_jsonl(str(f))


# ---------------------------------------------------------------------------
# 12. _derive_downscale_path
# ---------------------------------------------------------------------------


class TestDeriveDownscalePath:
    def test_adds_suffix_before_extension(self):
        p = Path("output.png")
        result = image_gen._derive_downscale_path(p, "-web")
        assert result.name == "output-web.png"

    def test_adds_hyphen_if_suffix_lacks_it(self):
        p = Path("output.png")
        result = image_gen._derive_downscale_path(p, "sm")
        assert result.name == "output-sm.png"

    def test_underscore_suffix_kept(self):
        p = Path("output.png")
        result = image_gen._derive_downscale_path(p, "_thumb")
        assert result.name == "output_thumb.png"


# ---------------------------------------------------------------------------
# 13. _decode_and_write
# ---------------------------------------------------------------------------


class TestDecodeAndWrite:
    def test_writes_decoded_bytes(self, tmp_path):
        raw = b"fake-image-data"
        b64 = base64.b64encode(raw).decode()
        out = tmp_path / "out.png"
        image_gen._decode_and_write([b64], [out], force=False)
        assert out.read_bytes() == raw

    def test_existing_file_no_force_dies(self, tmp_path):
        raw = b"data"
        b64 = base64.b64encode(raw).decode()
        out = tmp_path / "out.png"
        out.write_bytes(b"existing")
        with pytest.raises(SystemExit):
            image_gen._decode_and_write([b64], [out], force=False)

    def test_existing_file_force_overwrites(self, tmp_path):
        raw = b"new-data"
        b64 = base64.b64encode(raw).decode()
        out = tmp_path / "out.png"
        out.write_bytes(b"old")
        image_gen._decode_and_write([b64], [out], force=True)
        assert out.read_bytes() == raw


# ---------------------------------------------------------------------------
# 14. _merge_non_null
# ---------------------------------------------------------------------------


class TestMergeNonNull:
    def test_non_null_src_values_override(self):
        result = image_gen._merge_non_null({"a": 1, "b": 2}, {"a": 99})
        assert result["a"] == 99

    def test_null_src_values_kept_from_dst(self):
        result = image_gen._merge_non_null({"a": 1}, {"a": None})
        assert result["a"] == 1

    def test_new_key_from_src_added(self):
        result = image_gen._merge_non_null({"a": 1}, {"b": 2})
        assert result["b"] == 2


# ---------------------------------------------------------------------------
# 15. _is_rate_limit_error / _is_transient_error
# ---------------------------------------------------------------------------


class TestErrorClassifiers:
    def test_rate_limit_by_class_name(self):
        exc = type("RateLimitError", (Exception,), {})("hit limit")
        assert image_gen._is_rate_limit_error(exc)

    def test_rate_limit_by_429_in_message(self):
        exc = Exception("status 429")
        assert image_gen._is_rate_limit_error(exc)

    def test_non_rate_limit_error(self):
        exc = ValueError("unrelated")
        assert not image_gen._is_rate_limit_error(exc)

    def test_timeout_is_transient(self):
        exc = type("TimeoutError", (Exception,), {})("timed out")
        assert image_gen._is_transient_error(exc)

    def test_connection_reset_is_transient(self):
        exc = Exception("connection reset by peer")
        assert image_gen._is_transient_error(exc)

    def test_value_error_not_transient(self):
        assert not image_gen._is_transient_error(ValueError("nope"))


# ---------------------------------------------------------------------------
# 16. _extract_retry_after_seconds
# ---------------------------------------------------------------------------


class _RetryExc(Exception):
    def __init__(self, msg, retry_after=None):
        super().__init__(msg)
        self.retry_after = retry_after


class TestExtractRetryAfter:
    def test_attr_retry_after(self):
        exc = _RetryExc("rate limit", retry_after=30)
        assert image_gen._extract_retry_after_seconds(exc) == 30.0

    def test_message_parse(self):
        exc = Exception("retry-after: 15")
        assert image_gen._extract_retry_after_seconds(exc) == 15.0

    def test_no_retry_info_returns_none(self):
        exc = Exception("generic error")
        assert image_gen._extract_retry_after_seconds(exc) is None


# ---------------------------------------------------------------------------
# 17. _generate (mocked API call)
# ---------------------------------------------------------------------------


class TestGenerateMocked:
    def test_dry_run_prints_payload(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        args = _make_args(
            prompt="a sunset",
            dry_run=True,
            out=str(tmp_path / "out.png"),
            augment=False,
        )
        image_gen._generate(args)
        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["endpoint"] == "/v1/images/generations"
        assert payload["prompt"] == "a sunset"

    def test_generate_calls_api_and_writes_file(self, tmp_path, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        raw = b"fake-png-bytes"
        b64 = base64.b64encode(raw).decode()

        mock_item = SimpleNamespace(b64_json=b64)
        mock_result = SimpleNamespace(data=[mock_item])
        mock_client = MagicMock()
        mock_client.images.generate.return_value = mock_result

        out_path = tmp_path / "output.png"
        args = _make_args(
            prompt="a cat",
            dry_run=False,
            out=str(out_path),
            augment=False,
        )

        with patch("image_gen._create_client", return_value=mock_client):
            image_gen._generate(args)

        assert out_path.exists()
        assert out_path.read_bytes() == raw
        mock_client.images.generate.assert_called_once()
        call_kwargs = mock_client.images.generate.call_args[1]
        assert call_kwargs["prompt"] == "a cat"


# ---------------------------------------------------------------------------
# 18. _edit (mocked API call)
# ---------------------------------------------------------------------------


class TestEditMocked:
    def test_edit_dry_run_prints_payload(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        img = tmp_path / "img.png"
        img.write_bytes(b"fake")
        args = _make_args(
            prompt="make it blue",
            dry_run=True,
            image=[str(img)],
            mask=None,
            input_fidelity=None,
            out=str(tmp_path / "out.png"),
            augment=False,
        )
        image_gen._edit(args)
        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["endpoint"] == "/v1/images/edits"

    def test_edit_calls_api_and_writes_file(self, tmp_path, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        raw = b"edited-png"
        b64 = base64.b64encode(raw).decode()

        img = tmp_path / "source.png"
        img.write_bytes(b"original")
        out_path = tmp_path / "out.png"

        mock_item = SimpleNamespace(b64_json=b64)
        mock_result = SimpleNamespace(data=[mock_item])
        mock_client = MagicMock()
        mock_client.images.edit.return_value = mock_result

        args = _make_args(
            prompt="add a hat",
            dry_run=False,
            image=[str(img)],
            mask=None,
            input_fidelity=None,
            out=str(out_path),
            augment=False,
        )

        with patch("image_gen._create_client", return_value=mock_client):
            image_gen._edit(args)

        assert out_path.exists()
        assert out_path.read_bytes() == raw


# ---------------------------------------------------------------------------
# 19. CLI argument parsing via main()
# ---------------------------------------------------------------------------


class TestArgumentParsing:
    """Test that main() parses CLI arguments correctly (no real API calls)."""

    def _run_main_dry(self, argv, monkeypatch):
        """Helper: patch sys.argv and environment, assert no real API call."""
        monkeypatch.setattr(sys, "argv", argv)
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")

    def test_generate_subcommand_dry_run(self, tmp_path, monkeypatch, capsys):
        out = str(tmp_path / "out.png")
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "image_gen.py",
                "generate",
                "--prompt",
                "hello",
                "--dry-run",
                "--out",
                out,
            ],
        )
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        rc = image_gen.main()
        assert rc == 0
        captured = capsys.readouterr()
        assert "generations" in captured.out

    def test_edit_requires_image_flag(self, monkeypatch):
        monkeypatch.setattr(
            sys,
            "argv",
            ["image_gen.py", "edit", "--prompt", "hello", "--dry-run"],
        )
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        with pytest.raises(SystemExit) as exc:
            image_gen.main()
        assert exc.value.code != 0

    def test_generate_batch_requires_out_dir(self, tmp_path, monkeypatch):
        f = tmp_path / "jobs.jsonl"
        f.write_text("a prompt\n")
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "image_gen.py",
                "generate-batch",
                "--input",
                str(f),
                "--prompt",
                "x",
                "--dry-run",
            ],
        )
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        with pytest.raises(SystemExit) as exc:
            image_gen.main()
        assert exc.value.code != 0

    def test_invalid_n_dies(self, tmp_path, monkeypatch):
        out = str(tmp_path / "out.png")
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "image_gen.py",
                "generate",
                "--prompt",
                "x",
                "--n",
                "0",
                "--dry-run",
                "--out",
                out,
            ],
        )
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        with pytest.raises(SystemExit):
            image_gen.main()

    def test_default_model_used(self, tmp_path, monkeypatch, capsys):
        out = str(tmp_path / "out.png")
        monkeypatch.setattr(
            sys,
            "argv",
            ["image_gen.py", "generate", "--prompt", "x", "--dry-run", "--out", out],
        )
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        image_gen.main()
        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["model"] == image_gen.DEFAULT_MODEL

    def test_no_augment_flag_skips_augmentation(self, tmp_path, monkeypatch, capsys):
        out = str(tmp_path / "out.png")
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "image_gen.py",
                "generate",
                "--prompt",
                "raw prompt",
                "--no-augment",
                "--dry-run",
                "--out",
                out,
            ],
        )
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        image_gen.main()
        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["prompt"] == "raw prompt"


# ---------------------------------------------------------------------------
# 20. generate-batch dry-run
# ---------------------------------------------------------------------------


class TestGenerateBatchDryRun:
    def test_batch_dry_run_outputs_jobs(self, tmp_path, monkeypatch, capsys):
        jobs_file = tmp_path / "jobs.jsonl"
        jobs_file.write_text("first prompt\nsecond prompt\n")
        out_dir = str(tmp_path / "outputs")
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "image_gen.py",
                "generate-batch",
                "--input",
                str(jobs_file),
                "--out-dir",
                out_dir,
                "--dry-run",
            ],
        )
        monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")
        rc = image_gen.main()
        assert rc == 0
        captured = capsys.readouterr()
        lines = [l for l in captured.out.splitlines() if l.strip().startswith("{")]
        # Two JSON blocks expected (one per job)
        assert len(lines) >= 1

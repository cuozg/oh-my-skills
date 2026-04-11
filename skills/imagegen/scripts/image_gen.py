#!/usr/bin/env python3
"""Generate or edit images with the Google Gemini Imagen API.

Defaults to imagen-4.0-generate-001 and a structured prompt augmentation workflow.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any, Dict, Iterable, List, Optional, Tuple

from io import BytesIO

DEFAULT_MODEL_GENERATE = "imagen-4.0-generate-001"
DEFAULT_MODEL_EDIT = "imagen-3.0-capability-001"
DEFAULT_ASPECT_RATIO = "1:1"
DEFAULT_OUTPUT_FORMAT = "png"
DEFAULT_CONCURRENCY = 5
DEFAULT_DOWNSCALE_SUFFIX = "-web"

ALLOWED_ASPECT_RATIOS = {"1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"}

MAX_IMAGE_BYTES = 50 * 1024 * 1024
MAX_BATCH_JOBS = 500

# Deprecated --size mapping to --aspect-ratio
_SIZE_TO_ASPECT_RATIO = {
    "1024x1024": "1:1",
    "1536x1024": "3:2",
    "1024x1536": "2:3",
}


def _die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def _warn(message: str) -> None:
    print(f"Warning: {message}", file=sys.stderr)


def _ensure_api_key(dry_run: bool) -> None:
    if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
        key_name = "GEMINI_API_KEY" if os.getenv("GEMINI_API_KEY") else "GOOGLE_API_KEY"
        print(f"{key_name} is set.", file=sys.stderr)
        return
    if dry_run:
        _warn("GEMINI_API_KEY is not set; dry-run only.")
        return
    _die("GEMINI_API_KEY (or GOOGLE_API_KEY) is not set. Export it before running.")


def _read_prompt(prompt: Optional[str], prompt_file: Optional[str]) -> str:
    if prompt and prompt_file:
        _die("Use --prompt or --prompt-file, not both.")
    if prompt_file:
        path = Path(prompt_file)
        if not path.exists():
            _die(f"Prompt file not found: {path}")
        return path.read_text(encoding="utf-8").strip()
    if prompt:
        return prompt.strip()
    _die("Missing prompt. Use --prompt or --prompt-file.")
    return ""  # unreachable


def _check_image_paths(paths: Iterable[str]) -> List[Path]:
    resolved: List[Path] = []
    for raw in paths:
        path = Path(raw)
        if not path.exists():
            _die(f"Image file not found: {path}")
        if path.stat().st_size > MAX_IMAGE_BYTES:
            _warn(f"Image exceeds 50MB limit: {path}")
        resolved.append(path)
    return resolved


def _normalize_output_format(fmt: Optional[str]) -> str:
    if not fmt:
        return DEFAULT_OUTPUT_FORMAT
    fmt = fmt.lower()
    if fmt not in {"png", "jpeg", "jpg", "webp"}:
        _die("output-format must be png, jpeg, jpg, or webp.")
    return "jpeg" if fmt == "jpg" else fmt


def _validate_aspect_ratio(ratio: str) -> None:
    if ratio not in ALLOWED_ASPECT_RATIOS:
        _die(f"aspect-ratio must be one of {', '.join(sorted(ALLOWED_ASPECT_RATIOS))}.")


def _validate_generate_payload(payload: Dict[str, Any]) -> None:
    n = int(payload.get("number_of_images", 1))
    if n < 1 or n > 4:
        _die("n must be between 1 and 4")
    ratio = payload.get("aspect_ratio")
    if ratio:
        _validate_aspect_ratio(ratio)


def _build_output_paths(
    out: str,
    output_format: str,
    count: int,
    out_dir: Optional[str],
) -> List[Path]:
    ext = "." + output_format

    if out_dir:
        out_base = Path(out_dir)
        out_base.mkdir(parents=True, exist_ok=True)
        return [out_base / f"image_{i}{ext}" for i in range(1, count + 1)]

    out_path = Path(out)
    if out_path.exists() and out_path.is_dir():
        out_path.mkdir(parents=True, exist_ok=True)
        return [out_path / f"image_{i}{ext}" for i in range(1, count + 1)]

    if out_path.suffix == "":
        out_path = out_path.with_suffix(ext)
    elif output_format and out_path.suffix.lstrip(".").lower() != output_format:
        _warn(
            f"Output extension {out_path.suffix} does not match output-format {output_format}."
        )

    if count == 1:
        return [out_path]

    return [
        out_path.with_name(f"{out_path.stem}-{i}{out_path.suffix}")
        for i in range(1, count + 1)
    ]


def _augment_prompt(args: argparse.Namespace, prompt: str) -> str:
    fields = _fields_from_args(args)
    return _augment_prompt_fields(args.augment, prompt, fields)


def _augment_prompt_fields(
    augment: bool, prompt: str, fields: Dict[str, Optional[str]]
) -> str:
    if not augment:
        return prompt

    sections: List[str] = []
    if fields.get("use_case"):
        sections.append(f"Use case: {fields['use_case']}")
    sections.append(f"Primary request: {prompt}")
    if fields.get("scene"):
        sections.append(f"Scene/background: {fields['scene']}")
    if fields.get("subject"):
        sections.append(f"Subject: {fields['subject']}")
    if fields.get("style"):
        sections.append(f"Style/medium: {fields['style']}")
    if fields.get("composition"):
        sections.append(f"Composition/framing: {fields['composition']}")
    if fields.get("lighting"):
        sections.append(f"Lighting/mood: {fields['lighting']}")
    if fields.get("palette"):
        sections.append(f"Color palette: {fields['palette']}")
    if fields.get("materials"):
        sections.append(f"Materials/textures: {fields['materials']}")
    if fields.get("text"):
        sections.append(f'Text (verbatim): "{fields["text"]}"')
    if fields.get("constraints"):
        sections.append(f"Constraints: {fields['constraints']}")
    if fields.get("negative"):
        sections.append(f"Avoid: {fields['negative']}")

    return "\n".join(sections)


def _fields_from_args(args: argparse.Namespace) -> Dict[str, Optional[str]]:
    return {
        "use_case": getattr(args, "use_case", None),
        "scene": getattr(args, "scene", None),
        "subject": getattr(args, "subject", None),
        "style": getattr(args, "style", None),
        "composition": getattr(args, "composition", None),
        "lighting": getattr(args, "lighting", None),
        "palette": getattr(args, "palette", None),
        "materials": getattr(args, "materials", None),
        "text": getattr(args, "text", None),
        "constraints": getattr(args, "constraints", None),
        "negative": getattr(args, "negative", None),
    }


def _print_request(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _write_images(images: List[bytes], outputs: List[Path], force: bool) -> None:
    for idx, image_bytes in enumerate(images):
        if idx >= len(outputs):
            break
        out_path = outputs[idx]
        if out_path.exists() and not force:
            _die(f"Output already exists: {out_path} (use --force to overwrite)")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(image_bytes)
        print(f"Wrote {out_path}")


def _derive_downscale_path(path: Path, suffix: str) -> Path:
    if suffix and not suffix.startswith("-") and not suffix.startswith("_"):
        suffix = "-" + suffix
    return path.with_name(f"{path.stem}{suffix}{path.suffix}")


def _downscale_image_bytes(
    image_bytes: bytes, *, max_dim: int, output_format: str
) -> bytes:
    try:
        from PIL import Image
    except Exception:
        _die(
            "Downscaling requires Pillow. Install with `uv pip install pillow` (then re-run)."
        )

    if max_dim < 1:
        _die("--downscale-max-dim must be >= 1")

    with Image.open(BytesIO(image_bytes)) as img:
        img.load()
        w, h = img.size
        scale = min(1.0, float(max_dim) / float(max(w, h)))
        target = (max(1, int(round(w * scale))), max(1, int(round(h * scale))))

        resized = (
            img if target == (w, h) else img.resize(target, Image.Resampling.LANCZOS)
        )

        fmt = output_format.lower()
        if fmt == "jpg":
            fmt = "jpeg"

        if fmt == "jpeg":
            if resized.mode in ("RGBA", "LA") or (
                "transparency" in getattr(resized, "info", {})
            ):
                bg = Image.new("RGB", resized.size, (255, 255, 255))
                bg.paste(
                    resized.convert("RGBA"), mask=resized.convert("RGBA").split()[-1]
                )
                resized = bg
            else:
                resized = resized.convert("RGB")

        out = BytesIO()
        resized.save(out, format=fmt.upper())
        return out.getvalue()


def _write_and_downscale(
    images: List[bytes],
    outputs: List[Path],
    *,
    force: bool,
    downscale_max_dim: Optional[int],
    downscale_suffix: str,
    output_format: str,
) -> None:
    for idx, image_bytes in enumerate(images):
        if idx >= len(outputs):
            break
        out_path = outputs[idx]
        if out_path.exists() and not force:
            _die(f"Output already exists: {out_path} (use --force to overwrite)")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        out_path.write_bytes(image_bytes)
        print(f"Wrote {out_path}")

        if downscale_max_dim is None:
            continue

        derived = _derive_downscale_path(out_path, downscale_suffix)
        if derived.exists() and not force:
            _die(f"Output already exists: {derived} (use --force to overwrite)")
        derived.parent.mkdir(parents=True, exist_ok=True)
        resized = _downscale_image_bytes(
            image_bytes, max_dim=downscale_max_dim, output_format=output_format
        )
        derived.write_bytes(resized)
        print(f"Wrote {derived}")


def _create_client():
    try:
        from google import genai
    except ImportError:
        _die(
            "google-genai SDK not installed. Install with `uv pip install google-genai`."
        )
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    return genai.Client()


def _create_async_client():
    return _create_client()


def _slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value[:60] if value else "job"


def _normalize_job(job: Any, idx: int) -> Dict[str, Any]:
    if isinstance(job, str):
        prompt = job.strip()
        if not prompt:
            _die(f"Empty prompt at job {idx}")
        return {"prompt": prompt}
    if isinstance(job, dict):
        if "prompt" not in job or not str(job["prompt"]).strip():
            _die(f"Missing prompt for job {idx}")
        return job
    _die(f"Invalid job at index {idx}: expected string or object.")
    return {}  # unreachable


def _read_jobs_jsonl(path: str) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        _die(f"Input file not found: {p}")
    jobs: List[Dict[str, Any]] = []
    for line_no, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            item: Any
            if line.startswith("{"):
                item = json.loads(line)
            else:
                item = line
            jobs.append(_normalize_job(item, idx=line_no))
        except json.JSONDecodeError as exc:
            _die(f"Invalid JSON on line {line_no}: {exc}")
    if not jobs:
        _die("No jobs found in input file.")
    if len(jobs) > MAX_BATCH_JOBS:
        _die(f"Too many jobs ({len(jobs)}). Max is {MAX_BATCH_JOBS}.")
    return jobs


def _merge_non_null(dst: Dict[str, Any], src: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(dst)
    for k, v in src.items():
        if v is not None:
            merged[k] = v
    return merged


def _job_output_paths(
    *,
    out_dir: Path,
    output_format: str,
    idx: int,
    prompt: str,
    n: int,
    explicit_out: Optional[str],
) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = "." + output_format

    if explicit_out:
        base = Path(explicit_out)
        if base.suffix == "":
            base = base.with_suffix(ext)
        elif base.suffix.lstrip(".").lower() != output_format:
            _warn(
                f"Job {idx}: output extension {base.suffix} does not match output-format {output_format}."
            )
        base = out_dir / base.name
    else:
        slug = _slugify(prompt[:80])
        base = out_dir / f"{idx:03d}-{slug}{ext}"

    if n == 1:
        return [base]
    return [base.with_name(f"{base.stem}-{i}{base.suffix}") for i in range(1, n + 1)]


def _extract_retry_after_seconds(exc: Exception) -> Optional[float]:
    for attr in ("retry_after", "retry_after_seconds"):
        val = getattr(exc, attr, None)
        if isinstance(val, (int, float)) and val >= 0:
            return float(val)
    msg = str(exc)
    m = re.search(r"retry[- ]after[:= ]+([0-9]+(?:\\.[0-9]+)?)", msg, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1))
        except Exception:
            return None
    return None


def _is_rate_limit_error(exc: Exception) -> bool:
    name = exc.__class__.__name__.lower()
    if "ratelimit" in name or "rate_limit" in name:
        return True
    msg = str(exc).lower()
    return "429" in msg or "rate limit" in msg or "too many requests" in msg


def _is_transient_error(exc: Exception) -> bool:
    if _is_rate_limit_error(exc):
        return True
    name = exc.__class__.__name__.lower()
    if "timeout" in name or "timedout" in name or "tempor" in name:
        return True
    msg = str(exc).lower()
    return "timeout" in msg or "timed out" in msg or "connection reset" in msg


async def _generate_one_with_retries(
    client: Any,
    *,
    model: str,
    prompt: str,
    config: Any,
    attempts: int,
    job_label: str,
) -> Any:
    last_exc: Optional[Exception] = None
    for attempt in range(1, attempts + 1):
        try:
            return await client.aio.models.generate_images(
                model=model,
                prompt=prompt,
                config=config,
            )
        except Exception as exc:
            last_exc = exc
            if not _is_transient_error(exc):
                raise
            if attempt == attempts:
                raise
            sleep_s = _extract_retry_after_seconds(exc)
            if sleep_s is None:
                sleep_s = min(60.0, 2.0**attempt)
            print(
                f"{job_label} attempt {attempt}/{attempts} failed ({exc.__class__.__name__}); retrying in {sleep_s:.1f}s",
                file=sys.stderr,
            )
            await asyncio.sleep(sleep_s)
    raise last_exc or RuntimeError("unknown error")


async def _run_generate_batch(args: argparse.Namespace) -> int:
    jobs = _read_jobs_jsonl(args.input)
    out_dir = Path(args.out_dir)

    base_fields = _fields_from_args(args)
    base_config = {
        "number_of_images": args.n,
        "aspect_ratio": args.aspect_ratio,
    }
    if args.negative_prompt:
        base_config["negative_prompt"] = args.negative_prompt
    if args.person_generation:
        base_config["person_generation"] = args.person_generation
    if args.safety_filter_level:
        base_config["safety_filter_level"] = args.safety_filter_level

    if args.dry_run:
        for i, job in enumerate(jobs, start=1):
            prompt = str(job["prompt"]).strip()
            fields = _merge_non_null(base_fields, job.get("fields", {}))
            fields = _merge_non_null(
                fields, {k: job.get(k) for k in base_fields.keys()}
            )
            augmented = _augment_prompt_fields(args.augment, prompt, fields)

            job_config = dict(base_config)
            # Allow per-job overrides for config keys
            for k in list(base_config.keys()):
                if k in job and job[k] is not None:
                    job_config[k] = job[k]
            # Allow per-job n override
            if "n" in job:
                job_config["number_of_images"] = int(job["n"])

            _validate_generate_payload(job_config)
            effective_output_format = _normalize_output_format(
                job.get("output_format") or args.output_format
            )

            n = int(job_config.get("number_of_images", 1))
            outputs = _job_output_paths(
                out_dir=out_dir,
                output_format=effective_output_format,
                idx=i,
                prompt=prompt,
                n=n,
                explicit_out=job.get("out"),
            )
            downscaled = None
            if args.downscale_max_dim is not None:
                downscaled = [
                    str(_derive_downscale_path(p, args.downscale_suffix))
                    for p in outputs
                ]
            _print_request(
                {
                    "endpoint": "models.generate_images",
                    "job": i,
                    "model": job.get("model", args.model),
                    "prompt": augmented,
                    "config": job_config,
                    "outputs": [str(p) for p in outputs],
                    "outputs_downscaled": downscaled,
                }
            )
        return 0

    from google.genai.types import GenerateImagesConfig

    client = _create_async_client()
    sem = asyncio.Semaphore(args.concurrency)

    any_failed = False

    async def run_job(i: int, job: Dict[str, Any]) -> Tuple[int, Optional[str]]:
        nonlocal any_failed
        prompt = str(job["prompt"]).strip()
        job_label = f"[job {i}/{len(jobs)}]"

        fields = _merge_non_null(base_fields, job.get("fields", {}))
        fields = _merge_non_null(fields, {k: job.get(k) for k in base_fields.keys()})
        augmented = _augment_prompt_fields(args.augment, prompt, fields)

        job_config = dict(base_config)
        for k in list(base_config.keys()):
            if k in job and job[k] is not None:
                job_config[k] = job[k]
        if "n" in job:
            job_config["number_of_images"] = int(job["n"])

        _validate_generate_payload(job_config)
        effective_output_format = _normalize_output_format(
            job.get("output_format") or args.output_format
        )

        n = int(job_config.get("number_of_images", 1))
        job_model = job.get("model", args.model)

        outputs = _job_output_paths(
            out_dir=out_dir,
            output_format=effective_output_format,
            idx=i,
            prompt=prompt,
            n=n,
            explicit_out=job.get("out"),
        )
        try:
            async with sem:
                print(f"{job_label} starting", file=sys.stderr)
                started = time.time()
                result = await _generate_one_with_retries(
                    client,
                    model=job_model,
                    prompt=augmented,
                    config=GenerateImagesConfig(**job_config),
                    attempts=args.max_attempts,
                    job_label=job_label,
                )
                elapsed = time.time() - started
                print(f"{job_label} completed in {elapsed:.1f}s", file=sys.stderr)
            images = [img.image.image_bytes for img in result.generated_images]
            _write_and_downscale(
                images,
                outputs,
                force=args.force,
                downscale_max_dim=args.downscale_max_dim,
                downscale_suffix=args.downscale_suffix,
                output_format=effective_output_format,
            )
            return i, None
        except Exception as exc:
            any_failed = True
            print(f"{job_label} failed: {exc}", file=sys.stderr)
            if args.fail_fast:
                raise
            return i, str(exc)

    tasks = [
        asyncio.create_task(run_job(i, job)) for i, job in enumerate(jobs, start=1)
    ]

    try:
        await asyncio.gather(*tasks)
    except Exception:
        for t in tasks:
            if not t.done():
                t.cancel()
        raise

    return 1 if any_failed else 0


def _generate_batch(args: argparse.Namespace) -> None:
    exit_code = asyncio.run(_run_generate_batch(args))
    if exit_code:
        raise SystemExit(exit_code)


def _generate(args: argparse.Namespace) -> None:
    prompt = _read_prompt(args.prompt, args.prompt_file)
    prompt = _augment_prompt(args, prompt)

    config_kwargs = {
        "number_of_images": args.n,
        "aspect_ratio": args.aspect_ratio,
    }
    if args.negative_prompt:
        config_kwargs["negative_prompt"] = args.negative_prompt
    if args.person_generation:
        config_kwargs["person_generation"] = args.person_generation
    if args.safety_filter_level:
        config_kwargs["safety_filter_level"] = args.safety_filter_level

    payload = {
        "model": args.model,
        "prompt": prompt,
        "config": config_kwargs,
    }

    output_format = _normalize_output_format(args.output_format)
    output_paths = _build_output_paths(args.out, output_format, args.n, args.out_dir)

    if args.dry_run:
        _print_request({"endpoint": "models.generate_images", **payload})
        return

    print(
        "Calling Imagen API (generation). This can take up to a couple of minutes.",
        file=sys.stderr,
    )
    started = time.time()

    from google.genai.types import GenerateImagesConfig

    client = _create_client()
    result = client.models.generate_images(
        model=args.model,
        prompt=prompt,
        config=GenerateImagesConfig(**config_kwargs),
    )
    elapsed = time.time() - started
    print(f"Generation completed in {elapsed:.1f}s.", file=sys.stderr)

    images = [img.image.image_bytes for img in result.generated_images]
    _write_and_downscale(
        images,
        output_paths,
        force=args.force,
        downscale_max_dim=args.downscale_max_dim,
        downscale_suffix=args.downscale_suffix,
        output_format=output_format,
    )


def _edit(args: argparse.Namespace) -> None:
    prompt = _read_prompt(args.prompt, args.prompt_file)
    prompt = _augment_prompt(args, prompt)

    image_paths = _check_image_paths(args.image)
    mask_path = Path(args.mask) if args.mask else None
    if mask_path:
        if not mask_path.exists():
            _die(f"Mask file not found: {mask_path}")
        if mask_path.suffix.lower() != ".png":
            _warn(f"Mask should be a PNG with an alpha channel: {mask_path}")
        if mask_path.stat().st_size > MAX_IMAGE_BYTES:
            _warn(f"Mask exceeds 50MB limit: {mask_path}")

    config_kwargs = {
        "number_of_images": args.n,
    }
    if args.negative_prompt:
        config_kwargs["negative_prompt"] = args.negative_prompt
    if args.person_generation:
        config_kwargs["person_generation"] = args.person_generation
    if args.safety_filter_level:
        config_kwargs["safety_filter_level"] = args.safety_filter_level

    output_format = _normalize_output_format(args.output_format)
    output_paths = _build_output_paths(args.out, output_format, args.n, args.out_dir)

    if args.dry_run:
        payload_preview = {
            "endpoint": "models.edit_image",
            "model": args.model,
            "prompt": prompt,
            "reference_images": [str(p) for p in image_paths],
        }
        if mask_path:
            payload_preview["mask"] = str(mask_path)
        payload_preview["config"] = config_kwargs
        _print_request(payload_preview)
        return

    print(
        f"Calling Imagen API (edit) with {len(image_paths)} image(s).", file=sys.stderr
    )
    started = time.time()

    from google.genai.types import (
        RawReferenceImage,
        MaskReferenceImage,
        MaskReferenceConfig,
        EditImageConfig,
        Image,
    )

    client = _create_client()

    reference_images = []
    for idx, img_path in enumerate(image_paths):
        reference_images.append(
            RawReferenceImage(
                reference_image=Image.from_file(location=str(img_path)),
                reference_id=idx,
            )
        )
    if mask_path:
        reference_images.append(
            MaskReferenceImage(
                reference_image=Image.from_file(location=str(mask_path)),
                reference_id=0,
                config=MaskReferenceConfig(mask_mode="MASK_MODE_USER_PROVIDED"),
            )
        )

    result = client.models.edit_image(
        model=args.model,
        prompt=prompt,
        reference_images=reference_images,
        config=EditImageConfig(**config_kwargs),
    )

    elapsed = time.time() - started
    print(f"Edit completed in {elapsed:.1f}s.", file=sys.stderr)
    images = [img.image.image_bytes for img in result.generated_images]
    _write_and_downscale(
        images,
        output_paths,
        force=args.force,
        downscale_max_dim=args.downscale_max_dim,
        downscale_suffix=args.downscale_suffix,
        output_format=output_format,
    )


def _handle_size_deprecation(args: argparse.Namespace) -> None:
    size = getattr(args, "size", None)
    if size is None:
        return
    _warn(
        f"--size is deprecated and will be removed in a future version. "
        f"Use --aspect-ratio instead."
    )
    if size == "auto":
        # 'auto' means don't set aspect_ratio — leave the default
        return
    mapped = _SIZE_TO_ASPECT_RATIO.get(size)
    if mapped:
        args.aspect_ratio = mapped
    else:
        _warn(f"Unknown --size value '{size}'; ignoring. Use --aspect-ratio directly.")


def _add_shared_args(parser: argparse.ArgumentParser, *, default_model: str) -> None:
    parser.add_argument("--model", default=default_model)
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--n", type=int, default=1)
    parser.add_argument("--aspect-ratio", default=DEFAULT_ASPECT_RATIO)
    parser.add_argument(
        "--size",
        default=None,
        help="[DEPRECATED] Use --aspect-ratio instead. Maps: 1024x1024→1:1, 1536x1024→3:2, 1024x1536→2:3",
    )
    parser.add_argument("--negative-prompt", default=None)
    parser.add_argument(
        "--person-generation",
        default=None,
        choices=["DONT_ALLOW", "ALLOW_ADULT"],
    )
    parser.add_argument(
        "--safety-filter-level",
        default=None,
        choices=[
            "BLOCK_LOW_AND_ABOVE",
            "BLOCK_MEDIUM_AND_ABOVE",
            "BLOCK_ONLY_HIGH",
            "BLOCK_NONE",
        ],
    )
    parser.add_argument("--output-format")
    parser.add_argument("--out", default="output.png")
    parser.add_argument("--out-dir")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--augment", dest="augment", action="store_true")
    parser.add_argument("--no-augment", dest="augment", action="store_false")
    parser.set_defaults(augment=True)

    # Prompt augmentation hints
    parser.add_argument("--use-case")
    parser.add_argument("--scene")
    parser.add_argument("--subject")
    parser.add_argument("--style")
    parser.add_argument("--composition")
    parser.add_argument("--lighting")
    parser.add_argument("--palette")
    parser.add_argument("--materials")
    parser.add_argument("--text")
    parser.add_argument("--constraints")
    parser.add_argument("--negative")

    # Post-processing (optional): generate an additional downscaled copy for fast web loading.
    parser.add_argument("--downscale-max-dim", type=int)
    parser.add_argument("--downscale-suffix", default=DEFAULT_DOWNSCALE_SUFFIX)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or edit images via the Gemini Imagen API"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_parser = subparsers.add_parser("generate", help="Create a new image")
    _add_shared_args(gen_parser, default_model=DEFAULT_MODEL_GENERATE)
    gen_parser.set_defaults(func=_generate)

    batch_parser = subparsers.add_parser(
        "generate-batch",
        help="Generate multiple prompts concurrently (JSONL input)",
    )
    _add_shared_args(batch_parser, default_model=DEFAULT_MODEL_GENERATE)
    batch_parser.add_argument(
        "--input", required=True, help="Path to JSONL file (one job per line)"
    )
    batch_parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    batch_parser.add_argument("--max-attempts", type=int, default=3)
    batch_parser.add_argument("--fail-fast", action="store_true")
    batch_parser.set_defaults(func=_generate_batch)

    edit_parser = subparsers.add_parser("edit", help="Edit an existing image")
    _add_shared_args(edit_parser, default_model=DEFAULT_MODEL_EDIT)
    edit_parser.add_argument("--image", action="append", required=True)
    edit_parser.add_argument("--mask")
    edit_parser.set_defaults(func=_edit)

    args = parser.parse_args()
    if args.n < 1 or args.n > 4:
        _die("--n must be between 1 and 4")
    if getattr(args, "concurrency", 1) < 1 or getattr(args, "concurrency", 1) > 25:
        _die("--concurrency must be between 1 and 25")
    if getattr(args, "max_attempts", 3) < 1 or getattr(args, "max_attempts", 3) > 10:
        _die("--max-attempts must be between 1 and 10")
    if args.command == "generate-batch" and not args.out_dir:
        _die("generate-batch requires --out-dir")
    if (
        getattr(args, "downscale_max_dim", None) is not None
        and args.downscale_max_dim < 1
    ):
        _die("--downscale-max-dim must be >= 1")

    if getattr(args, "size", None) is not None:
        _handle_size_deprecation(args)

    _validate_aspect_ratio(args.aspect_ratio)

    _ensure_api_key(args.dry_run)

    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

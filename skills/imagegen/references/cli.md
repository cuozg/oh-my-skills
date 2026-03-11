# CLI reference (`scripts/image_gen.py`)

Command catalog for the bundled image generation CLI. See `SKILL.md` for overview.

## What this CLI does
- `generate`: generate new images from a prompt
- `edit`: edit an existing image (optionally with a mask)
- `generate-batch`: run many jobs from a JSONL file

Real API calls require **network access** + `OPENAI_API_KEY`. `--dry-run` does not.

## Quick start
Set a stable path (default `CODEX_HOME` is `~/.codex`):

```bash
export IMAGE_GEN="~/.codex/skills/imagegen/scripts/image_gen.py"
```

Dry-run (no API call; no key required):
```bash
python "$IMAGE_GEN" generate --prompt "Test" --dry-run
```

Generate (requires `OPENAI_API_KEY` + network):
```bash
python "$IMAGE_GEN" generate --prompt "A cozy alpine cabin at dawn" --size 1024x1024
```

## Guardrails
- Use full path: `python "$IMAGE_GEN" ...` for all CLI runs.
- **Never modify** `scripts/image_gen.py`. Ask user if something is missing.
- **Never** create one-off runners unless explicitly requested.

## Defaults (override with flags)
- Model: `gpt-image-1.5`
- Size: `1024x1024`
- Quality: `auto`
- Output format: `png`

## Quality + input fidelity
- `--quality`: `low|medium|high|auto` (applies to generate/edit/batch)
- `--input-fidelity`: `low|high` (edit-only; use `high` for identity/layout lock)

Example:
```bash
python "$IMAGE_GEN" edit --image input.png --prompt "Change only the background" \
  --quality high --input-fidelity high
```

## Masks (edits)
- Use **PNG** mask with alpha channel (recommended)
- Mask must match input image dimensions
- In edit prompt, repeat invariants: "change only X; keep Y unchanged"

## Common recipes

Generate + downscale for web:
```bash
python "$IMAGE_GEN" generate \
  --prompt "A cozy alpine cabin" \
  --size 1024x1024 \
  --downscale-max-dim 1024
```

Batch (many prompts concurrently):
```bash
cat > tmp/imagegen/prompts.jsonl << 'EOF'
{"prompt":"Wolf in snowy forest","use_case":"wildlife","composition":"100mm, shallow DoF","size":"1024x1024"}
{"prompt":"Hangar interior with shuttle","use_case":"concept art","composition":"wide-angle, cinematic","size":"1536x1024"}
EOF

python "$IMAGE_GEN" generate-batch --input tmp/imagegen/prompts.jsonl --out-dir out --concurrency 5
rm tmp/imagegen/prompts.jsonl
```

Edit:
```bash
python "$IMAGE_GEN" edit --image input.png --mask mask.png \
  --prompt "Replace the background with a warm sunset"
```

## Notes
- Supported sizes: `1024x1024`, `1536x1024`, `1024x1536`, `auto`
- Transparent backgrounds require `output_format` png or webp
- Default output: `output.png`; multiple images → `output-1.png`, `output-2.png`, etc.
- Use `--no-augment` to skip prompt augmentation
- `--n` generates multiple variants for a single prompt
- Treat JSONL batch files as temporary (write under `tmp/`, delete after)

## See also
- Prompting principles: `references/prompting.md`
- Prompt augmentation: `references/prompt-augmentation.md`
- API parameters: `references/image-api.md`
- Prompt examples: `references/sample-prompts-*.md`

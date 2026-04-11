# CLI reference (`scripts/image_gen.py`)

Command catalog for the bundled image generation CLI. See `SKILL.md` for overview.

## What this CLI does
- `generate`: generate new images from a prompt
- `edit`: edit an existing image (optionally with a mask)
- `generate-batch`: run many jobs from a JSONL file

Real API calls require **network access** + `GEMINI_API_KEY`. `--dry-run` does not.

## API key lookup
The CLI automatically searches for API keys in `.env` files before falling back to OS environment variables. The search order is:
1. `--env-file <path>` (explicit override)
2. `<cwd>/.env.local`
3. `<cwd>/.env`
4. `~/.env.local`
5. `~/.env`

OS environment variables already set take precedence — `.env` files only fill in missing values.

```bash
# Explicit .env file:
python "$IMAGE_GEN" generate --prompt "Test" --env-file /path/to/.env

# Or just have a .env.local in your project root:
echo 'GEMINI_API_KEY=your-key-here' >> .env.local
python "$IMAGE_GEN" generate --prompt "Test"
```

## Quick start
Resolve the CLI path from the skill directory (do not hardcode):

```bash
# The script lives at scripts/image_gen.py relative to the imagegen skill directory.
# In OpenCode, use run_skill_script or resolve the path dynamically.
# Example with a variable:
export IMAGE_GEN="<path-to-imagegen-skill>/scripts/image_gen.py"
```

Dry-run (no API call; no key required):
```bash
python "$IMAGE_GEN" generate --prompt "Test" --dry-run
```

Generate (requires `GEMINI_API_KEY` + network):
```bash
python "$IMAGE_GEN" generate --prompt "A cozy alpine cabin at dawn" --aspect-ratio 1:1
```

## Guardrails
- Use full path: `python "$IMAGE_GEN" ...` for all CLI runs.
- Prefer the bundled CLI; only create one-off runners if explicitly requested.

## Defaults (override with flags)
- Model: `imagen-4.0-generate-001` (generate), `imagen-3.0-capability-001` (edit)
- Aspect ratio: `1:1`
- Output format: `png` (handled by CLI post-processing)

## Aspect ratio + generation options
- `--aspect-ratio`: `1:1|16:9|9:16|4:3|3:4` (applies to generate/batch)
- `--negative-prompt`: what to avoid in the image
- `--person-generation`: `DONT_ALLOW|ALLOW_ADULT`
- `--safety-filter-level`: `BLOCK_LOW_AND_ABOVE|BLOCK_MEDIUM_AND_ABOVE|BLOCK_ONLY_HIGH|BLOCK_NONE`

Example:
```bash
python "$IMAGE_GEN" edit --image input.png --prompt "Change only the background" \
  --negative-prompt "blurry, overexposed"
```

## Masks (edits)
- Use **PNG** mask with alpha channel (recommended)
- Mask must match input image dimensions
- Gemini uses `MaskReferenceImage` with `reference_id` to associate mask with input image
- In edit prompt, repeat invariants: "change only X; keep Y unchanged"

## Common recipes

Generate + downscale for web:
```bash
python "$IMAGE_GEN" generate \
  --prompt "A cozy alpine cabin" \
  --aspect-ratio 1:1 \
  --downscale-max-dim 1024
```

Batch (many prompts concurrently):
```bash
cat > tmp/imagegen/prompts.jsonl << 'EOF'
{"prompt":"Wolf in snowy forest","use_case":"wildlife","composition":"100mm, shallow DoF","aspect_ratio":"1:1"}
{"prompt":"Hangar interior with shuttle","use_case":"concept art","composition":"wide-angle, cinematic","aspect_ratio":"16:9"}
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
- Supported aspect ratios: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`
- **Edit operations require Vertex AI mode** — `GEMINI_API_KEY` alone is not sufficient for edits. Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` with ADC.
- Default output: `output.png`; multiple images → `output-1.png`, `output-2.png`, etc.
- Use `--no-augment` to skip prompt augmentation
- `--n` generates multiple variants for a single prompt
- Treat JSONL batch files as temporary (write under `tmp/`, delete after)

## See also
- Prompting principles: `references/prompting.md`
- Prompt augmentation: `references/prompt-augmentation.md`
- API parameters: `references/image-api.md`
- Prompt examples: `references/sample-prompts-*.md`

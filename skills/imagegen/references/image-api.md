# Image API quick reference

## Endpoints
- Generate: `client.models.generate_images(...)` (Imagen)
- Edit: `client.models.edit_image(...)` (Imagen)
- Generate (native): `client.models.generate_content(...)` with `response_modalities=[Modality.IMAGE]` (Gemini models)

## Models
- Generate: `imagen-4.0-generate-001` (default)
- Edit: `imagen-3.0-capability-001` (default)
- Native Gemini: `gemini-2.5-flash-image` (text+image mixed output)

## Core parameters (generate)
- `prompt`: text prompt
- `model`: image model
- `config`: `GenerateImagesConfig` object with:
  - `number_of_images`: 1-4 (how many images to generate)
  - `aspect_ratio`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`
  - `negative_prompt`: what to avoid in the image
  - `person_generation`: `DONT_ALLOW` or `ALLOW_ADULT`
  - `safety_filter_level`: `BLOCK_LOW_AND_ABOVE`, `BLOCK_MEDIUM_AND_ABOVE`, `BLOCK_ONLY_HIGH`, `BLOCK_NONE`
  - `image_size`: optional size hint (e.g. `"2K"`)

## Edit-specific parameters
- `reference_images`: list of reference image objects
  - `RawReferenceImage`: input image with `reference_id` and `reference_image`
  - `MaskReferenceImage`: mask with `reference_id`, `reference_image`, and `config`
- `config`: `EditImageConfig` object with:
  - `number_of_images`: 1-4

## Reference image types for edits
- `RawReferenceImage(reference_image=Image.from_file(location="input.png"), reference_id=0)`
- `MaskReferenceImage(reference_image=Image.from_file(location="mask.png"), reference_id=0, config=MaskReferenceConfig(mask_mode="MASK_MODE_USER_PROVIDED"))`

## Output
- `response.generated_images` — list of generated image objects
- `response.generated_images[i].image.image_bytes` — raw bytes of the image
- `response.generated_images[i].image.save("output.png")` — save directly to file

## Limits & notes
- Imagen 4 is generate-only; edits use Imagen 3.
- **Edit operations (`edit_image`) require Vertex AI mode** — set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` with ADC. API-key-only clients will fail for edits.
- Multiple reference images supported for edits (compositing, style transfer).
- Mask must be same dimensions as input image; alpha channel marks edit region.
- Use `negative_prompt` to steer away from unwanted elements.
- Aspect ratio is set via config, not pixel dimensions.
- For async operations: `client.aio.models.generate_images(...)`.

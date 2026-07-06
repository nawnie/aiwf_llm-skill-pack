# LoRA And Adapter Compatibility

Treat LoRA as a loader contract, not just an extra file picker.

## Compatibility Checks

Validate before loading:

- Base model family and exact major version.
- Architecture and component target: UNet, diffusion transformer, text encoder, LLM, VAE, or other module.
- Adapter format: PEFT, Diffusers LoRA, LyCORIS, safetensors checkpoint, embedding, ControlNet, IP-Adapter, or project-specific adapter.
- Target module names and whether they exist in the loaded base model.
- Rank, alpha, scale range, and whether multiple adapters can be composed.
- Required trigger words or prompt tokens.
- Recommended VAE, clip skip, scheduler, steps, CFG, resolution, or other generation settings.

## Fine-Tune Source Priority

1. Adapter metadata in local file/header when available.
2. Hugging Face adapter repo model card and config.
3. Civitai version page and file hash for community LoRAs.
4. Base-model docs for architecture compatibility.
5. Local empirical smoke only after preflight says the adapter is plausible.

## Load Policy

- Do not attach a LoRA to a model family only because filenames look similar.
- Keep LoRA scale explicit and bounded.
- Preserve loaded adapter state per active base model; unloading a base model should unload its adapters.
- Make fuse/unfuse behavior explicit. Fused adapters may require reloading the base for clean removal.
- Multiple LoRAs need deterministic order and named scales.
- Reject adapters with a user-visible reason when target modules or base family do not match.

## UI/API Contract

Expose:

- Adapter name, source, base compatibility, trigger words, scale, and loaded state.
- Whether the adapter is loaded, fused, disabled, or rejected.
- Rejection reason from preflight.
- Whether adapter loading requires model reload.

Do not hide LoRA errors in terminal logs only.

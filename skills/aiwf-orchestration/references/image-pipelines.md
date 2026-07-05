# Image Pipeline Routing

Use this reference for image generation model families and Diffusers-style image pipeline code.

## Stock Skills

- `local-ai-dev`: repo/venv/local runtime wiring.
- `stable-diffusion-image-generation`: SD, SDXL, Flux, Qwen Image, Sana, Z-Image, Klein, checkpoint loading, schedulers, samplers.
- `hugging-face:hf-cli`: model snapshots, files, and catalog entries.
- `quantizing-models-bitsandbytes`: 4-bit/8-bit/NF4 loading paths.
- `gguf-quantization`: image model GGUF routes where present.

## Model Cues

- Qwen Image or Nunchaku: include `hugging-face:hf-cli` and `quantizing-models-bitsandbytes`.
- Sana or Sana Sprint: include `stable-diffusion-image-generation` and `hugging-face:hf-cli`.
- Flux.2 Klein, Z-Image, or GGUF image checkpoints: include `gguf-quantization`.
- Scheduler/default tuning: include `stable-diffusion-image-generation` and check local model presets.

## AIWF Files To Inspect First

- `aiwf/infrastructure/diffusers/`
- `aiwf/services/generation.py`
- `aiwf/services/pipeline_preflight.py`
- `aiwf/services/pipeline_registry.py`
- `aiwf/services/model_download_catalog.py`
- `scripts/smoke_models_and_pipelines.py`

## Guardrails

- Do not add React wiring for image pipelines unless explicitly asked.
- Do not download large models unless the user asked for downloads.
- Prefer preflight and metadata validation before real generation.

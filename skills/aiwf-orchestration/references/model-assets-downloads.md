# Model Assets And Downloads Routing

Use this reference for Hugging Face downloads, model catalog updates, local checkpoint placement, and asset discovery.

## Stock Skills

- `hugging-face:hf-cli`: primary skill for search, download, snapshot, and repo file checks.
- `local-ai-dev`: local path layout and repo integration.
- `gguf-quantization`: GGUF naming, quant family, and runtime compatibility.
- `quantizing-models-bitsandbytes`: bitsandbytes/NF4/INT4/INT8 model loading and memory fit.

## AIWF Asset Rules

- Treat `safetensors` and `GGUF` as separate runtime families unless existing code explicitly bridges them.
- Keep Wan high/low pairs matched by route, quant, and model generation.
- Put LTX files in the LTX-specific folders, not shared SD/Flux folders.
- Keep model catalog entries explicit about category, source, repo, filename, snapshot behavior, and notes.

## AIWF Files To Inspect First

- `aiwf/services/model_download_catalog.py`
- `aiwf/services/model_download.py`
- `aiwf/infrastructure/model_inventory.py`
- `aiwf/infrastructure/diffusers/checkpoints.py`
- `scripts/smoke_models_and_pipelines.py`

## Guardrails

- Download only when the user explicitly asks.
- For 8-12 GB GPU targets, prefer smaller quantized variants and clear CPU/offload expectations.
- Verify downloaded paths with local existence checks and no-GUI smoke/preflight where possible.

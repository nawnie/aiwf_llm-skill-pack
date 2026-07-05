# Video Pipeline Routing

Use this reference for Wan, LTX, image-to-video, video model workers, VAE compatibility, and video engine isolation.

## Stock Skills

- `local-ai-dev`: isolated engines, worker venvs, Windows paths, smoke commands.
- `stable-diffusion-image-generation`: Diffusers video/image pipelines and scheduler semantics.
- `hugging-face:hf-cli`: Wan/LTX model files and snapshots.
- `gguf-quantization`: Wan GGUF high/low routes.
- `optimizing-attention-flash`, `ml-training-recipes`: attention backend, offload, timing, and VRAM work.

## Model Cues

- Wan fast 5B: check standalone safetensors transformer, Wan 2.2 VAE, shared component base, UMT5 text encoder.
- Wan 14B high/low: check matched high and low transformer family, VAE generation, GGUF vs safetensors route, offload lock.
- LTX 2.3: check worker readiness, checkpoint path, Gemma text encoder folder, distilled upscaler when distilled route is selected.

## AIWF Files To Inspect First

- `aiwf/core/domain/wan.py`
- `aiwf/core/domain/ltx.py`
- `aiwf/services/wan.py`
- `aiwf/services/ltx.py`
- `engines/ltx/worker.py`
- `scripts/smoke_backend.py`
- `scripts/smoke_models_and_pipelines.py`

## Guardrails

- Do not claim a speedup without timing, VRAM, and backend evidence.
- Prefer `scripts\smoke_backend.py --video --list` before real video generation.
- If LTX or Wan assets are missing, report exact paths and expected file formats.

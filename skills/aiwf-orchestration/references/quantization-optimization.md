# Quantization And Optimization Routing

Use this reference for VRAM fit, attention backends, GGUF, bitsandbytes, FP8, NF4, offload, and speed work.

## Stock Skills

- `optimizing-attention-flash`: FlashAttention, SDPA, xFormers, backend gates.
- `ml-training-recipes`: timing discipline, precision/offload tradeoffs, reproducible receipts.
- `gguf-quantization`: GGUF file and runtime decisions.
- `quantizing-models-bitsandbytes`: bitsandbytes, NF4, 4-bit/8-bit loading.
- `awq-quantization`: LLM AWQ experiments for chat, serving, or training.
- `gptq`: LLM GPTQ experiments for chat, serving, or training.
- `hqq-quantization`: LLM HQQ experiments for chat, serving, or training.
- `local-ai-dev`: local Windows venv/runtime constraints.

## AIWF Cues

- `FP8`, `scaled_mm`, `native`, `fallback`, `Comfy FP8`: inspect Wan quant format and fallback metrics.
- `GGUF`, `Q4_K_M`, `Q5`, `Q8`: inspect GGUF compatibility and memory expansion risks.
- `AWQ`, `GPTQ`, `HQQ`: default to LLM chat, serving, or training routes unless local Diffusers/video loader support is verified.
- `offload`, `balanced`, `resident`, `streamed`, `sequential`: inspect runtime-specific offload contracts.
- `speed up`, `optimize`, `faster`: require timed before/after receipts.

## AIWF Files To Inspect First

- `aiwf/infrastructure/quant/`
- `aiwf/infrastructure/torch/wan_perf.py`
- `aiwf/infrastructure/wan/`
- `aiwf/services/wan.py`
- `tests/individual_tests/test_wan*.py`

## Guardrails

- No speed claim is valid without timing, VRAM, and active backend evidence.
- Keep Transformers LLM quantization separate from Diffusers, video, VAE, and worker-native quantization until local loader support is proven.
- Do not turn on expensive dequant paths by default for consumer GPUs.
- Keep fallback paths explicit so users know when they are slow compatibility routes.

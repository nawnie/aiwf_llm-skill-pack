# Model Source Checks

Use this reference when an audit depends on external model truth.

## Source Priority

1. Local receipts: smoke matrix, generated artifacts, failure JSONL, backend logs.
2. Hugging Face model card and repository file tree for base models.
3. Upstream GitHub or arXiv for architecture and runtime constraints.
4. Civitai page for fine-tuned checkpoints, variants, recommended base model, trigger words, VAE notes, precision, and file format.
5. Community reports only as supporting evidence.

## What To Compare

- Architecture: SD 1.5, SDXL, SD3.5, Flux, Flux.2, Z-Image, Qwen Image, Sana, Wan, LTX, LLM.
- Expected loader: Diffusers folder, single-file safetensors, GGUF, Nunchaku, ONNX, llama.cpp server, vLLM, custom worker.
- Required sidecars: tokenizer, scheduler, text encoder, VAE, config, model index, component folder, quantization metadata.
- Precision and quantization: fp16, bf16, fp8, int4, NF4, GGUF K-quant, Nunchaku, bitsandbytes.
- Resolution/frame constraints: divisible dimensions, max resolution, fps, frame count, duration, bucket or aspect-ratio requirements.
- Prompt/runtime quirks: CFG expectations, distilled guidance, negative prompt support, sampler constraints, trigger words.
- License and intended use only when relevant to shipping or defaults.

## Civitai Checks

Use Civitai when a filename looks like a fine-tune, merge, LoRA, or custom quant. Confirm:

- Base model family and version.
- Recommended sampler, steps, CFG, VAE, clipskip, and resolution.
- Whether it is a full checkpoint, LoRA, ControlNet, VAE, upscaler, or other asset.
- Whether the file is actually compatible with the route selected locally.

## lm-evaluation-harness Checks

Do not run expensive evals unless requested. Audit readiness by checking:

- Model path or server endpoint.
- Tokenizer availability.
- Supported backend: `hf`, `vllm`, or API-compatible server.
- Quantization flags or server mode.
- Safe quick tasks for later smoke: `hellaswag`, `gsm8k`, `arc_easy`, or a tiny custom task.

## Evidence Standard

A route is `working` only with a successful smoke row or verified artifact. Clean startup, registry presence, or model discovery alone means `registered` or `metadata-only`.

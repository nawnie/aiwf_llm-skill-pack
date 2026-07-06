# Source Routing

Use source truth before changing loader code. Prefer primary sources over README claims, stale local comments, or generic framework defaults.

## Priority Order

1. Local files and headers: `config.json`, `model_index.json`, tokenizer files, safetensors headers, GGUF metadata, index files, and existing project inventory.
2. Hugging Face model card and repository files.
3. Original maker GitHub, docs, examples, and release notes.
4. arXiv or technical report for architecture constraints.
5. Civitai page for community fine-tunes and LoRAs.
6. Runtime docs: Diffusers, Transformers, llama.cpp, vLLM, TensorRT, bitsandbytes, NVIDIA docs.

## Hugging Face

Check:

- Pipeline tag, library name, architecture, base model, and license.
- `config.json`, `model_index.json`, scheduler config, tokenizer config, and component subfolders.
- File sizes and shard/index structure.
- `torch_dtype`, `variant`, `quantization_config`, and safetensors metadata when available.
- Whether the repo uses custom code or points to an upstream inference implementation.
- Adapter metadata for PEFT/LoRA repos.

## Original GitHub

Use original GitHub when:

- The model has custom inference code, scheduler behavior, preprocessing, postprocessing, or prompt encoding.
- The Hugging Face repo is a conversion, mirror, or community packaging.
- Speed depends on an official optimized path.
- The model family is new enough that generic Diffusers support may be incomplete.

Record exact loader-relevant facts: required package, dtype, resolution limits, step count, scheduler, VAE/text encoder handling, and unsupported modes.

## arXiv Or Technical Report

Use papers to explain architecture, not to override code. Extract only loader-relevant facts:

- Diffusion, flow, autoregressive, or hybrid generation family.
- Latent size, patch size, tokenizer/text encoder family, and VAE assumptions.
- Distillation claims that affect step counts.
- Precision or hardware claims that have implementation consequences.
- Image, video, audio, or LLM-specific conditioning requirements.

## Civitai

Use Civitai for community models, not base-model truth.

Check:

- Base model and version.
- Trigger words, recommended sampler/steps/CFG, VAE, clip skip, and resolution.
- Whether it is a checkpoint, LoRA, LyCORIS, embedding, ControlNet, or other adapter.
- File hash when matching a local file.
- Compatibility warnings in model or version notes.

Treat Civitai settings as user/model recommendations unless confirmed by base-model docs.

## NVIDIA And Runtime Docs

Use NVIDIA and runtime docs for:

- CUDA capability, BF16/FP16/FP8 support, attention kernels, TensorRT, Model Optimizer, and memory behavior.
- Whether a quant format is supported by the intended runtime on consumer NVIDIA GPUs.
- Whether a claimed acceleration path is compile-time, export-time, or runtime selectable.

Do not assume FP8, TensorRT, or specialized attention is available just because the GPU is NVIDIA.

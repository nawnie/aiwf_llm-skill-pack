# Precision And Quantization Policy

Choose precision per component and backend. A single global dtype is usually wrong for mixed image, video, and LLM pipelines.

## Decision Order

1. Source requirement: original docs, model card, config, or known runtime restriction.
2. Backend support: Diffusers, Transformers, llama.cpp, vLLM, TensorRT, Nunchaku, ONNX, or native code.
3. Hardware support: CUDA capability, VRAM, CPU fallback, disk speed, and Windows compatibility.
4. Quality target: release smoke, default user generation, high-quality mode, or low-memory mode.
5. Failure behavior: unsupported precision must fail in preflight, not halfway through loading.

## Component Defaults

| Component | Conservative default | Notes |
| --- | --- | --- |
| Diffusion transformer or UNet | FP16 on NVIDIA | BF16 only when source/runtime/GPU support it. FP8 requires explicit runtime support. |
| VAE | FP16 or FP32 fallback | Keep independent from main model. Some VAEs need FP32 for stability. |
| Text encoder | FP16/BF16 on GPU or CPU offload | Prompt encoding on GPU can speed small models, but must account for VRAM and unload behavior. |
| Tokenizer | CPU | Do not treat tokenizer as a GPU precision decision. |
| LLM base model | Runtime-specific | Transformers, llama.cpp, vLLM, and TensorRT have different quant contracts. |
| LoRA/adapters | Match base module dtype at attach time | Validate base compatibility before loading. |

## GGUF

Use `gguf-quantization` and `llama-cpp` for detailed GGUF rules.

Practical loader policy:

- Use GGUF only with runtimes that understand GGUF metadata.
- Read metadata before choosing context size, tokenizer behavior, architecture, projector requirements, or GPU layer split.
- Q4_K_M is the usual balanced local default for LLMs when memory is tight.
- Q5_K_M or Q6_K is preferred when quality matters and VRAM/RAM allows.
- Q8_0 is useful for near-FP quality checks and debugging, but is not the smallest useful release target.
- Use imatrix-aware quants for low-bit quality when quantizing yourself.
- Multimodal GGUF may need a separate projector/mmproj file; preflight must catch missing projector files.

## Bitsandbytes

Use `quantizing-models-bitsandbytes` and `bitsandbytes` for implementation details.

Practical loader policy:

- Use 8-bit for simple Transformers memory reduction when supported.
- Use 4-bit NF4 for QLoRA-style loading or tight VRAM LLM inference when supported.
- Do not apply bitsandbytes to arbitrary Diffusers components unless the backend officially supports that component path.
- Keep quantization config visible in model metadata and logs.

## AWQ, GPTQ, HQQ, Nunchaku, TensorRT

- Treat each as a backend-specific artifact, not a generic precision flag.
- Validate that the selected runtime can load the artifact before exposing it in UI.
- For vLLM, confirm the exact quantization option supported by the installed vLLM version.
- For TensorRT or FP8, distinguish export/build steps from runtime loading.
- For Nunchaku or other custom acceleration formats, use source docs and preflight artifact layout.

## Image And Video Models

- Prefer source-native loaders when a family has custom optimized inference.
- Diffusers is appropriate when the model is officially supported or local code confirms compatibility.
- Keep prompt encoding, denoising, decoding, and postprocessing precision separate.
- Avoid CPU prompt encoding by default for small models if GPU prompt encoding is supported and faster, but expose offload for low VRAM.
- Video models often need stricter memory policy than image models: frame count, duration, FPS, latent size, and VAE decode can dominate.

## Unsupported Choices

Unsupported precision or quant choices should produce a clean reason:

- Unsupported by backend.
- Unsupported by hardware.
- Missing artifact.
- Incompatible architecture.
- Requires export/build step.
- Not verified for this model family.

# Precision And Quantization Policy

Choose precision and quantization per model component, artifact, backend, hardware, and quality target. Do not encode one quant name or dtype as a pack-wide default.

## Decision Order

1. Confirm model architecture and source requirements from local config and primary documentation.
2. Confirm the artifact format and the exact runtime that will load it.
3. Inspect hardware capability, available memory, OS, driver/runtime compatibility, and fallback behavior.
4. Define the quality, latency, memory, portability, and reproducibility target.
5. Select only a format and dtype supported by all four layers above.

## Component Contract

Record each component separately:

- weights and architecture
- loader/backend
- storage format
- runtime dtype
- quantization method and metadata
- device and offload policy
- memory estimate or measured peak
- fallback and rejection reason
- smoke check

Diffusion or language-model weights, VAE, text encoders, tokenizers, projectors, adapters, and postprocessors can have different constraints. A global dtype flag is not proof that every component supports it.

## Format Rules

### GGUF

- Use a runtime that understands the artifact's GGUF architecture and metadata.
- Inspect tokenizer, context, tensor, quantization, and architecture metadata before loading.
- Multimodal models may require a separate projector; reject incomplete layouts in preflight.
- Compare quant choices against the actual model family, runtime support, memory budget, and measured quality. Do not assume one Q4/Q5/Q8 label is universally best.
- Use calibration or importance-matrix workflows only when the selected quantizer and model support them.

### Transformers Quantization

- Treat bitsandbytes, AWQ, GPTQ, HQQ, and other formats as separate contracts.
- Confirm the installed Transformers, accelerator, backend, and hardware support before constructing a quantization config.
- Distinguish training-time QLoRA loading from serving artifacts and merged exports.

### TensorRT And Other Compiled Artifacts

- Separate export/build from runtime loading.
- Record TensorRT version, platform, GPU target or compatibility mode, precision, plugins, and build flags.
- Do not deserialize untrusted engine files.
- Treat ONNX, TensorRT, Nunchaku, and other compiled or custom formats as backend-specific artifacts, not generic precision toggles.

## Failure Behavior

Reject unsupported choices before allocating model weights. Return a specific reason: unsupported backend, unsupported hardware, missing artifact, incompatible architecture, invalid component combination, required export/build step, or unverified model-family support.

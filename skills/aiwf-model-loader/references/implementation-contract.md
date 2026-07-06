# Implementation Contract

Use this reference when changing AIWF or another local AI app.

## Loader Shape

Separate these phases in code:

1. Discover local assets.
2. Read local metadata and source-backed manifest.
3. Preflight required files, backend support, precision, quantization, and adapters.
4. Construct the loader without loading heavy weights when possible.
5. Load base components.
6. Attach optional components: VAE, text encoder overrides, projectors, LoRAs, ControlNet/IP adapters.
7. Generate.
8. Unload, cancel, or clean up.

## AIWF Guidance

In AIWF, prefer existing registry and inventory patterns. Current known truth sources include model inventory/header readers and pipeline registry metadata. Keep UI code thin; loader decisions belong in Python service/runtime layers first.

Add or update:

- Registry metadata for family, format, backend, source, maturity, and supported modes.
- Inventory parsing for file format and component layout.
- Preflight result with `supported`, `blocked_reason`, `warnings`, `required_files`, and `suggested_backend`.
- Loader precision map per component.
- Quantization metadata separate from dtype.
- LoRA/adapters metadata separate from base model metadata.
- Tests for each supported and blocked state.

## Fallback Rules

Allowed fallback examples:

- Use FP16 instead of BF16 when source permits and hardware lacks BF16.
- Use CPU prompt encoding when GPU prompt encoding would exceed memory and source permits.
- Use non-fused LoRA when fuse is unsupported.

Forbidden silent fallback examples:

- Diffusers fallback for a model whose source requires custom native inference.
- Loading a GGUF file through a safetensors path.
- Treating a LoRA as compatible when target modules are missing.
- Downgrading quantization or precision without reporting it.
- Hiding missing VAE/text encoder/projector files until generation time.

## Test Expectations

Minimum tests before a release-facing claim:

- Contract or manifest validates.
- Local asset discovery identifies the format and required components.
- Preflight catches missing required files.
- Unsupported precision/quant/LoRA choices return clean reasons.
- Loader can be constructed or dry-run without a full VRAM generation where possible.
- One route-level no-GPU test proves API shape for the selected model.

Full generation smoke is optional unless the user asks for runtime proof.

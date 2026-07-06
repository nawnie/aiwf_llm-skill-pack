# GPU Runtime Diagnostics

Use this reference to classify local AI runtime failures.

## First Split

- Device visibility: `nvidia-smi`, ROCm tools, DirectML availability, or framework device count fails.
- Import failure: Python package cannot import or DLL load fails.
- ABI mismatch: package imports, but CUDA/ROCm/TensorRT runtime symbols fail.
- OOM: device works but allocation fails.
- Unsupported operation: dtype, quantization, attention backend, or model architecture is incompatible.
- Throughput regression: run works, but step time, VRAM, or CPU offload changed.

## Evidence To Collect

- failing command and exact error
- active Python executable and virtual environment
- GPU name, driver version, VRAM, and current memory use
- `torch.__version__`, `torch.version.cuda`, `torch.cuda.is_available()`
- TensorRT, xformers, flash-attn, bitsandbytes, llama.cpp, vLLM, or Ollama versions when relevant
- model name, precision, quantization, resolution/context/batch settings
- whether the error happens at import, load, warmup, first token/step, or export

## Bounded Smokes

- Import-only smoke for package/DLL checks.
- Device-count smoke for framework visibility.
- Tiny tensor operation for CUDA/ROCm execution.
- Runtime health endpoint for serving.
- One very small model/load smoke only when Shawn explicitly asks or the model is already local.

Do not use a full generation, training run, or large model download as the first diagnostic.

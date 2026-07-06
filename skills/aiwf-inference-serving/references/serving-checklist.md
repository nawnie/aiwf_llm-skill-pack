# Serving checklist

Use this checklist before changing launchers, service code, ports, or runtime settings.

## Boundary

- Bind address is explicit: localhost, LAN, Tailscale, or public.
- Auth policy is explicit before any non-local exposure.
- API keys, tokens, and headers are never written into prompts or public docs.
- Firewall, tunnel, and reverse-proxy changes require explicit approval.

## Runtime contract

- Runtime is named: vLLM, llama.cpp server, Ollama, FastAPI worker, Gradio worker, or project-local wrapper.
- Model path, format, tokenizer, context length, dtype, quantization, and adapter state are known.
- OpenAI-compatible claims are verified against real endpoints.
- Streaming support is tested if the UI or client expects it.

## Operations

- Startup command is recorded.
- Shutdown path is known.
- Reload and unload behavior is known or explicitly unsupported.
- Queueing and concurrency behavior are known.
- Cancellation behavior is known where supported.
- Logs include startup, model load, request errors, and crashes.

## Smoke probes

- Health endpoint responds.
- Model list endpoint responds when available.
- Tiny completion or chat request works.
- Error response for a bad request is structured.
- Telemetry endpoint is fresh enough for UI use when present.

## Stability checks

- Latency check uses a fixed prompt and model state.
- Load loop has a bounded request count.
- GPU/RAM telemetry is captured before, during, and after.
- Failures leave the server in a known state.

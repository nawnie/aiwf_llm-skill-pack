# Eval gates

Use evals to answer a bounded question. Avoid expensive benchmarks until the baseline, candidate, and pass rule are clear.

## Required fields

- Target: model, adapter, route, endpoint, or UI workflow.
- Baseline: previous model, current route, or known-good receipt.
- Candidate: new model, adapter, config, or service.
- Runtime: local path, server URL, backend, dtype, quantization, and prompt settings.
- Suite: task list, prompt file, smoke matrix, or visual prompt set.
- Acceptance rule: numeric threshold, artifact rule, or manual review rubric.
- Receipt path: where command output, metrics, artifacts, and logs will be stored.

## LLM gates

- Tokenizer is known and compatible.
- Backend is known: Hugging Face, vLLM, llama.cpp, Ollama, or OpenAI-compatible API.
- Tiny prompt probe works before benchmark work.
- lm-evaluation-harness readiness checks path, tokenizer, batch size, dtype, quantization, and server mode.
- Custom prompt suites include expected behavior and failure labels.

## Image and video gates

- Prompts, negative prompts when used, seeds, dimensions, steps, scheduler, FPS, duration, and LoRA state are recorded.
- Output file exists, opens, and has expected dimensions or duration.
- Metadata or receipt links the artifact to the command and route.
- Manual review fields are explicit when quality cannot be measured numerically.

## Promotion gates

- The candidate beats or matches baseline on the named criteria.
- Any regression is listed and accepted by Shawn or blocks promotion.
- Receipts are reproducible enough for a future agent to rerun.

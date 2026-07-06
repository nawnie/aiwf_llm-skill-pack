# AIWF skill routing map

Choose the smallest set that owns the request.

| Prompt signal | Primary skill | Add when needed |
| --- | --- | --- |
| coding task, bug fix, debug, refactor, generated code cleanup, code review | `aiwf-ai-coding-guardrails` | focused language or repo guardrails |
| repo state, dirty tree, package manager, lockfile, shell commands, test integrity, broad diff | `aiwf-repo-sentinel` | `aiwf-ai-coding-guardrails` |
| security, auth, authorization, CORS, secrets, tokens, injection, unsafe deserialization, path traversal, SSRF, public exposure, dependency supply chain, model-source trust | `aiwf-security-guardrails` | `aiwf-web-api-ui-guardian`, `aiwf-repo-sentinel` |
| CUDA, ROCm, NVIDIA driver, PyTorch GPU, TensorRT, xformers, flash-attn, bitsandbytes, VRAM, OOM, DLL/PATH, GPU smoke, device visibility | `aiwf-gpu-runtime-diagnostics` | `aiwf-model-loader`, `aiwf-inference-serving` |
| FastAPI, Gradio, React, TypeScript, JavaScript, HTML, CSS, Vite, API contract, OpenAPI, frontend/backend drift, UI validation | `aiwf-web-api-ui-guardian` | `aiwf-repo-sentinel` |
| Python, C++, CMake, pytest, Ruff, Pyright, mypy, async blocking, serialization, compiler, CMake presets, memory safety | `aiwf-python-cpp-hardener` | `aiwf-repo-sentinel` |
| image generation, generated images, AI illustration, AI artifacts, logos, icons, signage, visual text, diagrams, flowcharts, charts, infographics, portraits, hands, fingers, anatomy, skin texture, pores, blemishes, photorealism, final image QA | `aiwf-avoid-ai-illustrations` | `aiwf-deep-research`, `aiwf-ai-evals` |
| deep research, literature review, source plan, source weighting, evidence weight, claim ledger, arXiv, OpenReview, Civitai research, Reddit limits, academic sources, college, graduate, postgraduate, thesis, dissertation, quantum physics, robotics research, mechanical engineering research | `aiwf-deep-research` | `aiwf-agent-mok`, domain skill |
| train, fine-tune, LoRA, QLoRA, dataset split, checkpoint, resume | `aiwf-local-ai-training` | `aiwf-ai-evals`, `aiwf-model-loader` |
| eval, benchmark, prompt suite, before/after, regression, promote | `aiwf-ai-evals` | `aiwf-inference-serving`, `aiwf-local-ai-training` |
| serve, endpoint, API, vLLM, llama.cpp server, Ollama, queue, latency | `aiwf-inference-serving` | `aiwf-model-loader`, `aiwf-ai-evals` |
| load model, dtype, quant, GGUF, safetensors, Nunchaku, LoRA compatibility | `aiwf-model-loader` | `aiwf-ai-pipelines` |
| pipeline route, backend wiring, smoke matrix, source mismatch | `aiwf-ai-pipelines` | `aiwf-model-loader`, `aiwf-ui-electrician` |
| UI button, progress, cancellation, API payload, response shape, telemetry display | `aiwf-ui-electrician` | `aiwf-ai-pipelines` |
| many agents, broad crawl, debug pass, independent lanes | `aiwf-debug-agent-swarm` | `aiwf-ai-pipelines`, `aiwf-ui-electrician` |
| source verification, findings dataset, plan.md, research route verification | `aiwf-agent-mok` | `aiwf-deep-research`, any domain skill |
| handoff, resume, continuity card, compact chat | `aiwf-atlas-cartographer` | any active work skill |
| Atlas Reader LoRA repo, Atlas adapter, training records, evaluation plans, measured logs, context-pack construction, Qwen LoRA failure | `aiwf-atlas-reader` | `aiwf-atlas-cartographer`, `aiwf-agent-mok`, `aiwf-local-ai-training` |
| dataset intake, source provenance, curation, synthetic guardrail rows, dashboard/reporting for datasets | `aiwf-dataset` | `aiwf-deep-research`, `aiwf-agent-mok` |
| AI-looking design, teal everywhere, default Gradio/shadcn, generated-looking PDF, document, dashboard, or web layout | `aiwf-avoid-ai-design` | `aiwf-web-api-ui-guardian`, `aiwf-avoid-ai-pushes` |
| README, public docs, release text, AI writing patterns, commit scope, push hygiene | `aiwf-avoid-ai-pushes` | domain skill for technical correctness |

If two skills seem equally likely, choose the one that prevents the first expensive mistake. Security outranks feature work, GPU runtime diagnostics outrank model-runtime edits, repo preflight outranks code patching, training outranks eval, serving outranks UI, model loading outranks pipeline status, and pipeline status outranks docs.

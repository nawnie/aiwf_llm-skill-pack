# AIWF Skill Routing Map

Choose the smallest route that owns the first risky decision. Add `aiwf-repo-sentinel` for edits in an existing repository and `aiwf-security-guardrails` only when a security boundary is touched.

## Coding

| Signal | Primary skill | Add only when needed |
| --- | --- | --- |
| C source, headers, ABI, ISO C | `aiwf-c-coding` | `aiwf-repo-sentinel` |
| C++, CMake, RAII, templates, native extension | `aiwf-cpp-coding` | versioned Python skill for extension packaging |
| Python 3.10 or cp310 | `aiwf-python310-coding` | `aiwf-cpp-coding` for native code |
| Python 3.12 or cp312 | `aiwf-python312-coding` | `aiwf-cpp-coding` for native code |
| CUDA, cuDNN, TensorRT, NVIDIA SDK | `aiwf-nvidia-cuda-cudnn-sdk` | `aiwf-gpu-runtime-diagnostics` for runtime failure |
| FastAPI, Pydantic, OpenAPI | `aiwf-fastapi-coding` | `aiwf-ui-electrician` for client contract drift |
| Gradio callbacks, queue, mount | `aiwf-gradio-coding` | `aiwf-avoid-ai-design` for visuals |
| React, hooks, JSX/TSX | `aiwf-react-coding` | `aiwf-typescript-coding`, `aiwf-css-coding` |
| Vue 3 or VitePress | `aiwf-vue-vitepress-coding` | `aiwf-typescript-coding`, `aiwf-web-seo` |
| TypeScript config or contracts | `aiwf-typescript-coding` | framework skill for component behavior |
| JavaScript, Node, ESM/CJS | `aiwf-javascript-coding` | `aiwf-security-guardrails` for unsafe input |
| CSS layout and responsive behavior | `aiwf-css-coding` | `aiwf-avoid-ai-design` for design direction |
| Android, Kotlin, Compose, Room, ADB | `aiwf-android-kotlin-coding` | `aiwf-data-storage`, `aiwf-cpp-coding` |

## AI And Data

| Signal | Primary skill | Add only when needed |
| --- | --- | --- |
| Model loading, dtype, quantization, adapters | `aiwf-model-loader` | `aiwf-gpu-runtime-diagnostics` |
| Pipeline registry, stages, source/runtime wiring | `aiwf-ai-pipelines` | `aiwf-ui-electrician` |
| Training, LoRA, QLoRA, checkpoints | `aiwf-local-ai-training` | `aiwf-ai-evals` |
| Benchmarks, prompt suites, promotion | `aiwf-ai-evals` | training or serving owner |
| vLLM, llama.cpp, Ollama, model endpoint | `aiwf-inference-serving` | `aiwf-model-loader` |
| GPU driver, ABI, VRAM, DLL, runtime failure | `aiwf-gpu-runtime-diagnostics` | NVIDIA coding skill for source changes |
| RAG, embeddings, chunking, reranking, citations | `aiwf-rag-retrieval` | `aiwf-data-storage`, `aiwf-ai-evals` |
| SQLite, Room, Postgres, vector stores, migrations | `aiwf-data-storage` | `aiwf-rag-retrieval` for result quality |
| Dataset intake, provenance, curation, captions | `aiwf-dataset` | `aiwf-deep-research` for external claims |

## Systems And Projects

| Signal | Primary skill | Add only when needed |
| --- | --- | --- |
| Robotics, ROS 2, sensors, control | `aiwf-robotics-systems` | physics, embedded, or field-pilot owner |
| Units, frames, dynamics, simulation | `aiwf-physics-simulation` | `aiwf-robotics-systems` |
| LAN, MQTT, WebSocket, RTSP, IoT | `aiwf-networking-iot` | security or field-pilot owner |
| MCU, RTOS, Jetson, power, thermal | `aiwf-embedded-edge-ai` | NVIDIA or robotics owner |
| Customer-site test, hazards, rollback | `aiwf-field-pilot-readiness` | robotics, networking, security |
| Windows paths, venvs, processes, ports, WSL/Docker | `aiwf-windows-local-dev` | GPU or networking diagnostics |
| Service lead, quote, AI-fit scoping | `aiwf-service-intake` | implementation owner after scope |

## Research, Debugging, And Output

| Signal | Primary skill | Add only when needed |
| --- | --- | --- |
| Deep research, claim ledger, source weighting | `aiwf-deep-research` | domain skill; `aiwf-agent-mok` for durable plan |
| `plan.md`, findings dataset, route verification | `aiwf-agent-mok` | `aiwf-deep-research` for external evidence |
| Subagents, broad crawl, debug pass | `aiwf-debug-agent-swarm` | owning domain skills |
| UI/API progress, errors, cancellation, payloads | `aiwf-ui-electrician` | backend and frontend owners |
| Handoff, continuity cards, resume state | `aiwf-atlas-cartographer` | current work owner |
| Atlas Reader LoRA protocol or measured claims | `aiwf-atlas-reader` | training or continuity owner |
| AI-looking UI or document design | `aiwf-avoid-ai-design` | framework skill for code changes |
| Generated-image artifact QA | `aiwf-avoid-ai-illustrations` | `aiwf-deep-research` for exact references |
| Crawlability, canonical, sitemap, structured data | `aiwf-web-seo` | site framework and design skills |
| Commit, push, release, public repo copy | `aiwf-avoid-ai-pushes` | `aiwf-repo-sentinel` |
| Torchie voice | `aiwf-torchie` | technical owner remains authoritative |

If more than four skills appear relevant, split the work into phases. Do not load broad wrappers that duplicate the focused owners.

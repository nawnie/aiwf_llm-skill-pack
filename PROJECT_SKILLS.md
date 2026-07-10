# Project Skill Routing

Generated: 2026-07-09

## Standing Rule

For each non-trivial task, let `aiwf-orchestrator` select the smallest focused route before acting. It is the only implicit pack skill. Use no more than four downstream skills and follow `AGENTS.md` over generic guidance.

## Workspace Routes

| Task signal | Preferred skills |
| --- | --- |
| Add, rename, validate, package, install, or document a skill/plugin | `projectskill-list`, `skill-creator`, `plugin-creator`, `aiwf-orchestrator` |
| Existing repository edit, debug, refactor, or review | `aiwf-repo-sentinel` plus the focused language/framework skill |
| Auth, secrets, injection, unsafe serialization, dependency, or public exposure risk | `aiwf-security-guardrails` |
| Commit, push, release, staging, ignored files, or public docs | `aiwf-avoid-ai-pushes`, `aiwf-repo-sentinel` |
| Weighted research, source plan, claim ledger, contradiction, or citations | `aiwf-deep-research` |
| Dataset intake, provenance, curation, validation, or synthetic records | `aiwf-dataset` |
| Durable plan, verification map, or optional findings dataset | `aiwf-agent-mok` |
| Continuity cards or compact-chat handoff | `aiwf-atlas-cartographer` |
| Atlas Reader LoRA records, evals, source protocol, or measured claims | `aiwf-atlas-reader` |
| Authorized broad read-only debug crawl | `aiwf-debug-agent-swarm`, `aiwf-repo-sentinel` |

## Coding Routes

| Task signal | Preferred skills |
| --- | --- |
| C source, headers, ABI, compiler flags, or memory safety | `aiwf-c-coding` |
| C++, CMake, ownership, templates, ABI, or native extensions | `aiwf-cpp-coding` |
| Python 3.10 compatibility | `aiwf-python310-coding` |
| Python 3.12 compatibility | `aiwf-python312-coding` |
| CUDA, cuDNN, TensorRT, `nvcc`, kernels, or NVIDIA SDKs | `aiwf-nvidia-cuda-cudnn-sdk` |
| GPU driver/runtime/DLL/VRAM failure | `aiwf-gpu-runtime-diagnostics`, `aiwf-nvidia-cuda-cudnn-sdk` |
| FastAPI, Pydantic, OpenAPI, ASGI, auth/CORS, or lifespan | `aiwf-fastapi-coding` |
| Gradio Blocks, events, queues, mounts, or callbacks | `aiwf-gradio-coding` |
| React components, hooks, state, rendering, or accessibility | `aiwf-react-coding` |
| Vue 3, Composition API, `.vue`, or VitePress | `aiwf-vue-vitepress-coding` |
| TypeScript configuration, strict types, JSX/TSX, or generated types | `aiwf-typescript-coding` |
| JavaScript runtime, modules, async, DOM, browser, or Node behavior | `aiwf-javascript-coding` |
| CSS cascade, layout, responsive behavior, or rendered polish | `aiwf-css-coding` |
| Android, Kotlin, Gradle, Compose, Room, Retrofit, ONNX, APK/AAB, or real device | `aiwf-android-kotlin-coding` |
| Frontend/backend payload, cancellation, progress, or stale-state wiring | `aiwf-ui-electrician` plus the two surface skills |

## Application And Data Routes

| Task signal | Preferred skills |
| --- | --- |
| RAG, embeddings, chunking, hybrid search, reranking, grounding, or retrieval eval | `aiwf-rag-retrieval` |
| SQLite, Room, Postgres, Chroma, pgvector, Qdrant, Milvus, schemas, or migrations | `aiwf-data-storage` |
| Windows paths, PowerShell, venvs, ports, processes, Docker Desktop, WSL, or local services | `aiwf-windows-local-dev` |
| Crawlability, metadata, canonicals, sitemaps, structured data, or web evidence | `aiwf-web-seo` |
| AI-looking UI, dashboard, PDF, or document layout | `aiwf-avoid-ai-design` |
| Generated image, logo, diagram, chart, portrait, hands, anatomy, or text artifact QA | `aiwf-avoid-ai-illustrations` |
| Explicit Torchie voice or AIWF beta copy | `aiwf-torchie` |

## AI Runtime Routes

| Task signal | Preferred skills |
| --- | --- |
| Pipeline graph, runtime wiring, source mapping, or smoke matrix | `aiwf-ai-pipelines` |
| Model format, precision, quantization, loader backend, component, or adapter contract | `aiwf-model-loader` |
| LoRA/QLoRA training plan, dataset split, checkpoint, resume, or export | `aiwf-local-ai-training` |
| Eval suite, regression, benchmark, acceptance threshold, or promotion gate | `aiwf-ai-evals` |
| vLLM, llama.cpp, Ollama, OpenAI-compatible endpoint, telemetry, queue, or latency | `aiwf-inference-serving` |

## Physical And Business Routes

| Task signal | Preferred skills |
| --- | --- |
| Robotics architecture, ROS 2, sensors, actuators, perception, planning, or controls | `aiwf-robotics-systems` |
| Units, frames, kinematics, dynamics, Gazebo, MuJoCo, or sim-to-real | `aiwf-physics-simulation` |
| LAN, Wi-Fi, MQTT, WebSocket, RTSP, telemetry, reconnect, or secure binding | `aiwf-networking-iot` |
| MCU, RTOS, Jetson, SBC, firmware, buses, power, thermal, or edge inference | `aiwf-embedded-edge-ai` |
| Customer-site pilot, hazards, operator handoff, rollback, or go/no-go | `aiwf-field-pilot-readiness` |
| Ai Embedded Systems lead, quote-ready first pass, workflow, bot, SEO, training, or AI fit | `aiwf-service-intake` |

## Verification

```powershell
.\scripts\validate_skills.ps1
python .\scripts\validate_pack.py
python .\scripts\test_orchestrator_routes.py
```

Use the project-native test, lint, typecheck, build, device, endpoint, browser, or artifact checks for the selected route. Router policy never substitutes for runtime evidence.

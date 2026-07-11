# Project Skill Routing

Generated: 2026-07-10

## Standing Rule

For each non-trivial task, let `aiwf-orchestrator` select the smallest focused route. It is the only implicit skill. Use no more than four downstream skills. For security work, use the guardrail plus at most two focused security owners so the repository or domain owner still fits.

## Workspace And Release

| Task signal | Preferred skills |
| --- | --- |
| Add, validate, package, install, or document a skill/plugin | `projectskill-list`, `skill-creator`, `plugin-creator`, `aiwf-orchestrator` |
| Existing repository edit, debug, refactor, or review | `aiwf-repo-sentinel` plus the focused implementation skill |
| Repeated QA or bug passes until stable | `aiwf-qa-convergence`, `aiwf-repo-sentinel`, and the focused implementation skill |
| Commit, push, PR, release, staging, or public docs | `aiwf-avoid-ai-pushes`, `aiwf-repo-sentinel` |
| Shared Codex/Claude/Grok state, context, handoffs, or leases | `aiwf-multi-agent-workspace` |

## Security And Privacy

| Task signal | Preferred skills |
| --- | --- |
| Security authorization, threat triage, evidence, or approval gates | `aiwf-security-guardrails` |
| Application/API auth, permissions, input, browser, webhook, or LLM tools | `aiwf-application-api-security` |
| Internet exposure, DNS/TLS, IAM, cloud/VPS, containers, or ports | `aiwf-online-infrastructure-security` |
| Windows/device hardening, encryption, credentials, local services/files | `aiwf-local-device-security` |
| Personal/customer data, minimization, retention, deletion, audit evidence | `aiwf-data-privacy-protection` |
| Dependencies, SBOM, build/release provenance, models, datasets, binaries | `aiwf-software-ai-supply-chain-security` |
| Credential compromise, malware, breach, evidence, containment, recovery | `aiwf-incident-response-recovery` |

## Startup Growth And Platforms

| Task signal | Preferred skills |
| --- | --- |
| Positioning, ICP, go-to-market, funnels, channels, experiments, KPIs | `aiwf-startup-marketing-growth` |
| Burn, runway, unit economics, grants, SBA, angels, VC, diligence | `aiwf-startup-finance-funding` |
| Answer engines, generative search, AI-search visibility, citation readiness | `aiwf-aeo-geo` |
| Facebook, Instagram, WhatsApp Business, Meta ads, Pixel/CAPI | `aiwf-meta-business` |
| Google Ads, GA4, Tag Manager, Business Profile, conversions | `aiwf-google-ads-business` |
| YouTube channels/APIs, YPP, AdSense, rights, monetization | `aiwf-youtube-adsense` |
| HTTP crawl/index, rendering, canonicals, sitemaps, structured data | `aiwf-web-seo` |

## Coding

| Task signal | Preferred skills |
| --- | --- |
| C source, headers, ABI, compiler flags, memory safety | `aiwf-c-coding` |
| C++, CMake, ownership, templates, ABI, native extensions | `aiwf-cpp-coding` |
| Python 3.10 compatibility | `aiwf-python310-coding` |
| Python 3.12 compatibility | `aiwf-python312-coding` |
| CUDA, cuDNN, TensorRT, kernels, NVIDIA SDKs | `aiwf-nvidia-cuda-cudnn-sdk` |
| FastAPI, Pydantic, OpenAPI, ASGI | `aiwf-fastapi-coding` |
| Gradio Blocks, events, queues, mounts, callbacks | `aiwf-gradio-coding` |
| React components, hooks, state, rendering | `aiwf-react-coding` |
| Vue 3, Composition API, VitePress | `aiwf-vue-vitepress-coding` |
| TypeScript config, strict types, JSX/TSX | `aiwf-typescript-coding` |
| JavaScript runtime, modules, async, DOM, Node | `aiwf-javascript-coding` |
| CSS cascade, layout, responsive behavior | `aiwf-css-coding` |
| Android, Kotlin, Gradle, Compose, Room, ADB | `aiwf-android-kotlin-coding` |
| Frontend/backend payload, progress, cancellation, stale state | `aiwf-ui-electrician` plus surface skills |
| Windows paths, PowerShell, venvs, ports, processes, WSL/Docker | `aiwf-windows-local-dev` |

## AI And Data

| Task signal | Preferred skills |
| --- | --- |
| Pipeline graph, engines, runtime wiring, smoke matrix | `aiwf-ai-pipelines` |
| Model format, precision, quantization, backend, components, adapters | `aiwf-model-loader` |
| LoRA/QLoRA plan, dataset split, checkpoint, resume, export | `aiwf-local-ai-training` |
| Eval suite, benchmark, regression, threshold, promotion gate | `aiwf-ai-evals` |
| vLLM, llama.cpp, Ollama, endpoints, queues, latency | `aiwf-inference-serving` |
| Driver/runtime/DLL/VRAM failure | `aiwf-gpu-runtime-diagnostics` |
| RAG, embeddings, chunking, hybrid search, reranking, grounding | `aiwf-rag-retrieval` |
| SQLite, Room, Postgres, vector stores, schemas, migrations | `aiwf-data-storage` |
| Dataset intake, provenance, curation, validation, synthetic data | `aiwf-dataset` |

## Physical, Research, And Output

| Task signal | Preferred skills |
| --- | --- |
| Robotics architecture, ROS 2, sensors, control | `aiwf-robotics-systems` |
| Units, frames, dynamics, Gazebo, MuJoCo, sim-to-real | `aiwf-physics-simulation` |
| LAN, MQTT, WebSocket, RTSP, IoT, telemetry | `aiwf-networking-iot` |
| MCU, RTOS, Jetson, firmware, power, thermal, edge inference | `aiwf-embedded-edge-ai` |
| Customer-site hazards, operator handoff, rollback, go/no-go | `aiwf-field-pilot-readiness` |
| Lead, quote-ready first pass, service fit | `aiwf-service-intake` |
| Weighted research, claim ledger, source verification | `aiwf-deep-research` |
| Durable plan, verification map, findings dataset | `aiwf-agent-mok` |
| Continuity cards or compact-chat handoff | `aiwf-atlas-cartographer` |
| Atlas Reader LoRA records, evals, measured claims | `aiwf-atlas-reader` |
| Authorized broad read-only debug crawl | `aiwf-debug-agent-swarm` |
| AI-looking UI or document cleanup | `aiwf-avoid-ai-design` |
| Generated-image artifact and semantic QA | `aiwf-avoid-ai-illustrations` |
| Explicit Torchie voice | `aiwf-torchie` |

## Verification

Run the project-native check for the selected route, then the pack validators in `AGENTS.md`. Router policy never substitutes for runtime evidence.

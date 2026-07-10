# AIWF LLM Skill Pack

`#techstartup` release `0.3.0` is a provider-portable Agent Skills pack and skills-only Codex plugin for local AI, focused coding, startup growth, funding, platform operations, security, privacy, embedded systems, robotics, and coordinated agent work.

The pack contains 56 focused `aiwf-` skills. `aiwf-orchestrator` is the only implicit Codex entrypoint; the other 55 skills are explicit, and one prompt selects at most four.

## Install For Codex, Claude, And Grok

From the source workspace:

```powershell
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\scripts\install_agent_skill_pack.ps1 -Providers All -Force -PruneRetired
```

The first run asks where to create the private shared-agent workspace. Press Enter for `%SystemDrive%\AI-Agent-Workspace`, or provide another local path. Non-interactive installs must choose one option explicitly:

```powershell
.\scripts\install_agent_skill_pack.ps1 -Providers All -AcceptDefaultAgentWorkspace -Force -PruneRetired
.\scripts\install_agent_skill_pack.ps1 -Providers All -AgentWorkspacePath "D:\AI-Agent-Workspace" -Force -PruneRetired
.\scripts\install_agent_skill_pack.ps1 -Providers All -SkipAgentWorkspace -Force -PruneRetired
```

The installer validates the source, installs the Codex personal plugin, refreshes the open Agent Skills copy under `~/.agents/skills`, links Claude user skills, preserves existing provider instructions, initializes private shared state, and registers known local projects. Start new provider chats after installation.

For a missing workspace, clone and install:

```powershell
git clone https://github.com/nawnie/aiwf_llm-skill-pack.git "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\scripts\install_agent_skill_pack.ps1 -Providers All -Force -PruneRetired
```

Codex-only and direct-copy fallbacks remain available:

```powershell
.\scripts\install_personal_plugin.ps1
.\install.ps1 -Force -PruneRetired
```

## Architecture

The orchestrator performs bounded routing for non-trivial prompts. Security routes use the common guardrail plus no more than two focused security owners, leaving room for the repository or framework owner. Policy values guide agent behavior; they do not reconfigure a provider model, reasoning effort, context window, or tool budget.

Each skill owns its instructions and any supporting material:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/             # optional source register and deep guidance
  evals/cases.jsonl       # required for #techstartup instruction modules
  scripts/                # optional deterministic helpers
```

Every referenced Python helper is bundled under its owning skill. The 22 skill-owned helpers have no required path into another project or global installation.

## Skill Map

<!-- AIWF-SKILL-CATALOG:BEGIN -->
| Lane | Skill | What it does | Use it when |
| --- | --- | --- | --- |
| Growth | `aiwf-aeo-geo` | Improves answer and generative-search visibility with clear, sourced content. | AI search, answer engines, citation readiness, or GEO work. |
| Research | `aiwf-agent-mok` | Builds durable plans, verification maps, and optional findings datasets. | Complex work needs checkpoints, reconciliation, or a lasting plan. |
| Local AI | `aiwf-ai-evals` | Designs regression suites, comparisons, thresholds, and promotion gates. | Model or pipeline quality must be measured before promotion. |
| Local AI | `aiwf-ai-pipelines` | Audits pipeline stages, runtime wiring, engines, and smoke matrices. | Building or debugging code-first AI generation pipelines. |
| Coding | `aiwf-android-kotlin-coding` | Handles Kotlin, Compose, Gradle, Room, networking, and device validation. | Developing or debugging Android and edge-device apps. |
| Security | `aiwf-application-api-security` | Reviews auth, permissions, input, browser, API, webhook, and LLM boundaries. | Application or API controls need threat review or remediation. |
| Research | `aiwf-atlas-cartographer` | Stores compact local continuity and retrieval cards. | Work must survive chat compaction or resume later. |
| Research | `aiwf-atlas-reader` | Governs Atlas Reader LoRA records, evals, and measured claims. | Working on Atlas Reader training or result evidence. |
| Design | `aiwf-avoid-ai-design` | Removes generic AI-looking UI and document design patterns. | A product, dashboard, PDF, or page needs design cleanup. |
| Design | `aiwf-avoid-ai-illustrations` | Audits generated images for visual, anatomy, text, and semantic defects. | AI-created images, diagrams, logos, or charts need QA. |
| Release | `aiwf-avoid-ai-pushes` | Protects staging, commits, branches, public docs, and release scope. | Preparing a commit, push, PR, or public package. |
| Coding | `aiwf-c-coding` | Covers ISO C, ABI, memory, headers, compilers, and native validation. | Editing or reviewing C source and libraries. |
| Coding | `aiwf-cpp-coding` | Covers modern C++, CMake, ownership, templates, ABI, and extensions. | Editing or reviewing C++ and native extension code. |
| Coding | `aiwf-css-coding` | Diagnoses cascade, layout, responsive behavior, and rendering. | CSS or cross-viewport presentation is incorrect. |
| Security | `aiwf-data-privacy-protection` | Maps data flows, minimization, access, retention, deletion, and audit evidence. | Personal, customer, employee, dataset, or agent data is handled. |
| Data | `aiwf-data-storage` | Protects schemas, migrations, transactions, backups, and vector stores. | Changing SQL, Room, Postgres, Chroma, Qdrant, or Milvus storage. |
| Data | `aiwf-dataset` | Curates datasets with provenance, lifecycle, validation, and synthetic boundaries. | Collecting, cleaning, labeling, or validating training data. |
| Debugging | `aiwf-debug-agent-swarm` | Coordinates bounded read-only parallel debugging passes. | An authorized broad repo crawl needs multiple focused reviewers. |
| Research | `aiwf-deep-research` | Runs weighted source research with claim ledgers and citations. | Current or contested facts require primary-source verification. |
| Physical AI | `aiwf-embedded-edge-ai` | Plans MCU, RTOS, Jetson, firmware, power, thermal, and edge inference. | Building embedded or constrained local-AI systems. |
| Coding | `aiwf-fastapi-coding` | Handles FastAPI routes, Pydantic models, OpenAPI, async, and tests. | Building or debugging a FastAPI backend. |
| Physical AI | `aiwf-field-pilot-readiness` | Defines field hazards, go/no-go gates, rollback, and operator handoff. | Preparing customer-site or partner pilot work. |
| Growth | `aiwf-google-ads-business` | Covers Google Ads, GA4, Tag Manager, conversions, and account hygiene. | Planning or auditing Google acquisition and measurement. |
| Local AI | `aiwf-gpu-runtime-diagnostics` | Diagnoses drivers, VRAM, DLLs, frameworks, and GPU runtime failures. | CUDA or another GPU runtime is missing, broken, or out of memory. |
| Coding | `aiwf-gradio-coding` | Handles Blocks, events, queues, mounts, callbacks, and app tests. | Building or debugging a Gradio interface. |
| Security | `aiwf-incident-response-recovery` | Structures evidence, containment choices, recovery, and post-incident work. | Credentials, systems, data, or dependencies may be compromised. |
| Local AI | `aiwf-inference-serving` | Reviews vLLM, llama.cpp, Ollama, endpoints, queues, and latency. | Deploying or debugging a local model server. |
| Coding | `aiwf-javascript-coding` | Handles JavaScript runtimes, modules, async behavior, DOM, and Node. | Editing or debugging JavaScript outside TypeScript ownership. |
| Local AI | `aiwf-local-ai-training` | Plans LoRA and QLoRA data, checkpoints, resumes, exports, and validation. | Fine-tuning or preparing a local training run. |
| Security | `aiwf-local-device-security` | Protects workstations, accounts, encryption, credentials, services, and local files. | Hardening Windows, Android, Linux, edge, or removable devices. |
| Growth | `aiwf-meta-business` | Covers Meta assets, ads, Pixel/CAPI, lead forms, roles, and policy. | Working with Facebook, Instagram, or WhatsApp Business. |
| Local AI | `aiwf-model-loader` | Maps formats, backends, precision, quantization, components, and adapters. | A model must load correctly across local runtimes. |
| Coordination | `aiwf-multi-agent-workspace` | Shares plans, six-turn context, handoffs, writer leases, and resource limits. | Codex, Claude, Grok, or other agents collaborate locally. |
| Physical AI | `aiwf-networking-iot` | Maps LAN, MQTT, WebSocket, RTSP, telemetry, reconnect, and offline behavior. | Devices, robots, or services communicate over networks. |
| NVIDIA | `aiwf-nvidia-cuda-cudnn-sdk` | Covers CUDA, cuDNN, TensorRT, kernels, tools, and compatibility. | Coding or integrating NVIDIA GPU SDKs. |
| Security | `aiwf-online-infrastructure-security` | Maps internet exposure, DNS/TLS, IAM, cloud/VPS, ports, and monitoring. | Hardening an online service or authorized infrastructure. |
| Routing | `aiwf-orchestrator` | Selects the smallest useful route with a four-skill ceiling. | Every non-trivial pack task starts here automatically in Codex. |
| Physical AI | `aiwf-physics-simulation` | Validates units, frames, dynamics, contacts, simulators, and sim-to-real. | Robotics or physical behavior depends on simulation correctness. |
| Coding | `aiwf-python310-coding` | Protects Python 3.10 syntax, typing, packaging, wheels, and tests. | A project must run specifically on Python 3.10. |
| Coding | `aiwf-python312-coding` | Protects Python 3.12 packaging, removals, typing, wheels, and tests. | A project targets or migrates to Python 3.12. |
| Data | `aiwf-rag-retrieval` | Tunes chunking, embeddings, hybrid retrieval, reranking, and grounding. | RAG answer quality or citation support is weak. |
| Coding | `aiwf-react-coding` | Handles components, hooks, state, effects, rendering, and accessibility. | Building or debugging React and JSX/TSX behavior. |
| Repository | `aiwf-repo-sentinel` | Enforces repo preflight, narrow diffs, contracts, and honest tests. | Modifying any existing repository. |
| Physical AI | `aiwf-robotics-systems` | Designs ROS 2, sensors, actuators, perception, planning, and control. | Building or reviewing an integrated robotics system. |
| Security | `aiwf-security-guardrails` | Establishes authorization, threat boundaries, evidence, and approval gates. | Any task crosses a security boundary. |
| Business | `aiwf-service-intake` | Converts leads into bounded service scope, evidence needs, and next steps. | Qualifying an Ai Embedded Systems customer request. |
| Security | `aiwf-software-ai-supply-chain-security` | Verifies dependencies, builds, releases, SBOMs, models, and dataset provenance. | Software or AI artifacts need trust and provenance review. |
| Growth | `aiwf-startup-finance-funding` | Models runway and compares grants, debt, angels, VC, and diligence. | Planning startup finances or US-first funding paths. |
| Growth | `aiwf-startup-marketing-growth` | Builds positioning, ICPs, funnels, channels, experiments, and KPIs. | Creating measurable startup go-to-market and growth plans. |
| Voice | `aiwf-torchie` | Applies the opt-in Torchie voice to appropriate public copy. | Shawn explicitly asks for Torchie or mascot voice. |
| Coding | `aiwf-typescript-coding` | Handles strict types, tsconfig, modules, JSX/TSX, and generated contracts. | TypeScript configuration or type behavior is involved. |
| Coding | `aiwf-ui-electrician` | Traces frontend/backend payloads, state, progress, errors, and cancellation. | A UI and API disagree or stale state appears. |
| Coding | `aiwf-vue-vitepress-coding` | Handles Vue 3, Composition API, VitePress, reactivity, and builds. | Building or debugging Vue and VitePress projects. |
| Web | `aiwf-web-seo` | Audits HTTP behavior, rendering, metadata, canonicals, sitemaps, and indexing. | Technical SEO or production crawlability is involved. |
| Coding | `aiwf-windows-local-dev` | Diagnoses PowerShell, paths, environments, ports, processes, WSL, and Docker. | Local Windows development or runtime behavior is failing. |
| Growth | `aiwf-youtube-adsense` | Covers channels, APIs, YPP, AdSense, rights, policy, and monetization. | Planning or auditing YouTube and publisher revenue work. |
<!-- AIWF-SKILL-CATALOG:END -->

## Security Authority

The security family permits passive review and non-destructive local or repository checks. Exact authorization is required before remote scans, account tests, exploit payloads, firewall or identity changes, quarantine, credential rotation, isolation, destructive remediation, or notifications. Security output records evidence, confidence, approvals, validation, and residual risk; it does not claim certification or guaranteed safety.

## Shared Agent Workspace

The workspace stores project status, plans, handoffs, decisions, leases, and the newest six complete visible user/assistant exchanges plus active pending turns. It excludes hidden prompts, reasoning, raw tool output, credentials, and attachment bodies. GPU work requires an exclusive lease; UI, browser, docs, lint, API-contract, and unit tests must not load a model.

## Validation

Run all checks before export or installation:

```powershell
.\scripts\validate_skills.ps1
python .\scripts\validate_pack.py
python .\scripts\validate_instruction_modules.py
python .\scripts\test_orchestrator_routes.py
python .\scripts\test_agent_workspace.py
python .\scripts\test_skill_helpers.py
python "C:\Users\Shawn\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
```

`validate_pack.py` checks inventory, metadata, implicit policy, route targets, helper references, source/eval structure, catalog parity, stale paths, generated artifacts, and the skills-only plugin boundary.

## Export

```powershell
.\scripts\export_agent_skills_pack.ps1
```

Archives under `dist/` include the plugin wrapper, all 56 skills, source registers, eval cases, deterministic helpers, provider installer, shared-workspace tooling, core documentation, and license.

## Authoring Rules

- Use `aiwf-` folder/frontmatter names and `aiwf_` OpenAI display names.
- Keep `SKILL.md` concise; place deep sources, evals, and deterministic code in owned resources.
- Keep third-party skills external. Link official sources rather than copying their instructions or branding.
- Verify version-sensitive technical, platform, funding, policy, legal, and security claims from current primary sources.
- Require explicit approval before spending, publishing, account mutation, public exposure, security changes, destructive work, model downloads, training, or expensive GPU jobs.

## License

MIT. See `LICENSE`.

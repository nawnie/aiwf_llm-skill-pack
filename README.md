# AIWF LLM Skill Pack

A skills-only Codex plugin for Shawn's local AI, coding, Android, retrieval, data, web, robotics, embedded, research, and release workflows.

The pack contains 43 focused `aiwf-` skills. `aiwf-orchestrator` is the only implicit entrypoint; all 42 downstream skills are explicit and the router selects at most four for one prompt.

## Install As A Codex Plugin

From the local source workspace:

```powershell
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\scripts\install_personal_plugin.ps1
codex plugin list
```

The installer validates the source, refreshes the personal plugin bundle, updates its cachebuster, writes a validated versioned cache, and ensures the plugin is enabled. It avoids the plugin CLI wrapper that stalls on this machine. Pass `-TryCodexCli` only to test whether that wrapper has been fixed.

For a fresh machine or missing workspace:

```powershell
git clone https://github.com/nawnie/aiwf_llm-skill-pack.git "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\scripts\install_personal_plugin.ps1
```

Direct skill installation is the fallback when plugin commands are unavailable:

```powershell
.\install.ps1 -Force -PruneRetired
```

Start a new Codex chat after installation so the loaded skill catalog refreshes.

## Architecture

`aiwf-orchestrator` performs a bounded routing check for non-trivial prompts. It prefers the smallest useful route and caps downstream selection at four skills. Its control values are agent policy only; they do not reconfigure the Codex model, reasoning effort, context window, or tool budgets.

Each skill owns its instructions and supporting resources:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/       # optional
  scripts/          # optional deterministic helpers
```

Every referenced Python helper is bundled under the owning skill. There are no required helper paths into a global skill installation or another project.

## Skill Catalog

### Routing, Safety, And Release

- `aiwf-orchestrator`: bounded prompt routing across the pack.
- `aiwf-repo-sentinel`: repository preflight, narrow edits, test integrity, and diff discipline.
- `aiwf-security-guardrails`: auth, secrets, injection, unsafe serialization, dependencies, and model-source trust.
- `aiwf-avoid-ai-pushes`: staging, commit, branch, remote, ignored-file, and public-copy checks.

### Research, Data, And Continuity

- `aiwf-deep-research`: weighted source plans, claim ledgers, contradictions, citations, and durable receipts.
- `aiwf-dataset`: dataset intake, provenance, curation, validation, and synthetic boundaries.
- `aiwf-agent-mok`: proportional verification, planning, and optional findings datasets.
- `aiwf-atlas-cartographer`: local continuity cards and retrieval.
- `aiwf-atlas-reader`: Atlas Reader LoRA source, record, eval, and measured-result protocol.
- `aiwf-debug-agent-swarm`: read-only parallel debug-pass coordination when subagents are authorized.

### Languages And Frameworks

- `aiwf-c-coding`
- `aiwf-cpp-coding`
- `aiwf-python310-coding`
- `aiwf-python312-coding`
- `aiwf-fastapi-coding`
- `aiwf-gradio-coding`
- `aiwf-react-coding`
- `aiwf-vue-vitepress-coding`
- `aiwf-typescript-coding`
- `aiwf-javascript-coding`
- `aiwf-css-coding`
- `aiwf-android-kotlin-coding`

### Retrieval, Storage, Web, And Windows

- `aiwf-rag-retrieval`: chunking, embeddings, hybrid retrieval, reranking, grounding, and retrieval evaluation.
- `aiwf-data-storage`: SQLite, Room, Postgres, Chroma, pgvector, Qdrant, Milvus, schemas, and migrations.
- `aiwf-ui-electrician`: frontend/backend contract and state-flow tracing.
- `aiwf-web-seo`: crawlability, canonical URLs, sitemaps, structured data, performance, and evidence-backed web copy.
- `aiwf-windows-local-dev`: PowerShell, paths, environments, ports, processes, Docker/WSL, and local services.

### Local AI And NVIDIA

- `aiwf-ai-pipelines`: backend pipeline and runtime audits.
- `aiwf-model-loader`: model format, backend, precision, quantization, component, and adapter contracts.
- `aiwf-local-ai-training`: LoRA/QLoRA planning, datasets, checkpoints, export, and validation.
- `aiwf-ai-evals`: eval suites, before/after comparisons, and promotion gates.
- `aiwf-inference-serving`: vLLM, llama.cpp, Ollama, endpoint, telemetry, queue, and latency checks.
- `aiwf-gpu-runtime-diagnostics`: driver, CUDA/ROCm, framework, VRAM, DLL/PATH, and GPU smoke diagnosis.
- `aiwf-nvidia-cuda-cudnn-sdk`: CUDA, cuDNN, TensorRT, NVIDIA SDKs, `nvcc`, kernels, and compatibility checks.

### Robotics, Embedded, And Field Work

- `aiwf-robotics-systems`
- `aiwf-physics-simulation`
- `aiwf-networking-iot`
- `aiwf-embedded-edge-ai`
- `aiwf-field-pilot-readiness`
- `aiwf-service-intake`

### Design And Voice

- `aiwf-avoid-ai-design`: UI, dashboard, PDF, and document design cleanup.
- `aiwf-avoid-ai-illustrations`: generated-image artifact and semantic QA.
- `aiwf-torchie`: opt-in AIWF public-copy voice.

## Validation

Run all pack checks before export or installation:

```powershell
.\scripts\validate_skills.ps1
python .\scripts\validate_pack.py
python .\scripts\test_orchestrator_routes.py
python "C:\Users\Shawn\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
```

`validate_pack.py` checks inventory/manifest parity, naming, metadata, implicit policy, route targets, helper references, stale paths, generated artifacts, and the skills-only plugin boundary.

## Export

```powershell
.\scripts\export_agent_skills_pack.ps1
```

Archives are written under `dist/`. The export includes the plugin wrapper, skills, scripts, documentation, manifest, installer, and license.

## Authoring Rules

- Use `aiwf-` folder and frontmatter names, plus `aiwf_` display names.
- Keep `SKILL.md` focused; move deep references and deterministic code to local resources.
- Keep external skills external. Do not vendor their files or branding.
- Verify version-sensitive technical claims against official primary documentation.
- Never assume a quantization, dtype, SDK, ROS distribution, database metric, or device network route is universally correct.
- Do not download large models, run training, expose services, flash devices, or start expensive GPU work unless explicitly requested.

## License

MIT. See `LICENSE`.

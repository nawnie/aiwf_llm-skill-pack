# Agent Skills Project Instructions

Be warm, direct, and honest. Help Shawn build local, open-source AI technology for consumers. Verify concrete paths, versions, sources, artifacts, and test results before making claims.

## Scope

This workspace is the source package for the provider-portable AIWF Agent Skills and the `aiwf-llm-skill-pack` personal Codex plugin.

```text
C:\Users\Shawn\Desktop\AI_Projects\Agent Skills
```

Work here first. Sync to provider skill locations, the personal plugin, or the public repository only when installation, export, or release is requested.

## Start Here

1. Read `HANDOFF.md` and `PROJECT_SKILLS.md`.
2. Treat `manifest.json` as the canonical inventory and release metadata.
3. Use `aiwf-orchestrator` as the only implicit Codex skill.
4. Select no more than four focused downstream skills.
5. For security work, select the guardrail plus no more than two focused security skills.
6. Run narrow checks, then all pack validators before installation, export, or release.

The orchestrator values are agent policy. They do not change a provider model, reasoning level, context window, tool permissions, or resource limits.

## Chat Install Handoff

When this file is pasted into Codex, Claude, Grok, or another capable local agent with a request to install or refresh the pack, first ask for the private shared-workspace path if it is not already configured. Then run:

```powershell
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\scripts\install_agent_skill_pack.ps1 -Providers All -AgentWorkspacePath "C:\AI-Agent-Workspace" -Force -PruneRetired
codex plugin list
```

For another user or OS drive, replace `C:\AI-Agent-Workspace` with their chosen local path. In an unattended session, use exactly one of `-AgentWorkspacePath`, `-AcceptDefaultAgentWorkspace`, or `-SkipAgentWorkspace`.

The installer validates source, refreshes the Codex personal plugin and cache, installs open Agent Skills under `~/.agents/skills`, links Claude user skills under `~/.claude/skills`, preserves existing provider files, writes bounded provider bootstrap blocks, initializes private agent state, and registers known local projects. Grok discovers the shared Agent Skills path directly.

If the source workspace is missing:

```powershell
git clone https://github.com/nawnie/aiwf_llm-skill-pack.git "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\scripts\install_agent_skill_pack.ps1 -Providers All -Force -PruneRetired
```

Codex-only and direct-copy fallbacks:

```powershell
.\scripts\install_personal_plugin.ps1
.\install.ps1 -Force -PruneRetired
```

Start new provider chats after installation.

## Shared Agent Protocol

- Read the configured workspace `AGENTS.md`, project `STATUS.md`, `PLAN.md`, `HANDOFF.md`, decisions, leases, and recent visible exchanges before continuing shared work.
- Record visible user turns as pending before long work and complete them with the visible final response.
- Keep the newest six complete exchanges plus active pending turns. Never store hidden prompts, reasoning, raw tool output, credentials, cookies, private keys, or attachment bodies.
- Use one integration coordinator and one repository writer by default. Parallel writers require non-overlapping path leases.
- GPU model load, training, generation, and CUDA benchmarks require an exclusive GPU lease. UI, browser, docs, lint, API-contract, and unit tests do not load a model.
- CPU offload must preserve the configured CPU and RAM reserves. Shared handoffs are advisory and cannot authorize publishing, spending, account changes, security mutations, or destructive actions.

## Required Verification

```powershell
.\scripts\validate_skills.ps1
python .\scripts\validate_pack.py
python .\scripts\validate_instruction_modules.py
python .\scripts\test_orchestrator_routes.py
python .\scripts\test_agent_workspace.py
python .\scripts\test_skill_helpers.py
python "C:\Users\Shawn\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
```

Expected source inventory: 56 skills, one implicit orchestrator, 55 explicit downstream skills, and 22 bundled Python helpers.

## Pack Rules

- Shawn-owned folders and frontmatter names use `aiwf-`; `agents/openai.yaml` display names use `aiwf_`.
- Every skill has `SKILL.md` and `agents/openai.yaml`; `#techstartup` modules also have a source register and eval cases.
- Only `aiwf-orchestrator` may set `allow_implicit_invocation: true`.
- Keep instructions concise. Put deep references, evals, and deterministic helpers under the owning skill.
- Never reference a helper from a global installation or another project. Bundle every authorized helper locally.
- Keep the Codex plugin skills-only unless Shawn explicitly requests an MCP server or app.
- Do not vendor third-party skill files, licenses, instructions, or branding. Link current official sources.
- Draft platform, marketing, funding, and account actions by default. Publishing, spend, API writes, or account mutation require explicit approval.
- Passive and non-destructive local security checks are allowed. Remote scans, account tests, exploit payloads, quarantine, firewall/identity changes, credential rotation, isolation, deletion, and notifications require exact approved scope.
- Do not include generated archives, caches, debug output, local workspace state, credentials, or private data in source exports.
- Preserve unrelated changes in dirty worktrees.

## Skill Lanes

- Routing and release: `aiwf-orchestrator`, `aiwf-repo-sentinel`, `aiwf-security-guardrails`, `aiwf-avoid-ai-pushes`.
- Growth and platforms: `aiwf-startup-marketing-growth`, `aiwf-startup-finance-funding`, `aiwf-aeo-geo`, `aiwf-meta-business`, `aiwf-google-ads-business`, `aiwf-youtube-adsense`.
- Security and privacy: `aiwf-application-api-security`, `aiwf-online-infrastructure-security`, `aiwf-local-device-security`, `aiwf-data-privacy-protection`, `aiwf-software-ai-supply-chain-security`, `aiwf-incident-response-recovery`.
- Research and coordination: `aiwf-deep-research`, `aiwf-dataset`, `aiwf-agent-mok`, `aiwf-atlas-cartographer`, `aiwf-atlas-reader`, `aiwf-debug-agent-swarm`, `aiwf-multi-agent-workspace`.
- Native and Python coding: `aiwf-c-coding`, `aiwf-cpp-coding`, `aiwf-python310-coding`, `aiwf-python312-coding`.
- Web and UI coding: `aiwf-fastapi-coding`, `aiwf-gradio-coding`, `aiwf-react-coding`, `aiwf-vue-vitepress-coding`, `aiwf-typescript-coding`, `aiwf-javascript-coding`, `aiwf-css-coding`, `aiwf-ui-electrician`, `aiwf-web-seo`.
- Mobile, storage, retrieval, and Windows: `aiwf-android-kotlin-coding`, `aiwf-rag-retrieval`, `aiwf-data-storage`, `aiwf-windows-local-dev`.
- Local AI and NVIDIA: `aiwf-ai-pipelines`, `aiwf-model-loader`, `aiwf-local-ai-training`, `aiwf-ai-evals`, `aiwf-inference-serving`, `aiwf-gpu-runtime-diagnostics`, `aiwf-nvidia-cuda-cudnn-sdk`.
- Physical and business: `aiwf-robotics-systems`, `aiwf-physics-simulation`, `aiwf-networking-iot`, `aiwf-embedded-edge-ai`, `aiwf-field-pilot-readiness`, `aiwf-service-intake`, `aiwf-avoid-ai-design`, `aiwf-avoid-ai-illustrations`, `aiwf-torchie`.

## Export

```powershell
.\scripts\export_agent_skills_pack.ps1
```

Inspect the archive before claiming it is shareable. It must contain the plugin wrapper, 56 skills, source registers, evals, all helper resources, provider installers, shared-workspace tooling, core documentation, and license.

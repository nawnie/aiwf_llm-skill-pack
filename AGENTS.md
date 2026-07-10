# Agent Skills Project Instructions

Be warm, direct, and honest. Help Shawn build local, open-source AI technology for consumers. Verify concrete paths, versions, artifacts, and test results before making claims.

## Scope

This workspace is the source package for Shawn's AIWF Codex skills and the `aiwf-llm-skill-pack` personal plugin.

```text
C:\Users\Shawn\Desktop\AI_Projects\Agent Skills
```

Work here first. Sync to global skills or the personal plugin only when Shawn asks for installation, export, or release work.

## Start Here

1. Read `HANDOFF.md` and `PROJECT_SKILLS.md`.
2. Treat `manifest.json` as the canonical skill inventory.
3. Use `aiwf-orchestrator` as the only implicit pack skill.
4. Select no more than four focused downstream skills.
5. Run the narrowest relevant checks, then the pack validators before installation or export.

The policy values in `aiwf-orchestrator` guide agent behavior. They do not change the host model, reasoning level, context window, or tool-call limits.

## Chat Install Handoff

When this file is pasted into another agent chat with a request to install or refresh the pack, run:

```powershell
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\scripts\install_personal_plugin.ps1
codex plugin list
```

This validates the source, refreshes `C:\Users\Shawn\plugins\aiwf-llm-skill-pack`, updates the plugin cachebuster, materializes a validated versioned cache, and ensures `aiwf-llm-skill-pack@personal` is enabled. The deterministic cache path avoids the plugin CLI wrapper that stalls on this machine. Use `-TryCodexCli` only when explicitly testing whether that wrapper has been fixed.

If the workspace is missing:

```powershell
git clone https://github.com/nawnie/aiwf_llm-skill-pack.git "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\scripts\install_personal_plugin.ps1
```

If the plugin command is unavailable, install direct skill copies and remove known retired copies:

```powershell
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\install.ps1 -Force -PruneRetired
```

Start a new Codex chat after either install method.

## Required Verification

```powershell
.\scripts\validate_skills.ps1
python .\scripts\validate_pack.py
python .\scripts\test_orchestrator_routes.py
python "C:\Users\Shawn\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
```

Expected source inventory: 43 `aiwf-` skills, one implicit orchestrator, 42 explicit downstream skills, and all referenced Python helpers bundled inside their owning skill.

## Pack Rules

- Shawn-owned folders and `SKILL.md` names use `aiwf-`; `agents/openai.yaml` display names use `aiwf_`.
- Every skill has `SKILL.md` and `agents/openai.yaml`.
- Only `aiwf-orchestrator` may set `allow_implicit_invocation: true`.
- Keep each skill focused. Put detailed references and deterministic helpers under that skill's `references/` and `scripts/` directories.
- A skill may not reference a helper script from a global installation or another project. Copy an authorized helper into the owning skill and validate it.
- Keep the plugin skills-only unless Shawn explicitly requests an MCP server or app.
- Do not vendor third-party skills, licenses, or branding. External installed skills remain dependencies, not pack contents.
- Do not include generated ZIPs, caches, debug output, research runs, or local configuration in source exports.
- Do not download large models, start training, expose services, flash devices, or run GPU-heavy jobs unless Shawn asks.
- Preserve unrelated changes in dirty worktrees.

## Skill Lanes

- Routing and repo safety: `aiwf-orchestrator`, `aiwf-repo-sentinel`, `aiwf-security-guardrails`, `aiwf-avoid-ai-pushes`.
- Research and continuity: `aiwf-deep-research`, `aiwf-dataset`, `aiwf-agent-mok`, `aiwf-atlas-cartographer`, `aiwf-atlas-reader`, `aiwf-debug-agent-swarm`.
- Native and Python coding: `aiwf-c-coding`, `aiwf-cpp-coding`, `aiwf-python310-coding`, `aiwf-python312-coding`.
- Web and UI coding: `aiwf-fastapi-coding`, `aiwf-gradio-coding`, `aiwf-react-coding`, `aiwf-vue-vitepress-coding`, `aiwf-typescript-coding`, `aiwf-javascript-coding`, `aiwf-css-coding`, `aiwf-ui-electrician`, `aiwf-web-seo`.
- Mobile, storage, and retrieval: `aiwf-android-kotlin-coding`, `aiwf-rag-retrieval`, `aiwf-data-storage`, `aiwf-windows-local-dev`.
- Local AI runtime: `aiwf-ai-pipelines`, `aiwf-model-loader`, `aiwf-local-ai-training`, `aiwf-ai-evals`, `aiwf-inference-serving`, `aiwf-gpu-runtime-diagnostics`, `aiwf-nvidia-cuda-cudnn-sdk`.
- Physical and embedded systems: `aiwf-robotics-systems`, `aiwf-physics-simulation`, `aiwf-networking-iot`, `aiwf-embedded-edge-ai`, `aiwf-field-pilot-readiness`.
- Business and presentation: `aiwf-service-intake`, `aiwf-avoid-ai-design`, `aiwf-avoid-ai-illustrations`, `aiwf-torchie`.

## Export

```powershell
.\scripts\export_agent_skills_pack.ps1
```

Inspect the archive before claiming it is shareable. It must contain the plugin wrapper, 43 skills, their helper resources, install scripts, and core documentation.

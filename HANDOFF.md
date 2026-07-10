# AIWF Skill Pack Handoff

Updated: 2026-07-10

## Current State

`C:\Users\Shawn\Desktop\AI_Projects\Agent Skills` is the source of truth for `#techstartup` release `0.3.0`.

- Source skills: 56
- Implicit skills: one, `aiwf-orchestrator`
- Explicit downstream skills: 55
- Maximum route size: four
- Bundled Python helpers: 22
- New instruction modules: 13, each with official-source register and eval cases
- Plugin capabilities: skills only
- Provider targets: Codex plugin plus open Agent Skills for Claude and Grok

The manifest owns inventory and release metadata. The executable router lives in `skills/aiwf-orchestrator/scripts/route_prompt.py`; exact route fixtures live in `scripts/orchestrator_route_cases.json`.

## #techstartup Additions

- Startup growth: marketing, finance/funding, AEO/GEO, Meta, Google Ads, and YouTube/AdSense.
- Security: application/API, online infrastructure, local devices, data privacy, software/AI supply chain, and incident recovery.
- Coordination: provider-neutral shared workspace with six visible exchanges, pending-turn recovery, project registry, handoffs, writer/resource leases, ACLs, redaction, and CPU/RAM/GPU reserves.
- GitHub docs: a validated four-column table explains every individual skill.

Platform and funding facts are source-gated because policies, APIs, programs, and legal thresholds move. Security output is evidence- and authorization-based; it does not claim certification, compliance, or guaranteed safety.

## Install

```powershell
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\scripts\install_agent_skill_pack.ps1 -Providers All -AgentWorkspacePath "C:\AI-Agent-Workspace" -Force -PruneRetired
codex plugin list
```

The installer preserves unrelated skills and provider instructions, writes managed bootstrap blocks, refreshes the Codex cache, initializes the private local workspace, and registers known projects. Start new provider chats after installation.

## Validation

```powershell
.\scripts\validate_skills.ps1
python .\scripts\validate_pack.py
python .\scripts\validate_instruction_modules.py
python .\scripts\test_orchestrator_routes.py
python .\scripts\test_agent_workspace.py
python .\scripts\test_skill_helpers.py
python "C:\Users\Shawn\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
```

## Release

Export with `scripts\export_agent_skills_pack.ps1`, inspect the archive, sync source into the clean public working copy, update PR #1, and merge only after source, mirror, cache, and provider-install parity pass.

## Boundaries

- Keep third-party skills external and attributed.
- Keep generated artifacts under `dist/` and private workspace state outside the repository.
- Keep one implicit router and the four-skill ceiling.
- Do not start spend, publishing, account mutation, public exposure, destructive security action, large downloads, training, or GPU-heavy work without explicit authority.

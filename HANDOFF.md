# AIWF Skill Pack Handoff

Updated: 2026-07-09

## Current State

`C:\Users\Shawn\Desktop\AI_Projects\Agent Skills` is the source of truth for the `aiwf-llm-skill-pack` skills-only Codex plugin.

- Pack version: `0.2.0`
- Source skills: 43
- Implicit skills: one, `aiwf-orchestrator`
- Explicit downstream skills: 42
- Maximum route size: four
- Bundled Python helpers: 17
- Plugin capabilities: skills only

The skill inventory is canonical in `manifest.json`. The route behavior is executable in `skills/aiwf-orchestrator/scripts/route_prompt.py` and tested by `scripts/orchestrator_route_cases.json`.

## Review Result

The July 9 audit consolidated overlapping umbrella guidance into focused owners, shortened every `SKILL.md` to 115 lines or fewer, and added six missing project lanes:

- `aiwf-android-kotlin-coding`
- `aiwf-rag-retrieval`
- `aiwf-data-storage`
- `aiwf-windows-local-dev`
- `aiwf-vue-vitepress-coding`
- `aiwf-web-seo`

Generic repository safety now belongs to `aiwf-repo-sentinel`. Cross-layer frontend/backend tracing belongs to `aiwf-ui-electrician`. Language, framework, runtime, storage, and physical-system work stays in its focused skill.

Corrected guidance includes Python 3.10 versus 3.12 feature boundaries, Python 3.12 environment packaging behavior, current FastAPI/Pydantic framing, TensorRT compatibility modes and plan trust, moving ROS 2 releases, current CSS snapshots, portable helper paths, and device-aware Android networking.

## Helper Policy

Every skill-owned Python helper is copied into that skill's `scripts/` directory. Skill instructions use `<this-skill>` or a relative `scripts/...` path. `scripts/validate_pack.py` fails when a referenced helper is missing or a bundled helper is undocumented.

## Install

```powershell
cd "C:\Users\Shawn\Desktop\AI_Projects\Agent Skills"
.\scripts\install_personal_plugin.ps1
codex plugin list
```

Direct-skill fallback:

```powershell
.\install.ps1 -Force -PruneRetired
```

Start a new Codex chat after installation.

The installer uses a validated versioned personal cache and preserves an enabled plugin entry in `C:\Users\Shawn\.codex\config.toml`. The Codex CLI wrapper is skipped by default because it stalls on this machine; `-TryCodexCli` is an explicit diagnostic option.

## Validation

```powershell
.\scripts\validate_skills.ps1
python .\scripts\validate_pack.py
python .\scripts\test_orchestrator_routes.py
python "C:\Users\Shawn\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
```

For a research receipt:

```powershell
python .\skills\aiwf-deep-research\scripts\validate_research_receipt.py "<run-dir>"
```

For a shareable archive:

```powershell
.\scripts\export_agent_skills_pack.ps1
```

## Boundaries

- Keep third-party skills external and attributed.
- Keep generated artifacts under `dist/`, never at repository root.
- Treat router controls as instruction policy, not host-runtime configuration.
- Keep Torchie opt-in.
- Do not start expensive or externally exposed work without explicit approval.

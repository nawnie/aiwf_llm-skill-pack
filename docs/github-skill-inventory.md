# GitHub Skill Inventory

Checked on 2026-07-06 against Shawn's `nawnie` GitHub repositories. Refreshed on 2026-07-07 against installed local AIWF-prefixed skills.

Repos reviewed for skill-like files by name or intent:

- `nawnie/aiwf_llm-skill-pack`
- `nawnie/AIWF-Studio`
- `nawnie/ai-without-fear`
- `nawnie/Model-Operating-Kernel`
- `nawnie/MOKSHA`
- `nawnie/atlas-lora-adapter`

Result:

- Added `aiwf-avoid-ai-design`, `aiwf-avoid-ai-pushes`, `aiwf-dataset`, and `aiwf-orchestration` from the existing public skill-pack and installed local AIWF sources.
- Confirmed `aiwf-atlas-cartographer` and `aiwf-agent-mok` are included in this pack.
- Imported the Atlas Reader protocol skill from `nawnie/atlas-lora-adapter/plugins/aiwf-atlas-protocol/skills/atlas-reader/SKILL.md` as `aiwf-atlas-reader`.
- Added installed local AIWF-owned lanes `aiwf-comfy-workflow-pipeline` and `aiwf-torchie`.
- Left the global `aiwf` router out of the vendored pack because `aiwf-orchestration` and `aiwf-orchestrator` are the pack-level routers.
- No other `SKILL.md` files were found in the reviewed AIWF, MoK, MOKSHA, or Atlas-related GitHub repos.

Packaging rule:

- Only Shawn-owned `aiwf-` skills are vendored here.

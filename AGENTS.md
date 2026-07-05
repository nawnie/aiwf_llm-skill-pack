# AIWF LLM Skill Pack Agent Guide

Use `aiwf-orchestration` first for any non-trivial task in this pack. It is the always-on control skill.

## Control Variables

The orchestration variables live near the top of `skills/aiwf-orchestration/SKILL.md`.

```yaml
AIWF_ORCHESTRATION_VERSION: 1
AIWF_MAX_AGENT_SPAWN: 3
AIWF_MAX_LOOPS_WITHOUT_PROGRESS: 2
AIWF_AI_AVOIDANCE_LEVEL: 1.0
AIWF_DEEP_RESEARCH_EXTRA_URLS: ""
AIWF_ALWAYS_ON_SKILLS:
  aiwf-orchestration: true
  aiwf-deep-research: false
  aiwf-dataset: false
  aiwf-avoid-ai-design: false
  aiwf-avoid-ai-pushes: false
  avoid-ai-writing: false
```

`aiwf-orchestration` stays always on. Do not turn it off.

## How To Use The Pack

Call `aiwf-orchestration` first, then let it choose the smallest useful downstream skill set.

Common calls:

- `Use $aiwf-orchestration to route this local AI task.`
- `Use $aiwf-deep-research with these extra URLs: <url>, <url>.`
- `Use $aiwf-dataset to validate this dataset intake folder.`
- `Use $aiwf-avoid-ai-design at avoidance level 2.0 on this UI.`
- `Use $aiwf-avoid-ai-pushes before committing these docs.`

## Always-On Skill Toggles

Set a skill to `true` in `AIWF_ALWAYS_ON_SKILLS` only when it should be considered for every non-trivial task.

Keep most skills off by default. Too many always-on skills make the agent slower and stricter than needed.

## AI-Avoidance Level

`AIWF_AI_AVOIDANCE_LEVEL` applies to writing cleanup, UI design cleanup, and push hygiene.

- `0.1`: effectively off unless the user explicitly asks.
- `1.0`: normal practical cleanup.
- `2.0`: extreme cleanup. This is intentionally strict and may be too high for everyday work.

The external `avoid-ai-writing` skill is downloaded by `install.ps1`; it is not vendored in this repo.

## Deep Research URL Seeds

Set `AIWF_DEEP_RESEARCH_EXTRA_URLS` to a comma-separated list when research must include known sources.

Example:

```yaml
AIWF_DEEP_RESEARCH_EXTRA_URLS: "https://arxiv.org/abs/2405.00000, https://github.com/example/project"
```

`aiwf-deep-research` must preserve those URLs in the source plan as required seed sources.

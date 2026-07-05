# AIWF LLM Skill Pack

AIWF LLM Skill Pack is a small set of Codex skills for local open-source AI work. It is built around an always-on orchestration skill, then routes into focused skills for deep research, dataset work, design cleanup, and push hygiene.

The pack is meant for Windows-first local AI work, but the skill files are plain `SKILL.md` files and can be adapted by any agent runtime that reads that format.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `aiwf-orchestration` | Always-on control layer. Reads variables, chooses downstream skills, sets loop and agent limits, and applies the AI-avoidance level. |
| `aiwf-deep-research` | Source-backed research with source plans, claim ledgers, evidence weights, contradictions, and receipt validation. |
| `aiwf-dataset` | Dataset intake, provenance checks, curation, validation, reporting, and synthetic guardrail boundaries. |
| `aiwf-avoid-ai-design` | Design audit for AI-looking UI, PDF, dashboard, document, Gradio, and web layouts. |
| `aiwf-avoid-ai-pushes` | Git and GitHub hygiene before commits or pushes, with checks for ignored files, generated files, and public prose. |

`avoid-ai-writing` is not vendored in this repo. The install script downloads it from its upstream project and this README acknowledges it below.

## Install

From PowerShell:

```powershell
git clone https://github.com/Nawnie/aiwf_llm-skill-pack.git
cd aiwf_llm-skill-pack
.\install.ps1
```

By default, the installer copies this pack to:

```powershell
$env:USERPROFILE\.codex\skills
```

It also downloads `avoid-ai-writing` into:

```powershell
$env:USERPROFILE\.codex\skills\avoid-ai-writing
```

Replace existing installed copies:

```powershell
.\install.ps1 -Force
```

Install to a custom skills directory:

```powershell
.\install.ps1 -CodexSkillsDir "D:\codex-skills"
```

Skip the external `avoid-ai-writing` download:

```powershell
.\install.ps1 -SkipAvoidAiWriting
```

Restart Codex after installation so the skill list refreshes.

## Validate The Pack

Run the local validator before publishing changes:

```powershell
python .\scripts\validate_pack.py
```

The validator checks that:

- all packaged skill names start with `aiwf-`
- required skill folders exist
- `avoid-ai-writing` is not vendored
- orchestration variables are present
- generated Python cache folders are absent

## Basic Use

Start with orchestration:

```text
Use $aiwf-orchestration to route this task.
```

Then let it choose downstream skills.

Examples:

```text
Use $aiwf-orchestration to inspect this local image-generation repo and tell me which smoke checks to run.
```

```text
Use $aiwf-deep-research to compare these two model-loading approaches. Include https://example.com/paper and https://github.com/example/repo.
```

```text
Use $aiwf-avoid-ai-design at avoidance level 2.0 to audit this Gradio UI.
```

```text
Use $aiwf-avoid-ai-pushes before committing these README changes.
```

## Orchestration Variables

The main control block lives at the top of:

```text
skills/aiwf-orchestration/SKILL.md
```

Default values:

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

### `AIWF_MAX_AGENT_SPAWN`

Caps helper agents or parallel research workers for one task.

- `0`: no spawned helpers
- `1`: one helper
- `3`: default bounded worker count

### `AIWF_MAX_LOOPS_WITHOUT_PROGRESS`

Stops work after repeated loops with no new evidence, no passing check, no useful diff, or the same blocker.

Default: `2`.

### `AIWF_ALWAYS_ON_SKILLS`

Controls which skills should be considered on every non-trivial task.

`aiwf-orchestration` must stay `true`. Keep the rest `false` unless you want that skill considered all the time.

Example: make deep research always considered.

```yaml
AIWF_ALWAYS_ON_SKILLS:
  aiwf-orchestration: true
  aiwf-deep-research: true
  aiwf-dataset: false
  aiwf-avoid-ai-design: false
  aiwf-avoid-ai-pushes: false
  avoid-ai-writing: false
```

### `AIWF_DEEP_RESEARCH_EXTRA_URLS`

Adds required seed URLs for `aiwf-deep-research`.

```yaml
AIWF_DEEP_RESEARCH_EXTRA_URLS: "https://arxiv.org/abs/2405.00000, https://github.com/example/project"
```

The deep-research initializer also reads this environment variable:

```powershell
$env:AIWF_DEEP_RESEARCH_EXTRA_URLS = "https://arxiv.org/abs/2405.00000, https://github.com/example/project"
python .\skills\aiwf-deep-research\scripts\init_research_run.py --title "wan attention research" --request "Compare WAN attention runtimes."
```

Or pass a URL directly:

```powershell
python .\skills\aiwf-deep-research\scripts\init_research_run.py --title "wan attention research" --request "Compare WAN attention runtimes." --extra-url "https://arxiv.org/abs/2405.00000"
```

Those URLs are written into `source_plan.json` as `required_seed_urls`.

### `AIWF_AI_AVOIDANCE_LEVEL`

Shared strictness level for:

- `avoid-ai-writing`
- `aiwf-avoid-ai-design`
- `aiwf-avoid-ai-pushes`

Levels:

- `0.1`: effectively off. Only use the AI-avoidance skills when explicitly requested or when a credibility or secret-risk issue is obvious.
- `1.0`: default practical level. Fix clear AI-looking writing, design, and repo hygiene issues.
- `2.0`: extreme level. Treat borderline AI-looking output as a failure. This can be too strict for normal work, but it is useful when you want a stress test.

Example:

```yaml
AIWF_AI_AVOIDANCE_LEVEL: 2.0
```

Then call:

```text
Use $aiwf-orchestration with AIWF_AI_AVOIDANCE_LEVEL 2.0 to review this README and UI.
```

## External Acknowledgements

This pack downloads `avoid-ai-writing` from:

https://github.com/conorbronsdon/avoid-ai-writing

`avoid-ai-writing` is authored by Conor Bronsdon and is MIT licensed. It is a separate project and is not copied into this repo.

The `aiwf-avoid-ai-design` skill was created after reviewing the public MIT-licensed `funboy322/avoid-ai-design` project and adapts the idea of pattern-based cleanup for AI-looking interfaces and documents.

## Publish Hygiene

Before pushing changes to this repo:

```powershell
git status --short --branch --untracked-files=all
git diff --stat
git diff --check
python .\scripts\validate_pack.py
```

For public prose, run the AI-avoidance scan at level `1.0` unless you intentionally need `0.1` or `2.0`.

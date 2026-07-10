---
name: aiwf-orchestrator
description: Implicit routing control for the AIWF skill pack. Use at the start of non-trivial local AI, coding, model, training, dataset, retrieval, robotics, embedded, mobile, web, research, debugging, deployment, documentation, or skill-pack work to select the smallest focused downstream skill route without requiring the user to name skills.
---

# AIWF Orchestrator

## Control Policy

```yaml
AIWF_MAX_DOWNSTREAM_SKILLS: 4
AIWF_MAX_AGENT_SPAWN: 3
AIWF_MAX_LOOPS_WITHOUT_PROGRESS: 2
AIWF_AI_AVOIDANCE_LEVEL: 1.0
AIWF_DEEP_RESEARCH_EXTRA_URLS: ""
AIWF_TORCHIE_DEFAULT: false
```

These are agent-read policy values. They guide this skill when it is loaded; they do not reconfigure the Codex host, model, context window, or tool limits. Provider-specific settings remain controlled by the host.

## Core Rule

Route first, then load only the skills that materially change the work. This orchestrator is the pack's only implicitly invoked skill; downstream skills are explicit routes so they do not compete for every prompt.

## Workflow

1. Honor skills explicitly named by the user.
2. Read project guidance and use `references/routing-map.md` for inferred routes.
3. For broad prompts, run the advisory classifier:

```powershell
python <this-skill>\scripts\route_prompt.py --prompt "<user request>"
```

4. Select no more than `AIWF_MAX_DOWNSTREAM_SKILLS`. Prefer the skill that owns the first risky or irreversible decision, then add only real cross-boundary owners.
5. Announce the route and reason in one line.
6. Read every selected downstream `SKILL.md` completely before editing, running services, starting expensive work, or publishing.
7. Stop repeated attempts after `AIWF_MAX_LOOPS_WITHOUT_PROGRESS` loops with no new evidence, useful diff, or passing check. Change the route or report the exact blocker.

## Route Shape

Use focused skills instead of the retired broad wrappers:

- Repository preflight and diff integrity: `aiwf-repo-sentinel`.
- C, C++, Python 3.10, Python 3.12, CUDA, FastAPI, Gradio, React, Vue/VitePress, CSS, JavaScript, TypeScript, or Android/Kotlin: the matching focused coding skill.
- Cross-layer API/UI wiring: `aiwf-ui-electrician` after the relevant backend and frontend skills.
- Model loading, training, evals, serving, pipelines, GPU failures, RAG, or data stores: the matching runtime skill.
- Robotics, physics, networking, embedded systems, field pilots, or Windows local runtime work: the matching systems skill.
- External research: `aiwf-deep-research`; durable plan verification: `aiwf-agent-mok` only when needed.
- Design, generated-image QA, SEO, release hygiene, service intake, or Torchie voice: the matching output skill.

If a task spans more than four owners, route in phases instead of loading the whole pack.

## Gates

- No large model or dataset downloads unless asked.
- No training, GPU-heavy generation, or long benchmarks unless asked.
- No public network exposure, firewall changes, or credential changes unless asked.
- No destructive data, filesystem, device, database, or git operations unless asked.
- No major dependency upgrades, package-manager switches, broad rewrites, weakened tests, or security-boundary reductions as hidden side effects.
- Keep Torchie off unless Shawn asks or `AIWF_TORCHIE_DEFAULT` is deliberately enabled.
- Pass `AIWF_DEEP_RESEARCH_EXTRA_URLS` into a deep-research source plan when it is non-empty.

## Output

Use:

```text
Route: aiwf-orchestrator -> <skill names>; reason: <short reason>
```

For routing-only questions, return the route. For implementation work, continue through the selected skills and report actual validation.

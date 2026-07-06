# Skill Findings: Universal Agentic Skills And Provider-Specific Capabilities

Created: 2026-07-06
Workspace: `C:\Users\Shawn\Desktop\AI_Projects\Agent Skills`
Research receipt: `research runs\20260706-083638-agentic-skill-best-practices`

## Direct Answer

The best way to make agentic skills universal is to split every skill into two layers:

1. A provider-neutral core that follows the open Agent Skills pattern: `SKILL.md` with `name`, `description`, concise workflow instructions, and optional `references/`, `scripts/`, and `assets/`.
2. Provider-specific adapters that exploit each environment's extra capabilities without contaminating the portable core.

The portable core should answer: "When should this skill activate, what must the agent do, what files can it load, what scripts can it run, and what output proves success?"

The provider adapter should answer: "How does this provider discover the skill, expose it in UI, attach tools, run evals, manage state, access MCP, or apply persistent project instructions?"

That structure lets one skill travel across Codex, Claude, Cursor, Copilot-style coding agents, MCP-aware apps, and framework-based agents while still using each provider's extra capabilities.

## Research Confidence

High confidence:

- Portable skill anatomy.
- Progressive disclosure.
- Script-backed deterministic behavior.
- `name` and `description` as activation-critical metadata.
- MCP tools/resources/prompts as a provider-neutral active capability boundary.
- Provider-specific sidecars as the right way to preserve portability.

Medium confidence:

- Exact Cursor implementation details. Official Cursor search results confirm Rules and Agent Skills surfaces, but the browsing tool did not expose line-readable page content in this run.

Important contradiction:

- AgentSkills.io permits optional frontmatter and metadata, while the local Codex skill-creator says to keep YAML frontmatter to `name` and `description`. The resolution for universal skills is to keep the portable core strict and put optional/provider metadata in sidecars unless a target provider validates it.

## Source Backbone

This file is based on the following source groups:

- Local Codex `skill-creator` and `openai_yaml.md` references for this machine's actual skill-authoring rules.
- AgentSkills.io open specification for portable skill packaging.
- Anthropic Claude Skills overview and best practices.
- OpenAI Codex Skills, OpenAI API Skills, OpenAI skill eval guidance, OpenAI Apps SDK, and OpenAI Agents SDK docs.
- Model Context Protocol tools, resources, and prompts specifications.
- VS Code custom instructions, GitHub Copilot custom instructions, and AGENTS.md project instruction docs.
- Google ADK overview, callbacks, and evaluation docs.
- Cursor official Rules and Agent Skills search-result snippets, used only as lower-confidence provider-surface confirmation.

Full source register and weights are in:

`research runs\20260706-083638-agentic-skill-best-practices\sources.jsonl`

## The Universal Skill Contract

A universal skill should be usable by an agent that knows nothing except:

- where the skill folder is
- how to read `SKILL.md`
- how to optionally inspect referenced files
- how to run scripts if the runtime allows local execution

The minimum portable shape is:

```text
skill-name/
  SKILL.md
  references/
  scripts/
  assets/
```

`SKILL.md` is the core contract. It should contain only what an agent must know to choose and operate the skill.

`references/` contains detailed knowledge that should not always be loaded.

`scripts/` contains deterministic helpers, validators, generators, probes, converters, or scaffolds.

`assets/` contains templates, images, schemas, boilerplate, fixtures, or other non-context resources.

Provider-specific files can be added, but they should not be required for the universal core to make sense.

## Naming And Trigger Design

The skill name should be short, lowercase, hyphenated, and action/domain oriented.

Good:

```text
aiwf-deep-research
aiwf-avoid-ai-illustrations
github-address-comments
pdf-redline-review
```

Weak:

```text
helper
researcher
smart-agent
misc-tools
```

The description is the most important activation surface. It should include:

- what the skill does
- when to use it
- exact trigger phrases users might say
- domain terms
- file types
- provider or runtime constraints if any
- boundaries that prevent over-activation

Bad description:

```yaml
description: Helps with research.
```

Better:

```yaml
description: Source-backed research workflow for technical due diligence. Use when Codex must compare official docs, papers, repos, model cards, APIs, standards, or implementation evidence; create a source plan; assign evidence weights; preserve contradictions; and write a validated research receipt.
```

Why this matters:

- Codex and Claude both use skill metadata to decide when to load a skill.
- Open skill specs and local creator docs treat `name` and `description` as the always-visible layer.
- The body loads later, so "when to use" guidance hidden inside the body is too late for discovery.

## Progressive Disclosure

Universal skills should use progressive disclosure:

1. Metadata is always visible.
2. `SKILL.md` loads when the skill triggers.
3. References, scripts, and assets load only when needed.

Practical rule:

- Keep `SKILL.md` under 500 lines unless the skill has a strong reason to be larger.
- Keep the skill body as a route map and workflow.
- Put long policies, schemas, examples, provider notes, and checklists in `references/`.
- Keep reference files one level deep and named by purpose.

Good layout:

```text
skills/aiwf-deep-research/
  SKILL.md
  references/
    source-policy.md
    domain-targets.md
    research-loop.md
    reddit-policy.md
  scripts/
    init_research_run.py
    validate_research_receipt.py
```

Bad layout:

```text
skills/mega-skill/
  SKILL.md     # 8,000 lines of every possible topic
  notes.md     # vague dumping ground
  misc.md      # vague dumping ground
```

## Universal Core Versus Provider Adapter

Treat `SKILL.md` as the portable core.

Treat provider extras as adapters.

Recommended layout for multi-provider skills:

```text
skill-name/
  SKILL.md
  references/
    workflow.md
    provider-openai.md
    provider-claude.md
    provider-copilot.md
    provider-cursor.md
    provider-mcp.md
  scripts/
    validate_skill.py
    smoke_provider_matrix.py
  assets/
    fixtures/
  agents/
    openai.yaml
  evals/
    prompts.jsonl
    expected.jsonl
```

Notes:

- `agents/openai.yaml` is a provider-specific sidecar for OpenAI/Codex surfaces in this workspace.
- `provider-*.md` reference files are loaded only when the runtime/provider matters.
- `evals/` is useful for local projects, but if a target skill system rejects extra folders, keep evals outside the distributed skill or adapt packaging.
- Some skill creators recommend avoiding extra documentation files inside the skill. That is about avoiding clutter, not forbidding useful references. Keep references operational and directly linked from `SKILL.md`.

## Provider Capability Matrix

| Surface | Best Use | Keep Universal? | Adapter Pattern |
| --- | --- | --- | --- |
| Agent Skills `SKILL.md` | Core portable workflow | Yes | Strict `name` and `description`; concise body |
| `references/` | Deep instructions, policies, schemas, examples | Yes | Load only when needed |
| `scripts/` | Deterministic operations, validators, probes | Yes | Include dependency notes and helpful errors |
| `assets/` | Templates, icons, fixtures, boilerplate | Yes | Do not load into context unless needed |
| `agents/openai.yaml` | OpenAI/Codex UI metadata, default prompt, MCP dependencies, implicit invocation | No | OpenAI sidecar |
| MCP tools | Provider-neutral actions with schemas | Mostly | Put MCP descriptors/server config in adapter |
| MCP resources | Provider-neutral context/data exposed by URI | Mostly | Use for shared read models and context bundles |
| MCP prompts | Reusable prompt templates | Mostly | Use for starter workflows, not whole skill bodies |
| OpenAI Apps SDK | ChatGPT app tools, UI bridge, tool metadata | No | Apps-specific adapter |
| OpenAI Agents SDK | Runtime loops, tools, handoffs, sessions, guardrails, tracing | No | Runtime wrapper around skill logic |
| Claude Skills | Claude-specific packaging and runtime behavior | Mostly | Keep core compatible; add Claude deployment notes |
| VS Code/GitHub Copilot instructions | Persistent repo instructions | No | Put project rules in AGENTS.md or Copilot files |
| Google ADK | Agent framework, callbacks, evals, deployment | No | Runtime wrapper |
| Cursor Rules/Skills | Cursor-specific editor rules and skill behavior | No | Keep Cursor adapter current with live docs |

## OpenAI And Codex Adapter Strategy

OpenAI/Codex has three useful layers:

1. Codex Skills.
2. Apps SDK / MCP-compatible tool descriptors.
3. Agents SDK runtime wrappers.

Use Codex Skills for reusable workflow knowledge:

```text
skills/my-skill/
  SKILL.md
  references/
  scripts/
  agents/openai.yaml
```

Use `agents/openai.yaml` for:

- user-facing display name
- short description
- default prompt
- MCP tool dependencies
- implicit invocation policy

Example:

```yaml
interface:
  display_name: "aiwf_deep-research"
  short_description: "Weighted source-backed deep research"
  default_prompt: "Use $aiwf-deep-research to plan and verify a weighted source-backed research pass."
dependencies:
  tools:
    - type: "mcp"
      value: "github"
      description: "GitHub MCP server"
policy:
  allow_implicit_invocation: true
```

Use Apps SDK when the skill must become an app/tool surface:

- Design one tool for one job.
- Use structured input and output schemas.
- Add annotations that help the model know read-only, destructive, or open-world behavior.
- Use metadata for UI and component behavior.
- Keep tool names and descriptions precise.

Use Agents SDK when the skill needs runtime behavior:

- handoffs
- approvals
- sessions/state
- guardrails
- tracing
- long-running orchestration
- sandboxed execution

Do not cram those into `SKILL.md`. `SKILL.md` should say when to use the workflow and what to do; the SDK runtime should execute and observe the workflow.

## Claude Skills Adapter Strategy

Claude Skills align closely with the open Agent Skills structure:

```text
skill-name/
  SKILL.md
  scripts/
  references/
  assets/
```

The important Claude-facing practices are:

- Keep `SKILL.md` concise.
- Use progressive disclosure.
- Include explicit examples and workflows.
- Use scripts for deterministic tasks.
- Test across the models and environments where the skill should work.

Claude-specific provider notes should live in a provider reference:

```text
references/provider-claude.md
```

That file can cover:

- Claude.ai packaging notes
- Claude Code behavior
- API behavior
- dependency or environment constraints
- model-specific testing notes

Do not make the universal `SKILL.md` assume Claude-only runtime features unless the skill is intentionally Claude-only.

## MCP Adapter Strategy

MCP is the cleanest protocol boundary for reusable active capabilities.

Use MCP tools for actions:

- create issue
- query database
- fetch build status
- run a bounded search
- update a calendar event

Use MCP resources for context:

- file metadata
- database schemas
- saved reports
- model cards
- project state

Use MCP prompts for reusable starting templates:

- "create weekly report"
- "triage this incident"
- "draft PR review"

Skill design rule:

- Put "when and why" in the skill.
- Put "how to call external capability" in MCP.
- Put "how to render or operate provider UI" in provider adapters.

MCP helps universality because many providers can connect to the same server, but MCP alone is not a skill. A skill should tell the agent when to use the MCP capability and how to validate the result.

## GitHub Copilot, VS Code, And AGENTS.md

Project instructions are baseline context. Skills are task-scoped workflows.

Use AGENTS.md or Copilot custom instructions for:

- repo layout
- coding standards
- test commands
- branch/commit policy
- security rules
- package-manager rules
- local environment notes

Use skills for:

- repeatable workflows
- domain-specific process
- multi-step procedures
- scripts and validators
- research or audit receipts

Do not duplicate everything between AGENTS.md and skills. The clean boundary is:

- AGENTS.md: "How to behave in this repo."
- Skill: "How to do this specialized task."

If a skill always applies in a repo, AGENTS.md can route to it:

```markdown
For source-backed research, use $aiwf-deep-research.
For public docs cleanup, use $aiwf-avoid-ai-pushes.
```

## Google ADK Adapter Strategy

Google ADK is a runtime framework, not a static skill format.

Use ADK when you need:

- code-defined agents
- tools
- sessions
- memory/state
- callbacks
- evaluation datasets and criteria
- deployment through the ADK ecosystem

The universal skill can specify:

- the workflow
- provider-independent acceptance gates
- what outputs count as success

The ADK adapter should implement:

- callbacks
- tool declarations
- evaluation criteria
- runtime state
- deployment details

## Cursor Adapter Strategy

Cursor has official Rules and Agent Skills surfaces, but the official pages were not line-readable through the browsing tool in this run.

Treat Cursor as:

- supported in principle
- requiring a current direct docs refresh before publishing exact paths or semantics

Practical adapter guidance until refreshed:

- Keep universal `SKILL.md` provider-neutral.
- Add a `references/provider-cursor.md` file only after current Cursor docs are verified.
- If exporting to Cursor, test activation in Cursor itself rather than assuming Codex or Claude behavior maps perfectly.

## What Belongs In SKILL.md

Include:

- what the skill does
- exact activation triggers
- routing and boundaries
- required workflow
- references to bundled files
- script names and when to use them
- output contract
- validation command
- safety/permission gates

Avoid:

- long theory dumps
- provider-specific syntax unless unavoidable
- API credentials
- full copies of external docs
- stale install instructions
- broad chat history assumptions
- examples that leak expected validation answers into forward tests

## What Belongs In References

Use references for:

- detailed policies
- domain checklists
- schemas
- provider-specific notes
- examples
- troubleshooting maps
- file format details
- long decision trees

Reference files should be one level deep from `SKILL.md`.

Good:

```text
references/source-policy.md
references/provider-openai.md
references/eval-gates.md
```

Weak:

```text
references/misc.md
references/notes/archive/old-v2/all-provider-details.md
```

## What Belongs In Scripts

Use scripts when the operation is:

- deterministic
- repeated
- easy to get subtly wrong
- easier to verify by running code than by model prose
- large enough that rewriting it each time wastes context

Good script tasks:

- validate frontmatter
- scaffold a skill
- initialize a research receipt
- compare expected route cases
- lint JSONL
- create a test fixture
- summarize package inventory
- run bounded provider smoke tests

Script rules:

- Make commands idempotent when possible.
- Print machine-readable JSON for receipts.
- Fail loudly and specifically.
- Avoid broad destructive operations.
- Document dependencies in the script or adjacent reference.
- Keep secrets out of logs and receipts.

## Evaluation Pattern For Skills

Evaluate skills before trusting them.

Minimum eval set:

1. Explicit invocation.
2. Implicit activation.
3. Near-miss prompt that should not trigger.
4. Happy-path task.
5. Failure-path task.
6. Provider-specific adapter task.
7. Validation command.

Example route eval:

```json
[
  {
    "name": "deep-research-provider-skills",
    "prompt": "deep research best practices for universal agent skills and provider-specific adapters",
    "must_include": ["aiwf-deep-research"]
  },
  {
    "name": "not-research",
    "prompt": "fix this typo in README",
    "must_not_include": ["aiwf-deep-research"]
  }
]
```

Track:

- prompt
- expected selected skill
- actual selected skill
- reason
- failures
- changed files
- validation artifacts

For provider testing, build a matrix:

| Test | Codex | Claude | Copilot/VS Code | Cursor | MCP App | ADK/OpenAI Agents |
| --- | --- | --- | --- | --- | --- | --- |
| Explicit invocation | required | required | maybe via instruction | verify | n/a | adapter |
| Implicit trigger | required | required | project-dependent | verify | n/a | adapter |
| Script execution | local shell | environment-dependent | editor-dependent | verify | server/runtime | runtime |
| MCP tool use | via connector/app | via MCP-capable runtime | via MCP support | verify | native | runtime |
| Eval receipt | local script | model eval | editor workflow | verify | app trace | framework eval |

## Provider-Specific Capability Should Be Additive

Provider capabilities should add value without making the skill unusable elsewhere.

Good:

```text
SKILL.md tells the universal workflow.
agents/openai.yaml adds OpenAI display metadata and MCP dependencies.
references/provider-claude.md explains Claude packaging caveats.
references/provider-copilot.md explains AGENTS.md or .github instruction mapping.
scripts/validate_skill.py validates the portable core.
```

Bad:

```text
SKILL.md assumes a single provider UI, a single exact model, and a single proprietary tool call format.
No fallback exists if that provider feature is unavailable.
```

## Universal Skill Template

```markdown
---
name: example-skill
description: Clear one-sentence-plus trigger description. Use when the agent must do <task>, including <trigger terms>, <file types>, <systems>, and <boundaries>. Triggers for <phrases users say>. Do not use for <near misses>.
---

# Example Skill

## Overview

Use this skill to <job>. Keep this section short.

## Runtime Defaults

State reasoning/context/tool expectations only if they materially change execution. If provider-specific controls exist, say to use them where available and continue gracefully where not available.

## Workflow

1. Confirm the target artifact or decision.
2. Read the required reference for the surface.
3. Run the smallest useful script or check.
4. Apply edits or produce the artifact.
5. Validate with the named command.
6. Report changed files, validation, gaps, and next steps.

## References

- Read `references/policy.md` when <condition>.
- Read `references/provider-openai.md` only when working in OpenAI/Codex.
- Read `references/provider-claude.md` only when packaging for Claude.

## Scripts

- `scripts/init_run.py`: create a receipt folder.
- `scripts/validate_receipt.py`: validate output.

## Output Contract

Return:

- summary
- changed files or artifacts
- validation command and result
- unresolved risks
```

## OpenAI Sidecar Template

```yaml
interface:
  display_name: "example_skill"
  short_description: "Do one clear thing well"
  default_prompt: "Use $example-skill to <short example task>."
dependencies:
  tools:
    - type: "mcp"
      value: "github"
      description: "GitHub MCP server"
policy:
  allow_implicit_invocation: false
```

Use implicit invocation sparingly. Routers and always-on guardrails can be implicit. Deep, expensive, or narrow skills should usually be explicit or routed through a lightweight orchestrator.

## MCP Tool Design Checklist

For each tool:

- one job
- clear name
- specific description
- strict input schema
- predictable output shape
- annotations for read-only/destructive/open-world behavior where available
- no hidden side effects
- no secrets in logs
- clear error messages
- test fixture

MCP tools should expose capability; skills should explain when capability is useful.

## Repository Instruction Checklist

Use AGENTS.md or Copilot custom instructions for:

- project path and repo scope
- install/test/build commands
- style rules
- security rules
- branch/commit rules
- local-only files
- relevant skill routing

Do not put long task playbooks in AGENTS.md unless they truly apply to every task. Route to a skill instead.

## Skill Portability Checklist

Before calling a skill universal, check:

- Does `SKILL.md` work if all provider sidecars are ignored?
- Does the description include enough trigger terms for discovery?
- Are provider-specific references optional?
- Are scripts documented and runnable without hidden global state?
- Are assets included or referenced safely?
- Does the skill avoid API keys, private paths, and machine-specific assumptions?
- Does it have a validation command?
- Does it include a near-miss test?
- Does it preserve copyrighted source limits?
- Does it degrade gracefully when a provider lacks a feature?

## AIWF Pack-Specific Recommendations

For Shawn's AIWF skill pack:

1. Keep `aiwf-orchestrator` as the lightweight router.
2. Keep expensive skills explicit or router-selected.
3. Keep the pack vendored to Shawn-owned `aiwf-` skills only; use external local helpers only as optional working tools, not pack source.
4. Use `aiwf-deep-research` for volatile provider docs and standards.
5. Add `provider-*` references only when a skill truly needs provider-specific behavior.
6. Validate with `scripts\validate_skills.ps1`.
7. Validate routing with `scripts\test_orchestrator_routes.py`.
8. If a skill affects global behavior, update `C:\Users\Shawn\.codex\skills\aiwf` rather than creating a parallel global router.
9. Restart Codex after global skill changes.

## Practical Design Rules

Use these as the short version:

1. Core first. Adapter second.
2. Metadata activates the skill; body operates it.
3. Keep `SKILL.md` short and operational.
4. References hold depth.
5. Scripts hold determinism.
6. Assets hold templates and fixtures.
7. MCP holds active cross-provider capability.
8. Apps SDK and UI bridges hold provider UI behavior.
9. Agent frameworks hold state, handoffs, callbacks, guardrails, and traces.
10. AGENTS.md and Copilot instructions hold persistent repo rules.
11. Evals prove the skill works.
12. Provider claims expire. Recheck current docs before publishing exact adapter instructions.

## Source List

- `src-001`: Local Codex skill-creator SKILL.md.
- `src-002`: Local skill-creator `openai_yaml.md`.
- `src-003`: Agent Skills specification, https://agentskills.io/specification
- `src-004`: Anthropic Claude Skills overview, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- `src-005`: Anthropic Skill authoring best practices, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- `src-006`: OpenAI Codex Skills, https://developers.openai.com/codex/skills
- `src-007`: OpenAI API Skills, https://developers.openai.com/api/docs/guides/tools-skills
- `src-008`: OpenAI skill eval guidance, https://developers.openai.com/blog/eval-skills
- `src-009`: MCP tools specification, https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- `src-010`: MCP resources specification, https://modelcontextprotocol.io/specification/2025-11-25/server/resources
- `src-011`: MCP prompts specification, https://modelcontextprotocol.io/specification/2025-11-25/server/prompts
- `src-012`: OpenAI Apps SDK tool planning, https://developers.openai.com/apps-sdk/plan/tools
- `src-013`: OpenAI Apps SDK reference, https://developers.openai.com/apps-sdk/reference
- `src-014`: OpenAI Agents SDK overview, https://developers.openai.com/api/docs/guides/agents
- `src-015`: OpenAI Agents Python SDK, https://openai.github.io/openai-agents-python/
- `src-016`: VS Code custom instructions, https://code.visualstudio.com/docs/agent-customization/custom-instructions
- `src-017`: GitHub Copilot custom instructions, https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions
- `src-018`: AGENTS.md, https://agents.md/
- `src-019`: Google ADK overview, https://adk.dev/
- `src-020`: Google ADK callbacks, https://adk.dev/callbacks/
- `src-021`: Google ADK evaluation, https://adk.dev/evaluate/
- `src-022`: Cursor Rules official docs search result, https://cursor.com/docs/rules
- `src-023`: Cursor Agent Skills official docs search result, https://cursor.com/docs/skills

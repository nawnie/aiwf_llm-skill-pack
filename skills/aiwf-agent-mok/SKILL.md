---
name: aiwf-agent-mok
description: Agent MoK structured planning, research verification, and findings-dataset capture for complex agentic work. Use when Codex needs to create or update plan.md, break work into Atlas lanes/cards, verify request interpretation, tool results, claims, memory/context, and affected project files, and organize searched or found data into per-usage moks findings training datasets. Trigger for planning, verification, double-checking, reducing mistakes, agentic reasoning, tool-use validation, deep research, full-learning, building a mental model, dataset or findings capture, risky edits, refactors, migrations, incident response, debugging, and tool-heavy workflows.
---

# Agent MoK

## Overview

Use this skill to separate "first idea" from "validated approach." Ruminate over the user's request, the current plan, tool results, and the project files that the plan will affect. Store the plan in a local `plan.md` as a small map instead of rewriting long planning prose every turn. Treat the plan like an Atlas: structured lanes, atomic cards, explicit route edges, source-backed verification state, and tool-result checkpoints.

Core principle:

```text
New evidence changes the map, not the whole conversation.
```

External data principle:

```text
Online data, user-provided data, and model-generated data all start as claims, not canon.
Classify the source, check freshness and provenance, then verify before the plan or answer depends on it.
```

Multi-source rule:

```text
When multiple sources are available, compare them instead of averaging them.
Keep contradictions visible, prefer the strongest current source, and only collapse claims after verification.
```

Default rumination rule:

```text
Do 4 verification passes by default.
Keep going only if a pass finds a material issue in the request interpretation, route, cards, affected project files, or safety of execution.
```

Planning-first trigger rule:

```text
When Agent MoK is triggered, always begin in planning-first behavior.
Create or adopt plan.md, restate the user's request operationally, map the active route, and run the verification loop before execution unless the task is truly trivial.
```

Findings dataset rule:

```text
When Agent MoK searches, researches, reads, receives, or otherwise finds reusable data,
organize the findings into a per-usage training dataset folder under `moks findings`.
Create the folder when it does not exist, write Atlas-style cards and training JSONL,
and report the path. If the user chooses another findings directory, use it. If no
writable findings directory is available or the user declines a custom directory, fall
back to a `moks findings` folder under the root skill/plugin folder when writable.
```

## Workflow

### 1. Always enter planning-first behavior

Agent MoK should not jump straight to implementation on non-trivial work.

When triggered:

- create or adopt `plan.md`
- restate the user's request in operational terms
- identify affected files, tools, sources, side effects, and gates
- initialize a findings run when the task searches or finds reusable data
- create or update the active route
- run the default 4 verification passes unless the task is truly trivial
- execute only after the route is aligned with the request and evidence

This is the skill-level planning mode. If the host application has a separate UI Plan Mode, the skill cannot force that UI state, but it should behave as if planning-first is required.

### 2. Create or adopt `plan.md`

Prefer a local `plan.md` whenever the task is multi-step, risky, or likely to require replanning.

If a plan file already exists, update it instead of replacing it wholesale.

Keep conversational replies short. Put durable planning state in the file.

Read [references/atlas-plan-template.md](references/atlas-plan-template.md) when creating or reshaping the file.

Read [references/agentic-reasoning-patterns.md](references/agentic-reasoning-patterns.md) when the task uses tools, has long-horizon state, includes failure recovery, code fixes, or side effects.

Read [references/deep-learning-research.md](references/deep-learning-research.md) when the user asks to deeply learn, fully understand, research, or build a mental model of a subject.

Read [references/memory-context-patterns.md](references/memory-context-patterns.md) when relevant memory, cached context, prior plan state, or durable project knowledge may reduce redundant tool calls or prevent stale decisions.

Read [references/findings-dataset.md](references/findings-dataset.md) whenever the task searches, browses, researches, reads files for learning, gathers evidence, or otherwise finds reusable data.

### 3. Ruminate on the user's request before trusting the plan

Start every non-trivial run by restating the user's request in operational terms.

Check:

- what the user explicitly asked for
- what constraints were stated directly
- what success would look like to the user
- what assumptions Codex is making beyond the request
- whether the current plan is solving the actual request or a substituted version of it

If the request is ambiguous, risky, or easy to misread, record that uncertainty in `plan.md` before proceeding.

If the user wants deep understanding rather than a quick answer, convert the request into learning threads before researching.

### 4. Build the plan as an Atlas

Organize the plan into small addressable units instead of long paragraphs.

Use these concepts:

- `lanes`: major workstreams or subproblems
- `cards`: atomic actions, facts, checks, or diagnostic branches
- `route`: the current execution path through the cards
- `evidence`: the source, file, command, or output that supports a card
- `verification_state`: whether a card is unverified, partially verified, or verified

For each active card, state:

- the goal
- the information or artifact it depends on
- the main failure mode
- how success will be checked
- the verification state
- the next route edge if the card succeeds or fails

Keep cards small enough that only changed cards need to be rewritten.

### 5. Verify affected project files before acting

Identify the files, modules, configs, tests, and interfaces the current route can affect.

Check for:

- existing patterns that the change must follow
- related files that must change together
- variables, flags, props, schema fields, env vars, or config keys that are introduced in one place but missing elsewhere
- imports, exports, registrations, types, tests, docs, or wiring that must stay in sync
- downstream breakage caused by renames, moved behavior, or changed assumptions

Do not treat a local edit as complete until the surrounding project surfaces are checked.

Record affected files or integration points in `plan.md` when the task is non-trivial.

### 6. Verify request, plan, and project before acting

Inspect the request interpretation, the active lane and route, and the affected project files for hidden assumptions before making changes.

Check at least these questions:

- Is the plan still aligned with the user's actual request?
- Did Codex accidentally optimize for a nearby but different task?
- Is every factual claim grounded in a source, file, command result, or user-provided requirement?
- If the claim came from online data or a provided artifact, has it been classified as draft, reference, or verified evidence?
- If several sources disagree, have we recorded the conflict and chosen the best-supported claim explicitly?
- Does any active card depend on a file, API, environment detail, or tool that has not been verified yet?
- Does any answer depend on memory or cached context that may be stale?
- Do the affected project files show any integration points that the current plan has not accounted for?
- Has every new variable, key, prop, type, or setting been added everywhere it must exist?
- Could this change break callers, imports, tests, config, or runtime behavior outside the edited file?
- Does the order of operations avoid irreversible or high-cost mistakes?
- Is there a faster or safer path that reaches the same result?
- Are success criteria observable rather than vague?

Read [references/verification-checklist.md](references/verification-checklist.md) when the work is risky, multi-stage, or easy to get subtly wrong.

### 7. Validate after every tool call

After each tool result, pause long enough to interpret it before continuing.

Check:

- whether the tool result actually answered the intended question
- whether the result changes the request interpretation, route, or affected project surfaces
- whether a failed tool call should trigger a fallback route
- whether state from the result must be carried forward into later cards
- whether the next action is still safe and useful

Update `plan.md` only where the result changes the map.

For independent checks, run tools in parallel when the results do not depend on each other.

For irreversible or external side effects, prepare and verify first, then ask for confirmation unless the user already gave explicit approval.

### 7.1 Capture findings as a training dataset

Whenever tool calls, web research, file reads, user uploads, or model consultations produce reusable findings, create or update a per-usage findings run.

Prefer running [scripts/create_findings_run.py](scripts/create_findings_run.py) to initialize the run folder. Use the default root `moks findings` under the current working directory, a user-specified findings directory when provided, or the root skill/plugin folder fallback described in [references/findings-dataset.md](references/findings-dataset.md).

Each findings run should include:

- `manifest.json` with request, timestamps, source classes, license/privacy notes, and validation status
- `atlas_cards.jsonl` with Atlas-style route/evidence cards
- `training_data.jsonl` with model-training-ready JSONL records derived from verified or clearly labeled findings
- `sources.jsonl` with source metadata, provenance, retrieval time, and usage constraints
- optional `raw/` files only for user-provided, generated, or license-cleared material

Do not store secrets, private credentials, unnecessary personal data, or long copyrighted source text. Store summaries, facts, citations, labels, source metadata, and short permitted excerpts instead. Mark uncertain, conflicting, stale, generated, or unlicensed material so it is not treated as training-ready ground truth.

### 8. Use model interrogation only as a fallback evidence source

If no suitable tool, connector, file, or live source can answer a needed question, Agent MoK may interrogate another model or helper expert.

Treat model answers as interview evidence, not truth.

Use this route:

- ask narrow questions instead of requesting a full essay
- record the question, answer, claim, and confidence signal
- ask follow-up questions only for missing or conflicting details
- when asking more than one model or repeated questions, merge only the differences
- keep unchanged claims out of the delta to avoid copying full model prose
- mark every model-provided claim as unverified until checked against a stronger source or an acceptance gate
- train or act only on verified deltas, clearly labeled hypotheses, or user-approved assumptions

Do not paste a helper model's full answer into the final response or training data as ground truth.

### 9. Keep a public verification trace, not private reasoning

Do not expose hidden chain-of-thought or long private reasoning transcripts.

Instead, record compact public reasoning artifacts:

- request interpretation
- active route
- evidence used
- pass findings
- tool-result checks
- changed assumptions
- remaining blockers
- final validation

Use `plan.md` to preserve durable state. Use the chat response to summarize decisions, deltas, and outcomes.

When the work uses external data, record the source class in the trace:

- `official`
- `user-provided`
- `repo-local`
- `generated`
- `stale-or-uncertain`

When the work uses multiple sources, also record:

- the primary source
- any rejected sources
- the conflict resolution rule used

### 10. Revise weak request interpretations, project assumptions, or cards, not whole essays

Rewrite only the request interpretation, affected-file assumptions, cards, route edges, or lane summaries that failed verification.

Prefer these repairs:

- replace assumptions with inspection
- split large uncertain steps into smaller testable steps
- add preconditions before destructive actions
- add explicit validation after each meaningful change
- remove unnecessary complexity
- move stable details out of chat replies and into `plan.md`

If two or more viable approaches remain, compare them briefly and choose the one with the best reliability-to-effort ratio.

### 11. Loop until the request interpretation, route, and project fit are solid

Run at least 4 verification passes over the user's request, the active route, and the affected project files unless the task is truly trivial.

For each pass:

- compare the current understanding to the original user request
- inspect the active lane and route
- inspect the affected project files and interfaces
- try to break the current plan
- record concrete issues, not vibes
- update only the affected interpretation notes, cards, evidence, or route edges

Number the passes clearly in the working file or notes as `Pass 1`, `Pass 2`, `Pass 3`, and `Pass 4`.

After pass 4, continue looping only if the latest pass still found a material issue such as:

- the request was interpreted incorrectly
- a broken assumption
- a missing prerequisite
- a missing integration update
- a new variable or config change was not propagated everywhere it belongs
- a tool result contradicted the plan or failed to answer the intended question
- an acceptance gate failed
- a safety problem
- a better route with meaningfully lower risk
- a verification gap that could change the outcome

Repeat the route and verification pass until all of these are true:

- the current plan matches the user's actual request
- the critical assumptions have been checked
- the remaining uncertainty is small or clearly called out
- each active card has a verification method
- the affected project files and integration points have been checked for consistency
- tool results have been validated before being used as evidence
- the execution order is safe
- the active lane is concise enough to follow under pressure

Do not loop forever. Stop when a full pass fails to uncover a material issue, or when additional passes are only restating known concerns without changing the route.

### 12. Execute with checkpoints

Carry out the plan one verified step at a time.

After each major step:

- compare the result to the expected outcome
- update only the affected cards or route edges if reality differs from the forecast
- re-run a shorter verification pass before continuing
- stop at hard gates instead of forcing progress

If evidence contradicts the plan, prefer replanning over forcing the original path.

## Plan File Rules

Prefer this behavior unless the user asks otherwise:

- keep a brief request interpretation in `plan.md`
- keep the working plan in `plan.md`
- keep an affected-files or integration-points note in `plan.md` for non-trivial tasks
- keep cards atomic and source-backed
- keep tool results tied to the card or route they validate
- keep public verification notes instead of private reasoning dumps
- keep the active findings run path and training-data status when reusable data is found
- update only changed sections
- summarize unchanged sections by ID or lane name instead of restating them
- retrieve or reread only the active lane when possible
- avoid rewriting full planning paragraphs in normal chat responses

Treat long narrative planning as a fallback, not the default.

## Output Shape

When helpful, present the work in this order:

1. Active route
2. Request check
3. Pass findings
4. Delta to `plan.md`
5. Findings dataset path, when applicable
6. Execution
7. Final validation

Compress the format for small tasks, but preserve the loop: map, verify, revise, confirm.

When the task is substantial, show pass-by-pass results briefly:

1. Pass 1
2. Pass 2
3. Pass 3
4. Pass 4
5. Extra pass only if needed

## Heuristics

Spend more effort on verification when:

- the task can delete, migrate, deploy, publish, or overwrite
- the bug has multiple plausible causes
- the request mixes code changes with environment assumptions
- the user explicitly asks for high confidence or correctness
- the current `plan.md` has grown large enough that card-level updates are cheaper than prose restatements
- the request is easy to subtly misread
- the edit touches shared code, config, schemas, or public interfaces
- the workflow uses several tools whose outputs affect later steps
- the workflow includes deployment, posting, publishing, or other side effects
- the work is a bug fix where the original failure, patch, and regression surface must stay connected
- the user asks to deeply learn, research, or understand a subject end to end
- memory or prior project context could be useful but may be stale

Spend less effort when the task is trivial, local, and easy to undo.

## Failure Recovery

If the verification pass keeps failing, surface the exact blocker.

State:

- how the request may have been misread
- what is still unverified
- why it matters
- what evidence would resolve it
- whether a safe partial path exists
- which lane or card is blocked
- which project files or integration points are still at risk
- which tool result, missing evidence, or acceptance gate is blocking progress

If four passes have completed and new issues keep appearing, say that explicitly and continue only on the unresolved lane or cards instead of re-reviewing the whole map.

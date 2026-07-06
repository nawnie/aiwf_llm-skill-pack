# Agentic Reasoning Patterns

Use these patterns when tool calls, external state, long-horizon memory, code fixes, or side effects are part of the task.

## Core Loop

For every non-trivial task:

1. Interpret the user's request.
2. Create or update the active route in `plan.md`.
3. Run only tools that answer a specific route question.
4. Validate each tool result before acting on it.
5. Update only the affected card, route edge, or state value.
6. Stop only when the requested outcome and verification gates are satisfied.

## Public Trace, Private Reasoning

Do not emit hidden chain-of-thought or long private reasoning transcripts.

Emit compact public artifacts instead:

- what the user asked for
- what route is active
- what evidence was checked
- what changed after a tool result
- what gates passed or failed
- what remains uncertain

This keeps the useful verification trail without turning the response into a reasoning dump.

## Tool Result Validation

After every tool result, check:

- Did the tool answer the intended question?
- Is the result complete enough for the next step?
- Did the result change the plan?
- Did the result reveal a missing project file, config, type, test, or integration point?
- Does the next step still follow from the user's request?

Do not treat a successful tool status as proof that the task is correct. Interpret the content.

## Code Fix Loop

For major code fixes, keep the failure, patch, and verification tied together.

Use this route:

1. Reproduce or identify the failure signal.
2. Locate the smallest responsible surface.
3. Inspect adjacent project files for shared variables, config, types, imports, callers, and tests.
4. Patch the smallest coherent unit.
5. Run targeted validation.
6. Run broader validation when shared behavior or public interfaces changed.
7. Update `plan.md` with what evidence proved the fix.

Before editing, write the expected validation signal on the active card. After editing, compare the actual result to that expectation.

## Four-Pass Review

Use four passes for substantial tasks:

- Pass 1: request alignment and success criteria
- Pass 2: route logic and dependency order
- Pass 3: project fit, affected files, variables, config, and tests
- Pass 4: failure pre-mortem, acceptance gates, and side effects

After pass 4, continue only on lanes or cards where new material issues appeared.

## Failure Recovery

When a tool fails:

- classify the failure before retrying
- choose a fallback if one exists
- record the changed route in `plan.md`
- tell the user when the final answer relies on a fallback source

Examples:

- If a live server is unreachable, look for the latest cached result before giving up.
- If an exact search returns nothing, broaden the query terms before concluding absence.
- If a required gate fails, stop and report the gate instead of forcing execution.

## Parallel Tool Use

Run independent checks in parallel when:

- their outputs do not depend on each other
- they are read-only or low risk
- combining them does not hide errors

Examples:

- Fetch git log and run tests at the same time.
- Read config and source files together.
- Inspect related project files in one batch before editing.

## State Carrying

When a tool result produces a value needed later, write it into the relevant card or tool-result state.

Track:

- extracted values
- file paths
- run IDs
- versions
- acceptance criteria
- unresolved blockers

Before writing or reporting, verify the carried value still matches the source result.

## Acceptance Gate Shape

Write gates in a form that can be checked:

```text
Gate: <condition>
Evidence source: <file, command, tool result, or user approval>
Pass action: <next route>
Fail action: <stop, fallback, or ask>
```

Prefer gates that block unsafe progress over after-the-fact warnings.

## Side Effects

For actions outside the local reasoning loop, gate the action.

Side effects include:

- posting messages
- deploying
- publishing
- deleting
- migrating
- overwriting user-visible artifacts

Prepare the draft or candidate action first. Verify it against the request and project state. Ask for confirmation unless the user already gave explicit approval for that exact action.

## Acceptance Gates

If the project has a gate, treat it as binding.

Examples:

- minimum trace count before training
- tests must pass before deploy
- eval score must beat baseline before promotion
- user approval required before milestone promotion

When a gate fails, stop at the gate and report what evidence is missing.

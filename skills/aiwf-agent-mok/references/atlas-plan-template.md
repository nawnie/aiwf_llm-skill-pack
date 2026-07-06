# Atlas Plan Template

Use this template when creating or reshaping `plan.md`.

## Purpose

Store the working plan as a map, not a repeated essay.

The file should help Codex:

- find the active lane quickly
- update only changed sections
- verify cards against evidence
- resume work without restating everything in chat

## Suggested Structure

```md
# Plan

## Objective
- short statement of the task

## Constraints
- user requirements
- repo or environment constraints
- safety constraints

## Request Interpretation
- what the user explicitly wants
- what success means
- assumptions that still need verification

## Affected Project Surfaces
- files likely to change
- related files that may need parallel updates
- shared variables, config, schema, or interface touchpoints

## Acceptance Gates
- gate condition
- evidence source
- pass action
- fail action

## Tool Result State
- tool results that changed the route
- failed tools and fallback route chosen
- state values that must carry forward

## Public Verification Trace
- request alignment notes
- pass findings
- changed assumptions
- final validation evidence

## Lanes
### Lane: <name>
Status: active | pending | blocked | done
Goal: ...

#### Card: <id>
Type: action | check | diagnostic_branch | fact | risk
Goal: ...
Depends on: ...
Evidence: ...
Tool result check: ...
Failure mode: ...
Success check: ...
Verification state: unverified | partial | verified
Project checks: ...
Acceptance gate: ...
Next if pass: ...
Next if fail: ...

## Active Route
- <card-id> -> <card-id> -> <card-id>

## Open Unknowns
- explicit unresolved questions

## Validation Log
- short dated notes about what was confirmed
- pass-by-pass notes for Pass 1 through Pass 4
```

## Card Design Rules

- Keep cards atomic.
- Give each card a stable ID.
- Prefer one checkable claim or action per card.
- Attach evidence directly to the card.
- Split oversized cards before revising them repeatedly.

## Update Rules

- Update only changed cards, route edges, or lane status.
- Do not rewrite unchanged lanes just to restate them.
- If a route changes, update `Active Route` first.
- If a verification result arrives, record it on the card before summarizing it in chat.
- If a tool result changes the route, update `Tool Result State` and the affected card.

## Chat Compression Rules

- Refer to card IDs and lane names when possible.
- Summarize deltas instead of reproducing the full map.
- Use full prose only when the user asks for a narrative explanation.

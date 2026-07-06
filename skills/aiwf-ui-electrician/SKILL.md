---
name: aiwf-ui-electrician
description: "AIWF middle-layer UI/API connector audit skill. Use when debugging the wiring between backend APIs and frontend UI state: FastAPI routes, Gradio callbacks, React fetch/SSE/WebSocket/polling clients, request/response normalization, runtime progress, cancellation, error presentation, client logs, cache/no-store behavior, settings/bootstrap contracts, and button/state synchronization."
---

# UI Electrician

Use this skill for the middle layer between model/backend runtime code and the visible UI. It is not a visual design audit and it is not a model-runtime audit; it checks whether routes, callbacks, clients, polling, events, progress, errors, resources, and generated outputs actually travel end to end.

## Workflow

1. Read project instruction boundaries. The parent agent may read full project rules. Subagents should only receive the `Known Issues` section of `AGENTS.md`, `SUB_AGENTS.md` if present, or a parent-written `_context.md`.
2. Read `references/debug-pass-protocol.md` before spawning subagents.
3. Create a debug pass folder:

```powershell
python C:\Users\Shawn\.codex\skills\aiwf-ui-electrician\scripts\scaffold_debug_pass.py --root F:\AIWF_Studio --slug ui-api
```

4. Inspect the contract from both sides: backend route/callback definitions, request models, response shapes, frontend fetch/client code, state reducers, polling or stream handlers, and user-visible error surfaces.
5. Spawn subagents only for independent lanes. Subagents are read-only issue loggers by default and must write Markdown reports into the debug pass folder.
6. Parent agent reads every report, deduplicates, verifies high-impact claims, researches framework behavior when confidence is below 90, then implements the smallest coherent fixes.
7. Verify with targeted API tests, frontend builds/tests, callback smokes, endpoint probes, and log inspection. Avoid GPU-heavy generation unless the user explicitly asks.

## Middle-Layer Lanes

- API contract shape: payload names, aliases, enum values, defaults, response keys, and error status shapes.
- Runtime progress stream: job states, phases, progress percentages, terminal state, and stale event cleanup.
- Cancellation and concurrency: stop buttons, second-generation behavior, active job ownership, duplicate submit guards, and cleanup after failure.
- Error propagation: backend exceptions, route errors, client log ingestion, toast/status text, and failures hidden only in terminal or console.
- Resource telemetry: GPU/RAM/CPU polling, endpoint freshness, task-manager style utilization fields, and UI refresh cadence.
- Settings and bootstrap: launch defaults, feature flags, selected model, precision, backend, and route readiness.
- File and media paths: image/video uploads, output thumbnails, download links, relative/static paths, and missing asset handling.
- Fetch/cache behavior: when volatile endpoints require `cache: "no-store"`, whether cached data is causing stale UI, and whether the reason is documented.

## Subagent Protocol

Use the shared debug-pass protocol:

- Default role is `explorer`: read-only issue discovery, no patches.
- Subagents write one Markdown report per lane under the selected `debug_pass` folder.
- Reports state the issue, evidence, user-visible impact, affected files/routes, confidence, and whether source research was used.
- Reports do not include implementation recipes or broad patch plans. The parent agent owns the fix.
- A subagent may make a simple syntax fix only when the entire repair is three changed lines or fewer. It must record the exact file and lines changed in its report.

## Research And Confidence

- Use project notes, current logs, tests, and route definitions before guessing.
- Use official docs or primary sources for framework behavior when the claim depends on FastAPI, Starlette, Gradio, React, browser fetch, SSE, WebSocket, or process/window integration details.
- If no source research is used for a claimed fix, confidence must be at least 90/100 and the report must say why the local evidence is enough.
- If many bugs are found, the parent may request an atlas-style `issues.jsonl` dataset in the same debug pass folder to reduce repeated reading.

## References

- `references/debug-pass-protocol.md`: shared subagent reporting contract.
- `references/middle-layer-checklist.md`: UI/API connector checks for FastAPI, Gradio, and React work.

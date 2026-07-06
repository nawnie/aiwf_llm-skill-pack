# Debug Pass Protocol

This protocol keeps subagents cheap and useful: they discover and log issues, while the parent agent owns repair.

## Folder

Default location:

```text
<project-root>/.codex/debug_pass/<YYYYMMDD-HHMMSS>-<slug>/
```

Use a repo-level `debug_pass/` folder only when the project already has one or the user explicitly asks for that exact path. Keep pass folders local and ignored where possible.

## Subagent Context

Subagents should not read full project instruction files unless the parent explicitly requires it.

Preferred context order:

1. Parent-provided lane prompt.
2. `_context.md` in the debug pass folder.
3. `SUB_AGENTS.md` if present.
4. Only the `Known Issues` section of `AGENTS.md`.

If `AGENTS.md` has no `Known Issues` section, do not expand to the full file by default. Ask the parent or proceed from the supplied context.

## Report Template

Each lane writes one Markdown report:

```markdown
# <Lane> Debug Report

- Agent:
- Scope:
- Status: complete | partial | blocked
- Confidence: NN/100
- Research used: yes | no
- Sources:
- Project notes read:
- Files/logs inspected:

## Issues

### <severity>: <title>
- Evidence:
- User-visible impact:
- Repro/trigger:
- Affected files/routes:
- Confidence:
- Needs parent research: yes | no
- Fix detail omitted: yes

## Syntax Fixes

- None
```

Severity values: `critical`, `high`, `medium`, `low`, `info`.

## Syntax Fix Exception

Subagents are read-only unless the repair is a simple syntax fix of three changed lines or fewer.

When using the exception, the report must include:

- File changed.
- Exact line numbers.
- Before/after summary.
- Validation command or reason validation was not run.

No other repair work belongs in subagents.

## Issue Detail Rules

Subagents should describe the issue, evidence, and impact. They should not spend tokens writing the implementation fix. The parent agent reads the reports, researches weak claims, and implements repairs.

Good issue detail:

- Route returns `detail` but frontend only reads `message`, so user sees a generic error.
- Resource endpoint returns fresh data in terminal, but React polling stopped after a failed fetch.
- Stop button sends cancel request without the active job id after the second generation.

Avoid:

- Long patch recipes.
- Full rewritten code blocks.
- Broad refactor proposals without evidence.

## Confidence Rule

If no online or primary-source research is used, confidence must be 90/100 or higher. Otherwise mark the item as needing parent research.

Use official docs or primary sources when claims depend on framework/runtime semantics:

- FastAPI, Starlette, or Pydantic behavior.
- Gradio callback behavior.
- React state, effect, fetch, SSE, or WebSocket behavior.
- Browser caching and `fetch` cache modes.
- OS/window/tray integration.

## Dataset Option

For large bug passes, the parent may request an atlas-style `issues.jsonl` beside the Markdown reports. Use one JSON object per finding:

```json
{"id":"ui-api-001","lane":"progress","severity":"high","file":"frontend/src/...","route":"/api/...","symptom":"...","evidence":"...","confidence":92,"research":"no","status":"open"}
```

Keep evidence compact and path-based. Do not include secrets.

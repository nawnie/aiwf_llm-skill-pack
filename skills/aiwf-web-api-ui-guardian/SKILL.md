---
name: aiwf-web-api-ui-guardian
description: AIWF web, API, and UI guardrail for FastAPI, Gradio, React, TypeScript, JavaScript, HTML, and CSS work. Use to prevent version drift, frontend/backend contract mismatch, broken Gradio deployment paths, Vite/Node issues, unsafe HTML, inaccessible UI, and unvalidated visual changes.
---

# AIWF Web API UI Guardian

## Mission

Keep API, UI, types, and build tooling aligned.

This skill applies to:

- FastAPI
- Pydantic
- Gradio
- React
- Vite
- TypeScript
- JavaScript
- HTML
- CSS

The main risk is not syntax. It is contract drift between backend, frontend, runtime, and deployment assumptions.

Read `references/preflight-checklist.md` when repository state is unclear. Read `references/source-map.md` only when source provenance for these guardrails matters.

---

## FastAPI guardrails

### Check versions first

Before changing FastAPI code, inspect:

```text
fastapi
pydantic
starlette
uvicorn
sqlalchemy
python version
```

From:

```text
pyproject.toml
requirements*.txt
poetry.lock
uv.lock
pip freeze output, if available
```

### Pydantic v1/v2 rules

Do not mix v1 and v2 patterns casually.

| Concern | Pydantic v1 style | Pydantic v2 style |
|---|---|---|
| validators | `@validator` | `@field_validator` |
| config | inner `class Config` | `model_config = ConfigDict(...)` |
| serialization | `.dict()` | `.model_dump()` |
| parsing | `.parse_obj()` | `.model_validate()` |

If the repo uses v1 patterns, do not migrate opportunistically. If the repo uses v2 patterns, do not reintroduce v1 APIs.

### API contract rules

When changing request/response models or endpoint returns:

- Export or inspect OpenAPI.
- Check whether the frontend uses generated types.
- Regenerate clients if the repo pattern does that.
- Update tests that assert contract behavior.
- Check input/output schema separation when defaults or computed values exist.
- Check HTTP status codes.
- Check error response shape.

Avoid this bad pattern:

```ts
// hand-maintained frontend type that silently drifts from FastAPI model
export type User = { id: string; name: string }
```

Prefer generated or shared types when available.

### Async rules

Do not block the event loop with heavy synchronous work inside `async def`.

Watch for:

```python
time.sleep(...)
requests.get(...)
heavy CPU/GPU work inline
large file reads inline
subprocess.run(...) inline
```

Use proper async libraries, background tasks, workers, or thread/process offload depending on repo architecture.

### Dependency injection rules

Reuse existing FastAPI dependencies for:

- auth
- db session
- settings/config
- rate limits
- current user
- permissions

Do not bypass router-level dependencies when adding endpoints.

---

## Gradio guardrails

### Check Gradio version and launch style

Inspect installed Gradio version and repo launch pattern before changing:

```text
Blocks
Interface
queue
launch
mount_gradio_app
root_path
server_name
server_port
share
auth
SSR
reverse proxy/subpath deployment
```

### Root path and proxy safety

When deployed behind a proxy or subpath, local asset paths may break.

Before changing Gradio URLs, static assets, custom CSS/JS, or mounting behavior, inspect:

```text
root_path
proxy prefix
FastAPI mount path
nginx/traefik/ingress config
HTTPS termination
custom CSS asset URLs
```

Avoid hardcoded absolute `/assets/...` style paths if the app may live under `/studio` or another prefix.

### Event handler rules

For Blocks events:

- Match callback return count to output component count.
- Keep component state explicit.
- Avoid hidden global state unless repo already centralizes runtime state safely.
- Keep queue/concurrency settings intentional.
- Do not use Gradio auth as production-grade app auth without explicit user acceptance.

### AI app resource rules

For local AI apps:

- Clean temp files intentionally.
- Avoid unbounded queues.
- Avoid loading models at import time unless the repo pattern requires it.
- Avoid global model reload loops.
- Clear GPU memory only where safe and intentional.
- Do not block UI callbacks with unbounded work without progress/status handling.

---

## React guardrails

### Check React version

Before using React 19 behavior or old React 17 patterns, inspect `package.json`.

Watch for:

- `ReactDOM.render` vs `createRoot`.
- Strict Mode double-effect behavior.
- server/client component confusion.
- stale hook dependencies.
- uncontrolled/controlled input flips.
- unnecessary global state.
- giant component files.

### Component rules

- Reuse existing components before creating new ones.
- Keep data fetching patterns consistent with the repo.
- Implement loading, error, empty, and disabled states.
- Do not hide errors in console-only behavior.
- Avoid prop drilling if repo already uses context/store, but do not introduce a new state library for a small fix.

### Hook rules

Do not silence hook lint without a precise reason.

Bad:

```ts
// eslint-disable-next-line react-hooks/exhaustive-deps
```

Better:

- stabilize callback with `useCallback` if needed
- move derived logic out of effect
- include dependency
- explain the one local exception

---

## Vite / Node / package tooling guardrails

### Check Node version

Before changing Vite or frontend tooling, inspect:

```text
node --version
package.json engines
.nvmrc
.node-version
CI setup-node config
```

Do not scaffold or upgrade Vite if the Node version cannot support it.

### ESM/CJS rules

Before changing imports or module config, inspect:

```text
package.json "type"
tsconfig module
moduleResolution
vite config
jest/vitest config
Node execution target
```

In Node ESM contexts, relative imports often require explicit file extensions. Do not blindly apply bundler-only import assumptions to Node-run code.

---

## TypeScript guardrails

### No lazy `any`

Avoid:

```ts
any
// @ts-ignore
as unknown as Something
Record<string, any>
```

Unless the unsafe boundary is explicit and local.

Prefer:

- generated API types
- `unknown` at boundaries
- narrowing functions
- schema validation
- discriminated unions
- exact optional handling

### API response handling

For every frontend call, check:

- success shape
- error shape
- null/undefined behavior
- array vs object
- pagination
- datetime/string conversion
- file/blob response
- streaming behavior
- cancellation/abort handling

---

## JavaScript guardrails

- Do not mix CommonJS and ESM without checking repo pattern.
- Do not add mutable globals for shared app state.
- Do not swallow errors with empty `catch`.
- Do not parse JSON without handling failure at boundaries.
- Do not add browser-only code to Node-run files.
- Do not add Node-only code to browser bundle.

---

## HTML / CSS guardrails

### Accessibility minimums

When changing UI, check:

- labels for inputs
- button text or accessible names
- keyboard navigation
- focus state
- focus trap for modals
- reduced motion preference
- color contrast
- semantic elements before div soup
- alt text where meaningful

### Styling rules

- Reuse existing design tokens/classes.
- Avoid inline styles unless repo pattern uses them or dynamic styles require them.
- Do not introduce a second CSS system.
- Check mobile layout.
- Check dark mode if app has it.
- Check loading/error/empty states visually.

### Unsafe HTML

Do not add `dangerouslySetInnerHTML` unless:

- input is trusted or sanitized
- sanitization library is already used or added intentionally
- XSS risk is documented
- test covers unsafe input

---

## UI validation checklist

For UI changes, Codex should validate with at least one relevant method:

```text
unit/component test
Storybook story if repo uses it
Playwright/Cypress browser flow
manual screenshot/visual check if browser tooling exists
build output
accessibility lint/check
```

Do not claim a visual fix from source inspection alone when a browser run is practical.

## Final summary add-on

For API/UI work, final response must mention:

```text
Contract impact:
- OpenAPI/client types changed: yes/no/not checked

UI impact:
- Loading/error/empty/accessibility states checked: yes/no/not applicable
```

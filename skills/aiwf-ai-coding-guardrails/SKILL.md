---
name: aiwf-ai-coding-guardrails
description: AIWF coding guardrail skill for existing repositories. Use before and during coding, debugging, refactoring, review, or generated-code cleanup to prevent version drift, wrong package manager use, wrong shell commands, duplicate files, fake-green tests, API contract drift, unsafe shortcuts, and over-broad rewrites.
---

# AIWF AI Coding Guardrails

## Purpose

This skill prevents the most common AI coding agent failure modes in real repositories.

Use it whenever you are asked to write, fix, refactor, debug, optimize, or review code.

The operating model is:

```text
Probe first. Patch small. Prove with logs.
```

Do not claim success without command output or a clear reason validation could not run.

---

## Core rules

### 1. Discover before editing

Before changing files, inspect the repository enough to answer:

- What language and framework versions are actually installed?
- Which package manager owns the repo?
- Which runtime versions are expected locally and in CI?
- Which shell and OS assumptions exist?
- How are tests, typechecks, lint, build, and app startup run?
- Are there existing services, components, routers, utilities, or patterns that should be reused?
- Is there an API contract, schema, generated client, or shared type package?

Look for:

```text
package.json
package-lock.json
pnpm-lock.yaml
yarn.lock
.npmrc
.node-version
.nvmrc
volta config in package.json
tsconfig.json
vite.config.*
pyproject.toml
requirements*.txt
setup.py
Pipfile
poetry.lock
uv.lock
pytest.ini
ruff.toml
pyrightconfig.json
mypy.ini
CMakeLists.txt
CMakePresets.json
CTestTestfile.cmake
.github/workflows/*
AGENTS.md
README*
CONTRIBUTING*
```

For a compact repo preflight list, read `references/preflight-checklist.md`. For Windows-safe command examples, read `references/windows-powershell-commands.md`.

### 2. Do not guess versions

Never assume latest docs match the repo.

Before using framework-specific APIs, check installed or pinned versions. If the version is unknown, write code in the most conservative compatible style or stop and report the ambiguity.

High-risk version traps:

| Area | Guardrail |
|---|---|
| FastAPI + Pydantic | Check FastAPI and Pydantic versions before using v1/v2 validators, config, or schemas. |
| React | Check React version before using React 19 patterns or old ReactDOM render patterns. |
| Vite | Check Node version before changing Vite config or scaffolding. |
| TypeScript | Check TS version and module resolution before changing imports or tsconfig. |
| Gradio | Check Gradio version before changing Blocks events, queue, SSR, mount, root path, or launch flags. |
| SQLAlchemy | Check v1 vs v2 before using engine/session patterns. |
| Python | Check Python minor version before using newer typing, async, or stdlib features. |
| C++ | Check configured standard before using C++20/23 features. |
| CMake | Check presets and generator expectations before configuring builds. |

### 3. Stay repo-native

Prefer editing existing files over creating new ones.

Do **not** create these unless explicitly requested:

```text
*_new.*
*_fixed.*
*_copy.*
backup/*
temp/*
new_app/*
new_frontend/*
new_backend/*
parallel routers
parallel service layers
parallel API clients
parallel CSS systems
parallel build configs
```

Search first. Modify existing architecture second. Create only when the repo pattern calls for creation.

### 4. Respect the package manager

Do not add or switch lockfiles.

| Existing file | Use |
|---|---|
| `pnpm-lock.yaml` | `pnpm` |
| `yarn.lock` | `yarn` |
| `package-lock.json` | `npm` |
| `uv.lock` | `uv` where repo already uses it |
| `poetry.lock` | `poetry` where repo already uses it |

Do not run `npm install` in a pnpm repo. Do not create `package-lock.json` in a Yarn or pnpm repo.

### 5. Windows and PowerShell are first-class

Unless the repo explicitly says Linux-only, commands and scripts should be Windows-safe.

Avoid adding Unix-only syntax to npm scripts:

```text
rm -rf
cp -r
FOO=bar command
command1 && command2 with shell-specific quoting assumptions
sed -i
export VAR=value
```

Prefer cross-platform tools or Node/Python scripts.

For PowerShell examples, use:

```powershell
$env:NAME = "value"
Remove-Item -Recurse -Force .\dist
Copy-Item -Recurse .\src .\dest
```

### 6. No fake-green testing

Never delete, skip, weaken, or over-mock tests just to pass.

Forbidden unless explicitly justified:

```text
pytest.mark.skip
pytest.mark.xfail
it.skip
describe.skip
test.skip
expect(true).toBe(true)
assert True
broad snapshot replacement
removing assertions
removing test files
loosening strict type settings
adding // @ts-ignore without local reason
adding # type: ignore without local reason
```

If a test is wrong, explain why with evidence before changing it.

### 7. Keep diffs small

Small fixes should produce small patches.

Stop and explain before broad changes such as:

- Replacing an architecture.
- Moving many files.
- Rewriting a component tree.
- Changing build tooling.
- Changing package manager.
- Upgrading major dependencies.
- Adding a new framework.
- Altering generated files by hand.

### 8. Guard API contracts

When backend or frontend API shapes change:

- Locate the source of truth.
- Check OpenAPI or schema generation.
- Diff server contract changes.
- Update generated clients/types if the repo uses them.
- Avoid duplicate hand-maintained request/response types unless that is the repo pattern.
- Check null/undefined/default behavior.
- Check datetime serialization.
- Check file upload contracts.
- Check streaming response handling.
- Check error envelope shape.

### 9. Avoid unsafe shortcuts

Do not introduce:

```text
dangerouslySetInnerHTML
pickle.load on untrusted data
yaml.load without safe loader
eval / exec on untrusted input
shell=True with user-controlled input
subprocess string commands with unsanitized args
broad CORS for production
client-only auth treated as real auth
secrets in frontend code
secrets in logs
```

Use safer alternatives or stop and request approval.

### 10. Report honestly

Final response must include:

```text
Changed:
- <file>: <purpose>

Validated:
- <command> -> passed
- <command> -> failed: <short reason>
- <command> -> not run: <reason>

Risks / follow-up:
- <remaining risk or none>
```

Do not say "fixed" if validation did not run.

---

## Standard workflow

### Phase A: Preflight

Run or inspect enough to learn the repo shape.

Recommended commands, adapted to repo:

```powershell
git status --short
Get-ChildItem -Force -Name
node --version
npm --version
python --version
py -0p
```

Then inspect files rather than guessing.

For reusable prompt framing, read `references/codex-task-prompt.md`. For the research source map behind these guardrails, read `references/source-map.md` only when provenance matters.

### Phase B: Plan the smallest patch

Before editing, decide:

- What exact files need changes?
- What existing patterns should be reused?
- What tests or checks will prove it?
- What should be explicitly left alone?

### Phase C: Patch

Make the minimal change.

Do not improve unrelated code while passing through. Opportunistic cleanup is a diffusion leak.

### Phase D: Verify

Run checks in this order where relevant:

1. Format or lint for touched language.
2. Typecheck.
3. Narrow unit test.
4. Broader unit suite.
5. API contract diff/regeneration.
6. Browser/UI test if UI changed.
7. Build/package.

### Phase E: Final summary

Include exact command evidence.

---

## Stop conditions

Stop and request explicit user approval when the task requires:

- Destructive data operations.
- Production database changes.
- Secret/key handling.
- Major dependency upgrades.
- Package manager switch.
- Removing or rewriting large subsystems.
- Running untrusted setup scripts.
- Changing CI credentials or permissions.
- Changing deployment topology.
- Altering generated files without regenerating from source.

## Common bad AI behaviors to avoid

| Bad behavior | Correct behavior |
|---|---|
| Creates a second app because existing app is confusing | Search routes/components/services and modify repo-native path |
| Deletes failing test | Fix code or explain why test is invalid |
| Upgrades dependencies to make API fit generated code | Use repo-pinned API or propose migration separately |
| Adds `any` everywhere | Fix the type contract |
| Hardcodes local path | Use config/env/pathlib/project convention |
| Uses Bash commands in PowerShell repo | Write PowerShell-safe or cross-platform commands |
| Claims success without running checks | Report commands actually run, or say not run |
| Hand-edits generated clients | Regenerate from source schema |
| Silences linter | Fix code or justify one local exception |

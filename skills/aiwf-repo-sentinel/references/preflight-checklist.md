# Preflight Checklist

Use this before Codex edits an existing repo.

## Repo state

```powershell
git status --short
git diff --stat
git diff --name-only
```

## File discovery

Look for:

```text
AGENTS.md
README.md
CONTRIBUTING.md
package.json
package-lock.json
pnpm-lock.yaml
yarn.lock
.nvmrc
.node-version
pyproject.toml
requirements*.txt
poetry.lock
uv.lock
pytest.ini
ruff.toml
pyrightconfig.json
tsconfig.json
vite.config.*
CMakeLists.txt
CMakePresets.json
.github/workflows/*
Dockerfile
```

## Required answers before editing

- What package manager owns the repo?
- What Node version is required?
- What Python version is required?
- What framework versions are installed?
- What shell/OS does CI use?
- What commands validate the touched area?
- What existing files/patterns should be reused?
- Is there an API schema or generated client?
- Does the change touch tests?
- Does the change require a major version migration?

## Stop if

- package manager is ambiguous
- lockfiles conflict
- task requires major upgrades
- tests must be weakened
- repo has uncommitted user work that would be overwritten
- required validation cannot be identified
- destructive data operation is required

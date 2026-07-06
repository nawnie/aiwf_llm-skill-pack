---
name: aiwf-repo-sentinel
description: AIWF repository preflight and diff-discipline guardrail. Use at the start of existing-repository coding tasks to prevent duplicate files, wrong package manager use, wrong shell commands, major upgrade drift, weakened tests, broad diffs, and unverifiable success claims.
---

# AIWF Repo Sentinel

## Mission

Protect the repository from avoidable agentic coding errors.

This skill is active before any edit. Its job is to force Codex to understand the repo before changing it.

```text
Search before creating. Modify before duplicating. Prove before declaring victory.
```

## Repository preflight checklist

Before editing, answer these questions from files or commands:

For a compact checklist, read `references/preflight-checklist.md`. For Windows-safe command examples, read `references/windows-powershell-commands.md`.

### Git state

- Is the working tree clean?
- Which files are already modified?
- Are there untracked files?
- Am I about to overwrite user work?

Commands:

```powershell
git status --short
git diff --stat
git diff --name-only
```

If there are existing user changes, do not overwrite them.

### Package manager ownership

Detect and obey:

| Lock/config | Package manager |
|---|---|
| `pnpm-lock.yaml` | pnpm |
| `yarn.lock` | Yarn |
| `package-lock.json` | npm |
| `poetry.lock` | Poetry |
| `uv.lock` | uv |
| `Pipfile.lock` | Pipenv |

Never introduce a second lockfile.

### Runtime versions

Inspect:

```text
.node-version
.nvmrc
.python-version
pyproject.toml
package.json engines
Dockerfile
.github/workflows/*
CMakePresets.json
README.md
```

If local version and repo version conflict, report it rather than patching around it.

### Repo conventions

Find existing patterns before creating:

- Where do routes live?
- Where do API clients live?
- Where do React components live?
- Where does state management live?
- Where do styles live?
- Where are tests located?
- What naming pattern is used?
- What dependency injection pattern exists?
- What error handling pattern exists?

## Diff discipline

### Edit in place

Prefer existing files and patterns. Do not create parallel systems.

Block these unless explicitly requested:

```text
new backend folder
new frontend folder
new API client
new router tree
new global state system
new CSS framework
new test harness
*_copy.*
*_new.*
*_fixed.*
backup/*
old/*
temp/*
```

### Keep scope narrow

Do not fix unrelated lint, formatting, TODOs, imports, naming, or architecture while solving a specific bug unless required by the change.

### Stop on large diffs

Stop and explain before changes that touch many files or replace a subsystem.

A good stop message:

```text
This fix crosses into migration territory because it changes the package manager and three build files. I should not do that as a hidden side effect. Proposed next step: make a migration branch or solve the original issue without changing tooling.
```

## Test integrity rules

Never make tests green by reducing their value.

Forbidden patterns:

```text
remove test file
remove assertion
replace assertion with broad truthiness
expect(true).toBe(true)
assert True
add skip without issue link or explanation
add xfail without exact reason
mock the unit under test
increase timeout to hide a hang
weaken typecheck settings
turn off strict mode
```

Allowed test edits:

- Update expected output when behavior intentionally changed.
- Add regression test for bug.
- Fix test setup that no longer matches repo contract.
- Mark expected failure only when explicitly documenting a known unresolved defect.

## Command discipline

### Windows-safe defaults

When giving commands for this user or a Windows-capable repo, prefer PowerShell.

Use:

```powershell
$env:PYTHONPATH = "."
Remove-Item -Recurse -Force .\dist
Copy-Item -Recurse .\src .\dest
New-Item -ItemType Directory -Force .\logs
```

Avoid:

```bash
export PYTHONPATH=.
rm -rf dist
cp -r src dest
```

### npm script safety

Do not add Unix-specific commands to `package.json` scripts unless the repo already requires Bash.

Use cross-platform packages or Node scripts for cleanup/copying.

## Final response contract

Every coding task ends with:

```text
Changed:
- path/to/file.ext: what changed and why

Validated:
- command -> passed/failed/not run

Risks / follow-up:
- remaining issue or none
```

If validation was not run, say so plainly.

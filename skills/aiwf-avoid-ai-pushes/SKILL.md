---
name: aiwf-avoid-ai-pushes
description: AIWF commit and push hygiene skill, alias aiwf_avoid-ai-pushes. Use before committing or pushing AIWF Studio changes, especially when ignored local files, agent notes, root-layout cleanup, README edits, release docs, or GitHub-facing updates are involved. Prevents accidentally staging ignored/local-only files and pairs scope checks with avoid-ai-writing for public prose.
---

# Aiwf Avoid AI Pushes

## AI Avoidance Variables

Read this value from `aiwf-orchestration` when it is present:

```yaml
AIWF_AI_AVOIDANCE_LEVEL: 1.0
```

Apply the level like this:

- `0.1`: check only for secrets, ignored local files, generated caches, and obvious wrong-remote pushes.
- `1.0`: normal mode. Run the required checks below and audit new public prose.
- `2.0`: extreme mode. Treat any ambiguous staged file, local-only note, generated artifact, AI-looking prose, or unexplained remote/branch mismatch as a blocker until it is explicitly justified.

Use this skill before any AIWF Studio commit or push that touches docs, root files, release notes, or agent guidance.

## Required Checks

Run these before staging:

```powershell
git status --short --branch --untracked-files=all
git diff --stat
git diff --check
```

For any file that looks local-only or agent-only, check ignore and tracked state:

```powershell
git check-ignore -v --no-index <path>
git ls-files -- <path>
```

Common AIWF local-only paths:

- `AGENTS.md`
- `plan.md`
- `_trash/`
- `_local/`
- `.codex/`
- `.codex-remote-attachments/`
- `models/`
- `outputs/`
- `logs/`
- `cache/`
- `venv/`

If a file is ignored but already tracked by mistake, remove only the tracked copy:

```powershell
git rm --cached <path>
```

Do not delete the local file unless the user explicitly asks.

## Staging Rule

Stage explicit intended paths only. Do not use `git add -A` in AIWF unless the user confirms the whole worktree belongs in the push.

Good:

```powershell
git add README.md docs/FEATURES.md
```

Use `git add -f` only when the user explicitly wants an ignored path tracked. If that happens, say which ignore rule is being bypassed.

## Public Prose Rule

For README, docs, UI copy, release notes, commit messages, and PR text, also use `avoid-ai-writing`.

At minimum scan for:

```powershell
rg -n 'delve|robust|comprehensive|leverage|seamless|pivotal|at its core|worth noting|game-changer|transformative|cutting-edge|utilize|showcasing|foster|empower|moreover|furthermore|additionally|in conclusion|to summarize|--' <files>
```

Fix only the new or edited prose unless the user asks for a broader rewrite.

## Pre-Push Receipt

Before commit, show or inspect:

```powershell
git diff --cached --stat
git diff --cached --check
git status --short --branch
```

Before push, confirm the remote and branch:

```powershell
git remote -v
git branch --show-current
```

After push, report the commit hash, pushed branch, files staged, validation commands, and anything intentionally left local or ignored.

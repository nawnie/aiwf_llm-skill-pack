---
name: aiwf-avoid-ai-pushes
description: AIWF commit and push hygiene skill, alias aiwf_avoid-ai-pushes. Use before committing or pushing AIWF Studio changes, especially when ignored local files, agent notes, root-layout cleanup, README edits, release docs, or GitHub-facing updates are involved. Prevents accidentally staging ignored/local-only files and pairs scope checks with public prose scans.
---

# Aiwf Avoid AI Pushes

Use this skill before any AIWF Studio commit or push that touches docs, root files, release notes, or agent guidance.

## Runtime Defaults

Use normal reasoning by default; raise reasoning only for complex release hygiene, messy staged changes, or repeated CI/review failures.

When the host supports `/goal`, create or continue a goal for active commit, push, or release-hygiene work. Use no fixed token ceiling, the largest available context limit, and unlimited or expanded tool-call limits where those controls exist. If the host requires finite settings, choose the highest available values except for reasoning, which stays normal unless the task warrants escalation.

Expanded budgets apply to the active repo inspection, staging, prose audit, validation, and push workflow, not to broad chat-history review. Use standard context length to decide which prior chat instructions matter, then focus on the live git state, changed files, ignore rules, and requested release scope.

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

Do not delete the local file unless Shawn explicitly asks.

## Staging Rule

Stage explicit intended paths only. Do not use `git add -A` in AIWF unless Shawn confirms the whole worktree belongs in the push.

Good:

```powershell
git add README.md docs/FEATURES.md
```

Use `git add -f` only when Shawn explicitly wants an ignored path tracked. If that happens, say which ignore rule is being bypassed.

## Public Prose Rule

For README, docs, UI copy, release notes, commit messages, and PR text, run a public-prose scan before staging or publishing. Keep it narrow: fix newly edited prose and leave quoted examples, code, and source text alone.

At minimum scan for:

```powershell
rg -n 'delve|robust|comprehensive|leverage|seamless|pivotal|at its core|worth noting|game-changer|transformative|cutting-edge|utilize|showcasing|foster|empower|moreover|furthermore|additionally|in conclusion|to summarize|--' <files>
```

Fix only the new or edited prose unless Shawn asks for a broader rewrite.

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
